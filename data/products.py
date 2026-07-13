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
        "peso_kg": 32,            # paq 10pz, calculado de 4.6 kg/m² × 7.44 m²
        "no_paqueteria": True,    # formato grande 1.22m, mejor por fletera
        # --- SEO (Fase 6.5) ---
        "seo_title": "Plafón acústico Brahe 1.22×0.61m · Lana mineral texturizada SusPan",
        "seo_description": (
            "Plafón acústico Brahe 2402 de lana mineral con textura fisurada · "
            "formato 1.22 × 0.61 m · paquete 10 piezas · NRC 0.50 · Clase B. "
            "Compatible con suspensión T 15/16\". Precio público $1,890 MXN. "
            "Envíos toda la República, factura CFDI 4.0."
        ),
        "seo_image_alt": (
            "Plafón acústico texturizado SusPan Brahe 2402 · lana mineral 1.22 × 0.61 m · "
            "Colección Astrónomos"
        ),
        "faqs": [
            {
                "q": "¿Qué tipo de plafón es el Brahe 2402?",
                "a": (
                    "Es un plafón acústico de lana mineral con textura fisurada no-direccional, "
                    "formato rectangular de 1.22 × 0.61 metros. Está diseñado para sistemas "
                    "de suspensión estándar tipo T de 15/16 pulgadas."
                ),
            },
            {
                "q": "¿Cuántas piezas necesito por metro cuadrado?",
                "a": (
                    "Cada paquete cubre 7.44 m² (10 piezas de 0.744 m² cada una). "
                    "Para calcular tu proyecto: divide el área total en m² entre 0.744 "
                    "y redondea hacia arriba."
                ),
            },
            {
                "q": "¿Es apto para áreas húmedas como baños o cocinas?",
                "a": (
                    "El Brahe 2402 tiene una humedad máxima de servicio de 70% HR. Para "
                    "áreas de humedad más alta te recomendamos el Kepler 0504 (90% HR) o "
                    "el Galilei 3004 (90% HR)."
                ),
            },
            {
                "q": "¿Qué diferencia hay entre Brahe, Kepler y Galilei?",
                "a": (
                    "Los tres son plafones acústicos de la Colección Astrónomos con mismo "
                    "NRC (0.50). Brahe es rectangular grande (1.22×0.61m) para instalación "
                    "rápida en áreas grandes. Kepler es cuadrado 61×61 cm con textura fisurada, "
                    "gama económica. Galilei es cuadrado 61×61 cm con textura micro, gama "
                    "premium para espacios de presentación."
                ),
            },
        ],
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
        "tipo": "Plafón acústico premium · textura micro",
        "tagline": "Plafón premium 61×61 cm · acabado micro refinado · alta reflexión lumínica",
        "precio_publico": 1200,
        "precio_mayoreo": None,
        "presentacion": "Paquete de 10 piezas",
        "dimensiones": "0.61 × 0.61 m por pieza",
        "rendimiento_m2": 3.72,
        "peso_kg": 16,            # paq 10pz, 4.6 kg/m² × 3.72 m²
        "no_paqueteria": False,   # 61×61 sí cabe en paquetería estándar
        # --- SEO (Fase 6.5) ---
        "seo_title": "Plafón acústico premium Galilei 61×61 · Textura micro SusPan",
        "seo_description": (
            "Plafón acústico Galilei 3004 premium con textura micro refinada · "
            "formato cuadrado 61×61 cm · paquete 10 piezas · Clase A · garantía 10 años. "
            "Ideal para oficinas corporativas y espacios de presentación. "
            "Precio $1,200 MXN. Envíos toda la República."
        ),
        "seo_image_alt": (
            "Plafón acústico premium SusPan Galilei 3004 · textura micro refinada · "
            "cuadrado 61×61 cm · Colección Astrónomos"
        ),
        "faqs": [
            {
                "q": "¿Por qué el Galilei es premium comparado con Kepler?",
                "a": (
                    "Comparten mismo formato (61×61 cm) y desempeño acústico (NRC 0.50), "
                    "pero Galilei tiene textura micro con acabado refinado, apariencia "
                    "sofisticada ideal para espacios de presentación. Kepler tiene textura "
                    "fisurada, más tradicional y económica."
                ),
            },
            {
                "q": "¿Es apto para áreas húmedas?",
                "a": (
                    "Sí. Su humedad máxima de servicio es 90% HR, apto para baños, cocinas "
                    "comerciales, áreas de servicio y espacios con humedad ambiental elevada."
                ),
            },
            {
                "q": "¿Es incombustible?",
                "a": (
                    "Cumple ASTM E84 Clase A (clasificación contra fuego más exigente en "
                    "sistemas de plafón) y viene con garantía de 10 años en aplicaciones "
                    "comerciales."
                ),
            },
            {
                "q": "¿Cuántos plafones caben en un metro cuadrado?",
                "a": (
                    "Cada plafón mide 0.61 × 0.61 m = 0.3721 m². Necesitas 2.69 piezas "
                    "por m². El paquete de 10 piezas cubre 3.72 m² brutos (sin considerar "
                    "recortes en orillas)."
                ),
            },
        ],
        "imagenes": [
            "galilei-3004-1.png",
            "galilei-3004-2.jpg",
            "galilei-3004-3.png",
        ],
        "ficha_tecnica": "galilei-ficha-tecnica.pdf",
        "descripcion": (
            "Panel acústico de lana mineral con textura tipo micro de acabado "
            "refinado, formato cuadrado versátil 0.61 × 0.61 m. La textura micro "
            "le da apariencia sofisticada ideal para espacios de presentación, "
            "salas de juntas y áreas de recepción. Orilla Tegular con acabado "
            "hundido, compatible con suspensión estándar de 15/16\". Mismo "
            "desempeño acústico (NRC 0.50) que Kepler pero con acabado superior."
        ),
        "specs": {
            "tipo_orilla": "Tegular (Orilla de sombra)",
            "tamano_panel": "0.61 × 0.61 m (2' × 2')",
            "espesor": "5/8\" (15 mm)",
            "textura": "Micro · acabado refinado",
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
            "Acabado decorativo premium en techos suspendidos",
            "Espacios de presentación que requieren apariencia refinada",
            "Mismo desempeño acústico que Kepler pero con textura micro sofisticada",
            "Mejor reflectancia lumínica (LR 0.82) — reduce necesidad de iluminación",
        ],
        "aplicaciones": [
            "Oficinas corporativas",
            "Comercios y retail premium",
            "Salas de cine",
            "Restaurantes",
            "Espacios educativos",
            "Áreas de recepción y presentación",
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
        "peso_kg": 16,            # paq 10pz, 4.6 kg/m² × 3.72 m²
        "no_paqueteria": False,
        # --- SEO (Fase 6.5) ---
        "seo_title": "Plafón acústico Kepler 61×61 · Lana mineral fisurada económica SusPan",
        "seo_description": (
            "Plafón acústico Kepler 0504 de lana mineral con textura fisurada · "
            "cuadrado 61×61 cm · paquete 10 piezas · NRC 0.50 · Clase A · "
            "garantía 10 años. Gama económica ideal para proyectos de volumen. "
            "Precio $950 MXN. Envíos toda la República, CFDI 4.0."
        ),
        "seo_image_alt": (
            "Plafón acústico SusPan Kepler 0504 · lana mineral fisurada · cuadrado 61×61 cm · "
            "Colección Astrónomos"
        ),
        "faqs": [
            {
                "q": "¿Cuál es la diferencia entre Kepler y Galilei si miden lo mismo?",
                "a": (
                    "Ambos son cuadrados 61×61 cm con mismo NRC (0.50). Kepler tiene textura "
                    "fisurada tradicional, gama económica. Galilei tiene textura micro "
                    "refinada, gama premium. Si tu presupuesto es ajustado y quieres el "
                    "mismo desempeño acústico, Kepler es la mejor opción."
                ),
            },
            {
                "q": "¿Sirve para baños u oficinas con humedad?",
                "a": (
                    "Sí, humedad máxima 90% HR — apto para casi cualquier ambiente comercial "
                    "incluyendo baños, cocinas y áreas de servicio."
                ),
            },
            {
                "q": "¿Qué certificaciones tiene?",
                "a": (
                    "ASTM E1264 Tipo III Forma 2 Patrón C · ASTM E84 Clase A (fuego) · "
                    "20-30% contenido reciclado · emisiones VOC bajas. Garantía de 10 años "
                    "en aplicaciones comerciales."
                ),
            },
        ],
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
        "peso_kg": 13,           # 2 rollos × 0.595 m³ × 10.81 kg/m³
        "no_paqueteria": True,   # rollo largo de 15.24m no entra en paquetería
        # --- SEO (Fase 6.5) ---
        "seo_title": "Aislante acústico fibra de vidrio 2.5\" · Glasswool para muros y tablaroca",
        "seo_description": (
            "Aislante acústico Insulglass · rollo de fibra de vidrio 0.61×15.24m × 2.5\" "
            "espesor · NRC 0.90 · R-8 · aislamiento térmico y acústico para muros con "
            "tablaroca. Bastidores 16\" o 24\". Precio $597 MXN/rollo. Envíos toda la "
            "República, CFDI 4.0."
        ),
        "seo_image_alt": (
            "Rollo de aislamiento acústico Insulglass · fibra de vidrio glasswool 2.5 pulgadas · "
            "0.61m × 15.24m para muros y tablaroca"
        ),
        "faqs": [
            {
                "q": "¿Sirve para aislar sonido entre habitaciones?",
                "a": (
                    "Sí, es su aplicación principal. Coeficiente NRC de 0.90 (absorción "
                    "acústica muy alta) en frecuencias 125 Hz a 1000 Hz. Instalado en muro "
                    "de tablaroca 2 caras con este aislante entre bastidores, alcanza STC "
                    "óptimo de 45-50 dB — suficiente para reducir voces, música y ruido "
                    "de oficinas."
                ),
            },
            {
                "q": "¿Cómo se instala en muros de tablaroca?",
                "a": (
                    "Se coloca entre bastidores de madera o metal separados a 41 cm (16\") "
                    "o 61 cm (24\") de centro a centro. No requiere adhesivos, permanece en "
                    "su lugar por compresión gracias a su flexibilidad. Ancho estándar del "
                    "rollo (0.61m) coincide con la separación de bastidores 24\"."
                ),
            },
            {
                "q": "¿Qué diferencia hay con MBI?",
                "a": (
                    "Este aislante acústico va SIN recubrimiento — ideal para MUROS "
                    "internos con tablaroca. El MBI incluye barrera de vapor de "
                    "polipropileno reforzado — diseñado para TECHOS de naves industriales "
                    "donde necesitas también protección contra condensación."
                ),
            },
            {
                "q": "¿Es incombustible?",
                "a": (
                    "Sí. Cumple ASTM E84 Clase A (incombustible), ASTM C1338 (no corrosivo), "
                    "ASTM C1304 (sin emisión de olores). Ideal para hospitales, escuelas "
                    "y espacios que exigen higiene y seguridad al fuego."
                ),
            },
            {
                "q": "¿Cuánta superficie cubre un paquete?",
                "a": (
                    "Cada paquete trae 2 rollos y cubre 18.6 m² totales (9.3 m² por rollo). "
                    "Precio por paquete equivalente: $1,194 MXN (2 rollos × $597 c/u)."
                ),
            },
        ],
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
        "peso_kg": 38,           # rollo 1.30 × 30.48 × 0.0762 m × ~12 kg/m³ + kraft + polipropileno
        "no_paqueteria": True,   # rollo industrial de 30m, requiere fletera obligatorio
        # --- SEO (Fase 6.5) ---
        "seo_title": "MBI aislante para techos R-10 · Manta fibra de vidrio con barrera de vapor",
        "seo_description": (
            "MBI Manta para techos · rollo fibra de vidrio 3\" × 1.30m × 30.48m con "
            "barrera de vapor polipropileno reforzado · R-10 · 39.63 m² por rollo. "
            "Aislante térmico para naves industriales, bodegas y techos comerciales. "
            "Reduce 30% consumo A/C. $4,332 MXN/rollo. Envíos toda la República."
        ),
        "seo_image_alt": (
            "Rollo MBI Insulglass · manta aislante fibra de vidrio 3 pulgadas con barrera "
            "de vapor · 1.30m × 30.48m para techos industriales"
        ),
        "faqs": [
            {
                "q": "¿Para qué techos sirve el MBI?",
                "a": (
                    "MBI está diseñado para techos y muros de naves industriales, "
                    "hangares, supermercados, bodegas, centros de distribución, colegios, "
                    "gimnasios y tiendas de conveniencia. Especialmente útil bajo lámina "
                    "metálica donde el calor exterior es intenso."
                ),
            },
            {
                "q": "¿Qué es la barrera de vapor y por qué importa?",
                "a": (
                    "Es una película de polipropileno reforzado con kraft que impide el "
                    "paso de humedad hacia el aislante. Sin ella, la condensación entre el "
                    "techo caliente y el aire acondicionado interior mojaría el aislante y "
                    "reduciría su capacidad térmica en meses. Con barrera de vapor el "
                    "MBI dura décadas."
                ),
            },
            {
                "q": "¿Cuánto ahorra en aire acondicionado?",
                "a": (
                    "En climas cálidos como Monterrey, Cancún, Mérida o Mexicali, un techo "
                    "sin aislar absorbe hasta 70% del calor ambiental. Instalando MBI R-10 "
                    "puede reducirse hasta 30% el consumo de A/C. El ROI típico es 12-24 meses "
                    "según tamaño de nave y horario de operación."
                ),
            },
            {
                "q": "¿Cuántos rollos necesito por m² de techo?",
                "a": (
                    "Cada rollo cubre 39.63 m². Divide el área de tu techo entre 39.63 y "
                    "redondea hacia arriba. Ejemplo: nave de 500 m² requiere 13 rollos."
                ),
            },
            {
                "q": "¿Se puede instalar sobre techo existente?",
                "a": (
                    "Sí, tanto en obra nueva como retrofit. Se coloca por la cara interior "
                    "del techo, entre estructura metálica o colgando de tirantes. Su "
                    "flexibilidad y ligereza permiten instalación ágil en naves ya en "
                    "operación con mínima interrupción."
                ),
            },
            {
                "q": "¿Es incombustible?",
                "a": (
                    "Sí. La fibra de vidrio es No combustible por ASTM E136. FHC 25/50 "
                    "según ASTM E84 / UL 723. Clasificado como Euro Class A1 según "
                    "EN 13501-1. Cumple con las normas de seguridad al fuego más estrictas."
                ),
            },
        ],
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
