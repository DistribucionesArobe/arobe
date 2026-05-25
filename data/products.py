"""
Catálogo de productos de Arobe Group.
Migrado desde insulglass.mx (Shopify) en Fase 1.2.
Enriquecido con fichas técnicas oficiales en Fase 1.3.

Estructura:
- precio_publico: precio MXN al público / detalle
- precio_mayoreo: precio para distribuidores (15% menos que público)
- imagenes: lista de filenames bajo static/img/products/
- ficha_tecnica: filename del PDF bajo static/datasheets/ (opcional)
- specs: dict de propiedades técnicas estructuradas

Para agregar producto: copiar un dict, ajustar slug único, marca/linea válida.
Precio mayoreo se calcula automático si queda en None.
"""

# --- Catálogo ---
PRODUCTS = [
    # =========================================================
    # SUSPAN — Colección Astrónomos (plafones acústicos)
    # =========================================================
    {
        "slug": "brahe-2402",
        "nombre": "Brahe 2402",
        "marca": "suspan",
        "linea": "ceilings",
        "tipo": "Plafón acústico de lana mineral",
        "tagline": "Formato rectangular grande · instalación rápida · Colección Astrónomos",
        "precio_publico": 1890,
        "precio_mayoreo": None,
        "presentacion": "Paquete de 10 piezas",
        "dimensiones": "1.22 m × 0.61 m por pieza",
        "rendimiento_m2": 7.44,
        "imagenes": [
            "brahe-2402-1.png",
            "brahe-2402-2.jpg",
            "brahe-2402-3.png",
            "brahe-2402-4.png",
        ],
        "ficha_tecnica": "brahe-ficha-tecnica.pdf",
        "descripcion": (
            "Plafón acústico de lana mineral con textura tipo fisurada no-direccional. "
            "Formato rectangular de mayor cobertura (1.22 × 0.61 m) ideal cuando "
            "necesitas instalar grandes superficies de plafón en menos tiempo. Orilla "
            "de sombra (Shadow Line / Tegular) compatible con sistemas de suspensión "
            "estándar de 15/16\". Acabado blanco con alto nivel de reflexión lumínica y "
            "resistencia a la humedad y al pandeo."
        ),
        "specs": {
            "tipo_orilla": "Tegular (Orilla de sombra)",
            "tamano_panel": "1.22 m × 0.61 m (4' × 2')",
            "espesor": "5/8\" (15 mm)",
            "clasificacion_fuego": "Clase B",
            "nrc": "0.50",
            "cac_min": "30",
            "lr": "0.82",
            "color": "Blanco estándar",
            "suspension": "Perfil T 15/16\"",
            "emisiones_voc": "Bajo",
            "resistencia_moho": "Estándar",
            "contenido_reciclado": "20-30%",
            "peso": "0.70-0.95 lb/ft² (3.4-4.6 kg/m²)",
            "resistencia_termica": "R-1.2",
            "humedad_max": "70% HR",
            "astm_e1264": "Tipo III, Forma 2, Patrón E",
            "astm_e84": "Clase B",
        },
        "usos": [
            "Mejorar la apariencia visual de techos interiores",
            "Disimular imperfecciones estructurales (grietas, uniones, desniveles)",
            "Contribuir a mejor acústica reduciendo reverberación (NRC 0.50)",
            "Acabado duradero de bajo mantenimiento",
        ],
        "aplicaciones": [
            "Oficinas",
            "Comercios y locales",
            "Espacios educativos",
            "Entretenimiento (cines, restaurantes)",
        ],
        "destacado": True,
    },
    {
        "slug": "galilei-3004",
        "nombre": "Galilei 3004",
        "marca": "suspan",
        "linea": "ceilings",
        "tipo": "Plafón acústico premium",
        "tagline": "Plafón cuadrado premium 61×61 cm · línea superior Astrónomos",
        "precio_publico": 1200,
        "precio_mayoreo": None,
        "presentacion": "Paquete de 10 piezas",
        "dimensiones": "0.61 × 0.61 m por pieza",
        "rendimiento_m2": 3.72,
        "imagenes": [
            "galilei-3004-1.png",
            "galilei-3004-2.jpg",
            "galilei-3004-3.png",
        ],
        # No tengo ficha técnica oficial todavía
        "descripcion": (
            "Plafón acústico cuadrado de 61 × 61 cm en presentación premium dentro "
            "de la Colección Astrónomos. Compatible con suspensión reticular estándar "
            "tipo T 15/16\". Acabado de lana mineral con textura fisurada para "
            "absorción acústica óptima y alta reflectancia lumínica."
        ),
        "specs": {
            "tipo_orilla": "Tegular (Orilla de sombra)",
            "tamano_panel": "0.61 × 0.61 m (2' × 2')",
            "espesor": "5/8\" (15 mm)",
            "color": "Blanco estándar",
            "suspension": "Perfil T 15/16\"",
        },
        "usos": [
            "Acabado decorativo premium en techos suspendidos",
            "Espacios donde se busca mejor desempeño acústico que en gama económica",
            "Disimular instalaciones eléctricas y de A/C con estética superior",
        ],
        "aplicaciones": [
            "Oficinas corporativas premium",
            "Salas de juntas y boardrooms",
            "Hoteles y espacios hospitality",
            "Showrooms y áreas comerciales premium",
        ],
        "destacado": True,
    },
    {
        "slug": "kepler-0504",
        "nombre": "Kepler 0504",
        "marca": "suspan",
        "linea": "ceilings",
        "tipo": "Plafón acústico de lana mineral",
        "tagline": "Plafón cuadrado tradicional 61×61 cm · garantía 10 años",
        "precio_publico": 950,
        "precio_mayoreo": None,
        "presentacion": "Paquete de 10 piezas",
        "dimensiones": "0.61 × 0.61 m por pieza",
        "rendimiento_m2": 3.72,
        "imagenes": [
            "kepler-0504-1.png",
            "kepler-0504-2.jpg",
            "kepler-0504-3.png",
        ],
        "ficha_tecnica": "kepler-ficha-tecnica.pdf",
        "descripcion": (
            "Panel acústico de lana mineral con textura fisurada no-direccional, "
            "formato cuadrado versátil de 0.61 × 0.61 m. Mismo formato Tegular "
            "compatible con cualquier proyecto de suspensión estándar. Ideal para "
            "techos interiores con desempeño acústico accesible. Garantía de 10 años "
            "en aplicaciones comerciales."
        ),
        "specs": {
            "tipo_orilla": "Tegular (Orilla de sombra)",
            "tamano_panel": "0.61 × 0.61 m (2' × 2')",
            "espesor": "5/8\" (15 mm)",
            "clasificacion_fuego": "Clase A",
            "nrc": "0.50",
            "cac_min": "30",
            "lr": "0.82",
            "color": "Blanco estándar",
            "suspension": "Perfil T 15/16\"",
            "emisiones_voc": "Bajo",
            "resistencia_moho": "Estándar",
            "contenido_reciclado": "20-30%",
            "peso": "0.70-0.95 lb/ft² (3.4-4.6 kg/m²)",
            "resistencia_termica": "R-1.4",
            "humedad_max": "90% HR",
            "astm_e1264": "Tipo III, Forma 2, Patrón C",
            "astm_e84": "Clase A",
            "garantia": "10 años en aplicaciones comerciales",
        },
        "usos": [
            "Acabado decorativo en techos suspendidos",
            "Mejor resistencia a humedad (90% HR) — apto para baños, cocinas, áreas húmedas",
            "Clasificación Clase A — apto para espacios institucionales",
            "Mejorar acústica del espacio (NRC 0.50)",
        ],
        "aplicaciones": [
            "Oficinas corporativas",
            "Comercios y retail",
            "Salas de cine",
            "Restaurantes",
            "Espacios educativos",
        ],
        "destacado": False,
    },

    # =========================================================
    # INSULGLASS — Aislantes térmicos y acústicos
    # =========================================================
    {
        "slug": "aislamiento-acustico",
        "nombre": "Insulglass Aislamiento Acústico",
        "marca": "insulglass",
        "linea": "glasswool",
        "tipo": "Rollo de fibra de vidrio · sin recubrimiento",
        "tagline": "Glasswool para muros · NRC 0.90 · óptimo control acústico interior",
        "precio_publico": 597,
        "precio_mayoreo": None,
        "presentacion": "Paquete de 2 rollos · 1.22 m combinado",
        "dimensiones": "0.61 m ancho × 15.24 m largo × 2.5\" (6.4 cm) espesor por rollo",
        "rendimiento_m2": 18.6,  # paquete completo (2 rollos × 9.3 m²)
        "imagenes": [
            "aislamiento-acustico-1.png",
            "aislamiento-acustico-2.png",
            "aislamiento-acustico-3.png",
        ],
        "ficha_tecnica": "aislamiento-acustico-ficha-tecnica.pdf",
        "descripcion": (
            "Rollos flexibles de fibra de vidrio sin recubrimiento, diseñados para "
            "aislamiento acústico y térmico en muros y techos con estructuras "
            "metálicas o de madera. Coeficiente NRC 0.90 — óptima absorción de "
            "sonido en frecuencias de 125 Hz a 1000 Hz. Compatible con bastidores "
            "separados a 41 cm (16\") o 61 cm (24\") de centro a centro."
        ),
        "specs": {
            "formato": "Paquete con 2 rollos",
            "dimensiones_rollo": "0.61 m × 15.24 m × 2.5\" (6.4 cm)",
            "cobertura_paquete": "18.6 m² (9.3 m² por rollo)",
            "valor_r": "R-8 (1.41 m²·K/W)",
            "conductividad_termica": "0.04412 W/m·K",
            "nrc": "0.90",
            "frecuencias_eficaces": "125 Hz a 1000 Hz",
            "peso_densidad": "10.81 kg/m³ (0.68 lb/ft³)",
            "permeabilidad_vapor": "1.35 ng/Pa·s·m²",
            "adsorcion_humedad": "0.66% en peso · 0.72% en volumen",
            "astm_e84": "Clase A · incombustible",
            "astm_c1338": "No corrosivo",
            "astm_c1304": "Sin emisión de olores",
            "stc_optimo": "45-50 (con paneles de yeso)",
            "compatibilidad": "Bastidores metálicos o de madera a 16\" o 24\" entre centros",
            "normatividad": "ASTM C665, NOM-018-ENER-2011, Euro class A1",
        },
        "usos": [
            "Control acústico en interiores · NRC 0.90",
            "Reducir transferencia de calor (R-8)",
            "Aplicaciones en clima templado",
            "Espacios sensibles (hospitales, escuelas) por composición no corrosiva e higiénica",
        ],
        "aplicaciones": [
            "Oficinas privadas y cubículos",
            "Salas de juntas y call centers",
            "Estudios de podcast/música (paredes internas)",
            "Cines residenciales",
            "Muros divisorios en departamentos",
            "Escuelas (aulas, bibliotecas)",
            "Consultorios médicos",
        ],
        "destacado": True,
    },
    {
        "slug": "mbi-techos",
        "nombre": "MBI · Manta para Techos",
        "marca": "insulglass",
        "linea": "mbi",
        "tipo": "Rollo MBI con barrera de vapor",
        "tagline": "Aislamiento térmico R-10 · reduce hasta 30% consumo energético",
        "precio_publico": 4332,
        "precio_mayoreo": None,
        "presentacion": "Rollo de 39.63 m²",
        "dimensiones": "1.30 m × 30.48 m × 3\" (7.62 cm) espesor",
        "rendimiento_m2": 39.63,
        "imagenes": [
            "mbi-techos-1.png",
            "mbi-techos-2.png",
            "mbi-techos-3.png",
        ],
        "ficha_tecnica": "mbi-ficha-tecnica.pdf",
        "descripcion": (
            "Rollo flexible de fibra de vidrio de alta densidad (3\" de espesor) con "
            "barrera de vapor de polipropileno reforzado con kraft. Diseñado "
            "específicamente para techos y muros de naves industriales y "
            "comerciales. En climas calurosos (Mérida, Cancún, Monterrey, Mexicali) "
            "puede reducir hasta 30% el consumo energético al actuar como escudo "
            "térmico contra temperaturas extremas (hasta 50°C en verano)."
        ),
        "specs": {
            "composicion": "Colchón fibra de vidrio + papel kraft + película polipropileno reforzado",
            "ancho": "1.30 m",
            "espesor": "3\" (7.62 cm)",
            "largo": "30.48 m",
            "rendimiento": "39.63 m² por rollo",
            "valor_r": "R-10",
            "resistencia_termica_astm": "ASTM C177/C518 → R-10",
            "barrera_vapor": "Polipropileno reforzado con Kraft",
            "nrc": "0.12 (banda 100 Hz)",
            "astm_e84_ul723": "FHC 25/50",
            "astm_e136": "No combustible",
            "astm_c1338": "Cumple resistencia a hongos",
            "astm_c665": "Cumple corrosividad",
            "astm_c1304": "Cumple emisión de olor",
            "astm_c1104": "Sorción vapor < 0.2% en volumen",
            "euro_class": "Euro class A1 (EN 13501-1:2007)",
            "normatividad": "ISO 9001:2008, ISO 14001:2004, EN 13162:2008, CE",
            "ahorro_energetico": "Hasta 30% consumo de A/C en climas cálidos",
        },
        "usos": [
            "Aislamiento térmico de techos y cubiertas",
            "Reducir hasta 30% el consumo de aire acondicionado",
            "Control de condensación gracias a barrera de vapor",
            "Compatibilidad con metales · no corrosivo",
            "Control acústico de impactos (lluvia, granizo)",
        ],
        "aplicaciones": [
            "Techos y muros de naves industriales y comerciales",
            "Hangares",
            "Supermercados",
            "Bodegas y almacenes",
            "Centros comerciales y de distribución",
            "Colegios y escuelas",
            "Gimnasios y centros deportivos",
            "Tiendas de conveniencia",
        ],
        "destacado": True,
    },
]


# --- Helpers ---
MAYOREO_FACTOR = 0.85  # 15% de descuento sobre precio público

def _normalize():
    """Calcula precio_mayoreo si quedó en None."""
    for p in PRODUCTS:
        if p.get("precio_mayoreo") is None:
            p["precio_mayoreo"] = round(p["precio_publico"] * MAYOREO_FACTOR, 2)

_normalize()


def all_products():
    """Lista completa, en el orden del catálogo."""
    return PRODUCTS


def featured_products():
    """Productos marcados como destacados (aparecen en home)."""
    return [p for p in PRODUCTS if p.get("destacado")]


def by_marca(marca):
    """Filtra por marca: 'suspan' o 'insulglass'."""
    return [p for p in PRODUCTS if p["marca"] == marca]


def by_marca_y_linea(marca, linea):
    """Filtra por marca + sub-línea (ej: suspan + ceilings)."""
    return [p for p in PRODUCTS if p["marca"] == marca and p["linea"] == linea]


def get(slug):
    """Devuelve un producto por slug, o None si no existe."""
    for p in PRODUCTS:
        if p["slug"] == slug:
            return p
    return None
