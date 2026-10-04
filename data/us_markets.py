"""
US metro areas target list for Arobe Dealer Program.
Phase 15 — US expansion as Mexican SA (SA de CV),
delivering FOB Reynosa / Matamoros / Nuevo Laredo.

status: available | reserved | assigned
"""

US_METROS = [
    # ---- Tier 1: border Texas (direct FOB delivery) ----
    {
        "slug": "laredo-tx",
        "metro": "Laredo",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "78040",
        "population": "280,000",
        "border_crossing": "Nuevo Laredo (FOB point)",
        "distance_from_fob_mi": 0,
        "distance_from_victoria_mi": 185,
        "tier": 1,
        "status": "available",
        "notes": "Direct FOB pickup at Nuevo Laredo warehouse. Largest inland port in US.",
    },
    {
        "slug": "mcallen-tx",
        "metro": "McAllen · Edinburg · Pharr",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "78501",
        "population": "900,000 (RGV)",
        "border_crossing": "Reynosa (FOB point)",
        "distance_from_fob_mi": 10,
        "distance_from_victoria_mi": 240,
        "tier": 1,
        "status": "available",
        "notes": "Rio Grande Valley. Fastest-growing residential market in TX. FOB Reynosa pickup.",
    },
    {
        "slug": "brownsville-tx",
        "metro": "Brownsville · Harlingen",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "78520",
        "population": "420,000",
        "border_crossing": "Matamoros (FOB point)",
        "distance_from_fob_mi": 5,
        "distance_from_victoria_mi": 220,
        "tier": 1,
        "status": "available",
        "notes": "FOB Matamoros pickup. Port + residential construction.",
    },
    {
        "slug": "eagle-pass-tx",
        "metro": "Eagle Pass · Del Rio",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "78852",
        "population": "90,000",
        "border_crossing": "Nuevo Laredo (FOB point)",
        "distance_from_fob_mi": 155,
        "distance_from_victoria_mi": 310,
        "tier": 1,
        "status": "available",
        "notes": "Smaller market but low competition. FOB Nuevo Laredo pickup.",
    },

    # ---- Tier 2: Texas inland (2-5 hrs from FOB) ----
    {
        "slug": "san-antonio-tx",
        "metro": "San Antonio",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "78201",
        "population": "2.6 million",
        "border_crossing": "Nuevo Laredo (FOB point)",
        "distance_from_fob_mi": 155,
        "distance_from_victoria_mi": 340,
        "tier": 2,
        "status": "available",
        "notes": "Major metro. Strong Hispanic contractor base. 2.5 hr drive from Laredo.",
    },
    {
        "slug": "corpus-christi-tx",
        "metro": "Corpus Christi",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "78401",
        "population": "440,000",
        "border_crossing": "Matamoros (FOB point)",
        "distance_from_fob_mi": 170,
        "distance_from_victoria_mi": 340,
        "tier": 2,
        "status": "available",
        "notes": "Coastal, humidity-resistant products priority. Port city.",
    },
    {
        "slug": "houston-tx",
        "metro": "Houston",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "77001",
        "population": "7.3 million",
        "border_crossing": "Matamoros or Laredo (FOB point)",
        "distance_from_fob_mi": 350,
        "distance_from_victoria_mi": 500,
        "tier": 2,
        "status": "available",
        "notes": "Largest TX market. High competition. Reserved for proven dealers (phase 2).",
    },
    {
        "slug": "austin-tx",
        "metro": "Austin",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "78701",
        "population": "2.3 million",
        "border_crossing": "Nuevo Laredo (FOB point)",
        "distance_from_fob_mi": 250,
        "distance_from_victoria_mi": 430,
        "tier": 2,
        "status": "available",
        "notes": "Explosive growth. Premium residential + commercial.",
    },

    # ---- Tier 3: Future expansion ----
    {
        "slug": "dallas-fort-worth-tx",
        "metro": "Dallas · Fort Worth",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "75201",
        "population": "8.0 million",
        "border_crossing": "Nuevo Laredo (FOB point)",
        "distance_from_fob_mi": 440,
        "distance_from_victoria_mi": 620,
        "tier": 3,
        "status": "reserved",
        "notes": "Phase 2 target. Freight cost from border is a factor; needs dealer with own trucks.",
    },
    {
        "slug": "el-paso-tx",
        "metro": "El Paso",
        "state": "TX",
        "state_full": "Texas",
        "zip_example": "79901",
        "population": "870,000",
        "border_crossing": "Nuevo Laredo (FOB point)",
        "distance_from_fob_mi": 625,
        "distance_from_victoria_mi": 810,
        "tier": 3,
        "status": "reserved",
        "notes": "Phase 3. Logistics challenging; FOB cost competitive only for large volumes.",
    },
    {
        "slug": "phoenix-az",
        "metro": "Phoenix",
        "state": "AZ",
        "state_full": "Arizona",
        "zip_example": "85001",
        "population": "5.0 million",
        "border_crossing": "Nuevo Laredo (FOB point)",
        "distance_from_fob_mi": 1050,
        "distance_from_victoria_mi": 1230,
        "tier": 3,
        "status": "reserved",
        "notes": "Phase 3. Hot/dry climate — MBI and glasswool priority.",
    },
]


def all_metros():
    return US_METROS


def available_metros():
    return [m for m in US_METROS if m["status"] == "available"]


def tier1_metros():
    return [m for m in US_METROS if m["tier"] == 1]


def by_slug(slug):
    for m in US_METROS:
        if m["slug"] == slug:
            return m
    return None


# ---- Minimum order & commercial terms (one place to tweak) ----
TERMS = {
    "min_order_usd": 30000,
    "min_order_label": "1 full 40 ft container (approx. $30,000 USD)",
    "min_quarterly_usd": 30000,
    "min_quarterly_label": "1 truckload every 90 days",
    "min_annual_usd": 120000,
    "exclusivity_months": 12,
    "private_label_min_truckloads": 2,
    "lead_time_days": 14,
    "sample_kit": "Free, shipped by DHL",
    "co_op_marketing_pct": 2,
    "payment_terms": "50% deposit + 50% on readiness. Net-30 after 3 successful loads.",
    "incoterms": "FOB Reynosa / FOB Matamoros / FOB Nuevo Laredo (dealer handles US customs with their broker).",
    "currency": "USD or MXN pesos — dealer's choice. Invoiced by Distribuciones Arobe S.A.S. de C.V.",
}
