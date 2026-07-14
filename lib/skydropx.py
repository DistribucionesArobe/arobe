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
_last_oauth_error = {"status": None, "body": None}
_last_quote_debug = {"status": None, "body": None, "payload": None, "url": None}


def _try_oauth(client_id, client_secret, scope=None):
    """Intenta obtener token con un scope específico. Devuelve (token, status, body)."""
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    if scope:
        payload["scope"] = scope
    try:
        r = requests.post(
            f"{BASE_URL}/oauth/token",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json()
            return data.get("access_token"), 200, data
        return None, r.status_code, r.text[:500]
    except Exception as e:
        return None, None, str(e)[:500]


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

        # Skydropx PRO acepta varios scopes. Probamos en orden: default → sin scope
        # → orders.create → shipments.create. El primero que funcione lo usamos.
        scopes_to_try = [
            "default",
            None,
            "default orders.create shipments.create",
            "orders.create shipments.create default",
            "orders.create",
        ]
        last_status = None
        last_body = None
        for scope in scopes_to_try:
            token, status, body = _try_oauth(client_id, client_secret, scope)
            last_status = status
            last_body = body
            if token:
                _token_cache["token"] = token
                _token_cache["expires_at"] = now + int(body.get("expires_in", 3600) if isinstance(body, dict) else 3600)
                log.info("Skydropx OAuth OK con scope=%r", scope)
                return token
            log.warning("Skydropx OAuth scope=%r → %s: %s", scope, status, str(body)[:200])

        _last_oauth_error["status"] = last_status
        _last_oauth_error["body"] = last_body
        return None


def last_oauth_error():
    """Para diagnóstico: último error de OAuth."""
    return dict(_last_oauth_error)


def is_configured():
    return bool(
        os.environ.get("SKYDROPX_CLIENT_ID", "").strip()
        and os.environ.get("SKYDROPX_CLIENT_SECRET", "").strip()
    )


# ============================================================
# Helpers de rates
# ============================================================
def _rate_ready(rate):
    """Rate lista = success=true + total válido (>0)."""
    if not isinstance(rate, dict):
        return False
    total = rate.get("total") or rate.get("amount")
    try:
        total_num = float(total) if total is not None else 0.0
    except (ValueError, TypeError):
        total_num = 0.0
    return bool(rate.get("success")) and total_num > 0


def _all_pending(rates):
    """True si TODAS las rates están pending o fallidas (nada listo aún)."""
    if not rates:
        return True
    return not any(_rate_ready(r) for r in rates)


# ============================================================
# Datos del origen (Victoria, Tamaulipas — almacén Arobe)
# ============================================================
ORIGIN_AREA = {
    "area_level1": "TAMAULIPAS",           # estado
    "area_level2": "VICTORIA",              # municipio
    "area_level3": "ADOLFO LOPEZ MATEOS",   # colonia (según CSF de la empresa)
}


# ============================================================
# Cotización
# ============================================================
def get_quotations(dest_zip, parcels, origin_zip=None, dest_area=None):
    """
    Cotiza envío en tiempo real.

    Args:
        dest_zip: CP destino de 5 dígitos
        parcels: lista de bultos [{"weight": kg, "length": cm, "width": cm, "height": cm}]
        origin_zip: opcional, default 87020 (Victoria)
        dest_area: dict con area_level1 (estado), area_level2 (municipio),
                   area_level3 (colonia) del destino. Si no viene, usamos
                   valores genéricos que la mayoría de carriers aceptan.

    Returns:
        Lista de opciones ordenadas por precio ascendente:
          [{"id", "carrier", "service", "price", "currency", "days"}, ...]
        None si Skydropx no está configurado o falla.
    """
    token = _get_token()
    if not token:
        return None

    origin = origin_zip or ORIGIN_ZIP

    # Área de destino: uso lo que venga del form o placeholders genéricos.
    dest = dest_area or {}
    dest_a1 = (dest.get("area_level1") or "MEXICO").upper().strip()[:120]
    dest_a2 = (dest.get("area_level2") or dest_a1 or "MEXICO").upper().strip()[:120]
    dest_a3 = (dest.get("area_level3") or "CENTRO").upper().strip()[:120]

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

    # Skydropx PRO v1 requiere area_level1/2/3 en address_from y address_to
    payload = {
        "quotation": {
            "address_from": {
                "country_code": "mx",
                "postal_code": str(origin),
                "area_level1": ORIGIN_AREA["area_level1"],
                "area_level2": ORIGIN_AREA["area_level2"],
                "area_level3": ORIGIN_AREA["area_level3"],
            },
            "address_to": {
                "country_code": "mx",
                "postal_code": str(dest_zip),
                "area_level1": dest_a1,
                "area_level2": dest_a2,
                "area_level3": dest_a3,
            },
            "parcels": clean_parcels,
            "requested_carriers": [
                "estafeta", "fedex", "dhl", "paquetexpress", "sendex",
            ],
        }
    }
    url = f"{BASE_URL}/quotations"

    _last_quote_debug["url"] = url
    _last_quote_debug["payload"] = payload

    try:
        r = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=15,
        )
        _last_quote_debug["status"] = r.status_code
        try:
            _last_quote_debug["body"] = r.json()
        except Exception:
            _last_quote_debug["body"] = r.text[:1500]

        if r.status_code not in (200, 201, 202):
            log.error("Skydropx quotation error %s: %s", r.status_code, r.text[:800])
            return None

        data = r.json()
        quotation_id = data.get("id") or (data.get("data") or {}).get("id")

        # Extraigo rates iniciales
        rates = data.get("rates") or (data.get("data") or {}).get("attributes", {}).get("rates")
        is_completed = data.get("is_completed", False)

        # Skydropx v1 procesa asíncronamente: si is_completed=False o todas las rates
        # están pending, tenemos que hacer polling hasta que estén completadas.
        if quotation_id and (not is_completed or _all_pending(rates or [])):
            poll_url = f"{BASE_URL}/quotations/{quotation_id}"
            for attempt in range(10):  # hasta ~10 segundos total
                time.sleep(1.0)
                try:
                    rp = requests.get(
                        poll_url,
                        headers={
                            "Authorization": f"Bearer {token}",
                            "Accept": "application/json",
                        },
                        timeout=10,
                    )
                    if rp.status_code != 200:
                        log.warning("Skydropx polling %s: %s", rp.status_code, rp.text[:200])
                        continue
                    poll_data = rp.json()
                    rates = poll_data.get("rates") or rates
                    is_completed = poll_data.get("is_completed", False)
                    completed_count = sum(1 for x in (rates or []) if _rate_ready(x))
                    log.info(
                        "Skydropx poll %d: is_completed=%s completed_rates=%d/%d",
                        attempt + 1, is_completed, completed_count, len(rates or []),
                    )
                    _last_quote_debug["body"] = poll_data
                    if is_completed or completed_count >= 3:
                        break
                except Exception as e:
                    log.warning("Skydropx polling exception: %s", e)
                    continue

        if not rates:
            log.warning("Skydropx sin rates: %s", str(data)[:600])
            return []

        options = []
        for rate in rates:
            attrs = rate.get("attributes") if isinstance(rate, dict) and "attributes" in rate else rate
            # SOLO acepto rates listas (success=true + total>0)
            if not _rate_ready(attrs):
                continue
            price = attrs.get("total") or attrs.get("amount") or attrs.get("amount_local")
            try:
                price_num = float(price)
            except (ValueError, TypeError):
                continue
            provider = (
                attrs.get("provider_display_name")
                or attrs.get("provider_name")
                or attrs.get("carrier")
                or "Carrier"
            )
            service = (
                attrs.get("provider_service_name")
                or attrs.get("service_level_name")
                or attrs.get("provider_service_code")
                or ""
            )
            options.append({
                "id": str(rate.get("id") or attrs.get("id") or ""),
                "carrier": provider,
                "service": service,
                "price": price_num,
                "currency": attrs.get("currency_code") or attrs.get("currency") or "MXN",
                "days": attrs.get("days") or attrs.get("estimated_delivery") or None,
            })

        options.sort(key=lambda o: o["price"])
        log.info("Skydropx devolvió %d opciones listas de %d rates totales", len(options), len(rates))
        return options
    except Exception as e:
        log.exception("Skydropx quotation exception")
        _last_quote_debug["status"] = "EXCEPTION"
        _last_quote_debug["body"] = str(e)[:500]
        return None


def last_quote_debug():
    """Para diagnóstico: último intento de cotización."""
    return dict(_last_quote_debug)
