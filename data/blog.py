"""
Blog SEO técnico de Arobe Group.
Cada artículo optimizado por keywords de alta intención B2B construcción MX.

Estructura de cada post:
  slug, title, seo_title, seo_description, keywords, published, updated,
  category, cover_image, excerpt, body_html (HTML directo para poder
  incrustar tablas, listas, secciones), faqs, related_products.
"""

POSTS = [

    # ============================================================
    # 1. Plafones acústicos (evergreen, alta intención)
    # ============================================================
    {
        "slug": "como-elegir-plafon-acustico",
        "title": "Cómo elegir un plafón acústico: guía completa para México",
        "seo_title": "Cómo elegir plafón acústico · NRC, CAC y tipos explicados | Arobe",
        "seo_description": (
            "Guía práctica para elegir el plafón acústico correcto: entiende NRC, CAC, "
            "LR, formatos 61×61 vs 122×61, texturas fisurada vs micro, y qué necesitas "
            "para oficinas, escuelas, hospitales o comercios en México."
        ),
        "keywords": [
            "plafón acústico", "cómo elegir plafón", "NRC plafones", "CAC plafón",
            "plafón 61x61", "plafón acústico México", "lana mineral plafón"
        ],
        "published": "2026-07-14",
        "updated": "2026-07-14",
        "category": "Guías técnicas",
        "cover_image": "brahe-2402-3.png",
        "excerpt": (
            "Elegir mal el plafón cuesta caro: reverberación, humedad, incendios. "
            "Aquí explicamos qué significan NRC, CAC y LR y cómo elegir el plafón "
            "correcto según tu espacio."
        ),
        "body_html": """
<p class="lead">Un plafón acústico no es solo un techo bonito — es un componente estructural
que afecta ruido, iluminación, resistencia al fuego y facturas de energía. Elegir el
plafón incorrecto termina costando el doble cuando toca reponerlo. En esta guía te
explicamos las 4 métricas clave (NRC, CAC, LR, ASTM E84), qué formato usar según
tu proyecto, y qué preguntas hacerle a tu proveedor antes de firmar la orden.</p>

<h2>Las 4 métricas que importan</h2>

<h3>1. NRC (Noise Reduction Coefficient)</h3>
<p>El NRC mide cuánto sonido <strong>absorbe</strong> el plafón (0 = refleja todo, 1 = absorbe todo).
Para oficinas modernas, aulas y consultorios busca <strong>NRC ≥ 0.50</strong>. Los plafones
de lana mineral texturizados (como los <a href="/producto/brahe-2402">Brahe</a>,
<a href="/producto/kepler-0504">Kepler</a> y <a href="/producto/galilei-3004">Galilei</a>
de la Colección Astrónomos SusPan) tienen NRC 0.50, absorbiendo la mitad del sonido
que rebota — suficiente para reducir la reverberación en espacios con techo alto.</p>

<h3>2. CAC (Ceiling Attenuation Class)</h3>
<p>El CAC mide qué tanto el plafón <strong>bloquea</strong> el sonido que viaja entre
espacios contiguos por el plenum (el hueco arriba del plafón). Para oficinas privadas,
salas de juntas o consultorios médicos donde hay conversaciones confidenciales busca
<strong>CAC ≥ 30</strong>. Sin buen CAC, la persona en el cubículo de al lado escucha
tu llamada aunque el plafón absorba mucho.</p>

<h3>3. LR (Light Reflectance)</h3>
<p>La reflectancia lumínica es qué porcentaje de la luz rebota del plafón hacia el
espacio. Un LR alto (0.82 o más, que es lo estándar en plafones blancos SusPan)
significa menos lámparas necesarias, menos consumo eléctrico. En una oficina de
500 m² con LR 0.82 vs una con LR 0.60, puedes ahorrar 15-20% en iluminación.</p>

<h3>4. ASTM E84 — clasificación al fuego</h3>
<p>Los plafones se clasifican Clase A (más resistente al fuego) o Clase B (aceptable
para uso general). Para hospitales, escuelas, hoteles y espacios institucionales
en México, casi todos los códigos exigen <strong>Clase A</strong>. El Brahe 2402 es
Clase B (comercios y oficinas estándar); Kepler y Galilei son Clase A (aptos para
proyectos institucionales exigentes).</p>

<h2>Formato: 61×61 vs 122×61</h2>

<p>La decisión de formato depende de 3 factores:</p>
<ul>
  <li><strong>Tamaño del espacio.</strong> Áreas grandes (naves industriales, showrooms) se instalan más rápido con formato 122×61 (Brahe). Áreas chicas con muchos recortes trabajan mejor con 61×61 (Kepler, Galilei).</li>
  <li><strong>Suspensión existente.</strong> Ambos formatos usan perfil T de 15/16 pulgadas — el estándar de la industria. Si ya tienes la retícula instalada, verifica el módulo antes de comprar.</li>
  <li><strong>Estética.</strong> El formato cuadrado 61×61 se ve más "clásico"; el rectangular 122×61 se ve más "moderno" y hace que los techos parezcan más altos.</li>
</ul>

<h2>Textura fisurada vs textura micro</h2>

<p>La textura del plafón afecta la percepción visual y el precio. Dentro de la Colección
Astrónomos SusPan, la diferencia entre Kepler y Galilei es exactamente eso: mismo formato
61×61, mismo NRC 0.50, pero Kepler es textura fisurada (tradicional, económica) y Galilei
es textura micro (refinada, premium para áreas de presentación).</p>

<div class="overflow-x-auto my-6">
<table class="w-full text-sm border-collapse">
  <thead class="bg-slate-100">
    <tr>
      <th class="p-3 text-left border">Modelo</th>
      <th class="p-3 border">Textura</th>
      <th class="p-3 border">Formato</th>
      <th class="p-3 border">Clase</th>
      <th class="p-3 border">Humedad máx</th>
      <th class="p-3 border">Precio (10pz)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="p-3 border font-semibold">Brahe 2402</td><td class="p-3 border">Fisurada</td><td class="p-3 border">1.22 × 0.61 m</td><td class="p-3 border">B</td><td class="p-3 border">70% HR</td><td class="p-3 border">$1,890</td></tr>
    <tr><td class="p-3 border font-semibold">Kepler 0504</td><td class="p-3 border">Fisurada</td><td class="p-3 border">0.61 × 0.61 m</td><td class="p-3 border">A</td><td class="p-3 border">90% HR</td><td class="p-3 border">$950</td></tr>
    <tr><td class="p-3 border font-semibold">Galilei 3004</td><td class="p-3 border">Micro</td><td class="p-3 border">0.61 × 0.61 m</td><td class="p-3 border">A</td><td class="p-3 border">90% HR</td><td class="p-3 border">$1,200</td></tr>
  </tbody>
</table>
</div>

<h2>Cómo elegir según tu proyecto</h2>

<h3>Oficinas corporativas estándar</h3>
<p>Kepler 0504 — mejor relación costo/beneficio. NRC 0.50, Clase A, humedad 90% HR
te cubre para casi cualquier ambiente comercial. Precio bajo permite proyectos de
volumen sin explotar el presupuesto.</p>

<h3>Oficinas premium, salas de junta, showrooms, hoteles</h3>
<p>Galilei 3004 — misma performance técnica que Kepler pero con textura micro que
se ve refinada. La diferencia visual la ves al voltear al techo.</p>

<h3>Comercios grandes, tiendas, plazas, naves con áreas amplias</h3>
<p>Brahe 2402 — el formato 122×61 reduce a la mitad el tiempo de instalación en
áreas grandes. Es Clase B (no apto para hospitales) pero suficiente para retail,
oficinas administrativas, restaurantes.</p>

<h3>Baños, cocinas comerciales, spas — cualquier área con humedad</h3>
<p>Kepler o Galilei — ambos aguantan 90% HR sin pandearse. Brahe se limita a
70% HR y no es la mejor opción para áreas húmedas.</p>

<h3>Hospitales, escuelas, edificios institucionales</h3>
<p>Kepler o Galilei (ambos Clase A). Además necesitas verificar contenido reciclado
y emisiones VOC para cumplir con LEED o especificaciones institucionales — ambos
tienen 20-30% contenido reciclado y VOC bajos.</p>

<h2>Cuántas piezas necesitas</h2>

<p>Los 3 modelos se venden en paquete de 10 piezas:</p>
<ul>
  <li>Brahe 2402: cubre 7.44 m² por paquete (10 piezas × 0.7442 m² c/u)</li>
  <li>Kepler / Galilei: cubre 3.72 m² por paquete (10 piezas × 0.3721 m² c/u)</li>
</ul>
<p><strong>Regla práctica:</strong> divide el área total en m² entre el rendimiento del
paquete y suma 10% para recortes en orillas y desperdicio. Ejemplo: oficina de
150 m² con Kepler → 150 / 3.72 = 40.3 paquetes → suma 10% = 45 paquetes.</p>

<h2>Preguntas para tu proveedor antes de comprar</h2>
<ol>
  <li><strong>¿La ficha técnica que me pasan es del producto real que voy a recibir?</strong> Pide el PDF oficial del fabricante con matrícula ASTM E1264.</li>
  <li><strong>¿Cuál es la garantía?</strong> Los Kepler y Galilei traen 10 años en aplicaciones comerciales.</li>
  <li><strong>¿Tienen stock o es bajo pedido?</strong> Un proyecto que se retrasa 3 meses por importación puede costar más que la diferencia de precio.</li>
  <li><strong>¿Facturan con CFDI 4.0?</strong> Si no, tu contador te va a odiar en la conciliación.</li>
</ol>
        """,
        "faqs": [
            {
                "q": "¿Qué NRC necesito para una oficina?",
                "a": "Para oficinas estándar y salas de juntas busca NRC ≥ 0.50. Espacios con techo muy alto o áreas de call center pueden requerir NRC ≥ 0.70 (requieren plafones especializados)."
            },
            {
                "q": "¿Puedo instalar plafón acústico sobre suspensión que ya tengo?",
                "a": "Sí, si es perfil T de 15/16 pulgadas (el estándar). Verifica el módulo (61×61 o 122×61) antes de comprar. Todos los plafones SusPan son compatibles con suspensión estándar."
            },
            {
                "q": "¿Cuál es la diferencia real entre Kepler y Galilei si tienen mismo formato?",
                "a": "Textura y precio. Kepler es fisurada (tradicional, económica); Galilei es micro (refinada, premium). Mismo NRC 0.50 y CAC 30, misma clasificación Clase A."
            }
        ],
        "related_products": ["brahe-2402", "kepler-0504", "galilei-3004"],
    },

    # ============================================================
    # 2. Glasswool vs MBI
    # ============================================================
    {
        "slug": "glasswool-vs-mbi-cual-aislante-elegir",
        "title": "Glasswool vs MBI: qué aislante de fibra de vidrio elegir",
        "seo_title": "Glasswool vs MBI · Guía comparativa aislante fibra de vidrio | Insulglass",
        "seo_description": (
            "¿Aislante glasswool o MBI? Comparativa técnica de fibra de vidrio para "
            "muros con tablaroca (NRC 0.90) vs techos industriales (R-10 con barrera "
            "de vapor). Precios, dimensiones y guía de aplicación."
        ),
        "keywords": [
            "glasswool vs mbi", "diferencia glasswool mbi", "aislante fibra de vidrio",
            "MBI aislante", "glasswool para tablaroca", "aislante para techo industrial"
        ],
        "published": "2026-07-14",
        "updated": "2026-07-14",
        "category": "Guías técnicas",
        "cover_image": "aislamiento-acustico-2.png",
        "excerpt": (
            "Ambos son fibra de vidrio, pero uno es para muros con tablaroca y el "
            "otro para techos de naves industriales. Elegir mal significa condensación, "
            "R-value insuficiente o desperdicio de material."
        ),
        "body_html": """
<p class="lead">Glasswool y MBI son ambos aislantes de fibra de vidrio de Insulglass®,
pero están diseñados para aplicaciones diferentes. Confundirlos es el error más común
que vemos en obra: instalar glasswool acústico en un techo industrial resulta en
condensación crónica; poner MBI en un muro divisorio es un desperdicio de valor R.
Aquí te explicamos exactamente cuándo usar cada uno.</p>

<h2>La diferencia estructural clave</h2>

<p>Glasswool acústico Insulglass viene <strong>sin recubrimiento</strong> — es un rollo
de fibra de vidrio "desnudo", flexible, listo para meterse entre bastidores de
tablaroca. MBI viene con <strong>barrera de vapor de polipropileno reforzado con kraft</strong>
laminada de fábrica — es un rollo mucho más rígido diseñado para techos donde el
diferencial de temperatura interior/exterior generaría condensación sin la barrera.</p>

<h2>Especificaciones lado a lado</h2>

<div class="overflow-x-auto my-6">
<table class="w-full text-sm border-collapse">
  <thead class="bg-slate-100">
    <tr>
      <th class="p-3 text-left border">Característica</th>
      <th class="p-3 border">Insulglass Glasswool Acústico</th>
      <th class="p-3 border">Insulglass MBI Techos</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="p-3 border font-semibold">Recubrimiento</td><td class="p-3 border">Sin recubrimiento</td><td class="p-3 border">Polipropileno + kraft (barrera de vapor)</td></tr>
    <tr><td class="p-3 border font-semibold">Espesor</td><td class="p-3 border">2.5" (6.4 cm)</td><td class="p-3 border">3" (7.62 cm)</td></tr>
    <tr><td class="p-3 border font-semibold">Ancho × largo</td><td class="p-3 border">0.61 m × 15.24 m</td><td class="p-3 border">1.30 m × 30.48 m</td></tr>
    <tr><td class="p-3 border font-semibold">Rendimiento</td><td class="p-3 border">9.29 m² por rollo (paquete 2 rollos = 18.6 m²)</td><td class="p-3 border">39.63 m² por rollo</td></tr>
    <tr><td class="p-3 border font-semibold">Valor R</td><td class="p-3 border">R-8</td><td class="p-3 border">R-10</td></tr>
    <tr><td class="p-3 border font-semibold">NRC (acústico)</td><td class="p-3 border">0.90 · óptimo</td><td class="p-3 border">0.12 · térmico principalmente</td></tr>
    <tr><td class="p-3 border font-semibold">Densidad</td><td class="p-3 border">10.81 kg/m³</td><td class="p-3 border">~12 kg/m³</td></tr>
    <tr><td class="p-3 border font-semibold">Fuego</td><td class="p-3 border">ASTM E84 Clase A</td><td class="p-3 border">Euro Class A1 · No combustible</td></tr>
    <tr><td class="p-3 border font-semibold">Precio referencia</td><td class="p-3 border">$597 / rollo</td><td class="p-3 border">$4,332 / rollo</td></tr>
    <tr><td class="p-3 border font-semibold">Aplicación</td><td class="p-3 border">Muros con tablaroca, plafones interiores</td><td class="p-3 border">Techos y muros de naves industriales</td></tr>
  </tbody>
</table>
</div>

<h2>Cuándo usar Glasswool Acústico</h2>

<p>El glasswool sin recubrimiento es tu opción cuando necesitas:</p>

<ul>
  <li><strong>Aislamiento entre habitaciones.</strong> Muros divisorios de tablaroca en oficinas privadas, cines residenciales, estudios de podcast, salas de juntas. Con el glasswool metido entre bastidores y tablaroca en ambas caras alcanzas <strong>STC 45-50</strong>, suficiente para bloquear voces y música moderada.</li>
  <li><strong>Reducción de reverberación.</strong> Su NRC 0.90 (uno de los más altos del mercado) absorbe casi todo el sonido reflejado en frecuencias de voz humana (125 Hz a 1000 Hz).</li>
  <li><strong>Cámaras frigoríficas, hospitales, escuelas.</strong> Su composición no corrosiva y sin emisión de olores (ASTM C1304) cumple normativas de espacios sensibles.</li>
  <li><strong>Aislamiento térmico complementario en muros.</strong> R-8 es suficiente para climas templados de la CDMX, Puebla, Bajío.</li>
</ul>

<p><a href="/producto/aislamiento-acustico" class="text-amber-600 font-bold">Ver ficha completa del Glasswool Acústico →</a></p>

<h2>Cuándo usar MBI</h2>

<p>El MBI con barrera de vapor es la opción cuando necesitas:</p>

<ul>
  <li><strong>Aislar un techo industrial metálico.</strong> Naves, hangares, bodegas, centros de distribución. La barrera de vapor evita que la condensación que se genera entre el techo caliente y el interior climatizado moje la fibra de vidrio y reduzca su capacidad térmica en meses.</li>
  <li><strong>Ahorro energético agresivo en clima cálido.</strong> En Monterrey, Cancún, Mérida o Mexicali un techo sin aislar absorbe hasta 70% del calor ambiental. Con MBI R-10 puedes <strong>reducir hasta 30% el consumo de aire acondicionado</strong>. El ROI típico es 12-24 meses.</li>
  <li><strong>Control acústico de impactos.</strong> Aunque su NRC es bajo (0.12), reduce ruido de lluvia y granizo sobre techo metálico.</li>
  <li><strong>Aplicaciones donde se requiere clasificación A1 europea.</strong> Certificación Euro Class A1 (EN 13501-1:2007) para proyectos con estándares internacionales.</li>
</ul>

<p><a href="/producto/mbi-techos" class="text-amber-600 font-bold">Ver ficha completa del MBI →</a></p>

<h2>El error que vemos más seguido en obra</h2>

<p>Contratistas que necesitan aislar un techo metálico compran glasswool "porque es
más barato" ($597 vs $4,332). Sin barrera de vapor, la humedad de la climatización
interna condensa contra la lámina caliente, moja el glasswool, este pierde volumen y
capacidad térmica, y en 6-12 meses el aislante está saturado, chorreando agua sobre
el falso plafón y bajando el R-value real a menos de la mitad. Costoso reemplazar.</p>

<p>La cuenta correcta: para 100 m² de nave industrial necesitas ~3 rollos MBI = $12,996.
Con glasswool serían ~11 paquetes = $6,567. Ahorras $6,400 al comprar pero pagarás
$50,000+ en reposición + tiempo perdido en 12 meses. El MBI es el estándar por algo.</p>

<h2>¿Puedo usar los dos juntos?</h2>

<p>Sí, y de hecho es la configuración óptima para naves industriales premium:
MBI directo sobre la lámina metálica del techo (aislamiento térmico + barrera de vapor)
y Glasswool en muros divisorios interiores (aislamiento acústico entre oficinas
dentro de la nave). Ambos se compran en un solo pedido a Insulglass — te ahorras
gestión de dos proveedores.</p>

<h2>Guía rápida de selección</h2>

<ul>
  <li>¿Es muro interior con tablaroca? → <strong>Glasswool</strong></li>
  <li>¿Es techo de nave industrial? → <strong>MBI</strong></li>
  <li>¿Es techo de casa habitación climatizada? → <strong>MBI</strong></li>
  <li>¿Es plafón interior sobre suspensión? → <strong>Glasswool</strong></li>
  <li>¿Es aislamiento acústico entre departamentos? → <strong>Glasswool</strong></li>
  <li>¿Es cubierta metálica en zona cálida (Monterrey, Cancún, Mérida)? → <strong>MBI</strong></li>
</ul>
        """,
        "faqs": [
            {
                "q": "¿Puedo instalar MBI en un muro divisorio interior?",
                "a": "Técnicamente sí, pero es sobre-dimensionar: el MBI cuesta 7x más y su NRC (0.12) es mucho menor que el del glasswool (0.90) en frecuencias de voz. Para muros usa glasswool acústico."
            },
            {
                "q": "¿Cuánto ahorra el MBI en aire acondicionado?",
                "a": "En climas cálidos (Monterrey, Cancún, Mérida, Mexicali) reduce hasta 30% el consumo del A/C. En zonas templadas el ahorro es menor (10-20%). El ROI típico es 12-24 meses según tamaño de nave y horas de operación."
            },
            {
                "q": "¿El glasswool puede ir en techo si le agrego barrera de vapor por separado?",
                "a": "Sí es posible pero requiere instalación cuidadosa y encarece el proyecto. Es más eficiente comprar directamente el MBI que ya viene con la barrera de vapor laminada de fábrica y sellada correctamente."
            }
        ],
        "related_products": ["aislamiento-acustico", "mbi-techos"],
    },

    # ============================================================
    # 3. R-value
    # ============================================================
    {
        "slug": "valor-r-aislamiento-guia-mexico",
        "title": "Valor R en aislamiento: guía práctica para México",
        "seo_title": "Valor R aislamiento: qué es, cómo elegir y tabla por región | Arobe",
        "seo_description": (
            "Guía completa del Valor R (R-value) para aislamiento térmico en México. "
            "Qué significa R-8, R-10, R-13, R-19. Recomendaciones por zona climática, "
            "conversión a unidades métricas y equivalencia por espesor."
        ),
        "keywords": [
            "valor r aislamiento", "r-value méxico", "r-8 r-10 r-13 r-19",
            "aislante térmico méxico", "eficiencia energética aislante"
        ],
        "published": "2026-07-14",
        "updated": "2026-07-14",
        "category": "Guías técnicas",
        "cover_image": "mbi-techos-2.png",
        "excerpt": (
            "R-8, R-10, R-13, R-19. Los números que ves en cada aislante significan "
            "algo específico. Aquí te explicamos qué es el valor R, cómo compararlo "
            "y qué necesitas según tu región climática."
        ),
        "body_html": """
<p class="lead">El "Valor R" (o R-value) es la métrica que define qué tanto resiste
un material el paso del calor. A mayor R, mejor aislamiento. Es el único número que
puedes comparar directamente entre dos aislantes distintos — sin importar si son
fibra de vidrio, poliestireno o lana de roca — para saber cuál te da más protección
térmica por unidad de espesor.</p>

<h2>Qué significa el Valor R técnicamente</h2>

<p>El R-value mide la resistencia térmica en unidades imperiales:
<code>h·ft²·°F / BTU</code>. En sistema métrico es <code>m²·K / W</code>. Un R-10
significa que ese material resiste 10 unidades imperiales de flujo de calor. No es
una escala logarítmica: <strong>un R-20 aísla el doble que un R-10</strong>.</p>

<p>La fórmula básica: cuando tienes una diferencia de temperatura entre dos lados de
una pared aislada, el calor que pasa se calcula como (temperatura diferencial / R-value).
Por eso una nave industrial con R-10 en el techo pierde/gana la mitad del calor que
la misma nave con R-5.</p>

<h2>Los R-values típicos que verás en México</h2>

<div class="overflow-x-auto my-6">
<table class="w-full text-sm border-collapse">
  <thead class="bg-slate-100">
    <tr>
      <th class="p-3 text-left border">R-value</th>
      <th class="p-3 border">Métrico (m²·K/W)</th>
      <th class="p-3 border">Uso típico</th>
      <th class="p-3 border">Producto Insulglass</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="p-3 border font-semibold">R-8</td><td class="p-3 border">1.41</td><td class="p-3 border">Muros con tablaroca en zona templada</td><td class="p-3 border"><a href="/producto/aislamiento-acustico">Glasswool 2.5"</a></td></tr>
    <tr><td class="p-3 border font-semibold">R-10</td><td class="p-3 border">1.76</td><td class="p-3 border">Techos de nave industrial en clima cálido</td><td class="p-3 border"><a href="/producto/mbi-techos">MBI 3"</a></td></tr>
    <tr><td class="p-3 border font-semibold">R-13</td><td class="p-3 border">2.29</td><td class="p-3 border">Muros exteriores en clima frío / norte</td><td class="p-3 border">Glasswool 3.5" (bajo pedido)</td></tr>
    <tr><td class="p-3 border font-semibold">R-19</td><td class="p-3 border">3.35</td><td class="p-3 border">Techos residenciales premium, climas extremos</td><td class="p-3 border">Glasswool 6" (bajo pedido)</td></tr>
    <tr><td class="p-3 border font-semibold">R-30</td><td class="p-3 border">5.28</td><td class="p-3 border">Ático residencial en zonas de nieve (norte MX)</td><td class="p-3 border">Combinación de capas</td></tr>
  </tbody>
</table>
</div>

<h2>Recomendaciones por zona climática de México</h2>

<h3>Zona cálida seca — Sonora, Baja California, Coahuila desierto, Chihuahua</h3>
<p>Temperaturas de verano superan 40°C. El techo es tu punto crítico — es donde entra 60-70%
del calor. <strong>Mínimo R-13 en techo, R-8 en muros exteriores.</strong> El MBI R-10
es aceptable pero R-13 devuelve el diferencial de costo en 12-18 meses vía ahorro
de A/C.</p>

<h3>Zona cálida húmeda — Yucatán, Tabasco, Veracruz costa, Guerrero costa</h3>
<p>Además del calor tienes humedad extrema (>80% HR). Aquí la <strong>barrera de vapor</strong>
del MBI es OBLIGATORIA. Sin ella, la humedad condensa contra la lámina y arruina
cualquier aislante. Recomendación: MBI R-10 en techo, glasswool R-8 en muros.</p>

<h3>Zona templada — CDMX, Puebla, Bajío, Jalisco, Michoacán</h3>
<p>Diferenciales moderados. <strong>R-8 en muros y R-10 en techos es suficiente</strong>.
Aquí el aislamiento se usa más para confort acústico (glasswool R-8) que para ahorro
energético masivo.</p>

<h3>Zona fría — Zacatecas, Durango, San Luis Potosí altiplano, sierras</h3>
<p>Inviernos con temperaturas bajo cero por las noches. <strong>Mínimo R-13 en muros,
R-19 en techos</strong>. Los sistemas de calefacción son caros; el aislamiento paga
en 2-3 inviernos.</p>

<h2>Cómo se calcula el R-value real de un aislante</h2>

<p>El R-value depende de 3 cosas:</p>
<ol>
  <li><strong>Conductividad térmica del material</strong> (k). La fibra de vidrio tiene k ≈ 0.044 W/m·K.</li>
  <li><strong>Espesor</strong> del material. R = espesor / k. Por eso un aislante de 3" (7.62 cm) da más R que uno de 2.5" (6.35 cm) del mismo material.</li>
  <li><strong>Densidad</strong>. Aislantes más densos suelen tener mejor R por pulgada pero pesan más y cuestan más.</li>
</ol>

<p>La fibra de vidrio te da aproximadamente <strong>R-3.2 por pulgada</strong>. El
poliestireno extruido (XPS) da R-5 por pulgada — es 50% más eficiente por espesor
pero cuesta ~3x más. Para la mayoría de proyectos comerciales/industriales, la
fibra de vidrio es la ecuación costo/beneficio ganadora.</p>

<h2>Errores comunes con el Valor R</h2>

<ul>
  <li><strong>Comparar R sin considerar espesor.</strong> "R-13 vs R-10, obvio R-13" — sí, si tienes espacio para la diferencia de espesor. Si tu plenum es de 4 pulgadas, no cabe un R-19 (~6").</li>
  <li><strong>Ignorar la compresión.</strong> Un aislante R-13 comprimido a la mitad de su espesor pierde la mitad de su R-value. La instalación importa.</li>
  <li><strong>Confiar en R nominal sin comprobar la ficha.</strong> Fabricantes chinos low-cost declaran R-values inflados. Pide siempre la certificación ASTM C177 o C518.</li>
  <li><strong>Aislar solo el techo.</strong> Un edificio bien aislado en techo pero con muros pelones sigue perdiendo/ganando calor por los muros. La estrategia debe ser sistémica.</li>
</ul>
        """,
        "faqs": [
            {
                "q": "¿Qué R-value necesito para una casa habitación en Monterrey?",
                "a": "Zona cálida seca: mínimo R-13 en techo, R-8 en muros exteriores. Con esto reduces la carga del A/C de manera significativa. Para clientes que quieren ahorro máximo, R-19 en techo."
            },
            {
                "q": "¿El R-value cambia con el tiempo?",
                "a": "Sí, si el aislante se moja (por condensación, filtración o humedad) pierde R-value permanentemente en fibra de vidrio no protegida. Por eso el MBI con barrera de vapor es crítico en techos: el R-10 se mantiene por décadas."
            },
            {
                "q": "¿Puedo sumar dos capas para conseguir más R?",
                "a": "Sí, R-values son aditivos: dos capas de R-8 dan R-16. Se usa mucho en climas extremos donde ningún producto individual llega al R deseado."
            }
        ],
        "related_products": ["aislamiento-acustico", "mbi-techos"],
    },

    # ============================================================
    # 4. Instalación de plafones
    # ============================================================
    {
        "slug": "instalacion-plafones-suspan-suspension-reticular",
        "title": "Cómo instalar plafones SusPan sobre suspensión reticular",
        "seo_title": "Instalación de plafones SusPan · Guía paso a paso perfil T 15/16 | Arobe",
        "seo_description": (
            "Guía técnica de instalación de plafones acústicos SusPan Brahe, Kepler "
            "y Galilei sobre sistemas de suspensión reticular perfil T 15/16 pulgadas. "
            "Cálculo de cantidad, herramientas, pasos y errores a evitar."
        ),
        "keywords": [
            "instalar plafones", "suspensión 15/16", "cómo colocar plafón",
            "instalación suspan", "plafón acústico instalación", "perfil T reticular"
        ],
        "published": "2026-07-14",
        "updated": "2026-07-14",
        "category": "Instalación",
        "cover_image": "brahe-2402-2.jpg",
        "excerpt": (
            "Instalar plafones acústicos SusPan sobre suspensión reticular estándar "
            "no requiere herramienta especializada. Con planeación básica una cuadrilla "
            "de 2 personas cubre 100 m² en un día."
        ),
        "body_html": """
<p class="lead">La suspensión reticular (o "T-bar") es el sistema de instalación más
común para plafones acústicos en México. Los plafones SusPan (Brahe, Kepler, Galilei)
están diseñados para perfil T de 15/16 pulgadas — el estándar de la industria. Esta
guía cubre desde el trazo hasta el remate final.</p>

<h2>Herramientas y materiales que necesitas</h2>

<ul>
  <li>Perfilería T 15/16" — perfiles principales, secundarios (1.20 m y 0.60 m), y angulares de muro</li>
  <li>Tirantes/alambres de suspensión con clip</li>
  <li>Taladro con broca para concreto o clavos con explosivo (según techo estructural)</li>
  <li>Nivel láser (ideal) o manguera de nivel + hilo tirol</li>
  <li>Cinta métrica, lápiz, escuadra</li>
  <li>Segueta de dientes finos o navaja para cortar plafones en orillas</li>
  <li>Guantes (los plafones de lana mineral irritan piel y pulmones sin protección)</li>
  <li>Mascarilla N95 al cortar (el polvo de fibra mineral no debe inhalarse)</li>
</ul>

<h2>Paso 1: Marca el nivel del plafón</h2>

<p>Define a qué altura irá el plafón desde el piso. Estándar comercial: 2.70 m. Para
oficinas ejecutivas o áreas de recepción: 3.00-3.20 m. Marca ese nivel en las 4
paredes del cuarto usando nivel láser. Este trazo es CRÍTICO — un plafón desnivelado
se ve mal desde el primer día y es visible desde cualquier ángulo.</p>

<h2>Paso 2: Instala el angular de muro</h2>

<p>El angular perimetral es el perfil L que se atornilla directo a los muros
siguiendo el trazo de nivel. Se coloca con tornillo autotaladrante cada 60 cm
en tablaroca, cada 40 cm en block/concreto. Verifica que quede perfectamente al
nivel — este angular es la referencia visual de todo el plafón.</p>

<h2>Paso 3: Cuelga los perfiles principales</h2>

<p>Los perfiles principales (de 3.66 m normalmente) van paralelos, separados según
el módulo del plafón:</p>

<ul>
  <li>Para plafón Brahe 122×61: perfiles a <strong>1.22 m</strong> entre centros</li>
  <li>Para plafón Kepler o Galilei 61×61: perfiles a <strong>1.22 m</strong> entre centros (el módulo se cierra con secundarios de 60 cm)</li>
</ul>

<p>Los perfiles se cuelgan del techo estructural con tirantes (alambre galvanizado #12
o varilla) cada 1.20-1.50 m a lo largo del perfil. Ajusta la altura con el clip
de suspensión hasta que quede al mismo nivel que el angular perimetral.</p>

<h2>Paso 4: Coloca los perfiles secundarios</h2>

<p>Los secundarios (60 cm) se enganchan perpendicular a los principales, formando la
retícula final. Para plafón 61×61 necesitas secundarios cada 60 cm; para plafón
122×61 solo necesitas los secundarios en los extremos (cada 122 cm), lo que reduce
material y tiempo de instalación.</p>

<h2>Paso 5: Coloca los plafones</h2>

<p>Con la retícula completa y nivelada, empieza a colocar los plafones desde una
esquina, avanzando hacia el centro. Los plafones tegular (orilla de sombra) se
sostienen por gravedad — no requieren clip ni sujeción adicional. En orillas, corta
los plafones con navaja o segueta fina.</p>

<p><strong>Regla de oro:</strong> nunca fuerces un plafón. Si no baja fácil en su
espacio, verifica el módulo — probablemente los perfiles están mal separados.</p>

<h2>Cálculo de material para un proyecto</h2>

<p>Ejemplo: oficina de 8 × 12 m (96 m²) con plafón Kepler 0504.</p>

<ul>
  <li><strong>Plafones:</strong> 96 m² / 3.72 m² por paquete = 26 paquetes. +10% recortes = 29 paquetes → costo aproximado $27,550 público / $23,417 mayoreo distribuidor.</li>
  <li><strong>Perfil principal:</strong> 96 m² requieren aprox 80 metros lineales de perfil principal → 22 perfiles de 3.66 m.</li>
  <li><strong>Perfil secundario 60 cm:</strong> aproximadamente 240 secundarios para módulo 60×60.</li>
  <li><strong>Angular perimetral:</strong> perímetro = 40 metros → 14 perfiles de 3 m.</li>
  <li><strong>Tirantes:</strong> uno cada 1.20 m sobre principales → 55 tirantes.</li>
</ul>

<p>Tiempo estimado con cuadrilla de 2 personas: 8-10 horas (1 día).</p>

<h2>Errores comunes en instalación</h2>

<ol>
  <li><strong>No verificar el nivel del angular perimetral.</strong> 2 mm de error en cada esquina se acumula y termina con un plafón inclinado 1 cm en 8 metros — visible al ojo.</li>
  <li><strong>Ahorrar en tirantes.</strong> Los perfiles principales necesitan soporte cada 1.20-1.50 m. Menos tirantes = perfiles que se pandean con el tiempo y plafones que se caen.</li>
  <li><strong>Instalar sin mascarilla al cortar.</strong> La fibra mineral irrita las vías respiratorias. Usa N95 mínimo, y ventila el área.</li>
  <li><strong>Confundir módulo.</strong> Plafón 122×61 no cabe en retícula 60×60. Confirma módulo antes de instalar la retícula.</li>
  <li><strong>Pisar el plafón durante instalación.</strong> Un plafón acústico no aguanta peso. Si necesitas subirte para pasar cableado, usa una tabla temporal sobre los perfiles.</li>
</ol>

<h2>Cuánto tiempo dura una instalación bien hecha</h2>

<p>Con plafones Kepler o Galilei (garantía 10 años) y suspensión galvanizada de
calidad, una instalación bien hecha dura 15-20 años sin mantenimiento visible. Los
únicos cambios que verás son reposición ocasional de plafones dañados por filtraciones
de agua (cuestión de reemplazar 1-2 piezas, no re-instalar todo el sistema).</p>
        """,
        "faqs": [
            {
                "q": "¿Puedo instalar plafones SusPan sobre suspensión que ya existe?",
                "a": "Sí, si es perfil T 15/16 pulgadas (el estándar). Verifica el módulo — si es 60×60 puedes usar Kepler o Galilei; si es 60×120 usa Brahe."
            },
            {
                "q": "¿Cuánto tiempo tarda instalar 100 m² de plafón?",
                "a": "Con cuadrilla de 2 personas y retícula ya instalada: 4-6 horas. Si incluye armar la retícula completa: 8-10 horas (1 día laboral)."
            },
            {
                "q": "¿Puedo pasar cableado eléctrico o de datos sobre el plafón?",
                "a": "Sí, el espacio entre plafón y techo estructural (plenum) es exactamente para eso. Asegúrate que el cableado no descanse sobre los plafones — debe ir grapado al techo estructural o en charolas separadas."
            }
        ],
        "related_products": ["brahe-2402", "kepler-0504", "galilei-3004"],
    },

    # ============================================================
    # 5. Ahorro energético MBI
    # ============================================================
    {
        "slug": "ahorro-energetico-mbi-naves-industriales",
        "title": "Ahorro energético con MBI: caso nave industrial en México",
        "seo_title": "MBI aislante para nave industrial · Reduce 30% consumo A/C | Insulglass",
        "seo_description": (
            "Cómo el MBI Insulglass reduce hasta 30% el consumo de aire acondicionado "
            "en naves industriales de México. Cálculo de ROI, caso práctico con "
            "1,500 m² de techo metálico en Monterrey, y guía de instalación."
        ),
        "keywords": [
            "aislante para nave industrial", "reducir consumo aire acondicionado",
            "aislamiento techo metálico", "MBI ahorro energético", "eficiencia energética nave"
        ],
        "published": "2026-07-14",
        "updated": "2026-07-14",
        "category": "Casos prácticos",
        "cover_image": "mbi-techos-3.png",
        "excerpt": (
            "En una nave industrial de 1,500 m² en Monterrey, instalar MBI puede "
            "ahorrar $180-240k MXN al año en electricidad. ROI típico: 12-18 meses. "
            "Aquí el cálculo real."
        ),
        "body_html": """
<p class="lead">Las naves industriales en México con techo metálico sin aislar son
hornos en verano. En Monterrey, Cancún o Mérida, la temperatura interior de una nave
puede llegar a 45°C aunque afuera "solo" haga 38°C — el techo metálico absorbe y
retransmite hasta 70% del calor solar. El resultado: sistemas de aire acondicionado
funcionando al 100% durante 8-10 horas diarias, o peor, empleados trabajando en
condiciones que reducen productividad 20-30%.</p>

<p>Aislar el techo con MBI Insulglass no es un lujo — es una decisión de negocio
con ROI comprobable. Aquí te enseñamos a hacer el cálculo.</p>

<h2>Cómo funciona el MBI en techo industrial</h2>

<p>El MBI es un rollo de fibra de vidrio de 3 pulgadas de espesor (7.62 cm) con
barrera de vapor de polipropileno reforzado con kraft laminada de fábrica. Se
instala por la cara interior del techo — colgado de tirantes desde la estructura o
directamente entre polines — y actúa como escudo térmico.</p>

<p>Sus propiedades clave para naves:</p>

<ul>
  <li><strong>R-10 (1.76 m²·K/W).</strong> Reduce la transferencia de calor por conducción del techo al interior.</li>
  <li><strong>Barrera de vapor.</strong> Impide que la humedad del A/C interior condense sobre la lámina metálica caliente. Sin esta barrera cualquier aislante se moja y pierde 50% de su capacidad térmica en meses.</li>
  <li><strong>Euro Class A1 (no combustible).</strong> Cumple normativas para naves con químicos, alimentos, farmacéutica o combustibles.</li>
  <li><strong>1.30 × 30.48 m por rollo (39.63 m²).</strong> Cubre naves grandes con pocas piezas — menos juntas = menos puntos débiles térmicos.</li>
</ul>

<h2>Caso práctico: nave 1,500 m² en Monterrey</h2>

<p>Nave de manufactura ligera. Techo metálico de 1,500 m². Aire acondicionado
instalado: 50 toneladas de refrigeración (60 HP). Operación: 10 horas al día,
6 días a la semana, 8 meses de temporada caliente.</p>

<h3>Sin aislar</h3>
<ul>
  <li>Consumo eléctrico A/C: ~180 kWh/día × 26 días/mes = <strong>4,680 kWh/mes</strong></li>
  <li>Costo eléctrico industrial CFE tarifa GDMTH: ~$2.50 MXN/kWh + demanda</li>
  <li>Factura mensual A/C en temporada: <strong>~$14,000-16,000 MXN</strong></li>
  <li>Costo anual de A/C: <strong>~$120,000-130,000 MXN</strong></li>
</ul>

<h3>Con MBI R-10 en techo</h3>
<ul>
  <li>Reducción de carga térmica del techo: ~30-40%</li>
  <li>Reducción proyectada en consumo A/C: <strong>25-30%</strong> (el A/C trabaja menos)</li>
  <li>Ahorro anual estimado: <strong>$36,000-$42,000 MXN/año</strong></li>
</ul>

<h3>Inversión en material</h3>
<ul>
  <li>1,500 m² / 39.63 m² por rollo = <strong>38 rollos MBI</strong></li>
  <li>Costo público: 38 × $4,332 = <strong>$164,616 MXN</strong></li>
  <li>Costo mayoreo distribuidor (-15%): <strong>~$139,924 MXN</strong></li>
  <li>Instalación cuadrilla (2 semanas): <strong>~$40,000-60,000 MXN</strong></li>
</ul>

<h3>ROI</h3>
<ul>
  <li>Inversión total: <strong>~$180,000-200,000 MXN</strong></li>
  <li>Ahorro anual: <strong>~$40,000 MXN</strong></li>
  <li><strong>Payback: 4.5-5 años</strong> considerando solo ahorro directo de A/C</li>
</ul>

<p>Ese payback baja significativamente si consideras:</p>
<ul>
  <li>Aumento de productividad (empleados no trabajan a 40°C interior)</li>
  <li>Menor deterioro de mercancía sensible a calor</li>
  <li>Menor mantenimiento del A/C (ciclos más cortos = menor desgaste)</li>
  <li>Depreciación fiscal del activo</li>
</ul>

<p>En naves con procesos sensibles a temperatura (farmacéutica, alimentos, electrónica),
el ROI puede caer a <strong>18-24 meses</strong>.</p>

<h2>Cuándo NO conviene MBI (honesto)</h2>

<p>El MBI no es para todos:</p>

<ul>
  <li><strong>Nave sin aire acondicionado.</strong> Si tu nave no tiene A/C, el ahorro es solo confort térmico — no hay factura eléctrica que reducir. El MBI sigue mejorando ambiente pero el ROI se calcula distinto.</li>
  <li><strong>Nave de menos de 500 m².</strong> El costo fijo de instalación (rentar andamios, cuadrilla, transporte) hace que naves chicas tengan payback más largo. Piensa 3+ años.</li>
  <li><strong>Nave en zona fría (Chihuahua, Zacatecas).</strong> Aquí el problema es calor que se escapa, no que entra. Igual el aislante ayuda, pero el cálculo cambia y a veces requiere R-13 o R-19.</li>
  <li><strong>Nave con techo de mala calidad.</strong> Si el techo mismo tiene filtraciones, poner aislante encima no las soluciona — se moja el aislante y se pierde efectividad. Repara el techo primero.</li>
</ul>

<h2>Consideraciones prácticas de instalación</h2>

<p>Para 1,500 m² de nave, planea:</p>
<ul>
  <li><strong>Tiempo:</strong> 2 semanas con cuadrilla de 4 personas</li>
  <li><strong>Andamio:</strong> renta $8,000-15,000 MXN/semana según altura</li>
  <li><strong>Equipo de protección:</strong> mascarillas N95, guantes, lentes, arnés si altura > 3.5 m</li>
  <li><strong>Sin interrupción operacional:</strong> el MBI se puede instalar en horario nocturno o fines de semana. La operación de la nave no requiere pararse.</li>
</ul>

<h2>Preguntas frecuentes que hacen los dueños</h2>

<p><strong>"¿Vale la pena aislar si mi nave ya tiene 10 años de operar sin aislante?"</strong>
Sí. El aislante trabaja igual desde el primer día que se instala. El costo de la
electricidad no baja porque tu nave sea vieja o nueva.</p>

<p><strong>"¿Necesito permiso o certificación para instalar?"</strong>
En la mayoría de estados, aislar un techo interior no requiere permiso municipal
adicional (no modifica estructura). Verifica con el ayuntamiento local. Sí requieres
certificación para bonos verdes o LEED — pídenos los certificados ASTM del MBI.</p>

<p><strong>"¿Puedo hacerlo por fases (aislar la mitad este año, la otra el siguiente)?"</strong>
Sí. Empieza por la zona con más carga térmica (área sur/oeste del techo, donde
pega más sol). El ahorro es proporcional al área aislada.</p>
        """,
        "faqs": [
            {
                "q": "¿Cuánto se ahorra realmente en aire acondicionado con MBI?",
                "a": "En climas cálidos (Monterrey, Cancún, Mérida) la reducción típica es 25-30% del consumo del A/C. En zonas templadas (Bajío, CDMX) el ahorro es 10-20%. Depende también de horas de operación y aislamiento actual."
            },
            {
                "q": "¿Cuánto tiempo tarda instalar MBI en 1,000 m²?",
                "a": "Cuadrilla de 4 personas puede instalar 1,000 m² en 5-7 días laborales. Se puede acelerar con más cuadrilla, pero por seguridad y calidad no conviene más de 6 personas trabajando en un mismo techo."
            },
            {
                "q": "¿El MBI aguanta que le camine gente encima durante mantenimiento?",
                "a": "No directamente. Igual que cualquier aislante, no está diseñado como piso. Para mantenimiento del techo, camina sobre las estructuras metálicas (polines) y usa tabla apoyada en polines para distribuir peso."
            }
        ],
        "related_products": ["mbi-techos"],
    },
]


def all_posts():
    """Devuelve todos los posts ordenados por fecha descendente."""
    return sorted(POSTS, key=lambda p: p["published"], reverse=True)


def get(slug):
    for p in POSTS:
        if p["slug"] == slug:
            return p
    return None


def by_category(cat):
    return [p for p in POSTS if p.get("category") == cat]


def categories():
    """Categorías únicas."""
    seen = []
    for p in POSTS:
        c = p.get("category")
        if c and c not in seen:
            seen.append(c)
    return seen
