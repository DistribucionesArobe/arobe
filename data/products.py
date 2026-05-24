"""
Catálogo de productos de Arobe Group.
Migrado desde insulglass.mx (Shopify) en Fase 1.2.

Estructura:
- precio_publico: precio MXN al público / detalle
- precio_mayoreo: precio para distribuidores (15% menos que público)
- imagenes: lista de filenames bajo static/img/products/

Para agregar producto nuevo: copiar un dict, ajustar slug único, marca/linea válida.
Para ajustar precios: editar precio_publico, el mayoreo se calcula automático abajo si quedó en None.
"""

# --- Catálogo ---
PRODUCTS = [
    # =========================================================
    # SUSPAN — Plafones texturizados (línea de astrónomos)
    # =========================================================
    {
        "slug": "brahe-2402",
        "nombre": "Brahe 2402",
        "marca": "suspan",
        "linea": "ceilings",
        "tipo": "Plafón texturizado",
        "tagline": "Acabado texturizado para techos interiores · formato rectangular",
        "precio_publico": 1890,
        "precio_mayoreo": None,  # se calcula auto
        "presentacion": "Paquete de 10 piezas",
        "dimensiones": "61 cm × 1.22 m por pieza",
        "rendimiento_m2": 7.44,   # 0.61 × 1.22 × 10
        "imagenes": [
            "brahe-2402-1.png",
            "brahe-2402-2.jpg",
            "brahe-2402-3.png",
            "brahe-2402-4.png",
        ],
        "descripcion": (
            "Plafón texturizado de formato 61 × 122 cm, ideal para techos interiores "
            "donde se busca un acabado decorativo de bajo mantenimiento. Pieza ligera, "
            "fácil de instalar sobre estructura de aluminio o suspensión metálica."
        ),
        "usos": [
            "Mejorar la apariencia visual de techos interiores",
            "Disimular imperfecciones estructurales (grietas, uniones, desniveles)",
            "Contribuir a mejor acústica reduciendo reverberación",
            "Acabado duradero de bajo mantenimiento",
        ],
        "aplicaciones": [
            "Viviendas particulares (casas y departamentos)",
            "Oficinas corporativas y edificios administrativos",
            "Locales comerciales y establecimientos de servicios",
            "Escuelas, hospitales y espacios institucionales",
        ],
        "destacado": True,
    },
    {
        "slug": "galilei-3004",
        "nombre": "Galilei 3004",
        "marca": "suspan",
        "linea": "ceilings",
        "tipo": "Plafón texturizado",
        "tagline": "Plafón cuadrado clásico 61 × 61 cm · ideal para reticulado estándar",
        "precio_publico": 1200,
        "precio_mayoreo": None,
        "presentacion": "Paquete de 10 piezas",
        "dimensiones": "61 × 61 cm por pieza",
        "rendimiento_m2": 3.72,
        "imagenes": [
            "galilei-3004-1.png",
            "galilei-3004-2.jpg",
            "galilei-3004-3.png",
        ],
        "descripcion": (
            "Plafón cuadrado de 61 × 61 cm, formato estándar para suspensión "
            "reticular tipo T. Acabado texturizado con relieves que mejoran la "
            "estética del techo y disimulan imperfecciones."
        ),
        "usos": [
            "Acabado decorativo en techos suspendidos",
            "Mejorar acústica del espacio",
            "Disimular instalaciones eléctricas y de A/C",
            "Reducir reverberación en aulas y oficinas",
        ],
        "aplicaciones": [
            "Oficinas corporativas",
            "Locales comerciales",
            "Escuelas y hospitales",
            "Viviendas residenciales",
        ],
        "destacado": True,
    },
    {
        "slug": "kepler-0504",
        "nombre": "Kepler 0504",
        "marca": "suspan",
        "linea": "ceilings",
        "tipo": "Plafón texturizado",
        "tagline": "Plafón económico 61 × 61 cm · mejor precio por pieza",
        "precio_publico": 950,
        "precio_mayoreo": None,
        "presentacion": "Paquete de 10 piezas",
        "dimensiones": "61 × 61 cm por pieza",
        "rendimiento_m2": 3.72,
        "imagenes": [
            "kepler-0504-1.png",
            "kepler-0504-2.jpg",
            "kepler-0504-3.png",
        ],
        "descripcion": (
            "Plafón cuadrado estándar 61 × 61 cm en presentación económica. "
            "Mismo formato y aplicación que la línea Galilei, optimizado para "
            "proyectos de gran volumen donde el costo por pieza es crítico."
        ),
        "usos": [
            "Acabado decorativo en techos suspendidos",
            "Proyectos de gran volumen donde el costo importa",
            "Disimular imperfecciones estructurales",
            "Mejorar acústica del espacio",
        ],
        "aplicaciones": [
            "Oficinas corporativas",
            "Locales comerciales y naves",
            "Escuelas y espacios institucionales",
            "Vivienda multifamiliar",
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
        "tipo": "Rollo de fibra de vidrio",
        "tagline": "Rollo de fibra de vidrio · reduce paso de sonido y calor",
        "precio_publico": 597,
        "precio_mayoreo": None,
        "presentacion": "Rollo individual (paquete contiene 2 rollos)",
        "dimensiones": "2.5\" espesor × 0.61 m ancho × 15.24 m largo",
        "rendimiento_m2": 9.29,
        "imagenes": [
            "aislamiento-acustico-1.png",
            "aislamiento-acustico-2.png",
            "aislamiento-acustico-3.png",
        ],
        "descripcion": (
            "La fibra de vidrio es un aislante ligero y flexible, fabricado con "
            "filamentos entrelazados que reducen el paso del sonido y el calor. "
            "Fácil de instalar, no se quema y se adapta a muros, techos o "
            "estructuras metálicas sin necesidad de adhesivos."
        ),
        "usos": [
            "Reducir transferencia de calor entre interior y exterior",
            "Aislamiento acústico (atenuación de ruido)",
            "Mejorar eficiencia energética del inmueble",
            "Mantener temperatura confortable",
        ],
        "aplicaciones": [
            "Techos, plafones y azoteas residenciales y comerciales",
            "Muros interiores y exteriores",
            "Pisos y entrepisos",
            "Cámaras frigoríficas y áreas de control térmico",
            "Naves industriales, bodegas y edificios corporativos",
        ],
        "destacado": True,
    },
    {
        "slug": "mbi-techos",
        "nombre": "MBI · Manta para Techos",
        "marca": "insulglass",
        "linea": "mbi",
        "tipo": "Rollo MBI con barrera de vapor",
        "tagline": "Aislante térmico para cubierta · barrera de vapor incluida",
        "precio_publico": 4332,
        "precio_mayoreo": None,
        "presentacion": "Rollo",
        "dimensiones": "1.30 m × 30.48 m",
        "rendimiento_m2": 39.62,
        "imagenes": [
            "mbi-techos-1.png",
            "mbi-techos-2.png",
            "mbi-techos-3.png",
        ],
        "descripcion": (
            "El MBI (Material de Barrera Insulante) de fibra de vidrio para techos "
            "es un aislante térmico diseñado para reducir la transferencia de "
            "calor a través de la cubierta del inmueble. Fabricado a base de "
            "fibra de vidrio con alta capacidad de aislamiento térmico y "
            "resistencia. Incluye barrera de vapor de polipropileno reforzado "
            "con kraft que ofrece mayor resistencia mecánica."
        ),
        "usos": [
            "Reducir transferencia de calor en cubiertas y techos",
            "Mejorar eficiencia energética del inmueble",
            "Mantener temperatura confortable bajo techo metálico",
            "Reducir condensación gracias a barrera de vapor",
        ],
        "aplicaciones": [
            "Techos y azoteas residenciales y comerciales",
            "Naves industriales y bodegas",
            "Edificios corporativos",
            "Cámaras frigoríficas",
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
