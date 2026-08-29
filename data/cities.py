"""
Ciudades objetivo dentro del radio de cobertura preferente 500 km
desde Ciudad Victoria, Tamaulipas (CP 87020).

Cada ciudad genera 2 landing SEO:
  /plafones-acusticos-<slug>
  /aislamiento-<slug>

Y aparece en la página /zonas-cobertura como zona preferente.
"""

# Radio de cobertura preferente (km desde Victoria)
RADIO_PREFERENTE_KM = 500

# 11 ciudades objetivo (~11M personas en cobertura preferente)
CITIES = [
    {
        "slug": "monterrey",
        "nombre": "Monterrey",
        "estado": "Nuevo León",
        "estado_slug": "nuevo-leon",
        "cp_ejemplo": "64000",
        "km_desde_victoria": 320,
        "poblacion_metro": "5.3 millones",
        "industria_destacada": "Construcción industrial y residencial premium · corredor manufacturero",
        "productos_gancho": ["MBI para naves industriales", "Plafones acústicos para oficinas corporativas", "Glasswool para tablaroca"],
        "areas_conurbadas": ["San Nicolás", "Guadalupe", "Apodaca", "San Pedro Garza García", "Escobedo", "Santa Catarina", "Juárez"],
        "tiempo_entrega": "24-48 horas",
    },
    {
        "slug": "saltillo",
        "nombre": "Saltillo",
        "estado": "Coahuila",
        "estado_slug": "coahuila",
        "cp_ejemplo": "25000",
        "km_desde_victoria": 400,
        "poblacion_metro": "900 mil",
        "industria_destacada": "Corredor automotriz · plantas Chrysler, GM, Ford",
        "productos_gancho": ["MBI para naves automotrices", "Aislamiento acústico oficinas", "Plafones para escuelas técnicas"],
        "areas_conurbadas": ["Ramos Arizpe", "Arteaga"],
        "tiempo_entrega": "24-48 horas",
    },
    {
        "slug": "san-luis-potosi",
        "nombre": "San Luis Potosí",
        "estado": "San Luis Potosí",
        "estado_slug": "san-luis-potosi",
        "cp_ejemplo": "78000",
        "km_desde_victoria": 460,
        "poblacion_metro": "1.2 millones",
        "industria_destacada": "Bajío norte · industria automotriz creciente (BMW, GM) · residencial",
        "productos_gancho": ["MBI naves industriales BMW/GM", "Glasswool oficinas", "Plafones plazas comerciales"],
        "areas_conurbadas": ["Soledad de Graciano Sánchez"],
        "tiempo_entrega": "24-48 horas",
    },
    {
        "slug": "reynosa",
        "nombre": "Reynosa",
        "estado": "Tamaulipas",
        "estado_slug": "tamaulipas",
        "cp_ejemplo": "88500",
        "km_desde_victoria": 200,
        "poblacion_metro": "900 mil",
        "industria_destacada": "Frontera con EU · maquilas · centros de distribución",
        "productos_gancho": ["MBI para maquilas y bodegas", "Glasswool para muros interiores", "Plafones oficinas administrativas"],
        "areas_conurbadas": ["Río Bravo"],
        "tiempo_entrega": "Mismo día o siguiente",
    },
    {
        "slug": "matamoros",
        "nombre": "Matamoros",
        "estado": "Tamaulipas",
        "estado_slug": "tamaulipas",
        "cp_ejemplo": "87300",
        "km_desde_victoria": 250,
        "poblacion_metro": "520 mil",
        "industria_destacada": "Frontera puerto · maquilas · construcción residencial",
        "productos_gancho": ["MBI naves industriales", "Aislamiento residencial", "Plafones comerciales"],
        "areas_conurbadas": [],
        "tiempo_entrega": "Mismo día o siguiente",
    },
    {
        "slug": "nuevo-laredo",
        "nombre": "Nuevo Laredo",
        "estado": "Tamaulipas",
        "estado_slug": "tamaulipas",
        "cp_ejemplo": "88000",
        "km_desde_victoria": 300,
        "poblacion_metro": "400 mil",
        "industria_destacada": "Aduana + logística · centros de distribución · residencial",
        "productos_gancho": ["MBI centros de distribución", "Plafones oficinas aduanales", "Glasswool oficinas"],
        "areas_conurbadas": [],
        "tiempo_entrega": "24-48 horas",
    },
    {
        "slug": "monclova",
        "nombre": "Monclova",
        "estado": "Coahuila",
        "estado_slug": "coahuila",
        "cp_ejemplo": "25700",
        "km_desde_victoria": 400,
        "poblacion_metro": "380 mil",
        "industria_destacada": "Capital del acero mexicano · AHMSA · industria pesada y metalmecánica",
        "productos_gancho": ["MBI para naves industriales y siderúrgicas", "Aislamiento térmico para procesos de alta temperatura", "Plafones oficinas administrativas"],
        "areas_conurbadas": ["Frontera", "Castaños", "Nadadores"],
        "tiempo_entrega": "24-48 horas",
    },
    {
        "slug": "piedras-negras",
        "nombre": "Piedras Negras",
        "estado": "Coahuila",
        "estado_slug": "coahuila",
        "cp_ejemplo": "26000",
        "km_desde_victoria": 430,
        "poblacion_metro": "250 mil",
        "industria_destacada": "Frontera con Eagle Pass TX · maquilas · logística binacional",
        "productos_gancho": ["MBI para maquilas y bodegas", "Glasswool para muros interiores", "Plafones oficinas aduanales"],
        "areas_conurbadas": ["Nava"],
        "tiempo_entrega": "24-48 horas",
    },
    {
        "slug": "ciudad-acuna",
        "nombre": "Ciudad Acuña",
        "estado": "Coahuila",
        "estado_slug": "coahuila",
        "cp_ejemplo": "26200",
        "km_desde_victoria": 450,
        "poblacion_metro": "140 mil",
        "industria_destacada": "Frontera con Del Rio TX · maquilas electrónicas y automotrices",
        "productos_gancho": ["MBI para maquilas", "Aislamiento térmico bodegas", "Plafones acústicos oficinas"],
        "areas_conurbadas": [],
        "tiempo_entrega": "24-48 horas",
    },
    {
        "slug": "poza-rica",
        "nombre": "Poza Rica",
        "estado": "Veracruz",
        "estado_slug": "veracruz",
        "cp_ejemplo": "93230",
        "km_desde_victoria": 350,
        "poblacion_metro": "500 mil",
        "industria_destacada": "Industria petrolera Pemex · clima cálido húmedo · residencial y comercial",
        "productos_gancho": ["MBI clave por clima cálido húmedo (ahorro A/C)", "Glasswool oficinas y hoteles", "Plafones humedad-resistentes"],
        "areas_conurbadas": ["Coatzintla", "Tihuatlán"],
        "tiempo_entrega": "24-48 horas",
    },
    {
        "slug": "tampico",
        "nombre": "Tampico",
        "estado": "Tamaulipas",
        "estado_slug": "tamaulipas",
        "cp_ejemplo": "89000",
        "km_desde_victoria": 250,
        "poblacion_metro": "900 mil",
        "industria_destacada": "Puerto · industria petroquímica · turismo · clima cálido húmedo",
        "productos_gancho": ["MBI clave por clima cálido húmedo (ahorro A/C)", "Glasswool para hoteles y oficinas", "Plafones humedad-resistentes"],
        "areas_conurbadas": ["Ciudad Madero", "Altamira"],
        "tiempo_entrega": "24 horas",
    },
]


def all_cities():
    return CITIES


def get(slug):
    for c in CITIES:
        if c["slug"] == slug:
            return c
    return None


def slugs():
    return [c["slug"] for c in CITIES]


def is_preferred_zip(zip_code):
    """Retorna True si el CP corresponde a una ciudad de cobertura preferente."""
    from data.shipping import km_from_victoria
    if not zip_code or len(str(zip_code)) < 2:
        return False
    km = km_from_victoria(zip_code)
    return km <= RADIO_PREFERENTE_KM


def preferred_city_by_zip(zip_code):
    """Si el CP coincide con el prefijo de una ciudad preferente, devuelve la ciudad."""
    if not zip_code or len(str(zip_code)) < 2:
        return None
    prefix = str(zip_code)[:2]
    prefix_map = {c["cp_ejemplo"][:2]: c for c in CITIES}
    return prefix_map.get(prefix)
