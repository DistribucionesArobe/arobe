"""
Arobe Labs — English portfolio section for AI/LLM partner-program credentials.
Served from arobe.mx/labs so the main domain shows credible AI work when
Z.ai / Anthropic / OpenAI partnership evaluators visit.
"""
import logging
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from data import labs_projects as labs

labs_bp = Blueprint("labs", __name__)
log = logging.getLogger("labs")


@labs_bp.get("/labs")
def index():
    return render_template(
        "labs/index.html",
        page="labs",
        projects=labs.PROJECTS,
        capabilities=labs.CAPABILITIES,
        stack=labs.STACK_SUMMARY,
        partners=labs.PARTNER_PROGRAMS,
    )


@labs_bp.get("/labs/<slug>")
def project(slug):
    proj = next((p for p in labs.PROJECTS if p["slug"] == slug), None)
    if proj is None:
        abort(404)
    return render_template(
        "labs/project.html",
        page=f"labs-{slug}",
        p=proj,
    )


@labs_bp.get("/labs/partners")
def partners():
    return render_template(
        "labs/partners.html",
        page="labs-partners",
        partners=labs.PARTNER_PROGRAMS,
        stack=labs.STACK_SUMMARY,
    )


@labs_bp.post("/labs/contact")
def contact():
    form = request.form
    name    = (form.get("name") or "").strip()
    org     = (form.get("org") or "").strip()
    email   = (form.get("email") or "").strip()
    inquiry = (form.get("inquiry_type") or "").strip()
    message = (form.get("message") or "").strip()

    if not (name and email):
        flash("Please complete name and email.", "error")
        return redirect(url_for("labs.index") + "#contact")

    html = f"""
    <h2>New Arobe Labs inquiry</h2>
    <p><b>Submitted:</b> {datetime.utcnow().isoformat()} UTC</p>
    <ul>
      <li><b>Name:</b> {name}</li>
      <li><b>Organization:</b> {org}</li>
      <li><b>Email:</b> {email}</li>
      <li><b>Inquiry type:</b> {inquiry}</li>
      <li><b>Message:</b><br>{message}</li>
    </ul>
    """
    try:
        from lib.emailer import send_email, _admin_email
        send_email(
            to=_admin_email(),
            subject=f"[Arobe Labs] {inquiry or 'Inquiry'} — {name} ({org or 'no org'})",
            html=html,
            reply_to=email,
        )
    except Exception as e:
        log.exception("Error sending Labs inquiry: %s", e)

    return render_template("labs/contact_thanks.html", page="labs-thanks", name=name)
