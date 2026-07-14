"""
Arobe Group — Sitio web e-commerce
Distribuidor de materiales de construcción ligera
Marcas: Suspan (paneles) · Insulglass (aislamiento)
"""
import os
import logging

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from models import db


# Logs por defecto a INFO (Render los muestra en su consola)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)


def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )
    # ProxyFix: Render sirve detrás de proxy SSL, respeta X-Forwarded-Proto
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_for=1)

    # ---- Config ----
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me-in-prod")
    app.config["COMPANY_NAME"] = "Arobe Group"
    app.config["COMPANY_DOMAIN"] = "arobegroup.com"
    app.config["WA_PHONE"] = os.environ.get("WA_PHONE", "525500000000")
    app.config["EMAIL_VENTAS"] = os.environ.get("EMAIL_VENTAS", "ventas@arobegroup.com")
    # Google Analytics 4 — si está set, se inyecta el snippet en todas las páginas
    app.config["GA4_ID"] = os.environ.get("GA4_ID", "").strip()

    # ---- Database ----
    db_url = os.environ.get("DATABASE_URL", "").strip()
    if db_url:
        # Render entrega postgres:// pero SQLAlchemy 2.x exige postgresql://
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    else:
        # Fallback local: SQLite (para dev / si Postgres no está configurado)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///arobegroup.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    db.init_app(app)

    with app.app_context():
        # Crea tablas si no existen (para producción ligera; cuando crezca usamos Alembic)
        try:
            db.create_all()
        except Exception as e:
            logging.error("Error creando tablas: %s", e)

    # ---- Routes ----
    from routes.web import web_bp
    from routes.cart import cart_bp, cart_summary
    from routes.checkout import checkout_bp
    from routes.seo import seo_bp
    from routes.admin import admin_bp
    app.register_blueprint(web_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(seo_bp)
    app.register_blueprint(admin_bp)

    # ---- Globals expuestos a Jinja ----
    @app.context_processor
    def inject_cart_count():
        try:
            return {"cart_count": cart_summary()}
        except Exception:
            return {"cart_count": 0}

    # ---- Healthcheck (para Render) ----
    @app.get("/healthz")
    def healthz():
        return {"ok": True}, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
