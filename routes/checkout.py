"""
Checkout con MercadoPago Checkout Pro — Fase 3.

Flujo:
  1. Cliente con items en carrito -> GET /checkout: muestra form de datos.
  2. Submit del form -> POST /checkout/start: crea Preference en MP y redirige.
  3. Cliente paga en checkout de MP.
  4. MP redirige a /checkout/exito | /fallo | /pendiente (back_urls).
  5. MP envía webhook a /api/mp/webhook (notification_url) — la fuente de
     verdad para el estado del pago.

En Fase 4 persistimos la orden en Postgres. Por ahora solo email + logs.
"""
import os
import json
import uuid
import logging

import mercadopago
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    session, flash, jsonify, current_app, abort
)

from data import products as catalog

log = logging.getLogger("checkout")

checkout_bp = Blueprint("checkout", __name__)

IVA_TASA = 0.16


def _mp_sdk():
    """Devuelve el SDK de MercadoPago configurado con el token de env."""
    token = os.environ.get("MP_ACCESS_TOKEN", "").strip()
    if not token:
        return None
    return mercadopago.SDK(token)


def _hydrate_cart():
    """Convierte el dict de sesión en items listos para MercadoPago."""
    cart_dict = session.get("cart", {})
    items = []
    total = 0.0
    for slug, qty in cart_dict.items():
        p = catalog.get(slug)
        if p is None:
            continue
        precio = float(p["precio_publico"])
        line_total = precio * qty
        items.append({
            "id": p["slug"],
            "title": p["nombre"],
            "description": p.get("tagline", "")[:250],
            "quantity": int(qty),
            "unit_price": round(precio, 2),
            "currency_id": "MXN",
            "category_id": "construction",
        })
        total += line_total
    return items, round(total, 2)


# ============================================================
# GET /checkout — formulario de datos del comprador
# ============================================================
@checkout_bp.get("/checkout")
def form():
    items, total = _hydrate_cart()
    if not items:
        flash("Tu carrito está vacío", "error")
        return redirect(url_for("cart.view"))
    return render_template(
        "checkout.html",
        page="checkout",
        items=items,
        total=total,
        public_key=os.environ.get("MP_PUBLIC_KEY", ""),
    )


# ============================================================
# POST /checkout/start — crea preference y redirige a MP
# ============================================================
@checkout_bp.post("/checkout/start")
def start():
    items, total = _hydrate_cart()
    if not items:
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
    nombre = request.form.get("nombre", "").strip()
    email = request.form.get("email", "").strip()
    telefono = request.form.get("telefono", "").strip()
    rfc = request.form.get("rfc", "").strip()
    direccion = request.form.get("direccion", "").strip()
    ciudad = request.form.get("ciudad", "").strip()
    estado = request.form.get("estado", "").strip()
    cp = request.form.get("cp", "").strip()
    notas = request.form.get("notas", "").strip()

    if not (nombre and email):
        flash("Faltan datos obligatorios (nombre y email)", "error")
        return redirect(url_for("checkout.form"))

    # Genero un ID único de orden para poder rastrear
    order_id = str(uuid.uuid4())[:8].upper()
    session["pending_order_id"] = order_id
    session["pending_order_data"] = {
        "nombre": nombre, "email": email, "telefono": telefono,
        "rfc": rfc, "direccion": direccion, "ciudad": ciudad,
        "estado": estado, "cp": cp, "notas": notas,
        "items": items, "total": total,
    }
    session.modified = True

    # URLs de retorno absolutas. MercadoPago RECHAZA back_urls con http://
    # (debe ser https). Forzamos siempre https en producción.
    base_url = request.host_url.rstrip("/")
    if base_url.startswith("http://"):
        base_url = base_url.replace("http://", "https://", 1)

    preference_data = {
        "items": items,
        "payer": {
            "name": nombre,
            "email": email,
            "phone": {"number": telefono} if telefono else None,
            "address": {
                "street_name": direccion,
                "zip_code": cp,
            } if direccion else None,
        },
        "back_urls": {
            "success": f"{base_url}/checkout/exito?order={order_id}",
            "failure": f"{base_url}/checkout/fallo?order={order_id}",
            "pending": f"{base_url}/checkout/pendiente?order={order_id}",
        },
        "auto_return": "approved",
        "external_reference": order_id,
        "notification_url": f"{base_url}/api/mp/webhook",
        "statement_descriptor": "AROBEGROUP",
        "binary_mode": False,  # permitir pagos pendientes (OXXO, SPEI)
    }
    # Limpio None del payer (MP no le gusta)
    preference_data["payer"] = {k: v for k, v in preference_data["payer"].items() if v}

    try:
        pref = sdk.preference().create(preference_data)
    except Exception as e:
        log.exception("Error creando preference MP")
        flash(f"No pudimos iniciar el pago: {e}", "error")
        return redirect(url_for("checkout.form"))

    status = pref.get("status")
    body = pref.get("response", {})
    if status != 201:
        # Log completo para diagnóstico
        log.error("MP preference error status=%s body=%s", status, json.dumps(body)[:1000])
        # Saco un mensaje legible para el usuario
        mp_msg = body.get("message") or body.get("error") or "(sin detalle)"
        cause = body.get("cause") or []
        cause_str = ""
        if cause:
            cause_str = " · " + "; ".join(
                f"[{c.get('code','?')}] {c.get('description','')}" for c in cause[:3]
            )
        flash(
            f"MercadoPago respondió error {status}: {mp_msg}{cause_str}",
            "error",
        )
        return redirect(url_for("checkout.form"))

    # init_point = URL del checkout en producción
    # sandbox_init_point = URL en sandbox (cuando usas TEST credentials)
    redirect_url = body.get("init_point") or body.get("sandbox_init_point")
    if not redirect_url:
        flash("MercadoPago no devolvió URL de pago", "error")
        return redirect(url_for("checkout.form"))

    log.info("MP preference creada order=%s pref_id=%s", order_id, body.get("id"))
    return redirect(redirect_url)


# ============================================================
# Retornos del checkout (back_urls)
# ============================================================
@checkout_bp.get("/checkout/exito")
def success():
    order_id = request.args.get("order", "")
    payment_id = request.args.get("payment_id", "")
    # Vacío el carrito porque la compra cuajó
    if session.get("cart"):
        session["cart"] = {}
        session.modified = True
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
# Debug — verifica config sin revelar token
# ============================================================
@checkout_bp.get("/debug/mp")
def debug_mp():
    token = os.environ.get("MP_ACCESS_TOKEN", "").strip()
    pub = os.environ.get("MP_PUBLIC_KEY", "").strip()

    def diag(val, name):
        if not val:
            return {"name": name, "set": False, "type": "—", "len": 0, "starts": "—"}
        kind = "PROD" if val.startswith("APP_USR-") else ("TEST" if val.startswith("TEST-") else "INVÁLIDO")
        return {
            "name": name,
            "set": True,
            "type": kind,
            "len": len(val),
            "starts": val[:8] + "…",
        }

    info = {
        "access_token": diag(token, "MP_ACCESS_TOKEN"),
        "public_key": diag(pub, "MP_PUBLIC_KEY"),
        "host_url": request.host_url,
        "is_https": request.host_url.startswith("https://"),
    }

    # Si hay token, intentamos llamar a /users/me como sanity check
    if token:
        try:
            sdk = mercadopago.SDK(token)
            # Endpoint barato que valida el token
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
                    "email_dominio": (u.get("email") or "").split("@")[-1] if u.get("email") else None,
                }
            else:
                info["users_me_error"] = r.text[:300]
        except Exception as e:
            info["users_me_exception"] = str(e)[:200]

    return jsonify(info)


# ============================================================
# Webhook IPN de MercadoPago
# ============================================================
@checkout_bp.post("/api/mp/webhook")
def webhook():
    """
    MercadoPago llama aquí cuando un pago cambia de estado.
    Body típico: {"action":"payment.updated","data":{"id":"<payment_id>"},"type":"payment"}
    """
    try:
        payload = request.get_json(silent=True) or {}
        log.info("MP webhook payload: %s", json.dumps(payload)[:500])

        payment_id = (payload.get("data") or {}).get("id") or request.args.get("id")
        topic = payload.get("type") or request.args.get("topic")

        if topic == "payment" and payment_id:
            sdk = _mp_sdk()
            if sdk:
                resp = sdk.payment().get(payment_id)
                pay = resp.get("response", {})
                log.info(
                    "MP payment %s | status=%s | external_ref=%s | amount=%s",
                    payment_id,
                    pay.get("status"),
                    pay.get("external_reference"),
                    pay.get("transaction_amount"),
                )
                # TODO Fase 4: guardar en Postgres + enviar email transaccional
        return jsonify({"ok": True}), 200
    except Exception as e:
        log.exception("Error en webhook MP")
        # Aún así devuelvo 200 para que MP no reintente infinito
        return jsonify({"ok": False, "error": str(e)}), 200
