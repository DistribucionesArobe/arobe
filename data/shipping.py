"""
Cálculo de envío para Arobe Group.
Almacén origen: Victoria, Tamaulipas (CP 87020).
Fletera base: Castores (tarifas promedio de mercado mientras Alejandro busca mejor).

Tres tiers:
  - paqueteria: pedidos chicos (~5 kg, sin rollos) — Estafeta/Mexpost/FedEx
  - fletera:    pedidos medianos (8-300 kg, o cualquier rollo) — Castores LTL
  - dedicado:   pedidos grandes (>300 kg o >$15k MXN) — cotización manual por WhatsApp

Para ajustar tarifas: editar la tabla ZONES más abajo.
"""

ORIGIN_ZIP = "87020"  # Victoria, Tamaulipas

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


def calculate_shipping(products_in_cart, dest_zip):
    """
    Calcula envío para una lista de productos en el carrito.

    Args:
        products_in_cart: lista de dicts con keys producto (dict) + qty (int)
                          ej. [{"producto": {...}, "qty": 3, "line_total": 5670}, ...]
        dest_zip: código postal destino (5 dígitos)

    Returns:
        dict con:
          - tier: "paqueteria" | "fletera" | "dedicado"
          - cost: int (MXN, sin IVA) o None si dedicado
          - carrier: nombre sugerido
          - days: rango de días estimado
          - zone: zona destino
          - zone_label: descripción amigable
          - weight_kg: peso total estimado
          - reason: explicación corta de por qué cae en este tier
    """
    zone = get_zone(dest_zip)
    zone_info = ZONES[zone]

    # Sumar peso y volumen total
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

    # Decidir tier
    if total_weight >= PESO_DEDICADO_MIN or total_amount >= MONTO_DEDICADO_MIN:
        return {
            "tier": "dedicado",
            "cost": None,
            "carrier": "Camión dedicado · cotización manual",
            "days": "1-3 (sale el día siguiente)",
            "zone": zone,
            "zone_label": zone_info["label"],
            "weight_kg": round(total_weight, 1),
            "reason": (
                "Pedido grande — te cotizamos por WhatsApp en minutos. "
                f"({total_weight:.0f} kg / ${total_amount:,.0f} MXN)"
            ),
        }

    if has_no_paq_item or total_weight > PESO_PAQUETERIA_MAX or total_amount > MONTO_PAQUETERIA_MAX:
        return {
            "tier": "fletera",
            "cost": zone_info["fletera"],
            "carrier": "Castores LTL",
            "days": zone_info["dias_ltl"],
            "zone": zone,
            "zone_label": zone_info["label"],
            "weight_kg": round(total_weight, 1),
            "reason": (
                "Pedido por fletera consolidada"
                + (" (incluye producto en rollo no apto para paquetería)" if has_no_paq_item else "")
            ),
        }

    return {
        "tier": "paqueteria",
        "cost": zone_info["paqueteria"],
        "carrier": "Estafeta / Mexpost",
        "days": zone_info["dias_paq"],
        "zone": zone,
        "zone_label": zone_info["label"],
        "weight_kg": round(total_weight, 1),
        "reason": "Pedido pequeño · paquetería estándar",
    }
