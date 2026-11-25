/*
 * Arobe Group — Industrial landings · gtag conversion tracker
 *
 * Variables globales expuestas por el template:
 *   window.__arobeLanding.producto   (slug: "mbi", "plafon", "glasswool", "pvc")
 *   window.__arobeLanding.ciudad     (nombre: "Monterrey" o "generica")
 *   window.__arobeLanding.landing    (path: "/aislamiento-naves" etc.)
 *
 * Reemplaza los placeholders siguientes con los valores reales de tu
 * cuenta Google Ads antes de activar las campañas:
 *   AW-XXXXXXXXX   → tu Google Ads account ID
 *   ETIQUETA_WA    → conversion label para click en WhatsApp
 *   ETIQUETA_TEL   → conversion label para click en teléfono
 *   ETIQUETA_FORM  → conversion label para submit del formulario
 */

(function () {
  // ---- Preservar UTMs + gclid para atribución downstream ----
  try {
    var params = new URLSearchParams(window.location.search);
    var tracking = {};
    ["utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","fbclid"]
      .forEach(function (k) { if (params.has(k)) tracking[k] = params.get(k); });
    if (Object.keys(tracking).length) {
      tracking._capturedAt = Date.now();
      sessionStorage.setItem("arobe_tracking", JSON.stringify(tracking));
    }
  } catch (e) { /* no sessionStorage */ }

  // ---- Helper global invocado desde onclick="arobeTrackLead(...)" ----
  window.arobeTrackLead = function (eventName) {
    var ctx = window.__arobeLanding || {};
    var saved = {};
    try { saved = JSON.parse(sessionStorage.getItem("arobe_tracking") || "{}"); }
    catch (e) {}

    // Mapeo de conversion labels — reemplaza cuando tengas los ID reales
    var LABELS = {
      whatsapp_hero:       "AW-XXXXXXXXX/ETIQUETA_WA",
      whatsapp_header:     "AW-XXXXXXXXX/ETIQUETA_WA",
      whatsapp_float:      "AW-XXXXXXXXX/ETIQUETA_WA",
      whatsapp_cta_final:  "AW-XXXXXXXXX/ETIQUETA_WA",
      phone:               "AW-XXXXXXXXX/ETIQUETA_TEL",
      form_submit:         "AW-XXXXXXXXX/ETIQUETA_FORM",
      ficha_pdf:           "AW-XXXXXXXXX/ETIQUETA_FORM"  // interés = micro-conversion
    };

    var sendTo = LABELS[eventName];
    if (!sendTo || typeof gtag !== "function") return;

    gtag("event", "conversion", {
      send_to:        sendTo,
      event_category: "lead",
      event_label:    eventName,
      producto:       ctx.producto || "unknown",
      ciudad:         ctx.ciudad   || "generica",
      landing:        ctx.landing  || window.location.pathname,
      utm_source:     saved.utm_source   || null,
      utm_medium:     saved.utm_medium   || null,
      utm_campaign:   saved.utm_campaign || null,
      gclid:          saved.gclid        || null,
      value:          1.0,
      currency:       "MXN"
    });

    // Opcional: también disparar un "generate_lead" para GA4 estándar
    gtag("event", "generate_lead", {
      lead_source:    eventName,
      producto:       ctx.producto,
      ciudad:         ctx.ciudad
    });
  };
})();
