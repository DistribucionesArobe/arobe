"""
Envío de emails transaccionales con Resend.
Requiere env vars:
  - RESEND_API_KEY (el API key del panel de Resend)
  - EMAIL_FROM (opcional, default: pedidos@arobegroup.com)
  - EMAIL_VENTAS (a quién copia los emails de admin)
"""
import os
import logging
import requests

log = logging.getLogger("emailer")

RESEND_API = "https://api.resend.com/emails"


def _api_key():
    return os.environ.get("RESEND_API_KEY", "").strip()


def _from():
    # Resend requiere que el dominio esté verificado.
    # arobegroup.com ya tiene DKIM (resend._domainkey).
    return os.environ.get("EMAIL_FROM", "Arobe Group <pedidos@arobegroup.com>")


def _admin_email():
    return os.environ.get("EMAIL_VENTAS", "contacto@arobegroup.com")


def send_email(to, subject, html, reply_to=None):
    """Envía un email vía Resend. Devuelve (ok, mensaje)."""
    key = _api_key()
    if not key:
        log.warning("RESEND_API_KEY no configurado — saltando envío de email")
        return False, "RESEND_API_KEY no configurado"

    payload = {
        "from": _from(),
        "to": [to] if isinstance(to, str) else list(to),
        "subject": subject,
        "html": html,
    }
    if reply_to:
        payload["reply_to"] = reply_to

    try:
        r = requests.post(
            RESEND_API,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=15,
        )
        if r.status_code in (200, 201, 202):
            data = r.json()
            log.info("Email enviado id=%s to=%s subject=%s", data.get("id"), to, subject)
            return True, data.get("id", "ok")
        else:
            log.error("Resend error %s: %s", r.status_code, r.text[:500])
            return False, f"Resend {r.status_code}: {r.text[:200]}"
    except Exception as e:
        log.exception("Excepción enviando email")
        return False, str(e)


# ============================================================
# Templates HTML
# ============================================================
def _money(v):
    return f"${v:,.2f} MXN"


def _items_table(items):
    """Genera tabla HTML con los items de la orden."""
    rows = []
    for it in items:
        rows.append(
            "<tr>"
            f"<td style='padding:12px 8px;border-bottom:1px solid #e2e8f0'>"
            f"  <strong>{it.product_name}</strong><br>"
            f"  <small style='color:#64748b'>{it.product_brand.title()}</small>"
            "</td>"
            f"<td style='padding:12px 8px;border-bottom:1px solid #e2e8f0;text-align:center'>{it.qty}</td>"
            f"<td style='padding:12px 8px;border-bottom:1px solid #e2e8f0;text-align:right'>{_money(it.unit_price)}</td>"
            f"<td style='padding:12px 8px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700'>{_money(it.line_total)}</td>"
            "</tr>"
        )
    return (
        "<table style='width:100%;border-collapse:collapse;margin:20px 0;font-family:Inter,Arial,sans-serif'>"
        "<thead><tr style='background:#0a1a2e;color:white'>"
        "<th style='padding:12px 8px;text-align:left'>Producto</th>"
        "<th style='padding:12px 8px;text-align:center'>Cant.</th>"
        "<th style='padding:12px 8px;text-align:right'>Unitario</th>"
        "<th style='padding:12px 8px;text-align:right'>Total</th>"
        "</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
    )


def _wrapper(title, body):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:Inter,Arial,sans-serif;color:#0f172a">
  <div style="max-width:600px;margin:0 auto;background:white">
    <div style="background:#0a1a2e;padding:24px;text-align:center">
      <div style="display:inline-block;width:48px;height:48px;background:white;color:#0a1a2e;font-weight:900;font-size:28px;line-height:48px;border-radius:6px">A</div>
      <div style="color:white;font-weight:800;font-size:20px;margin-top:8px">AROBE GROUP</div>
      <div style="color:#9ab3d4;font-size:11px;letter-spacing:2px;text-transform:uppercase">Construcción ligera</div>
    </div>
    <div style="padding:32px 24px">
      {body}
    </div>
    <div style="background:#0a1a2e;color:#9ab3d4;padding:20px;text-align:center;font-size:12px">
      <p style="margin:0">SusPan® · Insulglass® son marcas registradas de Arobe Group.</p>
      <p style="margin:8px 0 0">© 2026 Distribuciones Arobe · arobegroup.com</p>
    </div>
  </div>
</body>
</html>
"""


def send_order_confirmation(order):
    """Email al cliente confirmando pedido pagado."""
    body = f"""
      <h1 style="color:#0a1a2e;margin:0 0 8px">¡Gracias por tu compra, {order.buyer_name.split(' ')[0]}!</h1>
      <p style="color:#475569;font-size:16px;line-height:1.6">
        Recibimos tu pedido <strong>#{order.id}</strong> y tu pago fue aprobado.
        En las próximas horas te contactaremos por <strong>WhatsApp</strong>
        ({order.buyer_phone or 'al teléfono que nos compartas'}) para confirmar
        los detalles de envío.
      </p>

      <div style="background:#fef9c3;border-left:4px solid #f2c84a;padding:16px;margin:24px 0;border-radius:0 8px 8px 0">
        <strong style="color:#0a1a2e">Folio:</strong> <code style="background:white;padding:4px 8px;border-radius:4px">#{order.id}</code>
      </div>

      <h3 style="color:#0a1a2e;margin-top:32px">Detalle del pedido</h3>
      {_items_table(order.items)}

      <table style="width:100%;font-family:Inter,Arial,sans-serif">
        <tr><td style="padding:6px 0;color:#64748b">Subtotal sin IVA:</td>
            <td style="padding:6px 0;text-align:right">{_money(order.subtotal)}</td></tr>
        <tr><td style="padding:6px 0;color:#64748b">IVA 16%:</td>
            <td style="padding:6px 0;text-align:right">{_money(order.iva)}</td></tr>
        <tr style="border-top:2px solid #0a1a2e">
          <td style="padding:12px 0;font-size:18px;font-weight:800;color:#0a1a2e">Total pagado:</td>
          <td style="padding:12px 0;text-align:right;font-size:20px;font-weight:900;color:#0a1a2e">{_money(order.total)}</td>
        </tr>
      </table>

      {f'<div style="background:#dcfce7;border-radius:8px;padding:16px;margin:24px 0"><strong>Datos de envío:</strong><br>{order.ship_address}<br>{order.ship_city or ""} {order.ship_state or ""} {order.ship_zip or ""}</div>' if order.ship_address else ''}

      {f'<div style="background:#dbeafe;border-radius:8px;padding:16px;margin:24px 0"><strong>RFC para CFDI 4.0:</strong> {order.buyer_rfc}<br><small>Te enviaremos tu factura en las próximas 24h.</small></div>' if order.buyer_rfc else ''}

      <p style="margin-top:32px;font-size:14px;color:#64748b">
        Si tienes cualquier duda escríbenos a
        <a href="mailto:contacto@arobegroup.com" style="color:#0a1a2e">contacto@arobegroup.com</a>
        o por WhatsApp a <a href="https://wa.me/528130783171" style="color:#10b981">+52 81 3078 3171</a>.
      </p>
    """
    html = _wrapper("Confirmación de pedido", body)
    return send_email(order.buyer_email, f"✅ Pedido #{order.id} confirmado — Arobe Group", html)


def send_distributor_confirmation(lead):
    """Email al distribuidor confirmando su solicitud + kit de bienvenida."""
    body = f"""
      <h1 style="color:#0a1a2e;margin:0 0 8px">¡Gracias por tu interés, {lead.contacto_nombre.split(' ')[0]}!</h1>
      <p style="color:#475569;font-size:16px;line-height:1.6">
        Recibimos la solicitud de <strong>{lead.razon_social}</strong> para el programa
        <strong>Distribuidores Arobe</strong>. En las próximas <strong>24 horas hábiles</strong>
        te contactaremos por WhatsApp o teléfono ({lead.telefono}) para validar tu perfil
        y darte de alta.
      </p>

      <div style="background:#fef9c3;border-left:4px solid #f2c84a;padding:16px;margin:24px 0;border-radius:0 8px 8px 0">
        <strong style="color:#0a1a2e">Folio de solicitud:</strong> <code style="background:white;padding:4px 8px;border-radius:4px">#{lead.id}</code>
      </div>

      <h3 style="color:#0a1a2e;margin-top:32px">Beneficios del programa</h3>
      <ul style="color:#475569;line-height:1.8">
        <li>✅ <strong>15% de descuento</strong> sobre precio público en todos los productos SusPan e Insulglass</li>
        <li>✅ <strong>5% adicional</strong> en tu primer pedido de bienvenida</li>
        <li>✅ <strong>Envío gratis</strong> para pedidos de $30,000 MXN o más dentro del norte de México</li>
        <li>✅ <strong>Crédito 30 días</strong> después de 3 pedidos consecutivos pagados</li>
        <li>✅ Acceso a fichas técnicas oficiales y kit de venta para tus clientes</li>
        <li>✅ Soporte técnico directo por WhatsApp para dudas de instalación</li>
        <li>✅ Materiales de marketing (folletos, flyers, mockups) para tu ferretería/showroom</li>
      </ul>

      <h3 style="color:#0a1a2e;margin-top:32px">Mientras nos contactamos, revisa nuestro catálogo</h3>
      <p>
        <a href="https://arobegroup.com/catalogo" style="display:inline-block;background:#0a1a2e;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:700;margin-right:8px">Ver catálogo</a>
        <a href="https://wa.me/{os.environ.get('WA_PHONE','528130783171')}?text=Hola%2C+soy+distribuidor+registrado+folio+{lead.id}" style="display:inline-block;background:#10b981;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:700">💬 Escríbenos por WhatsApp</a>
      </p>

      <p style="margin-top:32px;font-size:14px;color:#64748b">
        Si tienes dudas escríbenos a
        <a href="mailto:contacto@arobegroup.com" style="color:#0a1a2e">contacto@arobegroup.com</a>
        o por WhatsApp a <a href="https://wa.me/528130783171" style="color:#10b981">+52 81 3078 3171</a>.
      </p>
    """
    html = _wrapper("Bienvenido al programa Distribuidores Arobe", body)
    return send_email(lead.email, f"✅ Solicitud #{lead.id} recibida · Distribuidores Arobe", html)


def send_distributor_admin(lead):
    """Email al admin notificando nueva solicitud de distribuidor."""
    marcas = (lead.marcas_interes or "").replace(",", ", ") or "—"
    body = f"""
      <h1 style="color:#0a1a2e;margin:0 0 8px">🔔 Nueva solicitud de distribuidor</h1>
      <p style="color:#475569;font-size:16px">
        Folio <strong>#{lead.id}</strong> — recibida {lead.created_at.strftime('%d/%m/%Y %H:%M UTC') if lead.created_at else ''}
      </p>

      <h3 style="color:#0a1a2e">Empresa</h3>
      <p style="margin:4px 0"><strong>Razón social:</strong> {lead.razon_social}</p>
      {f'<p style="margin:4px 0"><strong>Nombre comercial:</strong> {lead.nombre_comercial}</p>' if lead.nombre_comercial else ''}
      {f'<p style="margin:4px 0"><strong>RFC:</strong> <code>{lead.rfc}</code></p>' if lead.rfc else ''}
      {f'<p style="margin:4px 0"><strong>Giro:</strong> {lead.giro}</p>' if lead.giro else ''}
      {f'<p style="margin:4px 0"><strong>Ubicación:</strong> {lead.ciudad or ""} {lead.estado or ""}</p>' if (lead.ciudad or lead.estado) else ''}

      <h3 style="color:#0a1a2e;margin-top:24px">Contacto</h3>
      <p style="margin:4px 0"><strong>{lead.contacto_nombre}</strong>{f' — {lead.contacto_puesto}' if lead.contacto_puesto else ''}</p>
      <p style="margin:4px 0">📧 <a href="mailto:{lead.email}">{lead.email}</a></p>
      <p style="margin:4px 0">📱 <a href="https://wa.me/{lead.telefono.replace(' ','').replace('+','').replace('-','')}">{lead.telefono}</a></p>

      <h3 style="color:#0a1a2e;margin-top:24px">Interés comercial</h3>
      <p style="margin:4px 0"><strong>Volumen mensual estimado:</strong> {lead.volumen_mensual_mxn or 'No especificado'}</p>
      <p style="margin:4px 0"><strong>Marcas de interés:</strong> {marcas}</p>
      {f'<p style="margin:4px 0"><strong>Productos:</strong> {lead.productos_interes}</p>' if lead.productos_interes else ''}
      {f'<p style="margin:4px 0"><strong>Cómo nos conoció:</strong> {lead.origen}</p>' if lead.origen else ''}
      {f'<div style="background:#f8fafc;border-radius:8px;padding:12px;margin:12px 0"><strong>Notas:</strong><br>{lead.notas}</div>' if lead.notas else ''}

      <p style="margin-top:32px">
        <a href="https://arobegroup.com/admin/distribuidores/{lead.id}" style="display:inline-block;background:#0a1a2e;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:700">Ver en admin</a>
      </p>

      <p style="margin-top:24px;font-size:13px;color:#64748b">
        Acción requerida: contactar por WhatsApp/teléfono en las próximas 24h hábiles para validar
        y activar cuenta de distribuidor.
      </p>
    """
    html = _wrapper("Nueva solicitud de distribuidor", body)
    return send_email(_admin_email(), f"🤝 Nuevo distribuidor: {lead.razon_social} · {lead.ciudad or ''}", html, reply_to=lead.email)


def send_order_admin_notification(order):
    """Email al administrador notificando nuevo pedido pagado."""
    body = f"""
      <h1 style="color:#0a1a2e;margin:0 0 8px">🔔 Nuevo pedido pagado</h1>
      <p style="color:#475569;font-size:16px">
        Pedido <strong>#{order.id}</strong> · MercadoPago {order.mp_payment_id or 'N/A'}
      </p>

      <h3 style="color:#0a1a2e">Cliente</h3>
      <p style="margin:4px 0"><strong>{order.buyer_name}</strong></p>
      <p style="margin:4px 0">📧 <a href="mailto:{order.buyer_email}">{order.buyer_email}</a></p>
      {f'<p style="margin:4px 0">📱 <a href="https://wa.me/{order.buyer_phone.replace(" ","").replace("+","")}">{order.buyer_phone}</a></p>' if order.buyer_phone else ''}
      {f'<p style="margin:4px 0">🧾 RFC: <code>{order.buyer_rfc}</code></p>' if order.buyer_rfc else ''}

      {f'<h3 style="color:#0a1a2e">Envío</h3><p>{order.ship_address}<br>{order.ship_city or ""} {order.ship_state or ""} {order.ship_zip or ""}</p>' if order.ship_address else '<p style="color:#dc2626"><strong>⚠️ Cliente no proporcionó dirección de envío</strong></p>'}
      {f'<p><strong>Notas:</strong> {order.ship_notes}</p>' if order.ship_notes else ''}

      <h3 style="color:#0a1a2e;margin-top:32px">Productos</h3>
      {_items_table(order.items)}

      <table style="width:100%">
        <tr><td style="color:#64748b">Subtotal sin IVA:</td><td style="text-align:right">{_money(order.subtotal)}</td></tr>
        <tr><td style="color:#64748b">IVA:</td><td style="text-align:right">{_money(order.iva)}</td></tr>
        <tr style="border-top:2px solid #0a1a2e">
          <td style="padding:12px 0;font-weight:800">Total:</td>
          <td style="padding:12px 0;text-align:right;font-weight:900;font-size:18px">{_money(order.total)}</td>
        </tr>
      </table>

      <p style="margin-top:32px;font-size:13px;color:#64748b">
        Acción requerida: contactar al cliente para confirmar envío y preparar la entrega.
      </p>
    """
    html = _wrapper("Nuevo pedido pagado", body)
    return send_email(_admin_email(), f"🛒 Pedido #{order.id} · ${order.total:,.2f} MXN", html, reply_to=order.buyer_email)
