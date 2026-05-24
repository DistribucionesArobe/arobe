# arobegroup.com

Sitio web e-commerce de **Arobe Group** — Distribuidor mexicano de materiales para construcción ligera.

Casa de las marcas:

- **SusPan®** — Suspended Panels
  - SusPan Board (láminas y tableros)
  - SusPan Ceilings (plafones)
  - SusPan Decor (decorativos de muro: lambrín, mármol PVC)
- **Insulglass®** — Premium Insulation
  - Glasswool (aislante en rollos para tablaroca)
  - MBI Manta (industrial y residencial)

## Stack

- **Backend:** Python 3.11 + Flask 3
- **Templates:** Jinja2 (server-rendered, SEO-friendly)
- **Estilos:** Tailwind CSS (vía CDN en Fase 1, compilado en Fase 6)
- **Deploy:** Render.com (web service)
- **Datos:** En Fase 1 sin DB. En Fase 2 agregamos PostgreSQL.

## Estructura

```
arobegroup-web/
├── app.py                  # Flask entry
├── routes/
│   └── web.py              # Rutas públicas
├── templates/
│   ├── base.html           # Layout (header, footer, mega-menús de marca)
│   ├── index.html          # Home
│   └── coming_soon.html    # Placeholder para secciones en construcción
├── static/
│   ├── css/                # Hojas de estilo (Fase 6)
│   ├── js/
│   └── img/
│       ├── favicon.svg
│       └── logos/          # Aquí van los PNG de SusPan, Insulglass, etc.
├── data/                   # Datos del catálogo (Fase 1.2)
├── requirements.txt
├── render.yaml             # Config Render
├── Procfile                # Alternativa a render.yaml
└── .gitignore
```

## Correr localmente

```bash
# 1. Clonar el repo
git clone https://github.com/DistribucionesArobe/arobe.git
cd arobe

# 2. Crear entorno virtual y dependencias
python3 -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Correr
python app.py
# Abrir http://localhost:5000
```

## Deploy a Render

Primera vez:

1. Entra a [render.com](https://render.com) → **New** → **Web Service**.
2. Conecta el repo `DistribucionesArobe/arobe`.
3. Render detecta `render.yaml` automáticamente y configura todo.
4. Click **Apply**. El primer deploy tarda 2-3 minutos.
5. Tu sitio queda en `https://arobegroup-web.onrender.com`.

Cada `git push` a `main` después de eso re-despliega automáticamente.

### Apuntar el dominio arobegroup.com

1. En Render → tu servicio → **Settings** → **Custom Domains** → agrega `arobegroup.com` y `www.arobegroup.com`.
2. Render te da un CNAME (algo como `arobegroup-web.onrender.com`).
3. En tu proveedor de dominio (GoDaddy/Namecheap):
   - Tipo A `@` → IP que te da Render (para el apex)
   - Tipo CNAME `www` → `arobegroup-web.onrender.com`
4. Render genera el certificado SSL automáticamente en ~10 min.

## Variables de entorno (Render → Environment)

| Variable | Valor | Notas |
|---|---|---|
| `SECRET_KEY` | (generada por Render) | Para sesiones Flask |
| `WA_PHONE` | `525500000000` | Tu WhatsApp en formato internacional sin `+` |
| `EMAIL_VENTAS` | `ventas@arobegroup.com` | Email público |

## Roadmap por fases

| Fase | Estado | Qué incluye |
|---|---|---|
| 1.1 | ✅ Listo | Bootstrap Flask, home, mega-menús de marca, footer |
| 1.2 | ⏳ | Catálogo: `data/products.py` con SKUs reales, página `/catalogo` |
| 1.3 | ⏳ | Ficha de producto `/producto/<sku>` con galería + precios |
| 1.4 | ⏳ | Páginas de marca con sub-líneas filtradas |
| 1.5 | ⏳ | Formularios: distribuidor B2B, contacto (envío a email) |
| 2   | ⏳ | Carrito persistente (Postgres) |
| 3   | ⏳ | Checkout con MercadoPago Checkout Pro |
| 4   | ⏳ | Órdenes y cuenta de cliente |
| 5   | ⏳ | Facturación CFDI 4.0 con Facturama |
| 6   | ⏳ | SEO, sitemap, Tailwind compilado, analytics |

## Marcas

SusPan® e Insulglass® son marcas registradas de Arobe Group.

© 2026 Distribuciones Arobe.
