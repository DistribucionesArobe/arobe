"""
Modelos de base de datos.
Fase 4.1: Order, OrderItem. Persisten en Postgres.
Fase 4.3 futuro: User (cuando agreguemos cuenta de cliente).
"""
import uuid
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def _now():
    return datetime.now(timezone.utc)


def _gen_id():
    return str(uuid.uuid4())[:8].upper()


# ============================================================
# Order — un pedido completo
# ============================================================
class Order(db.Model):
    __tablename__ = "orders"

    # PK humana corta para mostrar al cliente (ej. "A3B7F2C1")
    id = Column(String(16), primary_key=True, default=_gen_id)

    # Estado del pedido
    status = Column(
        String(20),
        default="pending",   # pending, paid, failed, refunded
        nullable=False,
        index=True,
    )

    # MercadoPago tracking
    mp_preference_id = Column(String(120), nullable=True, index=True)
    mp_payment_id = Column(String(120), nullable=True, index=True)
    mp_status = Column(String(40), nullable=True)            # approved, pending, rejected
    mp_status_detail = Column(String(120), nullable=True)
    mp_payment_type = Column(String(40), nullable=True)      # credit_card, ticket (oxxo), bank_transfer

    # Datos del comprador
    buyer_name = Column(String(200), nullable=False)
    buyer_email = Column(String(200), nullable=False)
    buyer_phone = Column(String(40), nullable=True)
    buyer_rfc = Column(String(13), nullable=True)            # opcional, para CFDI 4.0

    # Envío
    ship_address = Column(String(500), nullable=True)
    ship_city = Column(String(120), nullable=True)
    ship_state = Column(String(120), nullable=True)
    ship_zip = Column(String(10), nullable=True)
    ship_notes = Column(Text, nullable=True)

    # Cotización de envío
    shipping_tier = Column(String(20), nullable=True)      # paqueteria | fletera | dedicado
    shipping_carrier = Column(String(80), nullable=True)
    shipping_cost = Column(Float, default=0.0, nullable=False)
    shipping_days = Column(String(40), nullable=True)
    shipping_zone = Column(String(40), nullable=True)
    shipping_weight_kg = Column(Float, nullable=True)

    # Totales (todos en MXN; el precio_publico ya incluye IVA)
    subtotal = Column(Float, nullable=False)         # sin IVA, productos
    iva = Column(Float, nullable=False)
    total = Column(Float, nullable=False)            # con IVA, INCLUYE envío

    # Auditoría
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)
    paid_at = Column(DateTime(timezone=True), nullable=True)

    # Notificaciones enviadas (para no duplicar email)
    email_customer_sent = Column(Boolean, default=False, nullable=False)
    email_admin_sent = Column(Boolean, default=False, nullable=False)

    # Relación con items
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "buyer_name": self.buyer_name,
            "buyer_email": self.buyer_email,
            "buyer_phone": self.buyer_phone,
            "total": self.total,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "items": [i.to_dict() for i in self.items],
        }


# ============================================================
# OrderItem — cada línea de un pedido
# ============================================================
class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(16), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)

    # Snapshot del producto (por si cambian precios después)
    product_slug = Column(String(80), nullable=False)
    product_name = Column(String(200), nullable=False)
    product_brand = Column(String(40), nullable=False)        # suspan, insulglass
    product_image = Column(String(200), nullable=True)        # filename para mostrar en email

    qty = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)                # con IVA al momento de la compra
    line_total = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")

    def to_dict(self):
        return {
            "product_slug": self.product_slug,
            "product_name": self.product_name,
            "qty": self.qty,
            "unit_price": self.unit_price,
            "line_total": self.line_total,
        }


# ============================================================
# DistributorLead — solicitudes de distribuidor B2B
# ============================================================
class DistributorLead(db.Model):
    __tablename__ = "distributor_leads"

    id = Column(String(12), primary_key=True, default=_gen_id)

    # Empresa
    razon_social = Column(String(200), nullable=False)
    nombre_comercial = Column(String(200), nullable=True)
    rfc = Column(String(13), nullable=True)
    giro = Column(String(80), nullable=True)   # ferretería, constructora, arquitecto, contratista, distribuidor

    # Contacto
    contacto_nombre = Column(String(200), nullable=False)
    contacto_puesto = Column(String(120), nullable=True)
    email = Column(String(200), nullable=False, index=True)
    telefono = Column(String(40), nullable=False)

    # Ubicación
    ciudad = Column(String(120), nullable=True)
    estado = Column(String(120), nullable=True)

    # Comercial
    volumen_mensual_mxn = Column(String(60), nullable=True)  # rango como texto ("$5k-20k")
    marcas_interes = Column(String(120), nullable=True)      # "suspan,insulglass,ambas"
    productos_interes = Column(Text, nullable=True)
    origen = Column(String(120), nullable=True)              # cómo nos conociste
    notas = Column(Text, nullable=True)

    # Auditoría
    status = Column(String(20), default="nuevo", nullable=False, index=True)  # nuevo, contactado, aprobado, rechazado
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False, index=True)
    ip = Column(String(60), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Notificaciones
    email_customer_sent = Column(Boolean, default=False, nullable=False)
    email_admin_sent = Column(Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "razon_social": self.razon_social,
            "contacto_nombre": self.contacto_nombre,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "estado": self.estado,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
