"""
Rutas públicas del sitio web (frontend).
Paso 1.2 — catálogo real con SKUs migrados desde insulglass.mx.
"""
import logging
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash

from data import products as catalog
from data import blog as blog_data
from models import db, DistributorLead
from lib.emailer import send_distributor_confirmation, send_distributor_admin

log = logging.getLogger("web")

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
    return render_template("distributors.html", page="distribuidores")


@web_bp.post("/distribuidores/aplicar")
def distribuidores_aplicar():
    # Datos del formulario
    razon = request.form.get("razon_social", "").strip()
    nombre_comercial = request.form.get("nombre_comercial", "").strip()
    rfc = request.form.get("rfc", "").strip().upper()
    giro = request.form.get("giro", "").strip()
    contacto = request.form.get("contacto_nombre", "").strip()
    puesto = request.form.get("contacto_puesto", "").strip()
    email = request.form.get("email", "").strip()
    telefono = request.form.get("telefono", "").strip()
    ciudad = request.form.get("ciudad", "").strip()
    estado = request.form.get("estado", "").strip()
    volumen = request.form.get("volumen_mensual", "").strip()
    marcas = request.form.getlist("marcas")
    productos = request.form.get("productos_interes", "").strip()
    origen = request.form.get("origen", "").strip()
    notas = request.form.get("notas", "").strip()

    # Anti-spam simple: honeypot
    if request.form.get("website"):
        return redirect(url_for("web.distribuidores"))

    # Validación mínima
    if not (razon and contacto and email and telefono):
        flash("Faltan datos obligatorios (razón social, contacto, email y teléfono)", "error")
        return redirect(url_for("web.distribuidores"))

    lead = DistributorLead(
        razon_social=razon,
        nombre_comercial=nombre_comercial or None,
        rfc=rfc or None,
        giro=giro or None,
        contacto_nombre=contacto,
        contacto_puesto=puesto or None,
        email=email,
        telefono=telefono,
        ciudad=ciudad or None,
        estado=estado or None,
        volumen_mensual_mxn=volumen or None,
        marcas_interes=",".join(marcas) if marcas else None,
        productos_interes=productos or None,
        origen=origen or None,
        notas=notas or None,
        ip=request.headers.get("X-Forwarded-For", request.remote_addr or "")[:60],
        user_agent=(request.headers.get("User-Agent") or "")[:500],
    )
    db.session.add(lead)
    db.session.commit()
    log.info("Nuevo distribuidor: %s (%s) %s", razon, email, lead.id)

    # Emails
    try:
        ok, _ = send_distributor_confirmation(lead)
        if ok:
            lead.email_customer_sent = True
        ok, _ = send_distributor_admin(lead)
        if ok:
            lead.email_admin_sent = True
        db.session.commit()
    except Exception as e:
        log.warning("Error enviando emails de distribuidor: %s", e)

    return render_template("distributors_thanks.html", page="distribuidores-gracias", lead=lead)


# ============================================================
# Blog SEO
# ============================================================
@web_bp.get("/blog")
def blog_list():
    return render_template(
        "blog_list.html",
        page="blog",
        posts=blog_data.all_posts(),
        categories=blog_data.categories(),
    )


@web_bp.get("/blog/<slug>")
def blog_post(slug):
    post = blog_data.get(slug)
    if post is None:
        abort(404)
    # Productos relacionados hidratados
    related = [catalog.get(s) for s in (post.get("related_products") or [])]
    related = [p for p in related if p]
    return render_template(
        "blog_post.html",
        page="blog-post",
        post=post,
        related=related,
        other_posts=[p for p in blog_data.all_posts() if p["slug"] != slug][:3],
    )


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
