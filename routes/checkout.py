"""
Checkout con MercadoPago Checkout Pro — Fase 3 + 4.1 + 4.2.

Flujo:
  1. Cliente con items en carrito -> GET /checkout: muestra form.
  2. Submit del form -> POST /checkout/start:
       a. Crea Order en BD con status=pending
       b. Crea Preference en MercadoPago
       c. Guarda mp_preference_id
       d. Redirige al init_point
  3. Cliente paga en checkout de MP.
  4. MP redirige a /checkout/exito | /fallo | /pendiente (back_urls).
  5. MP envía webhook a /api/mp/webhook (notification_url):
       a. Lee detalles del payment vía SDK
       b. Marca Order.status = paid/failed/pending
       c. Si paid: dispara emails al cliente y admin (con guard idempotente)
"""
import os
import json
import logging
from datetime import datetime, timezone

import mercadopago
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    session, flash, jsonify
)

from data import products as catalog
from data import shipping
from models import db, Order, OrderItem
from lib.emailer import send_order_confirmation, send_order_admin_notification

log = logging.getLogger("checkout")

checkout_bp = Blueprint("checkout", __name__)

IVA_TASA = 0.16


def _mp_sdk():
    token = os.environ.get("MP_ACCESS_TOKEN", "").strip()
    if not token:
        return None
    return mercadopago.SDK(token)


def _hydrate_cart():
    """Convierte el dict de sesión en items para MercadoPago + producto enriquecido."""
    cart_dict = session.get("cart", {})
    mp_items = []
    full_lines = []   # con producto entero, para guardar en BD
    total = 0.0
    for slug, qty in cart_dict.items():
        p = catalog.get(slug)
        if p is None:
            continue
        precio = float(p["precio_publico"])
        line_total = precio * qty
        mp_items.append({
            "id": p["slug"],
            "title": p["nombre"],
            "description": p.get("tagline", "")[:250],
            "quantity": int(qty),
            "unit_price": round(precio, 2),
            "currency_id": "MXN",
            "category_id": "construction",
        })
        full_lines.append({
            "producto": p,
            "qty": int(qty),
            "unit_price": round(precio, 2),
            "line_total": round(line_total, 2),
        })
        total += line_total
    return mp_items, full_lines, round(total, 2)


# ============================================================
# GET /checkout
# ============================================================
@checkout_bp.get("/checkout")
def form():
    mp_items, _, total = _hydrate_cart()
    if not mp_items:
        flash("Tu carrito está vacío", "error")
        return redirect(url_for("cart.view"))
    return render_template(
        "checkout.html",
        page="checkout",
        items=mp_items,
        total=total,
        public_key=os.environ.get("MP_PUBLIC_KEY", ""),
    )


# ============================================================
# GET /api/shipping/quote?zip=XXXXX
# Devuelve OPCIONES múltiples de envío (Skydropx si está configurado,
# fallback estático si no). El frontend muestra radio buttons.
# ============================================================
@checkout_bp.get("/api/shipping/quote")
def shipping_quote():
    zip_code = request.args.get("zip", "").strip()
    _, full_lines, _ = _hydrate_cart()
    if not full_lines:
        return jsonify({"error": "Carrito vacío"}), 400
    if not zip_code or not zip_code.isdigit() or len(zip_code) != 5:
        return jsonify({"error": "CP inválido (5 dígitos)"}), 400
    result = shipping.get_shipping_options(full_lines, zip_code)
    return jsonify(result)


# ============================================================
# POST /checkout/start
# ============================================================
@checkout_bp.post("/checkout/start")
def start():
    mp_items, full_lines, total = _hydrate_cart()
    if not mp_items:
        flash("Tu carrito está vacío", "error")
        return redirect(url_for("cart.view"))

    sdk = _mp_sdk()
    if sdk is None:
        flash(
            "MercadoPago no está configurado en este servidor. "
            "Avisa al administrador (falta MP_ACCESS_TOKEN).",
            "error",
        )
        return redirect(url_for("cart.view"))

    # Datos del comprador
    nombre    = request.form.get("nombre", "").strip()
    email     = request.form.get("email", "").strip()
    telefono  = request.form.get("telefono", "").strip()
    rfc       = request.form.get("rfc", "").strip().upper()
    direccion = request.form.get("direccion", "").strip()
    ciudad    = request.form.get("ciudad", "").strip()
    estado    = request.form.get("estado", "").strip()
    cp        = request.form.get("cp", "").strip()
    notas     = request.form.get("notas", "").strip()

    if not (nombre and email):
        flash("Faltan datos obligatorios (nombre y email)", "error")
        return redirect(url_for("checkout.form"))

    # Calculo de totales: el precio_publico ya incluye IVA
    subtotal_sin_iva = round(total / (1 + IVA_TASA), 2)
    iva_amount = round(total - subtotal_sin_iva, 2)

    # Envío: el cliente ya eligió una opción del radio en el form
    # (o si Skydropx no está disponible viene 1 sola opción del fallback).
    ship_cost = 0.0
    ship_carrier = None
    ship_service = None
    ship_days = None
    ship_zone = None
    ship_tier = None
    ship_weight = None
    try:
        ship_price_form = request.form.get("shipping_price", "").strip()
        if ship_price_form:
            ship_cost = float(ship_price_form)
        ship_carrier = request.form.get("shipping_carrier", "").strip() or None
        ship_service = request.form.get("shipping_service", "").strip() or None
        ship_days = request.form.get("shipping_days", "").strip() or None
        ship_tier = request.form.get("shipping_tier", "").strip() or None
    except (ValueError, TypeError):
        ship_cost = 0.0

    # Si no vino nada del form pero tenemos CP, cotizo la más barata como fallback
    if not ship_carrier and cp and cp.isdigit() and len(cp) == 5:
        fallback = shipping.get_shipping_options(full_lines, cp)
        if fallback.get("options"):
            opt = fallback["options"][0]
            ship_cost = float(opt["price"])
            ship_carrier = opt["carrier"]
            ship_service = opt.get("service")
            ship_days = str(opt.get("days") or "")
            ship_tier = opt.get("tier")
        ship_zone = fallback.get("zone")
        ship_weight = fallback.get("weight_kg")

    total_con_envio = round(total + ship_cost, 2)

    # 1) Crear Order en BD (status=pending)
    order = Order(
        status="pending",
        buyer_name=nombre,
        buyer_email=email,
        buyer_phone=telefono or None,
        buyer_rfc=rfc or None,
        ship_address=direccion or None,
        ship_city=ciudad or None,
        ship_state=estado or None,
        ship_zip=cp or None,
        ship_notes=notas or None,
        shipping_tier=ship_tier,
        shipping_carrier=(ship_carrier + (" · " + ship_service if ship_service else "")) if ship_carrier else None,
        shipping_cost=ship_cost,
        shipping_days=ship_days,
        shipping_zone=ship_zone,
        shipping_weight_kg=ship_weight,
        subtotal=subtotal_sin_iva,
        iva=iva_amount,
        total=total_con_envio,
    )
    db.session.add(order)
    db.session.flush()  # para obtener order.id

    for line in full_lines:
        p = line["producto"]
        item = OrderItem(
            order_id=order.id,
            product_slug=p["slug"],
            product_name=p["nombre"],
            product_brand=p["marca"],
            product_image=p["imagenes"][0] if p.get("imagenes") else None,
            qty=line["qty"],
            unit_price=line["unit_price"],
            line_total=line["line_total"],
        )
        db.session.add(item)
    db.session.commit()
    log.info("Order %s creada en BD · buyer=%s · total=%s", order.id, email, total)

    # 2) URLs absolutas con https
    base_url = request.host_url.rstrip("/")
    if base_url.startswith("http://"):
        base_url = base_url.replace("http://", "https://", 1)

    # Si hay envío con costo, lo agrego como item separado en MP
    mp_items_with_shipping = list(mp_items)
    if ship_cost > 0:
        title = f"Envío · {ship_carrier or 'Fletera'}"
        if ship_service:
            title += " " + ship_service
        mp_items_with_shipping.append({
            "id": "envio",
            "title": title[:250],
            "description": f"Entrega en {ship_days or '3-5'} días hábiles"[:250],
            "quantity": 1,
            "unit_price": round(ship_cost, 2),
            "currency_id": "MXN",
            "category_id": "shipping",
        })

    preference_data = {
        "items": mp_items_with_shipping,
        "payer": {
            "name": nombre,
            "email": email,
        },
        "back_urls": {
            "success": f"{base_url}/checkout/exito?order={order.id}",
            "failure": f"{base_url}/checkout/fallo?order={order.id}",
            "pending": f"{base_url}/checkout/pendiente?order={order.id}",
        },
        "auto_return": "approved",
        "external_reference": order.id,
        "notification_url": f"{base_url}/api/mp/webhook",
        "statement_descriptor": "AROBEGROUP",
        "binary_mode": False,
    }
    if telefono:
        preference_data["payer"]["phone"] = {"number": telefono}
    if direccion:
        preference_data["payer"]["address"] = {"street_name": direccion, "zip_code": cp}

    try:
        pref = sdk.preference().create(preference_data)
    except Exception as e:
        log.exception("Error creando preference MP para order=%s", order.id)
        flash(f"No pudimos iniciar el pago: {e}", "error")
        return redirect(url_for("checkout.form"))

    status = pref.get("status")
    body = pref.get("response", {})
    if status != 201:
        log.error("MP preference error order=%s status=%s body=%s", order.id, status, json.dumps(body)[:1000])
        mp_msg = body.get("message") or body.get("error") or "(sin detalle)"
        cause = body.get("cause") or []
        cause_str = ""
        if cause:
            cause_str = " · " + "; ".join(
                f"[{c.get('code','?')}] {c.get('description','')}" for c in cause[:3]
            )
        flash(f"MercadoPago respondió error {status}: {mp_msg}{cause_str}", "error")
        return redirect(url_for("checkout.form"))

    # Guardar preference_id en la orden
    order.mp_preference_id = body.get("id")
    db.session.commit()

    redirect_url = body.get("init_point") or body.get("sandbox_init_point")
    if not redirect_url:
        flash("MercadoPago no devolvió URL de pago", "error")
        return redirect(url_for("checkout.form"))

    log.info("Order %s · preference_id=%s · redirigiendo a MP", order.id, body.get("id"))
    return redirect(redirect_url)


# ============================================================
# Retornos del checkout
# ============================================================
@checkout_bp.get("/checkout/exito")
def success():
    order_id = request.args.get("order", "")
    payment_id = request.args.get("payment_id", "")
    # Vacía el carrito porque la compra cuajó
    if session.get("cart"):
        session["cart"] = {}
        session.modified = True
    # Si el webhook ya llegó, la orden ya está en BD con status=paid
    return render_template(
        "checkout_result.html",
        page="checkout-exito",
        estado="exito",
        order_id=order_id,
        payment_id=payment_id,
        titulo="¡Gracias por tu compra!",
        mensaje="Tu pago fue aprobado. Recibirás un correo con la confirmación y los detalles del envío.",
    )


@checkout_bp.get("/checkout/fallo")
def failure():
    order_id = request.args.get("order", "")
    return render_template(
        "checkout_result.html",
        page="checkout-fallo",
        estado="fallo",
        order_id=order_id,
        titulo="Tu pago no se completó",
        mensaje="Algo salió mal con el pago. Tu carrito sigue intacto — puedes intentar de nuevo o pagar por otro método.",
    )


@checkout_bp.get("/checkout/pendiente")
def pending():
    order_id = request.args.get("order", "")
    return render_template(
        "checkout_result.html",
        page="checkout-pendiente",
        estado="pendiente",
        order_id=order_id,
        titulo="Tu pago está en revisión",
        mensaje="Si pagaste en OXXO o transferencia SPEI, recibirás un correo cuando el pago se acredite (1-2 días hábiles).",
    )


# ============================================================
# Debug — sin token (vivo para revisar config)
# ============================================================
@checkout_bp.get("/debug/mp")
def debug_mp():
    token = os.environ.get("MP_ACCESS_TOKEN", "").strip()
    pub = os.environ.get("MP_PUBLIC_KEY", "").strip()

    def diag(val, name):
        if not val:
            return {"name": name, "set": False, "type": "—", "len": 0, "starts": "—"}
        kind = "PROD" if val.startswith("APP_USR-") else ("TEST" if val.startswith("TEST-") else "INVÁLIDO")
        return {"name": name, "set": True, "type": kind, "len": len(val), "starts": val[:8] + "…"}

    # Estado Skydropx (sin exponer valores)
    sk_id = os.environ.get("SKYDROPX_CLIENT_ID", "").strip()
    sk_sec = os.environ.get("SKYDROPX_CLIENT_SECRET", "").strip()
    sk_diag = {
        "configured": bool(sk_id and sk_sec),
        "client_id_len": len(sk_id),
        "client_secret_len": len(sk_sec),
    }
    if sk_diag["configured"]:
        try:
            from lib import skydropx
            token_ok = skydropx._get_token() is not None
            sk_diag["oauth_token_ok"] = token_ok
        except Exception as e:
            sk_diag["oauth_error"] = str(e)[:200]

    info = {
        "access_token": diag(token, "MP_ACCESS_TOKEN"),
        "public_key": diag(pub, "MP_PUBLIC_KEY"),
        "resend_key_set": bool(os.environ.get("RESEND_API_KEY", "").strip()),
        "skydropx": sk_diag,
        "db_url_set": bool(os.environ.get("DATABASE_URL", "").strip()),
        "host_url": request.host_url,
        "is_https": request.host_url.startswith("https://"),
    }

    if token:
        try:
            import requests as _rq
            r = _rq.get(
                "https://api.mercadopago.com/users/me",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            info["users_me_status"] = r.status_code
            if r.status_code == 200:
                u = r.json()
                info["account"] = {
                    "site_id": u.get("site_id"),
                    "country_id": u.get("country_id"),
                    "nickname": u.get("nickname"),
                }
        except Exception as e:
            info["users_me_exception"] = str(e)[:200]
    return jsonify(info)


# ============================================================
# Webhook IPN de MercadoPago
# ============================================================
@checkout_bp.post("/api/mp/webhook")
def webhook():
    try:
        payload = request.get_json(silent=True) or {}
        log.info("MP webhook payload: %s", json.dumps(payload)[:500])

        payment_id = (payload.get("data") or {}).get("id") or request.args.get("id")
        topic = payload.get("type") or request.args.get("topic")

        if topic != "payment" or not payment_id:
            return jsonify({"ok": True, "ignored": True}), 200

        sdk = _mp_sdk()
        if sdk is None:
            log.error("MP webhook recibido pero SDK no configurado")
            return jsonify({"ok": False, "error": "MP_ACCESS_TOKEN no configurado"}), 200

        resp = sdk.payment().get(payment_id)
        pay = resp.get("response", {})
        mp_status = pay.get("status")               # approved, pending, rejected, refunded, ...
        mp_status_detail = pay.get("status_detail")
        mp_payment_type = pay.get("payment_type_id")
        external_ref = pay.get("external_reference")  # = order.id

        log.info(
            "MP payment %s · status=%s · external_ref=%s · amount=%s",
            payment_id, mp_status, external_ref, pay.get("transaction_amount"),
        )

        if not external_ref:
            return jsonify({"ok": True, "no_external_ref": True}), 200

        order = Order.query.get(external_ref)
        if order is None:
            log.error("MP webhook: orden %s no existe en BD", external_ref)
            return jsonify({"ok": True, "order_not_found": True}), 200

        # Actualizar estado de la orden
        order.mp_payment_id = str(payment_id)
        order.mp_status = mp_status
        order.mp_status_detail = mp_status_detail
        order.mp_payment_type = mp_payment_type

        if mp_status == "approved":
            order.status = "paid"
            if order.paid_at is None:
                order.paid_at = datetime.now(timezone.utc)
        elif mp_status in ("rejected", "cancelled"):
            order.status = "failed"
        elif mp_status in ("pending", "in_process", "authorized"):
            order.status = "pending"
        elif mp_status == "refunded":
            order.status = "refunded"

        db.session.commit()
        log.info("Order %s actualizada a status=%s", order.id, order.status)

        # Disparar emails solo cuando se aprueba el pago (idempotente)
        if order.status == "paid":
            if not order.email_customer_sent:
                ok, _ = send_order_confirmation(order)
                if ok:
                    order.email_customer_sent = True
                    db.session.commit()
            if not order.email_admin_sent:
                ok, _ = send_order_admin_notification(order)
                if ok:
                    order.email_admin_sent = True
                    db.session.commit()

        return jsonify({"ok": True, "order_id": order.id, "status": order.status}), 200
    except Exception as e:
        log.exception("Error en webhook MP")
        # Aún así 200 para que MP no reintente infinito
        return jsonify({"ok": False, "error": str(e)}), 200
