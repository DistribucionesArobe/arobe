"""
Cliente Skydropx PRO API — Fase 7.2.

Skydropx v1 (pro.skydropx.com) usa OAuth 2.0 client_credentials.
Docs: https://docs.skydropx.com/

Env vars requeridas:
  - SKYDROPX_CLIENT_ID     (Clave de cliente / API Key)
  - SKYDROPX_CLIENT_SECRET (Clave secreta del cliente / API Secret Key)

Almacén origen: CP 87020 (Victoria, Tamaulipas)
"""
import os
import time
import logging
import threading

import requests

log = logging.getLogger("skydropx")

BASE_URL = "https://pro.skydropx.com/api/v1"
ORIGIN_ZIP = "87020"

# Cache del OAuth token en memoria (renovamos a los 55 min)
_token_lock = threading.Lock()
_token_cache = {"token": None, "expires_at": 0.0}


# ============================================================
# Auth
# ============================================================
def _get_token():
    """Devuelve un access token válido, cacheado en memoria."""
    now = time.time()
    with _token_lock:
        if _token_cache["token"] and _token_cache["expires_at"] > now + 60:
            return _token_cache["token"]

        client_id = os.environ.get("SKYDROPX_CLIENT_ID", "").strip()
        client_secret = os.environ.get("SKYDROPX_CLIENT_SECRET", "").strip()
        if not (client_id and client_secret):
            log.warning("Skydropx no configurado (falta CLIENT_ID/SECRET)")
            return None

        try:
            r = requests.post(
                f"{BASE_URL}/oauth/token",
                json={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": "client_credentials",
                    "scope": "default orders.create shipments.create",
                },
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                _token_cache["token"] = data.get("access_token")
                _token_cache["expires_at"] = now + int(data.get("expires_in", 3600))
                log.info("Skydropx token renovado (expira en %ss)", data.get("expires_in"))
                return _token_cache["token"]
            else:
                log.error("Skydropx OAuth error %s: %s", r.status_code, r.text[:400])
                return None
        except Exception as e:
            log.exception("Skydropx OAuth exception")
            return None


def is_configured():
    return bool(
        os.environ.get("SKYDROPX_CLIENT_ID", "").strip()
        and os.environ.get("SKYDROPX_CLIENT_SECRET", "").strip()
    )


# ============================================================
# Cotización
# ============================================================
def get_quotations(dest_zip, parcels, origin_zip=None):
    """
    Cotiza envío en tiempo real.

    Args:
        dest_zip: CP destino de 5 dígitos
        parcels: lista de bultos [{"weight": kg, "length": cm, "width": cm, "height": cm}]
        origin_zip: opcional, default 87020 (Victoria)

    Returns:
        Lista de opciones ordenadas por precio ascendente:
          [{"id", "carrier", "service", "price", "currency", "days"}, ...]
        None si Skydropx no está configurado o falla.
    """
    token = _get_token()
    if not token:
        return None

    origin = origin_zip or ORIGIN_ZIP

    # Normalizo parcels: Skydropx requiere int, weight >= 1kg
    clean_parcels = []
    for p in parcels:
        clean_parcels.append({
            "weight": max(1, round(float(p.get("weight", 1)))),
            "length": max(5, int(p.get("length", 30))),
            "width": max(5, int(p.get("width", 30))),
            "height": max(5, int(p.get("height", 30))),
            "distance_unit": "CM",
            "mass_unit": "KG",
        })

    payload = {
        "quotation": {
            "address_from": {"country_code": "mx", "postal_code": str(origin)},
            "address_to": {"country_code": "mx", "postal_code": str(dest_zip)},
            "parcels": clean_parcels,
            "requested_carriers": [
                "estafeta", "fedex", "dhl", "paquetexpress",
                "redpack", "sendex", "carssa", "quiken", "ampm",
            ],
        }
    }

    try:
        r = requests.post(
            f"{BASE_URL}/quotations",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=25,
        )
        if r.status_code not in (200, 201):
            log.error("Skydropx quotation error %s: %s", r.status_code, r.text[:500])
            return None

        data = r.json()
        # La respuesta puede venir en {data:{attributes:{rates:[]}}} o {rates:[]}
        rates = None
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], dict):
                rates = data["data"].get("attributes", {}).get("rates")
            if rates is None:
                rates = data.get("rates")

        if not rates:
            log.warning("Skydropx no devolvió rates: %s", str(data)[:400])
            return []

        options = []
        for rate in rates:
            price = rate.get("total") or rate.get("amount_local") or rate.get("amount")
            if price is None:
                continue
            options.append({
                "id": str(rate.get("id") or ""),
                "carrier": rate.get("provider_name") or rate.get("provider") or "Carrier",
                "service": rate.get("provider_service_name") or rate.get("service_level_name") or rate.get("service_level_code") or "",
                "price": float(price),
                "currency": rate.get("currency") or "MXN",
                "days": rate.get("days") or rate.get("estimated_delivery") or None,
            })

        # Ordeno por precio ascendente
        options.sort(key=lambda o: o["price"])
        return options
    except Exception as e:
        log.exception("Skydropx quotation exception")
        return None
