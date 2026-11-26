"""
Fase 18 — Landings para obra industrial.
URLs destino de campañas Google Ads segmentadas por ciudad.

Rutas:
  /aislamiento-naves         → MBI manta R-10 (techos y muros de lámina)
  /plafon-industrial         → plafón reticulado/acústico (oficinas de planta)
  /aislamiento-muros         → Glasswool para tablaroca (oficinas industriales)
  /pvc-areas-sanitarias      → tablero PVC SusPan (plantas alimentos, cuartos limpios)
  /obra/contacto             → POST del formulario corto

Query params soportados:
  ?ciudad=<slug>             → cambia titular + mensaje WhatsApp
  ?utm_source=... etc        → preservados en gtag + sessionStorage
  ?gclid=...                 → preservado para atribución
"""
import logging
from datetime import datetime
from urllib.parse import quote

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)

from data import industrial_cities as ic

industrial_bp = Blueprint("industrial", __name__)
log = logging.getLogger("industrial")


# ============================================================
# Catálogo de landings — un dict por producto con todo lo que
# necesita el template. Mantener en el mismo archivo para
# edición rápida sin saltar entre múltiples módulos.
# ============================================================
LANDINGS = {
    "aislamiento-naves": {
        "path":      "/aislamiento-naves",
        "producto":  "mbi",
        "marca":     "Insulglass",
        "nombre":    "Manta MBI R-10",
        "tipo":      "aislante para naves industriales",
        # Hero
        "pretitulo":         "Manta MBI R-10 para naves industriales",
        "subtitulo_tpl":     "Entrega {TITULAR_CIUDAD} · precio de importador directo",
        "subcopy":           (
            "Manta Insulglass R-10 para techos y muros de lámina. Baja el calor "
            "interior, elimina el goteo por condensación y mejora la acústica. "
            "Surtimos tráiler completo o tarima — entrega directa en obra."
        ),
        # Para qué sirve
        "beneficios": [
            ("☀️", "Menos calor interior",     "Reduce la transferencia térmica del techo de lámina. Impacto medible en temperatura de nave y consumo de A/C donde lo haya."),
            ("💧", "Evita goteo por condensación", "La barrera de vapor del facing WMP-VR impide que la humedad del interior condense sobre la cara fría de la lámina."),
            ("🔇", "Mejora acústica interior", "Absorbe reverberación generada por maquinaria, montacargas y operación. Reduce fatiga auditiva del personal."),
            ("🔥", "No propaga llama",         "Fibra de vidrio inorgánica, no combustible. Aceptada por aseguradoras y códigos de construcción industrial."),
        ],
        # Specs (se cruza con data/products.py cuando el slug coincide)
        "producto_slug":     "mbi-techos",
        "ficha_pdf":         "mbi-ficha-tecnica.pdf",
        "pedido_minimo":     "[PEDIDO_MINIMO_TARIMAS_MBI] tarimas",
        "pedido_minimo_nota":"Pedidos menores se cotizan con flete por separado.",
        # Imagen hero
        "hero_image":        "banner-envios-gratis.jpg",
        "foto_obra":         "[FOTO_OBRA_ALTAMIRA]",
        "foto_obra_alt":     "Obra industrial surtida con MBI R-10 en Altamira, Tamaulipas",
        # WhatsApp
        "wa_tpl":            "Hola, quiero cotizar MBI para una nave {EN_CIUDAD}. Aprox ___ m²",
        # SEO
        "seo_title_tpl":     "Manta MBI R-10 para naves industriales {EN_CIUDAD} · Entrega directa | Arobe Group",
        "seo_desc_tpl":      (
            "Aislante MBI R-10 Insulglass para techos y muros de naves industriales {EN_CIUDAD}. "
            "Precio de importador directo, entrega en obra, factura CFDI 4.0. "
            "Cotiza por WhatsApp."
        ),
        "seo_keywords":      [
            "aislante para nave industrial", "manta para techo de lámina",
            "MBI R-10", "aislante Insulglass naves", "aislamiento techo metálico",
            "evitar condensación nave industrial", "aislante para nave de lámina",
        ],
        "faqs": [
            ("¿Cuál es el tiempo de entrega?",
             "Para proyectos dentro del radio de 500 km de Ciudad Victoria entregamos en 2 a 5 días hábiles después de confirmar la orden. Para distancias mayores o pedidos especiales, coordinamos fecha de llegada contigo."),
            ("¿Cuál es el pedido mínimo?",
             "Pedido mínimo [PEDIDO_MINIMO_TARIMAS_MBI] tarimas con flete incluido en obra. Pedidos menores los cotizamos con flete por separado según destino."),
            ("¿Facturan a constructoras y empresas industriales?",
             "Sí. Facturamos CFDI 4.0 en el mismo día. Aceptamos pago por transferencia SPEI y Mercado Pago empresarial. Crédito 15/30 días a evaluación para clientes recurrentes."),
            ("¿Tienen ficha técnica para integrar en licitación?",
             "Sí, la descargas abajo en PDF. También te podemos preparar documentos adicionales para licitación: hoja de seguridad, constancia de no combustibilidad, carta de garantía del fabricante."),
            ("¿Incluyen instalación?",
             "No instalamos directamente, pero te podemos poner en contacto con cuadrillas de instalación en tu zona con experiencia en MBI. El material llega en tarima listo para instalar."),
            ("¿Venden también a distribuidores?",
             "Sí, pero bajo el programa de distribuidores. Si eres distribuidor, pasa a la sección de distribuidores desde el enlace al final de la página."),
        ],
    },

    "plafon-industrial": {
        "path":      "/plafon-industrial",
        "producto":  "plafon",
        "marca":     "SusPan",
        "nombre":    "Plafón reticulado y acústico SusPan",
        "tipo":      "plafón para oficinas industriales",
        "pretitulo":         "Plafón reticulado y acústico para oficinas industriales",
        "subtitulo_tpl":     "Entrega {TITULAR_CIUDAD} · precio de importador directo",
        "subcopy":           (
            "Plafón reticulado SusPan para oficinas administrativas, comedores y "
            "áreas de supervisión dentro de planta. Formato 61×61 cm compatible con "
            "suspensión T 15/16\" estándar. Entregamos tráiler o tarima directo en obra."
        ),
        "beneficios": [
            ("🏢", "Oficinas de planta",       "Áreas administrativas, salas de juntas, comedores, control de piso de producción."),
            ("🔇", "Reduce la reverberación",  "NRC 0.50 — mejora inteligibilidad del habla en oficinas con piso de concreto y muros lisos."),
            ("🔥", "Clase A al fuego",         "ASTM E84 Clase A. Apto para espacios institucionales y proyectos con requerimientos de código."),
            ("💧", "Resiste humedad",          "Hasta 90% HR a 40°C. Aguanta ambientes industriales y limpiezas frecuentes."),
            ("⚡", "Instalación rápida",       "Modular 61×61 cm. Una cuadrilla de 2 instala hasta 150 m² por día en suspensión preparada."),
        ],
        "producto_slug":     "kepler-0504",
        "ficha_pdf":         "kepler-ficha-tecnica.pdf",
        "pedido_minimo":     "[PEDIDO_MINIMO_TARIMAS_PLAFON] tarimas",
        "pedido_minimo_nota":"Pedidos menores se cotizan con flete por separado.",
        "hero_image":        "banner-envios-gratis.jpg",
        "foto_obra":         "[FOTO_OBRA_ALTAMIRA]",
        "foto_obra_alt":     "Oficinas de planta industrial con plafón reticulado SusPan",
        "wa_tpl":            "Hola, quiero cotizar plafón reticulado SusPan para oficinas de una planta {EN_CIUDAD}. Aprox ___ m²",
        "seo_title_tpl":     "Plafón industrial para oficinas de planta {EN_CIUDAD} · SusPan · Entrega directa | Arobe Group",
        "seo_desc_tpl":      (
            "Plafón reticulado y acústico SusPan para oficinas administrativas, comedores y salas "
            "dentro de plantas industriales {EN_CIUDAD}. Precio importador directo, entrega en obra, "
            "factura CFDI. Cotiza por WhatsApp."
        ),
        "seo_keywords":      [
            "plafón para oficinas industriales", "plafón reticulado industrial",
            "plafón acústico planta industrial", "plafón 61x61 industrial",
            "plafón para comedor industrial", "plafón sala de juntas planta",
            "SusPan Kepler", "plafón suspendido T 15/16",
        ],
        "faqs": [
            ("¿Cuál es el tiempo de entrega?",
             "De 2 a 5 días hábiles dentro del radio de 500 km de Ciudad Victoria después de confirmar el pedido."),
            ("¿Cuál es el pedido mínimo?",
             "Pedido mínimo [PEDIDO_MINIMO_TARIMAS_PLAFON] tarimas con flete incluido. Pedidos menores los cotizamos."),
            ("¿Tienen plafones con mejor NRC o Clase A1?",
             "Sí. Tenemos Brahe (rectangular grande 1.22×0.61 m) y Galilei (premium textura micro). Pídenos la comparativa técnica."),
            ("¿Incluyen la perfilería T?",
             "No por defecto, pero la cotizamos junto. Tenemos perfil T 15/16\" blanco y también negro para proyectos con techo oscuro."),
            ("¿Facturan a constructoras?",
             "Sí, CFDI 4.0 en el día. Crédito 15/30 días a evaluación para clientes recurrentes."),
            ("¿Venden también a distribuidores?",
             "Sí, con el programa de distribuidores (ver enlace al final de la página)."),
        ],
    },

    "aislamiento-muros": {
        "path":      "/aislamiento-muros",
        "producto":  "glasswool",
        "marca":     "Insulglass",
        "nombre":    "Glasswool Insulglass",
        "tipo":      "aislante para muros de tablaroca en oficinas industriales",
        "pretitulo":         "Glasswool para muros de tablaroca en oficinas industriales",
        "subtitulo_tpl":     "Entrega {TITULAR_CIUDAD} · precio de importador directo",
        "subcopy":           (
            "Lana de vidrio Insulglass para rellenar muros divisorios de tablaroca "
            "en oficinas administrativas, salas de juntas y cuartos de control. "
            "Reduce ruido entre áreas y mejora confort térmico. Surtimos por tarima o tráiler."
        ),
        "beneficios": [
            ("🔇", "Bloquea ruido entre áreas", "Instalado en muro de tablaroca con cámara, reduce 15–25 dB — suficiente para privacidad en sala de juntas."),
            ("🌡️", "Confort térmico",          "Aísla paredes expuestas a nave caliente o al exterior. Reduce carga térmica en oficinas climatizadas."),
            ("🔥", "No combustible",            "Fibra de vidrio inorgánica. ASTM E136 no combustible. Cumple código."),
            ("⚡", "Fácil de instalar",         "Rollos y paños pre-cortados que caben entre canaletas estándar de 46 y 64 mm."),
        ],
        "producto_slug":     "aislamiento-acustico",
        "ficha_pdf":         "aislamiento-acustico-ficha-tecnica.pdf",
        "pedido_minimo":     "[PEDIDO_MINIMO_TARIMAS_GLASSWOOL] tarimas",
        "pedido_minimo_nota":"Pedidos menores se cotizan con flete por separado.",
        "hero_image":        "banner-envios-gratis.jpg",
        "foto_obra":         "[FOTO_OBRA_ALTAMIRA]",
        "foto_obra_alt":     "Instalación de Glasswool en muros de tablaroca de oficinas industriales",
        "wa_tpl":            "Hola, quiero cotizar Glasswool para muros de tablaroca en oficinas de una planta {EN_CIUDAD}. Aprox ___ m² de muro",
        "seo_title_tpl":     "Glasswool para muros de tablaroca en oficinas industriales {EN_CIUDAD} · Entrega directa | Arobe",
        "seo_desc_tpl":      (
            "Lana de vidrio Insulglass para muros divisorios de tablaroca en oficinas "
            "industriales {EN_CIUDAD}. Precio importador directo, entrega en obra, "
            "factura CFDI 4.0. Cotiza por WhatsApp."
        ),
        "seo_keywords":      [
            "glasswool para muros de tablaroca", "aislante para oficinas industriales",
            "aislamiento acústico oficinas planta", "aislamiento térmico tablaroca",
            "lana de vidrio México", "Insulglass Glasswool",
            "aislante para muro divisorio industrial",
        ],
        "faqs": [
            ("¿Cuál es el tiempo de entrega?",
             "De 2 a 5 días hábiles dentro del radio de 500 km de Ciudad Victoria."),
            ("¿Cuál es el pedido mínimo?",
             "Pedido mínimo [PEDIDO_MINIMO_TARIMAS_GLASSWOOL] tarimas con flete incluido. Menores se cotizan aparte."),
            ("¿Qué espesor conviene para una sala de juntas?",
             "Para muros divisorios internos buscando privacidad acústica, muro doble tablaroca de 1/2\" con glasswool de 2-1/2\" (64 mm) reduce 15-25 dB. Para separación con área productiva de alta sonoridad, pasar a muro con doble capa de tablaroca y glasswool 4\"."),
            ("¿Es segura para salud?",
             "Las lanas de vidrio modernas (post 2000) no están clasificadas como carcinógenas. Durante instalación usar guantes, mangas largas y mascarilla P2. Una vez instalada tras el muro no hay exposición."),
            ("¿Facturan a constructoras?",
             "Sí, CFDI 4.0 en el día. Crédito a evaluación para clientes recurrentes."),
            ("¿Venden también a distribuidores?",
             "Sí, con el programa de distribuidores (enlace al final)."),
        ],
    },

    "pvc-areas-sanitarias": {
        "path":      "/pvc-areas-sanitarias",
        "producto":  "pvc",
        "marca":     "SusPan",
        "nombre":    "Tablero PVC SusPan Board",
        "tipo":      "tablero PVC para plantas de alimentos, cuartos limpios y áreas húmedas",
        "pretitulo":         "Tablero PVC para plantas de alimentos, cuartos limpios y áreas sanitarias",
        "subtitulo_tpl":     "Entrega {TITULAR_CIUDAD} · precio de importador directo",
        "subcopy":           (
            "Tablero PVC SusPan Board — lavable con agua a presión, no se oxida, "
            "no absorbe humedad ni genera moho. Para plantas de alimentos, cuartos "
            "limpios, cámaras frigoríficas, lavanderías industriales y baños "
            "industriales. Entrega directa en obra."
        ),
        "beneficios": [
            ("🧼", "Lavable con agua a presión", "Superficie 100% impermeable. Resiste jet de limpieza diaria en plantas de alimentos y lavanderías."),
            ("🦠", "No genera moho ni bacterias","Sin celulosa, sin papel. No hay sustrato biológico que soporte crecimiento microbiano."),
            ("🧪", "Resiste químicos de limpieza","Cloro, amonios cuaternarios, ácido peracético — compatible con protocolos HACCP."),
            ("❄️", "Para cámaras frigoríficas", "Estabilidad dimensional entre -20°C y 60°C sin craqueo ni delaminación."),
            ("🔥", "Autoextinguible",            "Clase A al fuego (ASTM E84). Apto para espacios con regulación institucional."),
        ],
        "producto_slug":     None,
        "ficha_pdf":         None,
        "pedido_minimo":     "[PEDIDO_MINIMO_TARIMAS_PVC] tarimas",
        "pedido_minimo_nota":"Pedidos menores se cotizan con flete por separado.",
        "hero_image":        "banner-envios-gratis.jpg",
        "foto_obra":         "[FOTO_PRODUCTO_PVC_INDUSTRIAL]",
        "foto_obra_alt":     "Tablero PVC SusPan instalado en planta de alimentos",
        "wa_tpl":            "Hola, quiero cotizar tablero PVC SusPan para una planta {EN_CIUDAD}. Aprox ___ m²",
        "seo_title_tpl":     "Tablero PVC para plantas de alimentos y cuartos limpios {EN_CIUDAD} · SusPan | Arobe",
        "seo_desc_tpl":      (
            "Tablero PVC SusPan Board para plantas de alimentos, cuartos limpios, cámaras "
            "frigoríficas y baños industriales {EN_CIUDAD}. Lavable, no se oxida, Clase A. "
            "Precio importador directo. Cotiza por WhatsApp."
        ),
        "seo_keywords":      [
            "tablero PVC industrial", "panel PVC planta de alimentos",
            "panel PVC cuarto limpio", "revestimiento PVC lavable",
            "PVC para cámara frigorífica", "panel sanitario industrial",
            "SusPan Board PVC", "PVC HACCP",
        ],
        "faqs": [
            ("¿Para qué industrias aplica?",
             "Plantas de alimentos (cárnicos, lácteos, panaderías), lavanderías industriales, cámaras frigoríficas, baños y vestidores de planta, farmacéuticas, hospitales (áreas específicas), estéticas y spas."),
            ("¿Cuál es el tiempo de entrega?",
             "De 2 a 5 días hábiles dentro del radio de 500 km de Ciudad Victoria."),
            ("¿Cuál es el pedido mínimo?",
             "Pedido mínimo [PEDIDO_MINIMO_TARIMAS_PVC] tarimas con flete incluido. Menores se cotizan."),
            ("¿Se puede instalar sobre muro existente?",
             "Sí, con bastidor ligero o directo con adhesivo construcción si el muro es parejo. Se puede reemplazar lambrín o revestimiento viejo sin demoler el muro completo."),
            ("¿Facturan a plantas?",
             "Sí, CFDI 4.0 en el día. Crédito a evaluación para clientes recurrentes con órdenes de compra formales."),
            ("¿Venden también a distribuidores?",
             "Sí, con el programa de distribuidores (enlace al final)."),
        ],
    },
}


def _get_landing_or_404(key):
    data = LANDINGS.get(key)
    if data is None:
        from flask import abort
        abort(404)
    return data


def _get_producto(slug):
    """Carga el producto del catálogo si existe (para specs)."""
    try:
        from data import products as catalog
        for p in catalog.all_products():
            if p.get("slug") == slug:
                return p
    except Exception:
        pass
    return None


def _render_landing(key):
    landing = _get_landing_or_404(key)
    ciudad_slug = (request.args.get("ciudad") or "").strip().lower()
    ciudad = ic.get(ciudad_slug)
    producto = _get_producto(landing["producto_slug"])

    # Build dynamic strings
    titular_ciudad = ciudad["titular"]          # "en Monterrey" o "en tu obra"
    en_ciudad = f"en {ciudad['nombre']}" if ciudad["nombre"] else ""
    seo_en_ciudad = en_ciudad                    # mismo fallback

    subtitulo = landing["subtitulo_tpl"].format(TITULAR_CIUDAD=titular_ciudad)
    seo_title = landing["seo_title_tpl"].format(EN_CIUDAD=en_ciudad or "en México").strip()
    seo_desc  = landing["seo_desc_tpl"].format(EN_CIUDAD=en_ciudad or "en toda la República")

    wa_message = landing["wa_tpl"].format(EN_CIUDAD=en_ciudad or "en mi obra")
    wa_link = f"https://wa.me/{request.host.replace(':','_')}"  # replaced below
    import os as _os
    from flask import current_app
    wa_phone = current_app.config.get("WA_PHONE", "")
    wa_link = f"https://wa.me/{wa_phone}?text={quote(wa_message)}"

    return render_template(
        "industrial/landing.html",
        landing=landing,
        ciudad=ciudad,
        ciudad_slug=ciudad_slug,
        producto=producto,
        coverage_chips=ic.COVERAGE_CHIPS,
        subtitulo=subtitulo,
        seo_title=seo_title,
        seo_description=seo_desc,
        wa_message=wa_message,
        wa_link=wa_link,
    )


# ============================================================
# Rutas públicas
# ============================================================
@industrial_bp.get("/aislamiento-naves")
def aislamiento_naves():
    return _render_landing("aislamiento-naves")


@industrial_bp.get("/plafon-industrial")
def plafon_industrial():
    return _render_landing("plafon-industrial")


@industrial_bp.get("/aislamiento-muros")
def aislamiento_muros():
    return _render_landing("aislamiento-muros")


@industrial_bp.get("/pvc-areas-sanitarias")
def pvc_areas_sanitarias():
    return _render_landing("pvc-areas-sanitarias")


# ============================================================
# Form corto (POST) — envía email y redirige a WhatsApp
# ============================================================
@industrial_bp.post("/obra/contacto")
def obra_contacto():
    form = request.form
    nombre        = (form.get("nombre") or "").strip()
    empresa       = (form.get("empresa") or "").strip()
    ciudad_obra   = (form.get("ciudad_obra") or "").strip()
    m2_aprox      = (form.get("m2_aprox") or "").strip()
    telefono      = (form.get("telefono") or "").strip()
    producto_key  = (form.get("producto_key") or "").strip()
    ciudad_param  = (form.get("ciudad") or "").strip()

    producto_nombre = LANDINGS.get(producto_key, {}).get("nombre", "producto")

    if not (nombre and telefono):
        flash("Faltan nombre y teléfono.", "error")
        return redirect(request.referrer or url_for("industrial.aislamiento_naves"))

    html = f"""
    <h2>Lead obra industrial · {producto_nombre}</h2>
    <p><b>Recibido:</b> {datetime.utcnow().isoformat()} UTC</p>
    <ul>
      <li><b>Nombre:</b> {nombre}</li>
      <li><b>Empresa:</b> {empresa}</li>
      <li><b>Ciudad de la obra:</b> {ciudad_obra}</li>
      <li><b>m² aproximados:</b> {m2_aprox}</li>
      <li><b>Teléfono:</b> {telefono}</li>
      <li><b>Producto landing:</b> {producto_key}</li>
      <li><b>Ciudad del param:</b> {ciudad_param}</li>
    </ul>
    """
    try:
        from lib.emailer import send_email, _admin_email
        send_email(
            to=_admin_email(),
            subject=f"[Obra industrial] {producto_nombre} — {nombre} ({ciudad_obra})",
            html=html,
        )
    except Exception as e:
        log.exception("Error enviando lead obra: %s", e)

    # Redirige a WhatsApp con mensaje precargado (mejor conversión que gracias estática)
    from flask import current_app
    wa_phone = current_app.config.get("WA_PHONE", "")
    wa_text = (
        f"Hola, soy {nombre} de {empresa or 'una empresa'}. "
        f"Tengo una obra {('en '+ciudad_obra) if ciudad_obra else ''} "
        f"de {m2_aprox or '___'} m² aprox. Quiero cotizar {producto_nombre}."
    )
    return redirect(f"https://wa.me/{wa_phone}?text={quote(wa_text)}")
