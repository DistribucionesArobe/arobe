"""
Ciudades industriales objetivo para landings de obra (Fase 18).
Se consumen vía ?ciudad=<slug> en las URLs industriales.
Si el slug no mapea, fallback genérico "en tu obra".
"""

INDUSTRIAL_CITIES = {
    "monterrey": {
        "nombre":       "Monterrey",
        "region":       "Nuevo León",
        "titular":      "en Monterrey",
        "wa_ciudad":    "Monterrey",
    },
    "apodaca": {
        "nombre":       "Apodaca",
        "region":       "Nuevo León",
        "titular":      "en Apodaca",
        "wa_ciudad":    "Apodaca, NL",
    },
    "escobedo": {
        "nombre":       "Escobedo",
        "region":       "Nuevo León",
        "titular":      "en Escobedo",
        "wa_ciudad":    "Escobedo, NL",
    },
    "santa-catarina": {
        "nombre":       "Santa Catarina",
        "region":       "Nuevo León",
        "titular":      "en Santa Catarina",
        "wa_ciudad":    "Santa Catarina, NL",
    },
    "saltillo": {
        "nombre":       "Saltillo",
        "region":       "Coahuila",
        "titular":      "en Saltillo",
        "wa_ciudad":    "Saltillo",
    },
    "ramos-arizpe": {
        "nombre":       "Ramos Arizpe",
        "region":       "Coahuila",
        "titular":      "en Ramos Arizpe",
        "wa_ciudad":    "Ramos Arizpe",
    },
    "derramadero": {
        "nombre":       "Derramadero",
        "region":       "Coahuila",
        "titular":      "en Derramadero",
        "wa_ciudad":    "Derramadero, Saltillo",
    },
    "slp": {
        "nombre":       "San Luis Potosí",
        "region":       "San Luis Potosí",
        "titular":      "en San Luis Potosí",
        "wa_ciudad":    "San Luis Potosí",
    },
    "altamira": {
        "nombre":       "Altamira",
        "region":       "Tamaulipas",
        "titular":      "en Altamira",
        "wa_ciudad":    "Altamira",
    },
    "tampico": {
        "nombre":       "Tampico",
        "region":       "Tamaulipas",
        "titular":      "en Tampico",
        "wa_ciudad":    "Tampico",
    },
    "madero": {
        "nombre":       "Ciudad Madero",
        "region":       "Tamaulipas",
        "titular":      "en Ciudad Madero",
        "wa_ciudad":    "Ciudad Madero",
    },
    "reynosa": {
        "nombre":       "Reynosa",
        "region":       "Tamaulipas",
        "titular":      "en Reynosa",
        "wa_ciudad":    "Reynosa",
    },
    "matamoros": {
        "nombre":       "Matamoros",
        "region":       "Tamaulipas",
        "titular":      "en Matamoros",
        "wa_ciudad":    "Matamoros",
    },
    "nuevo-laredo": {
        "nombre":       "Nuevo Laredo",
        "region":       "Tamaulipas",
        "titular":      "en Nuevo Laredo",
        "wa_ciudad":    "Nuevo Laredo",
    },
}

# Chips de cobertura mostrados en la landing (todas las ciudades principales)
COVERAGE_CHIPS = [
    "Monterrey", "Apodaca", "Escobedo", "Santa Catarina",
    "Saltillo", "Ramos Arizpe",
    "San Luis Potosí",
    "Altamira", "Tampico", "Cd. Madero",
    "Reynosa", "Matamoros", "Nuevo Laredo",
]


def get(slug):
    """Devuelve el dict de la ciudad o un fallback genérico."""
    if not slug:
        return _fallback()
    c = INDUSTRIAL_CITIES.get(slug.strip().lower())
    return c or _fallback()


def _fallback():
    return {
        "nombre":    "",
        "region":    "",
        "titular":   "en tu obra",
        "wa_ciudad": "",   # mensaje genérico de WA sin ciudad
    }
