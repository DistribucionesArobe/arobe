"""
Cálculo de envío para Arobe Group.
Almacén origen: Victoria, Tamaulipas (CP 87020).

Estrategia:
  1) Si SKYDROPX está configurado → cotización en tiempo real con Skydropx API
     (múltiples carriers, precios reales, days estimados).
  2) Si Skydropx falla o no está configurado → fallback a tabla estática por zona
     (tarifas promedio Castores como estimación).
  3) Si pedido cae en "dedicado" (>300 kg o >$15k) → siempre cotización manual
     por WhatsApp, no importa qué diga la API.
"""
import logging

log = logging.getLogger("shipping")

ORIGIN_ZIP = "87020"  # Victoria, Tamaulipas

# ----------------------------------------------------------
# Dimensiones aproximadas de bulto por SKU (cm)
# Se usan para el cálculo volumétrico de Skydropx.
# ----------------------------------------------------------
PRODUCT_DIMS = {
    "brahe-2402":           {"length": 122, "width": 61, "height": 15},   # caja 10 pz
    "galilei-3004":         {"length": 61,  "width": 61, "height": 15},   # caja 10 pz
    "kepler-0504":          {"length": 61,  "width": 61, "height": 15},   # caja 10 pz
    "aislamiento-acustico": {"length": 61,  "width": 61, "height": 100},  # rollo enrollado
    "mbi-techos":           {"length": 130, "width": 60, "height": 60},   # rollo grande
}

# ----------------------------------------------------------
# Mapeo CP → zona
# Los primeros 2 dígitos del CP identifican el estado en MX.
# ----------------------------------------------------------
ZIP_PREFIX_TO_ZONE = {
    # Tamaulipas (mismo estado que el almacén) — más barato
    "87": "local", "88": "local", "89": "local",

    # Nuevo León — vecino (Monterrey está a 4 horas de Victoria)
    "64": "local_nl", "65": "local_nl", "66": "local_nl", "67": "local_nl",

    # Norte cercano: Coahuila, San Luis Potosí, Zacatecas
    "25": "norte", "26": "norte", "27": "norte",   # Coahuila
    "78": "norte", "79": "norte",                   # SLP
    "98": "norte", "99": "norte",                   # Zacatecas

    # Frontera: Chihuahua, Durango
    "31": "frontera", "32": "frontera", "33": "frontera",
    "34": "frontera", "35": "frontera",

    # Centro: CDMX, Edomex, Hidalgo, Querétaro, Guanajuato, Aguascalientes, Tlaxcala, Morelos
    "00": "centro",
    "01": "centro", "02": "centro", "03": "centro", "04": "centro",
    "05": "centro", "06": "centro", "07": "centro", "08": "centro",
    "09": "centro", "10": "centro", "11": "centro", "12": "centro",
    "13": "centro", "14": "centro", "15": "centro", "16": "centro",
    "50": "centro", "51": "centro", "52": "centro", "53": "centro",
    "54": "centro", "55": "centro", "56": "centro", "57": "centro",
    "20": "centro",                                                   # Aguascalientes
    "36": "centro", "37": "centro", "38": "centro",                   # Guanajuato
    "42": "centro", "43": "centro",                                   # Hidalgo
    "62": "centro", "63": "centro",                                   # Morelos / Nayarit
    "76": "centro",                                                   # Querétaro
    "90": "centro",                                                   # Tlaxcala

    # Occidente / Bajío sur
    "44": "occidente", "45": "occidente", "46": "occidente",
    "47": "occidente", "48": "occidente", "49": "occidente",   # Jalisco
    "28": "occidente",                                          # Colima
    "58": "occidente", "59": "occidente", "60": "occidente", "61": "occidente",   # Michoacán

    # Pacífico norte: Sinaloa, Sonora, Baja California
    "80": "pacifico", "81": "pacifico", "82": "pacifico",       # Sinaloa
    "83": "pacifico", "84": "pacifico", "85": "pacifico",       # Sonora
    "21": "pacifico", "22": "pacifico", "23": "pacifico",       # Baja California / BCS

    # Sureste: Veracruz, Puebla, Tabasco, Yucatán, QR, Campeche
    "91": "sureste", "92": "sureste", "93": "sureste",
    "94": "sureste", "95": "sureste", "96": "sureste",          # Veracruz
    "72": "sureste", "73": "sureste", "74": "sureste", "75": "sureste",   # Puebla
    "86": "sureste",                                            # Tabasco
    "97": "sureste",                                            # Yucatán
    "77": "sureste",                                            # QR
    "24": "sureste",                                            # Campeche

    # Sur: Oaxaca, Guerrero, Chiapas
    "68": "sur", "69": "sur", "70": "sur", "71": "sur",         # Oaxaca
    "39": "sur", "40": "sur", "41": "sur",                       # Guerrero
    "29": "sur", "30": "sur",                                    # Chiapas
}


# ----------------------------------------------------------
# Tarifas por zona (MXN, sin IVA)
# Costo aproximado Castores Victoria → destino.
# paqueteria = 1 caja chica · fletera = 1 tarima estándar · dedicado = sólo cotizar
# ----------------------------------------------------------
ZONES = {
    "local":     {"label": "Tamaulipas (mismo estado)", "paqueteria": 180, "fletera": 480,  "dias_paq": "1-2", "dias_ltl": "2-3"},
    "local_nl":  {"label": "Nuevo León / Monterrey",     "paqueteria": 230, "fletera": 620,  "dias_paq": "2",   "dias_ltl": "2-3"},
    "norte":     {"label": "Norte (Coah/SLP/Zac)",      "paqueteria": 280, "fletera": 820,  "dias_paq": "2-3", "dias_ltl": "3-4"},
    "frontera":  {"label": "Frontera (Chih/Dgo)",       "paqueteria": 360, "fletera": 1100, "dias_paq": "3-4", "dias_ltl": "4-5"},
    "centro":    {"label": "Centro (CDMX/QRO/GTO/etc)", "paqueteria": 340, "fletera": 1150, "dias_paq": "3-4", "dias_ltl": "4-5"},
    "occidente": {"label": "Occidente (Jal/Mich/Col)",  "paqueteria": 390, "fletera": 1350, "dias_paq": "3-5", "dias_ltl": "5-6"},
    "pacifico":  {"label": "Pacífico Norte (Sin/Son/BC)", "paqueteria": 490, "fletera": 1850, "dias_paq": "4-6", "dias_ltl": "6-8"},
    "sureste":   {"label": "Sureste (Ver/Pue/Yuc/QR)",  "paqueteria": 410, "fletera": 1550, "dias_paq": "4-5", "dias_ltl": "5-7"},
    "sur":       {"label": "Sur (Oax/Gro/Chis)",        "paqueteria": 470, "fletera": 1750, "dias_paq": "4-6", "dias_ltl": "6-7"},
    "unknown":   {"label": "Otro destino",              "paqueteria": 500, "fletera": 1900, "dias_paq": "5-7", "dias_ltl": "7-9"},
}

# Umbrales para tier
PESO_PAQUETERIA_MAX = 8       # kg — más de esto pasa a fletera
PESO_DEDICADO_MIN = 300       # kg — más de esto pasa a camión dedicado
MONTO_DEDICADO_MIN = 15000    # MXN
MONTO_PAQUETERIA_MAX = 1500   # MXN — si es muy chico va por paquetería


def get_zone(zip_code):
    """Devuelve la zona para un CP mexicano de 5 dígitos."""
    if not zip_code or len(str(zip_code).strip()) < 2:
        return "unknown"
    prefix = str(zip_code).strip()[:2]
    return ZIP_PREFIX_TO_ZONE.get(prefix, "unknown")


def _cart_totals(products_in_cart):
    """Suma peso, monto y detecta bultos no-paqueteria."""
    total_weight = 0.0
    total_amount = 0.0
    has_no_paq_item = False
    for line in products_in_cart:
        p = line["producto"]
        qty = line["qty"]
        total_weight += p.get("peso_kg", 0) * qty
        total_amount += line.get("line_total", p.get("precio_publico", 0) * qty)
        if p.get("no_paqueteria"):
            has_no_paq_item = True
    return round(total_weight, 1), round(total_amount, 2), has_no_paq_item


def _build_parcels(products_in_cart):
    """
    Consolida el carrito en 1 o más bultos para pasar a Skydropx.
    Estrategia simple: 1 parcel por línea del carrito × qty.
    """
    parcels = []
    for line in products_in_cart:
        p = line["producto"]
        qty = line["qty"]
        dims = PRODUCT_DIMS.get(p["slug"], {"length": 40, "width": 40, "height": 30})
        peso_por_unidad = max(1.0, float(p.get("peso_kg", 5)))
        for _ in range(qty):
            parcels.append({
                "weight": peso_por_unidad,
                "length": dims["length"],
                "width":  dims["width"],
                "height": dims["height"],
            })
    return parcels


def _static_option(zone_info, tier_name, weight_kg):
    """Convierte una fila de ZONES en un formato de opción unificado."""
    if tier_name == "paqueteria":
        return {
            "source": "estimate",
            "id": f"static-paq-{zone_info['label']}",
            "carrier": "Estafeta / Mexpost",
            "service": "Terrestre (estimado)",
            "price": zone_info["paqueteria"],
            "currency": "MXN",
            "days": zone_info["dias_paq"],
            "tier": "paqueteria",
            "weight_kg": weight_kg,
        }
    else:  # fletera
        return {
            "source": "estimate",
            "id": f"static-ltl-{zone_info['label']}",
            "carrier": "Castores LTL",
            "service": "Consolidada (estimado)",
            "price": zone_info["fletera"],
            "currency": "MXN",
            "days": zone_info["dias_ltl"],
            "tier": "fletera",
            "weight_kg": weight_kg,
        }


def get_shipping_options(products_in_cart, dest_zip, try_realtime=True):
    """
    Devuelve las opciones de envío para el carrito.

    Returns:
        dict con:
          - tier: "paqueteria" | "fletera" | "dedicado"
          - options: lista de opciones (vacía si dedicado)
          - dedicated: True/False
          - weight_kg, amount, zone, zone_label
          - reason: explicación
          - source: "skydropx" | "estimate"
    """
    total_weight, total_amount, has_no_paq_item = _cart_totals(products_in_cart)
    zone = get_zone(dest_zip)
    zone_info = ZONES[zone]

    base = {
        "weight_kg": total_weight,
        "amount": total_amount,
        "zone": zone,
        "zone_label": zone_info["label"],
        "options": [],
        "dedicated": False,
        "source": "estimate",
    }

    # Regla dura: pedido grande = cotización manual
    if total_weight >= PESO_DEDICADO_MIN or total_amount >= MONTO_DEDICADO_MIN:
        base.update({
            "tier": "dedicado",
            "dedicated": True,
            "reason": (
                f"Pedido grande ({total_weight:.0f} kg / ${total_amount:,.0f} MXN) — "
                "te cotizamos por WhatsApp en minutos."
            ),
        })
        return base

    # Intento Skydropx primero
    if try_realtime:
        try:
            from lib import skydropx
            if skydropx.is_configured():
                parcels = _build_parcels(products_in_cart)
                rt_options = skydropx.get_quotations(dest_zip, parcels)
                if rt_options:
                    # Filtro top 5 y agrego metadatos
                    top = rt_options[:5]
                    for opt in top:
                        opt["source"] = "skydropx"
                        opt["tier"] = "fletera" if opt["price"] > 400 else "paqueteria"
                        opt["weight_kg"] = total_weight
                    base.update({
                        "tier": "auto",
                        "options": top,
                        "source": "skydropx",
                        "reason": f"Cotización en vivo ({len(top)} opciones · {total_weight:.0f} kg)",
                    })
                    return base
                else:
                    log.info("Skydropx sin rates, uso fallback estático")
        except Exception as e:
            log.warning("Skydropx exception, fallback estático: %s", e)

    # Fallback: tabla estática — devuelvo 1 opción según el tier
    if has_no_paq_item or total_weight > PESO_PAQUETERIA_MAX or total_amount > MONTO_PAQUETERIA_MAX:
        opt = _static_option(zone_info, "fletera", total_weight)
        base.update({
            "tier": "fletera",
            "options": [opt],
            "reason": (
                "Pedido por fletera consolidada"
                + (" (incluye producto en rollo)" if has_no_paq_item else "")
            ),
        })
    else:
        opt = _static_option(zone_info, "paqueteria", total_weight)
        base.update({
            "tier": "paqueteria",
            "options": [opt],
            "reason": "Pedido pequeño · paquetería estándar",
        })
    return base


# ----------------------------------------------------------
# Retrocompatible: la función vieja sigue funcionando
# (usada por endpoints antiguos que solo quieren 1 opción)
# ----------------------------------------------------------
def calculate_shipping(products_in_cart, dest_zip):
    """Retorna 1 sola opción (la más barata) para compatibilidad."""
    result = get_shipping_options(products_in_cart, dest_zip)
    if result["dedicated"]:
        return {
            "tier": "dedicado",
            "cost": None,
            "carrier": "Camión dedicado · cotización manual",
            "days": "1-3 (sale el día siguiente)",
            "zone": result["zone"],
            "zone_label": result["zone_label"],
            "weight_kg": result["weight_kg"],
            "reason": result["reason"],
        }
    if not result["options"]:
        return None
    opt = result["options"][0]
    return {
        "tier": opt.get("tier", result["tier"]),
        "cost": opt["price"],
        "carrier": opt["carrier"] + (" · " + opt["service"] if opt.get("service") else ""),
        "days": opt.get("days") or "3-5",
        "zone": result["zone"],
        "zone_label": result["zone_label"],
        "weight_kg": result["weight_kg"],
        "reason": result["reason"],
    }
