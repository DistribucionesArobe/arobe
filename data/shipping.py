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
PESO_HIBRIDO_MIN = 300        # kg — 300-800 kg: LTL + dedicado (cliente elige)
PESO_SOLO_DEDICADO_MIN = 800  # kg — más: solo camión dedicado tiene sentido
MONTO_DEDICADO_MIN = 15000    # MXN
MONTO_PAQUETERIA_MAX = 1500   # MXN — si es muy chico va por paquetería

# Retrocompat con código viejo que use la constante anterior
PESO_DEDICADO_MIN = PESO_HIBRIDO_MIN


# ============================================================
# Camión dedicado (caja seca 25 ton · 2.60m × 16m)
# ============================================================
# Tarifa: $1.60/km/ton × 25 ton = $40/km neto → $46.40/km con IVA 16%
DEDICADO_CAPACIDAD_TON = 25
DEDICADO_TARIFA_KM_TON = 1.60           # MXN neto
DEDICADO_COSTO_KM_NETO = DEDICADO_CAPACIDAD_TON * DEDICADO_TARIFA_KM_TON  # = $40
DEDICADO_COSTO_KM_CON_IVA = round(DEDICADO_COSTO_KM_NETO * (1 + 0.16), 2)  # = $46.40
DEDICADO_DIMS = "2.60 m ancho × 16 m largo · 25 toneladas"

# Distancia aproximada (km terrestres) desde Victoria, Tamaulipas (CP 87020)
# al centro de cada estado. Prefijo de 2 dígitos del CP → km.
# Ajustar cuando tengas datos reales por ruta.
KM_DESDE_VICTORIA = {
    # Tamaulipas (mismo estado)
    "87": 0, "88": 250, "89": 250,   # Victoria / Reynosa-Matamoros / Tampico
    # Nuevo León (Monterrey área)
    "64": 320, "65": 340, "66": 340, "67": 320,
    # Norte cercano
    "25": 400, "26": 500, "27": 620,   # Coahuila (Saltillo → Torreón)
    "78": 460, "79": 480,               # SLP
    "98": 470, "99": 470,               # Zacatecas
    # Frontera / Chihuahua-Durango
    "31": 850, "32": 1100, "33": 900,   # Chihuahua / Cd. Juárez
    "34": 800, "35": 620,                # Durango
    # Centro (CDMX área extendida)
    "00": 620, "01": 620, "02": 620, "03": 620, "04": 620, "05": 620,
    "06": 620, "07": 620, "08": 620, "09": 620, "10": 620, "11": 620,
    "12": 620, "13": 620, "14": 620, "15": 620, "16": 620,
    "50": 620, "51": 620, "52": 620, "53": 620,
    "54": 620, "55": 620, "56": 620, "57": 620,
    "20": 570, "36": 550, "37": 480, "38": 480,   # Ags / Guanajuato
    "42": 580,                                     # Hidalgo
    "62": 700, "63": 730,                          # Morelos / Nayarit
    "76": 480,                                     # Querétaro
    "90": 660,                                     # Tlaxcala
    # Occidente
    "44": 750, "45": 750, "46": 780, "47": 700, "48": 800, "49": 800,   # Jalisco
    "28": 850,                                                            # Colima
    "58": 850, "59": 830, "60": 800, "61": 800,                          # Michoacán
    # Pacífico norte
    "80": 950, "81": 950, "82": 900,     # Sinaloa
    "83": 1200, "84": 1350, "85": 1400,  # Sonora
    "21": 1800, "22": 1900, "23": 1900,  # Baja California
    # Sureste
    "91": 780, "92": 850, "93": 900, "94": 950, "95": 1000, "96": 1000,   # Veracruz
    "72": 720, "73": 750, "74": 800, "75": 780,                            # Puebla
    "86": 1050,                                                             # Tabasco
    "97": 1700,                                                             # Yucatán
    "77": 2000,                                                             # QR
    "24": 1500,                                                             # Campeche
    # Sur
    "68": 1000, "69": 1050, "70": 1000, "71": 1050,   # Oaxaca
    "39": 900, "40": 900, "41": 850,                   # Guerrero
    "29": 1300, "30": 1400,                            # Chiapas
}
KM_DEFAULT = 800   # si no encuentro el CP


def km_from_victoria(dest_zip):
    """Distancia aproximada en km desde Victoria (87020) al CP destino."""
    if not dest_zip or len(str(dest_zip)) < 2:
        return KM_DEFAULT
    prefix = str(dest_zip).strip()[:2]
    return KM_DESDE_VICTORIA.get(prefix, KM_DEFAULT)


def dedicated_price(dest_zip):
    """Calcula precio de camión dedicado según distancia."""
    km = km_from_victoria(dest_zip)
    price = round(km * DEDICADO_COSTO_KM_CON_IVA, 2)
    return {
        "km": km,
        "price": price,
        "detail": (
            f"Camión seca dedicado ({DEDICADO_DIMS}) · "
            f"{km} km × ${DEDICADO_COSTO_KM_CON_IVA:.2f}/km"
        ),
    }


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


def get_shipping_options(products_in_cart, dest_zip, try_realtime=True, dest_area=None):
    """
    Devuelve las opciones de envío para el carrito.

    Args:
        products_in_cart: lista de items del carrito
        dest_zip: CP destino de 5 dígitos
        try_realtime: si intentar Skydropx antes del fallback estático
        dest_area: dict opcional con area_level1 (estado), area_level2 (municipio),
                   area_level3 (colonia). Skydropx PRO los requiere.

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

    # ------------------------------------------------------------
    # Camión dedicado — construido para reuso en varios ramos
    # ------------------------------------------------------------
    def _dedicated_option():
        ded = dedicated_price(dest_zip)
        return {
            "source": "dedicated",
            "id": f"dedicated-{zone}",
            "carrier": "Camión seca dedicado",
            "service": f"{ded['km']} km · caja 25 ton (2.60 × 16 m)",
            "price": ded["price"],
            "currency": "MXN",
            "days": "1-2 (sale al día siguiente)",
            "tier": "dedicado",
            "weight_kg": total_weight,
            "requires_confirmation": True,
        }

    # Peso muy grande: SOLO camión dedicado (LTL ya no aplica)
    if total_weight >= PESO_SOLO_DEDICADO_MIN:
        base.update({
            "tier": "dedicado",
            "dedicated": True,
            "options": [_dedicated_option()],
            "reason": (
                f"Pedido de {total_weight:.0f} kg — supera capacidad de fletera "
                "consolidada. Camión dedicado exclusivo. Confirmamos disponibilidad "
                "por WhatsApp antes de despachar."
            ),
            "source": "dedicated",
        })
        return base

    # Rango híbrido: 300-800 kg O monto > $15k → LTL + dedicado juntos
    if total_weight >= PESO_HIBRIDO_MIN or total_amount >= MONTO_DEDICADO_MIN:
        options = []
        # Intento Skydropx primero para tener opciones LTL reales
        if try_realtime:
            try:
                from lib import skydropx
                if skydropx.is_configured():
                    parcels = _build_parcels(products_in_cart)
                    rt = skydropx.get_quotations(dest_zip, parcels, dest_area=dest_area)
                    if rt:
                        for opt in rt[:4]:  # top 4 más baratas
                            opt["source"] = "skydropx"
                            opt["tier"] = "fletera"
                            opt["weight_kg"] = total_weight
                            options.append(opt)
            except Exception as e:
                log.warning("Skydropx exception en híbrido: %s", e)
        # Siempre agrego el dedicado como opción premium al final
        options.append(_dedicated_option())
        base.update({
            "tier": "hibrido",
            "dedicated": True,   # marca visual: hay opción dedicada
            "options": options,
            "reason": (
                f"Pedido grande ({total_weight:.0f} kg / ${total_amount:,.0f} MXN) · "
                f"{len(options)} opciones: fletera consolidada (más económica, 3-6 días) "
                "o camión dedicado (más rápido, exclusivo). Confirmamos disponibilidad "
                "de camión dedicado por WhatsApp."
            ),
            "source": "skydropx" if any(o.get("source") == "skydropx" for o in options) else "dedicated",
        })
        return base

    # Intento Skydropx primero
    if try_realtime:
        try:
            from lib import skydropx
            if skydropx.is_configured():
                parcels = _build_parcels(products_in_cart)
                rt_options = skydropx.get_quotations(dest_zip, parcels, dest_area=dest_area)
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
