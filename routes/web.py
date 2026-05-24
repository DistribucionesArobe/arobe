"""
Rutas públicas del sitio web (frontend).
Paso 1.2 — catálogo real con SKUs migrados desde insulglass.mx.
"""
from flask import Blueprint, render_template, abort

from data import products as catalog

web_bp = Blueprint("web", __name__)


# ============================================================
# Home
# ============================================================
@web_bp.get("/")
def index():
    return render_template(
        "index.html",
        page="home",
        destacados=catalog.featured_products(),
    )


# ============================================================
# Catálogo completo y ficha de producto
# ============================================================
@web_bp.get("/catalogo")
def catalogo():
    return render_template(
        "catalog.html",
        page="catalogo",
        productos=catalog.all_products(),
        titulo="Catálogo completo",
        subtitulo="Plafones SusPan y aislantes Insulglass · stock disponible",
        marca_filtro=None,
    )


@web_bp.get("/producto/<slug>")
def producto(slug):
    p = catalog.get(slug)
    if p is None:
        abort(404)
    return render_template(
        "product.html",
        page="producto",
        producto=p,
    )


# ============================================================
# Marcas: SusPan con sub-líneas
# ============================================================
SUSPAN_SUBS = {
    "board":    {"nombre": "SusPan Board",    "desc": "Láminas y tableros · Lámina PVC, paneles rígidos"},
    "ceilings": {"nombre": "SusPan Ceilings", "desc": "Plafones · Reticulado, mineral, acústico"},
    "decor":    {"nombre": "SusPan Decor",    "desc": "Decorativos de muro · Lambrín, mármol PVC, paneles 3D"},
}


@web_bp.get("/marcas/suspan", defaults={"sub": None})
@web_bp.get("/marcas/suspan/<sub>")
def marca_suspan(sub):
    if sub is None:
        productos = catalog.by_marca("suspan")
        return render_template(
            "catalog.html",
            page="marca-suspan",
            productos=productos,
            titulo="SusPan · Suspended Panels",
            subtitulo="Plafones, lambrín y decorativos de muro",
            marca_filtro="suspan",
        )
    if sub not in SUSPAN_SUBS:
        abort(404)
    productos = catalog.by_marca_y_linea("suspan", sub)
    info = SUSPAN_SUBS[sub]
    if not productos:
        return render_template(
            "coming_soon.html",
            titulo=info["nombre"],
            subtitulo=info["desc"] + " · próximamente en línea",
            paso="1.3",
        )
    return render_template(
        "catalog.html",
        page=f"suspan-{sub}",
        productos=productos,
        titulo=info["nombre"],
        subtitulo=info["desc"],
        marca_filtro="suspan",
    )


# ============================================================
# Marcas: Insulglass con sub-líneas
# ============================================================
INSUL_SUBS = {
    "glasswool": {"nombre": "Insulglass Glasswool", "desc": "Aislante en rollos · térmico y acústico"},
    "mbi":       {"nombre": "Insulglass MBI",       "desc": "Manta industrial y residencial para cubierta"},
}


@web_bp.get("/marcas/insulglass", defaults={"sub": None})
@web_bp.get("/marcas/insulglass/<sub>")
def marca_insulglass(sub):
    if sub is None:
        productos = catalog.by_marca("insulglass")
        return render_template(
            "catalog.html",
            page="marca-insulglass",
            productos=productos,
            titulo="Insulglass · Premium Insulation",
            subtitulo="Aislamiento térmico y acústico de fibra de vidrio",
            marca_filtro="insulglass",
        )
    if sub not in INSUL_SUBS:
        abort(404)
    productos = catalog.by_marca_y_linea("insulglass", sub)
    info = INSUL_SUBS[sub]
    if not productos:
        return render_template(
            "coming_soon.html",
            titulo=info["nombre"],
            subtitulo=info["desc"] + " · próximamente en línea",
            paso="1.3",
        )
    return render_template(
        "catalog.html",
        page=f"insulglass-{sub}",
        productos=productos,
        titulo=info["nombre"],
        subtitulo=info["desc"],
        marca_filtro="insulglass",
    )


# ============================================================
# Páginas institucionales
# ============================================================
@web_bp.get("/nosotros")
def nosotros():
    return render_template("about.html", page="nosotros")


@web_bp.get("/distribuidores")
def distribuidores():
    return render_template("coming_soon.html", titulo="Programa B2B para distribuidores", paso="1.5")


@web_bp.get("/contacto")
def contacto():
    return render_template("coming_soon.html", titulo="Contacto", paso="1.5")


# ============================================================
# 404 amable
# ============================================================
@web_bp.app_errorhandler(404)
def not_found(e):
    return render_template(
        "coming_soon.html",
        titulo="Página no encontrada",
        subtitulo="Revisa la URL o vuelve al inicio.",
        paso=None,
    ), 404
