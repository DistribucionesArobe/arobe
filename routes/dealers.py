"""
US Dealer Program routes — Fase 15.

All pages in English, served from arobe.mx under /dealer-program and friends.
The site operates as Distribuciones Arobe S.A.S. de C.V. (Mexican SA) with
FOB delivery at Reynosa / Matamoros / Nuevo Laredo. No US entity required.
"""
import logging
from datetime import datetime

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, abort,
    Response, current_app,
)

from data import us_markets

dealers_bp = Blueprint("dealers", __name__)
log = logging.getLogger("dealers")


# ---- 1) Dealer Program (main landing) ----
@dealers_bp.get("/dealer-program")
def program():
    return render_template(
        "dealers/dealer_program.html",
        page="dealer-program",
        metros=us_markets.tier1_metros(),
        terms=us_markets.TERMS,
    )


# ---- 2) Wholesale Truckload (SEO landing) ----
@dealers_bp.get("/wholesale-truckload")
def wholesale():
    return render_template(
        "dealers/wholesale_truckload.html",
        page="wholesale-truckload",
        terms=us_markets.TERMS,
    )


# ---- 3) Private Label (SEO landing) ----
@dealers_bp.get("/private-label")
def private_label():
    return render_template(
        "dealers/private_label.html",
        page="private-label",
        terms=us_markets.TERMS,
    )


# ---- 4) US Territories map ----
@dealers_bp.get("/us-territories")
def territories():
    return render_template(
        "dealers/us_territories.html",
        page="us-territories",
        metros=us_markets.all_metros(),
        terms=us_markets.TERMS,
    )


# ---- 5) Dealer login (placeholder for future portal) ----
@dealers_bp.get("/dealer-login")
def login():
    return render_template(
        "dealers/dealer_login.html",
        page="dealer-login",
    )


# ---- 6) Printable spec sheets (US units) ----
SPEC_SHEETS = {
    "suspan-board-us": {
        "title": "SusPan Board — Technical Spec Sheet (US)",
        "product": "SusPan PVC Panel / Board",
        "brand": "SusPan",
        "intro": "Lightweight PVC panels & boards for interior walls, soffits and ceilings. Moisture-proof, flame-retardant, dimensionally stable.",
        "rows": [
            ("Material",                    "Rigid foamed PVC"),
            ("Standard thickness",          "1/4 in · 3/8 in · 1/2 in · 3/4 in"),
            ("Standard width",              "48 in"),
            ("Standard length",             "96 in · 120 in"),
            ("Density",                     "35–55 lb/ft³"),
            ("Weight (1/2 in panel)",       "~1.9 lb/ft²"),
            ("Fire rating",                 "Class A per ASTM E84 (Flame Spread ≤ 25, Smoke ≤ 450)"),
            ("Moisture absorption",         "< 0.1 % by weight (ASTM D570)"),
            ("Service temperature",         "–20 °F to 140 °F"),
            ("R-value (1/2 in)",            "≈ 0.5 hr·ft²·°F/BTU"),
            ("Impact resistance",           "High (Izod > 2.0 ft·lb/in)"),
            ("Finish",                      "Smooth white · wood-grain · marble · textured"),
            ("Installation",                "Screws, construction adhesive, or H/J aluminum trim"),
            ("Standards",                   "ASTM D1784 Class 14244, ASTM E84 Class A"),
            ("Shelf life",                  "Unlimited (indoors, out of direct UV)"),
            ("Country of origin",           "Made in Mexico"),
        ],
        "truckload": "1 × 40 ft container ≈ 24 pallets ≈ 7,200 panels (1/2 in · 4 × 8 ft).",
    },
    "suspan-ceiling-us": {
        "title": "SusPan Ceiling Tiles — Technical Spec Sheet (US)",
        "product": "SusPan Acoustic Ceiling Tiles",
        "brand": "SusPan",
        "intro": "Lay-in acoustic ceiling tiles for suspended T-grid systems. Humidity resistant and dimensionally stable in high-humidity climates (ideal for Gulf Coast + border Texas).",
        "rows": [
            ("Format",                      "2 × 2 ft · 2 × 4 ft"),
            ("Thickness",                   "5/8 in · 3/4 in"),
            ("Edge",                        "Square (lay-in) · Tegular"),
            ("Weight (2 × 2 ft)",           "~0.9 lb / tile"),
            ("NRC (acoustic absorption)",   "0.55 – 0.70 depending on grade"),
            ("CAC (attenuation)",           "≥ 35"),
            ("Light reflectance (LR)",      "0.82"),
            ("Fire rating",                 "Class A per ASTM E84"),
            ("Humidity resistance",         "Up to 95 % RH, 104 °F sustained"),
            ("Grid compatibility",          "Standard 15/16 in or 9/16 in T-grid"),
            ("Finish",                      "White washable paint, perforated or fissured"),
            ("Standards",                   "ASTM E84 Class A, ASTM E795, ASTM C367"),
            ("Country of origin",           "Made in Mexico"),
        ],
        "truckload": "1 × 40 ft container ≈ 20 pallets ≈ 10,000 tiles (2 × 2 ft).",
    },
    "insulglass-glasswool-us": {
        "title": "Insulglass Glasswool — Technical Spec Sheet (US)",
        "product": "Insulglass Glasswool Batt / Roll",
        "brand": "Insulglass",
        "intro": "Fiberglass insulation batts and rolls for walls, ceilings, floors and metal buildings. Non-combustible, dimensionally stable, formaldehyde-free formulation.",
        "rows": [
            ("Form",                        "Batt (pre-cut) · Roll (continuous)"),
            ("Density",                     "0.5 – 2.0 lb/ft³"),
            ("Thickness",                   "3-1/2 in · 6-1/4 in · 9-1/2 in"),
            ("Width",                       "15 in · 23 in (stud bay spacing)"),
            ("R-values",                    "R-11 (3-1/2 in) · R-13 · R-19 (6-1/4 in) · R-30 (9-1/2 in)"),
            ("Thermal conductivity (k)",    "0.26 – 0.29 BTU·in / hr·ft²·°F"),
            ("Service temperature",         "Up to 450 °F continuous"),
            ("Fire rating",                 "Non-combustible per ASTM E136"),
            ("Flame spread / smoke",        "≤ 25 / ≤ 50 (ASTM E84)"),
            ("Vapor permeability",          "Unfaced > 30 perm · Kraft-faced ≤ 1 perm"),
            ("Facings available",           "Unfaced · Kraft paper · FSK (foil)"),
            ("Standards",                   "ASTM C665 Type I/II/III, ASTM E84, ASTM E136"),
            ("Formaldehyde",                "GREENGUARD-equivalent (ultra-low)"),
            ("Country of origin",           "Made in Mexico"),
        ],
        "truckload": "1 × 40 ft container ≈ 44 bags R-13 15 in × 93 in ≈ 3,500 ft² coverage per truckload at R-13 (varies by R-value).",
    },
    "insulglass-mbi-us": {
        "title": "Insulglass MBI — Technical Spec Sheet (US)",
        "product": "Insulglass MBI (Metal Building Insulation)",
        "brand": "Insulglass",
        "intro": "Faced fiberglass blanket insulation for pre-engineered metal buildings (PEMB). Reduces condensation, improves thermal performance and provides acoustic absorption inside the envelope.",
        "rows": [
            ("Form",                        "Fiberglass blanket laminated to vapor-retarder facing"),
            ("Facings",                     "WMP-VR (white vinyl) · FSK (foil / scrim / kraft) · Reinforced polyethylene"),
            ("Thickness",                   "3 in · 4 in · 6 in · 8 in"),
            ("Standard width",              "48 in · 72 in · custom"),
            ("Standard roll length",        "Up to 150 ft"),
            ("R-values (installed)",        "R-10 (3 in) · R-13 (4 in) · R-19 (6 in) · R-25 (8 in)"),
            ("Permeance",                   "WMP-VR ≤ 0.02 perm (acts as vapor retarder)"),
            ("Fire rating (facing)",        "Class A per ASTM E84"),
            ("Service temperature",         "Up to 450 °F (core)"),
            ("Application",                 "Over purlins / girts in metal buildings (PEMB), bar joist roofs, pre-eng steel"),
            ("Climate performance",         "Priority in hot-humid zones (ASHRAE 1A, 2A, 3A) — Gulf Coast, Texas border, Mexico coast"),
            ("Standards",                   "ASTM C991 Type I/II, NAIMA 202, FM 4411"),
            ("Country of origin",           "Made in Mexico"),
        ],
        "truckload": "1 × 40 ft container ≈ 40–60 rolls (varies by thickness) ≈ 20,000–40,000 ft² of coverage.",
    },
}


@dealers_bp.get("/spec-sheet/<slug>")
def spec_sheet(slug):
    sheet = SPEC_SHEETS.get(slug)
    if sheet is None:
        abort(404)
    return render_template(
        "dealers/spec_sheet.html",
        page=f"spec-{slug}",
        sheet=sheet,
        slug=slug,
    )


# ---- 7) Dealer application form (POST) ----
@dealers_bp.post("/dealer-program/apply")
def apply():
    form = request.form

    company    = (form.get("company") or "").strip()
    years      = (form.get("years") or "").strip()
    website    = (form.get("website") or "").strip()
    product_lines = (form.get("product_lines") or "").strip()
    current_suppliers = (form.get("current_suppliers") or "").strip()
    territory  = (form.get("territory") or "").strip()
    volume_tl  = (form.get("volume_tl") or "").strip()
    warehouse  = (form.get("warehouse") or "").strip()
    fleet      = (form.get("fleet") or "").strip()
    private_label_int = (form.get("private_label") or "no").strip()
    contact_name  = (form.get("contact_name") or "").strip()
    contact_role  = (form.get("contact_role") or "").strip()
    contact_phone = (form.get("contact_phone") or "").strip()
    contact_email = (form.get("contact_email") or "").strip()
    message       = (form.get("message") or "").strip()

    if not (company and territory and contact_name and contact_email):
        flash("Please complete the required fields.", "error")
        return redirect(url_for("dealers.program") + "#apply")

    # Compose admin email
    html = f"""
    <h2>New Dealer Program application</h2>
    <p><b>Submitted:</b> {datetime.utcnow().isoformat()} UTC</p>
    <table style="border-collapse:collapse" cellpadding="6">
      <tr><td><b>Company</b></td><td>{company}</td></tr>
      <tr><td><b>Years in business</b></td><td>{years}</td></tr>
      <tr><td><b>Website</b></td><td>{website}</td></tr>
      <tr><td><b>Current product lines</b></td><td>{product_lines}</td></tr>
      <tr><td><b>Current suppliers</b></td><td>{current_suppliers}</td></tr>
      <tr><td><b>Territory of interest</b></td><td>{territory}</td></tr>
      <tr><td><b>Volume estimate (truckloads/month)</b></td><td>{volume_tl}</td></tr>
      <tr><td><b>Warehouse</b></td><td>{warehouse}</td></tr>
      <tr><td><b>Fleet</b></td><td>{fleet}</td></tr>
      <tr><td><b>Private-label interest</b></td><td>{private_label_int}</td></tr>
      <tr><td><b>Contact</b></td><td>{contact_name} — {contact_role}</td></tr>
      <tr><td><b>Phone</b></td><td>{contact_phone}</td></tr>
      <tr><td><b>Email</b></td><td>{contact_email}</td></tr>
      <tr><td><b>Message</b></td><td>{message}</td></tr>
    </table>
    """

    try:
        from lib.emailer import send_email, _admin_email
        send_email(
            to=_admin_email(),
            subject=f"[Arobe · US Dealer] Application — {company} ({territory})",
            html=html,
            reply_to=contact_email,
        )
    except Exception as e:
        log.exception("Error sending dealer application: %s", e)

    return render_template(
        "dealers/application_thanks.html",
        page="dealer-apply-thanks",
        company=company,
        contact_name=contact_name,
    )
