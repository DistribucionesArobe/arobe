"""
Arobe Group — Sitio web e-commerce
Distribuidor de materiales de construcción ligera
Marcas: Suspan (paneles) · Insulglass (aislamiento)
"""
import os
from flask import Flask, render_template

def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )

    # ---- Config ----
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me-in-prod")
    app.config["COMPANY_NAME"] = "Arobe Group"
    app.config["COMPANY_DOMAIN"] = "arobegroup.com"
    app.config["WA_PHONE"] = os.environ.get("WA_PHONE", "525500000000")
    app.config["EMAIL_VENTAS"] = os.environ.get("EMAIL_VENTAS", "ventas@arobegroup.com")

    # ---- Routes ----
    from routes.web import web_bp
    app.register_blueprint(web_bp)

    # ---- Healthcheck (para Render) ----
    @app.get("/healthz")
    def healthz():
        return {"ok": True}, 200

    return app


app = create_app()

if __name__ == "__main__":
    # Solo para desarrollo local: `python app.py`
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
