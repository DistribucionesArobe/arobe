"""
Landing SEO por ciudad · Fase 12.

URLs:
  /plafones-acusticos-<slug>   — landing SEO productos SusPan por ciudad
  /aislamiento-<slug>          — landing SEO productos Insulglass por ciudad
  /zonas-cobertura              — página general de cobertura preferente
"""
from flask import Blueprint, render_template, abort

from data import cities as cities_data
from data import products as catalog

cities_bp = Blueprint("cities", __name__)


@cities_bp.get("/zonas-cobertura")
def coverage():
    return render_template(
        "coverage.html",
        page="cobertura",
        cities=cities_data.all_cities(),
        radio_km=cities_data.RADIO_PREFERENTE_KM,
    )


@cities_bp.get("/plafones-acusticos-<slug>")
def plafones_ciudad(slug):
    city = cities_data.get(slug)
    if city is None:
        abort(404)
    productos = [p for p in catalog.by_marca("suspan") if p.get("linea") == "ceilings"]
    return render_template(
        "city_landing.html",
        page=f"ciudad-plafones-{slug}",
        city=city,
        variant="plafones",
        variant_title=f"Plafones acústicos en {city['nombre']}",
        variant_keyword="plafones acústicos",
        variant_marca="SusPan",
        productos=productos,
    )


@cities_bp.get("/aislamiento-<slug>")
def aislamiento_ciudad(slug):
    city = cities_data.get(slug)
    if city is None:
        abort(404)
    productos = catalog.by_marca("insulglass")
    return render_template(
        "city_landing.html",
        page=f"ciudad-aislamiento-{slug}",
        city=city,
        variant="aislamiento",
        variant_title=f"Aislamiento térmico y acústico en {city['nombre']}",
        variant_keyword="aislamiento térmico y acústico",
        variant_marca="Insulglass",
        productos=productos,
    )
