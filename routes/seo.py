"""
SEO endpoints — Fase 6.
  - /robots.txt
  - /sitemap.xml  (dinámico desde el catálogo)
"""
from flask import Blueprint, Response, url_for, request, current_app
from datetime import datetime, timezone

from data import products as catalog

seo_bp = Blueprint("seo", __name__)


def _abs_url(path):
    """Construye URL absoluta con el host actual (con https forzado)."""
    base = request.host_url.rstrip("/")
    if base.startswith("http://"):
        base = base.replace("http://", "https://", 1)
    return f"{base}{path}"


@seo_bp.get("/robots.txt")
def robots_txt():
    sitemap_url = _abs_url("/sitemap.xml")
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /carrito\n"
        "Disallow: /carrito/\n"
        "Disallow: /checkout\n"
        "Disallow: /checkout/\n"
        "Disallow: /api/\n"
        "Disallow: /debug/\n"
        "Disallow: /healthz\n"
        "\n"
        f"Sitemap: {sitemap_url}\n"
    )
    return Response(body, mimetype="text/plain")


@seo_bp.get("/sitemap.xml")
def sitemap_xml():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # URLs estáticas — (path, priority, changefreq)
    static_urls = [
        ("/",                              "1.0", "weekly"),
        ("/catalogo",                      "0.9", "weekly"),
        ("/nosotros",                      "0.7", "monthly"),
        ("/marcas/suspan",                 "0.8", "weekly"),
        ("/marcas/suspan/board",           "0.6", "monthly"),
        ("/marcas/suspan/ceilings",        "0.6", "monthly"),
        ("/marcas/suspan/decor",           "0.6", "monthly"),
        ("/marcas/insulglass",             "0.8", "weekly"),
        ("/marcas/insulglass/glasswool",   "0.6", "monthly"),
        ("/marcas/insulglass/mbi",         "0.6", "monthly"),
        ("/distribuidores",                "0.8", "weekly"),
        ("/contacto",                      "0.5", "monthly"),
    ]

    rows = []
    for path, prio, freq in static_urls:
        rows.append(
            "  <url>\n"
            f"    <loc>{_abs_url(path)}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{prio}</priority>\n"
            "  </url>"
        )

    # URLs dinámicas de productos
    for p in catalog.all_products():
        rows.append(
            "  <url>\n"
            f"    <loc>{_abs_url('/producto/' + p['slug'])}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n"
            "    <priority>0.8</priority>\n"
            "  </url>"
        )

    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    return Response(body, mimetype="application/xml")
