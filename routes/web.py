"""
Rutas públicas del sitio web (frontend).
Paso 1.1 — solo home + placeholders. En 1.2 agregamos catálogo real.
"""
from flask import Blueprint, render_template, request, abort

web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def index():
    return render_template("index.html", page="home")


# --- Catálogo (placeholder hasta Paso 1.2) ---
@web_bp.get("/catalogo")
def catalogo():
    return render_template("coming_soon.html", titulo="Catálogo completo", paso="1.2")


# --- Marcas: SusPan con sub-líneas ---
SUSPAN_SUBS = {
    "board":    {"nombre": "SusPan Board",    "desc": "Láminas y tableros · Lámina PVC, paneles rígidos"},
    "ceilings": {"nombre": "SusPan Ceilings", "desc": "Plafones · Reticulado, mineral, acústico"},
    "decor":    {"nombre": "SusPan Decor",    "desc": "Decorativos de muro · Lambrín, mármol PVC, paneles 3D"},
}

@web_bp.get("/marcas/suspan")
@web_bp.get("/marcas/suspan/<sub>")
def marca_suspan(sub=None):
    if sub is None:
        return render_template("coming_soon.html", titulo="SusPan · Suspended Panels", paso="1.4")
    if sub not in SUSPAN_SUBS:
        abort(404)
    info = SUSPAN_SUBS[sub]
    return render_template("coming_soon.html", titulo=info["nombre"], subtitulo=info["desc"], paso="1.4")


# --- Marcas: Insulglass con líneas ---
INSUL_SUBS = {
    "glasswool": {"nombre": "Insulglass Glasswool", "desc": "Aislante en rollos para tablaroca · R-11, R-19"},
    "mbi":       {"nombre": "Insulglass MBI",       "desc": "Manta industrial y residencial"},
}

@web_bp.get("/marcas/insulglass")
@web_bp.get("/marcas/insulglass/<sub>")
def marca_insulglass(sub=None):
    if sub is None:
        return render_template("coming_soon.html", titulo="Insulglass · Premium Insulation", paso="1.4")
    if sub not in INSUL_SUBS:
        abort(404)
    info = INSUL_SUBS[sub]
    return render_template("coming_soon.html", titulo=info["nombre"], subtitulo=info["desc"], paso="1.4")


# --- Distribuidores B2B ---
@web_bp.get("/distribuidores")
def distribuidores():
    return render_template("coming_soon.html", titulo="Programa B2B para distribuidores", paso="1.5")


# --- Contacto ---
@web_bp.get("/contacto")
def contacto():
    return render_template("coming_soon.html", titulo="Contacto", paso="1.5")


# --- 404 amable ---
@web_bp.app_errorhandler(404)
def not_found(e):
    return render_template("coming_soon.html", titulo="Página no encontrada", subtitulo="Revisa la URL o vuelve al inicio.", paso=None), 404
