"""
Carrito de compras — Fase 2.

Persistencia en sesión Flask (sin DB). Cuando agreguemos cuenta de usuario en
Fase 4 movemos esto a Postgres y respetamos los carritos por usuario.

Estructura en sesión:
    session['cart'] = {
        'brahe-2402': 3,
        'mbi-techos': 1,
    }
"""
from flask import Blueprint, session, redirect, url_for, request, render_template, flash

from data import products as catalog

cart_bp = Blueprint("cart", __name__)


# --- Configuración fiscal MX ---
IVA_TASA = 0.16  # 16% IVA general en México


# ============================================================
# Helpers de sesión
# ============================================================
def _get_cart():
    """Devuelve el dict del carrito desde la sesión, creando si no existe."""
    if "cart" not in session:
        session["cart"] = {}
    return session["cart"]


def _save_cart(cart):
    session["cart"] = cart
    session.modified = True


def _hydrate(cart_dict):
    """Convierte {slug: qty} en lista de items con datos del producto y subtotales."""
    items = []
    subtotal = 0.0
    for slug, qty in cart_dict.items():
        p = catalog.get(slug)
        if p is None:
            continue  # producto fue eliminado del catálogo
        precio = p["precio_publico"]  # TODO Fase 4: precio_mayoreo si user es distribuidor
        line_total = precio * qty
        items.append({
            "producto": p,
            "qty": qty,
            "precio_unitario": precio,
            "line_total": line_total,
        })
        subtotal += line_total
    iva = round(subtotal * IVA_TASA, 2)
    # Como los precios del catálogo YA incluyen IVA, el "subtotal" real es sin IVA:
    subtotal_sin_iva = round(subtotal / (1 + IVA_TASA), 2)
    iva = round(subtotal - subtotal_sin_iva, 2)
    return {
        "lines": items,  # renombrado para evitar choque con dict.items() en Jinja
        "count": sum(cart_dict.values()),
        "subtotal_sin_iva": subtotal_sin_iva,
        "iva": iva,
        "total": round(subtotal, 2),
    }


def cart_summary():
    """Util para el header — devuelve cuántos items hay en el carrito."""
    return sum(_get_cart().values())


# ============================================================
# Rutas
# ============================================================
@cart_bp.get("/carrito")
def view():
    """Vista del carrito."""
    data = _hydrate(_get_cart())
    return render_template("cart.html", page="carrito", cart=data)


@cart_bp.post("/carrito/add")
def add():
    """Agrega producto al carrito. Body: slug, qty."""
    slug = request.form.get("slug", "").strip()
    try:
        qty = int(request.form.get("qty", "1"))
    except ValueError:
        qty = 1
    qty = max(1, min(qty, 999))

    p = catalog.get(slug)
    if p is None:
        flash("Producto no encontrado", "error")
        return redirect(url_for("web.catalogo"))

    cart = _get_cart()
    cart[slug] = cart.get(slug, 0) + qty
    _save_cart(cart)
    flash(f"✓ {p['nombre']} agregado al carrito ({qty} {'unidad' if qty == 1 else 'unidades'})", "success")
    return redirect(url_for("cart.view"))


@cart_bp.post("/carrito/update")
def update():
    """Actualiza la cantidad de un item. Body: slug, qty."""
    slug = request.form.get("slug", "").strip()
    try:
        qty = int(request.form.get("qty", "0"))
    except ValueError:
        qty = 0

    cart = _get_cart()
    if slug not in cart:
        return redirect(url_for("cart.view"))

    if qty <= 0:
        del cart[slug]
    else:
        cart[slug] = min(qty, 999)
    _save_cart(cart)
    return redirect(url_for("cart.view"))


@cart_bp.post("/carrito/remove")
def remove():
    """Quita un item del carrito. Body: slug."""
    slug = request.form.get("slug", "").strip()
    cart = _get_cart()
    if slug in cart:
        del cart[slug]
        _save_cart(cart)
    return redirect(url_for("cart.view"))


@cart_bp.post("/carrito/clear")
def clear():
    """Vacía todo el carrito."""
    session["cart"] = {}
    session.modified = True
    return redirect(url_for("cart.view"))
