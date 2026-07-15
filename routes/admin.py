"""
Admin — Fase 4.1.
Dashboard simple para ver órdenes. Protegido con HTTP Basic Auth.
Credenciales en env vars:
  - ADMIN_USER  (default: admin)
  - ADMIN_PASSWORD  (REQUERIDO, si no está set el admin está deshabilitado)
"""
import os
import functools
import logging
from datetime import datetime, timezone

from flask import Blueprint, render_template, Response, request, abort, redirect, url_for

from models import db, Order, OrderItem, DistributorLead
from lib.emailer import send_order_confirmation, send_order_admin_notification

log = logging.getLogger("admin")

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _admin_credentials():
    return (
        os.environ.get("ADMIN_USER", "admin").strip(),
        os.environ.get("ADMIN_PASSWORD", "").strip(),
    )


def require_admin(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        user, password = _admin_credentials()
        if not password:
            # Si no se configuró password, el admin está deshabilitado por seguridad
            return Response(
                "Admin no configurado. Establece ADMIN_PASSWORD en las variables de entorno.",
                status=503,
                mimetype="text/plain",
            )
        auth = request.authorization
        if not auth or auth.username != user or auth.password != password:
            return Response(
                "Credenciales requeridas.",
                status=401,
                headers={"WWW-Authenticate": 'Basic realm="Arobe Admin"'},
            )
        return f(*args, **kwargs)
    return wrapper


@admin_bp.get("/")
@require_admin
def home():
    return render_template("admin/home.html", page="admin-home")


@admin_bp.get("/pedidos")
@require_admin
def orders():
    estado = request.args.get("estado", "").strip()
    q = Order.query.order_by(Order.created_at.desc())
    if estado:
        q = q.filter_by(status=estado)
    pedidos = q.limit(200).all()

    # Stats rápidas
    from sqlalchemy import func
    stats = {
        "total": Order.query.count(),
        "paid": Order.query.filter_by(status="paid").count(),
        "pending": Order.query.filter_by(status="pending").count(),
        "failed": Order.query.filter_by(status="failed").count(),
        "ingresos_paid": db.session.query(func.coalesce(func.sum(Order.total), 0.0))
            .filter_by(status="paid").scalar() or 0,
    }
    return render_template(
        "admin/orders.html",
        page="admin-orders",
        pedidos=pedidos,
        estado_filtro=estado,
        stats=stats,
    )


@admin_bp.get("/pedidos/<order_id>")
@require_admin
def order_detail(order_id):
    order = Order.query.get(order_id)
    if order is None:
        abort(404)
    return render_template("admin/order_detail.html", page="admin-order", order=order)


@admin_bp.get("/distribuidores")
@require_admin
def distributor_leads():
    estado = request.args.get("estado", "").strip()
    q = DistributorLead.query.order_by(DistributorLead.created_at.desc())
    if estado:
        q = q.filter_by(status=estado)
    leads = q.limit(200).all()
    stats = {
        "total": DistributorLead.query.count(),
        "nuevos": DistributorLead.query.filter_by(status="nuevo").count(),
        "contactados": DistributorLead.query.filter_by(status="contactado").count(),
        "aprobados": DistributorLead.query.filter_by(status="aprobado").count(),
    }
    return render_template("admin/distributors.html", page="admin-distribuidores",
                           leads=leads, estado_filtro=estado, stats=stats)


@admin_bp.get("/distribuidores/<lead_id>")
@require_admin
def distributor_detail(lead_id):
    lead = DistributorLead.query.get(lead_id)
    if lead is None:
        abort(404)
    return render_template("admin/distributor_detail.html", page="admin-distribuidor", lead=lead)


@admin_bp.post("/distribuidores/<lead_id>/estado")
@require_admin
def distributor_set_status(lead_id):
    lead = DistributorLead.query.get(lead_id)
    if lead is None:
        abort(404)
    nuevo_estado = request.form.get("estado", "").strip()
    if nuevo_estado in ("nuevo", "contactado", "aprobado", "rechazado"):
        lead.status = nuevo_estado
        db.session.commit()
    return redirect(url_for("admin.distributor_detail", lead_id=lead_id))


@admin_bp.post("/pedidos/<order_id>/reenviar-email")
@require_admin
def resend_email(order_id):
    """Re-envía emails de confirmación de un pedido (útil si fallaron en su momento)."""
    order = Order.query.get(order_id)
    if order is None:
        abort(404)
    if order.status != "paid":
        return Response("Solo se envían emails para pedidos pagados.", status=400)

    ok1, msg1 = send_order_confirmation(order)
    ok2, msg2 = send_order_admin_notification(order)
    log.info("Reenvío manual emails order=%s · customer=%s · admin=%s", order.id, ok1, ok2)
    if ok1:
        order.email_customer_sent = True
    if ok2:
        order.email_admin_sent = True
    db.session.commit()
    return render_template(
        "admin/order_detail.html",
        page="admin-order",
        order=order,
        flash_msg=f"Emails reenviados: cliente={ok1} · admin={ok2}",
    )
