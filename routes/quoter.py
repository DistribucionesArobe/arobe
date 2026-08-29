"""
Cotizador B2B "libre de flete" — Fase 10.

Simulador público sin login para distribuidores:
  1. Cliente elige producto + cantidad + CP destino + ciudad + estado
  2. Sistema calcula shipping usando shipping.get_shipping_options()
  3. Devuelve precio unitario prorrateado (precio_mayoreo + flete/cantidad)
  4. Cliente ve breakdown y puede solicitar cotización oficial vía WhatsApp/email
"""
import logging
from flask import Blueprint, render_template, request, jsonify

from data import products as catalog
from data import shipping
from data import cities as cities_data

log = logging.getLogger("quoter")

quoter_bp = Blueprint("quoter", __name__)


@quoter_bp.get("/cotizador")
def form():
    """Landing del cotizador con formulario."""
    # Solo productos con precio_mayoreo definido
    productos_b2b = [
        p for p in catalog.all_products()
        if p.get("precio_mayoreo") and p.get("precio_mayoreo") > 0
    ]
    return render_template("quoter.html", page="cotizador", productos=productos_b2b)


@quoter_bp.get("/api/cotizar")
def api_cotizar():
    """
    Calcula precio libre de flete via AJAX.

    Query params:
      - slug: identificador del producto
      - cantidad: cuántas unidades
      - zip: CP destino
      - ciudad, estado: para Skydropx area_levels
    """
    slug = request.args.get("slug", "").strip()
    try:
        cantidad = int(request.args.get("cantidad", "0"))
    except ValueError:
        cantidad = 0
    zip_code = request.args.get("zip", "").strip()
    ciudad = request.args.get("ciudad", "").strip()
    estado = request.args.get("estado", "").strip()

    if not slug or cantidad < 1 or not zip_code or len(zip_code) != 5:
        return jsonify({"error": "Datos incompletos: producto, cantidad, CP (5 dígitos)"}), 400

    producto = catalog.get(slug)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    precio_mayoreo = float(producto.get("precio_mayoreo") or 0)
    if precio_mayoreo <= 0:
        return jsonify({"error": "Este producto no está disponible en precio mayoreo"}), 400

    # Simulo carrito con la cantidad solicitada
    fake_cart = [{
        "producto": producto,
        "qty": cantidad,
        "line_total": precio_mayoreo * cantidad,
    }]

    dest_area = {}
    if estado: dest_area["area_level1"] = estado
    if ciudad:
        dest_area["area_level2"] = ciudad
        dest_area["area_level3"] = ciudad  # colonia default = ciudad si no hay más info
    result = shipping.get_shipping_options(fake_cart, zip_code, dest_area=dest_area)

    # Elijo la opción más barata (o el dedicado si aplica)
    opciones = result.get("options", [])
    if not opciones:
        return jsonify({
            "error": "No hay opciones de envío disponibles para ese CP",
            "shipping_result": result,
        }), 400

    opt_barata = min(opciones, key=lambda o: o.get("price", 999999))
    flete_total = float(opt_barata["price"])

    # Cálculo libre de flete
    subtotal_producto = round(precio_mayoreo * cantidad, 2)
    total_pedido = round(subtotal_producto + flete_total, 2)
    precio_libre_flete = round(precio_mayoreo + (flete_total / cantidad), 2)

    # Zona preferente (radio 500km)
    is_pref = cities_data.is_preferred_zip(zip_code)
    pref_city = cities_data.preferred_city_by_zip(zip_code)

    return jsonify({
        "producto": {
            "slug": producto["slug"],
            "nombre": producto["nombre"],
            "precio_publico": producto.get("precio_publico"),
            "precio_mayoreo": precio_mayoreo,
        },
        "cantidad": cantidad,
        "zip": zip_code,
        "ciudad": ciudad,
        "estado": estado,
        "peso_total_kg": round(producto.get("peso_kg", 0) * cantidad, 1),
        "zona_preferente": is_pref,
        "ciudad_preferente": {
            "nombre": pref_city["nombre"],
            "estado": pref_city["estado"],
            "tiempo_entrega": pref_city["tiempo_entrega"],
            "km_desde_victoria": pref_city["km_desde_victoria"],
        } if pref_city else None,
        "shipping": {
            "carrier": opt_barata.get("carrier"),
            "service": opt_barata.get("service"),
            "price": flete_total,
            "days": opt_barata.get("days"),
            "source": opt_barata.get("source"),
            "tier": opt_barata.get("tier") or result.get("tier"),
            "all_options": [
                {
                    "carrier": o.get("carrier"),
                    "service": o.get("service"),
                    "price": o.get("price"),
                    "days": o.get("days"),
                    "source": o.get("source"),
                }
                for o in opciones[:5]
            ],
            "zone_label": result.get("zone_label"),
        },
        "calculo": {
            "precio_mayoreo_unitario": precio_mayoreo,
            "subtotal_producto": subtotal_producto,
            "flete_total": flete_total,
            "flete_por_unidad": round(flete_total / cantidad, 2),
            "precio_libre_flete_unitario": precio_libre_flete,
            "total_pedido_libre_flete": total_pedido,
            "vs_precio_publico_ahorro_pct": round(
                (1 - (precio_libre_flete / producto.get("precio_publico", precio_libre_flete))) * 100, 1
            ),
        },
    })
