document.documentElement.classList.add("js");

const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");
const contactForm = document.querySelector("[data-contact-form]");
const formNote = document.querySelector("[data-form-note]");
const builders = document.querySelectorAll("[data-builder]");
const whatsappBase = "https://wa.me/595972187822?text=";

if (navToggle && siteNav) {
  const dropdowns = siteNav.querySelectorAll("details");
  const closeDropdowns = () => dropdowns.forEach((dropdown) => { dropdown.open = false; });
  const setMenuOpen = (isOpen) => {
    siteNav.classList.toggle("is-open", isOpen);
    navToggle.setAttribute("aria-expanded", String(isOpen));
    navToggle.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
    document.body.classList.toggle("no-scroll", isOpen);
    if (!isOpen) closeDropdowns();
  };
  setMenuOpen(false);

  navToggle.addEventListener("click", () => setMenuOpen(navToggle.getAttribute("aria-expanded") !== "true"));
  siteNav.addEventListener("click", (event) => {
    if (event.target.closest("a")) setMenuOpen(false);
  });
  document.addEventListener("click", (event) => {
    if (!siteNav.contains(event.target) && !navToggle.contains(event.target)) setMenuOpen(false);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    const openDropdown = Array.from(dropdowns).find((dropdown) => dropdown.open);
    if (openDropdown) {
      closeDropdowns();
      openDropdown.querySelector("summary")?.focus();
    } else if (navToggle.getAttribute("aria-expanded") === "true") {
      setMenuOpen(false);
      navToggle.focus();
    }
  });
  siteNav.addEventListener("focusout", (event) => {
    if (event.relatedTarget && !siteNav.contains(event.relatedTarget) && event.relatedTarget !== navToggle) setMenuOpen(false);
  });
  // Match the actual CSS visibility instead of duplicating a responsive breakpoint.
  window.addEventListener("resize", () => {
    if (window.getComputedStyle(navToggle).display === "none") setMenuOpen(false);
  });

  // The preview serves .html files; Cloudflare Pages uses extensionless URLs.
  const pageKey = (pathname) => pathname.replace(/\/+$/, "").split("/").pop().replace(/\.html$/, "") || "index";
  const pageName = pageKey(window.location.pathname);
  siteNav.querySelectorAll("a[href]").forEach((link) => {
    const destination = new URL(link.href, window.location.href);
    const destinationPage = pageKey(destination.pathname);
    if (destination.origin === window.location.origin && destinationPage === pageName && !destination.hash) {
      link.setAttribute("aria-current", "page");
      link.closest("details")?.classList.add("has-current");
    }
  });
}

if (contactForm && formNote) {
  const prepared = contactForm.querySelector("[data-contact-prepared]");
  const preview = contactForm.querySelector("[data-contact-preview]");
  const whatsappLink = contactForm.querySelector("[data-contact-whatsapp]");
  const submitButton = contactForm.querySelector('[type="submit"]');
  // Keep the HTML submit disabled until the local handoff can be prepared safely.
  if (submitButton && prepared && preview && whatsappLink) submitButton.disabled = false;
  const invalidatePreparedMessage = () => {
    if (prepared) prepared.hidden = true;
    if (whatsappLink) {
      whatsappLink.removeAttribute("href");
      delete whatsappLink.dataset.analyticsService;
    }
    formNote.textContent = "Tu consulta se prepara en este dispositivo. Vos decidís cuándo enviarla por WhatsApp.";
  };
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!contactForm.reportValidity() || !prepared || !preview || !whatsappLink) return;
    const data = new FormData(contactForm);
    const field = (name) => String(data.get(name) || "").trim();
    const lines = [
      "Hola, Closer. Quiero conversar sobre un proyecto.",
      "",
      `Nombre: ${field("name")}`,
      `Contacto: ${field("contact")}`,
      ...(field("company") ? [`Marca o empresa: ${field("company")}`] : []),
      `Servicio: ${field("goal")}`,
      ...(field("message") ? ["", "Sobre el proyecto:", field("message")] : []),
    ];
    const message = lines.join("\n");
    preview.textContent = message;
    whatsappLink.href = `${whatsappBase}${encodeURIComponent(message)}`;
    whatsappLink.dataset.analyticsService = contactServices[field("goal")] || "unknown";
    prepared.hidden = false;
    formNote.textContent = "Consulta preparada. Revisá el mensaje y abrí WhatsApp para enviarlo cuando quieras.";
    prepared.querySelector("h3")?.focus();
    document.dispatchEvent(new CustomEvent("closer:contact-prepared", {
      detail: { service: String(data.get("goal") || "") },
    }));
  });
  contactForm.addEventListener("input", invalidatePreparedMessage);
  contactForm.addEventListener("change", invalidatePreparedMessage);
  contactForm.addEventListener("reset", invalidatePreparedMessage);
}

const nonNegativeNumber = (value) => {
  const number = Number(value);
  return Number.isFinite(number) && number >= 0 ? number : 0;
};
const readQuantity = (input) => {
  const quantity = Math.floor(nonNegativeNumber(input?.value));
  return Number.isSafeInteger(quantity) ? quantity : 0;
};

builders.forEach((builder, builderIndex) => {
  const rate = nonNegativeNumber(builder.dataset.rate);
  const basePyg = nonNegativeNumber(builder.dataset.basePyg);
  const quantityInputs = builder.querySelectorAll("[data-builder-quantity]");
  const addons = builder.querySelectorAll("[data-builder-addon]");
  const choices = builder.querySelectorAll("[data-builder-choice]");
  const totalUsd = builder.querySelector("[data-total-usd]");
  const totalPyg = builder.querySelector("[data-total-pyg]");
  const breakdown = builder.querySelector("[data-builder-breakdown]");
  const variableNotes = builder.querySelector("[data-builder-variable-notes]");
  const publicationsInput = builder.querySelector("[data-builder-publications]");
  const marketingAuto = builder.querySelector("[data-builder-auto-marketing]");
  const creativeAuto = builder.querySelector("[data-builder-auto-creative]");
  const whatsappLink = builder.querySelector("[data-builder-whatsapp]");
  const builderForm = builder.querySelector("form");
  const summary = builder.querySelector(".builder-summary");
  const total = builder.querySelector(".builder-total");
  const formatUsd = (value) => `USD ${Math.round(value).toLocaleString("en-US")}`;
  const formatPyg = (value) => `Gs. ${Math.round(value).toLocaleString("es-PY")}`;
  const dollarEquivalent = (value) => rate > 0 ? formatUsd(value / rate) : "Conversión no disponible";

  // Announce the total once instead of reading every line again on each keystroke.
  summary?.removeAttribute("aria-live");
  if (total) {
    total.setAttribute("role", "status");
    total.setAttribute("aria-live", "polite");
    total.setAttribute("aria-atomic", "true");
  }

  const updateTotal = () => {
    let totalPygValue = basePyg;
    const lineItems = [{ label: "Base operativa mensual (Instagram + Facebook)", value: basePyg }];
    const variableItems = [];
    const hasContent = readQuantity(publicationsInput) > 0;
    if (marketingAuto) marketingAuto.checked = hasContent;
    if (creativeAuto) creativeAuto.checked = hasContent;

    quantityInputs.forEach((input) => {
      const quantity = readQuantity(input);
      const unitPyg = nonNegativeNumber(input.dataset.unitPyg);
      const minQty = Math.floor(nonNegativeNumber(input.dataset.minQty));
      const effectiveQuantity = minQty && quantity > 0 ? Math.max(quantity, minQty) : quantity;
      if (effectiveQuantity > 0) {
        const value = effectiveQuantity * unitPyg;
        totalPygValue += value;
        const label = input.dataset.label || input.closest("label")?.querySelector("span")?.textContent || "Ítem";
        const minimumNote = quantity < minQty ? " (mínimo aplicado)" : "";
        lineItems.push({ label: `${label} × ${effectiveQuantity}${minimumNote}`, value });
      }
    });
    if (hasContent) {
      lineItems.push({ label: "Campaña de marketing básica para redes", value: 0, included: true });
      lineItems.push({ label: "Campaña creativa", value: 0, included: true });
    }
    addons.forEach((input) => {
      if (!input.checked) return;
      const value = nonNegativeNumber(input.dataset.unitPyg);
      totalPygValue += value;
      lineItems.push({ label: input.dataset.label || input.parentElement?.textContent?.trim() || "Adicional", value });
    });
    choices.forEach((input) => {
      if (!input.checked) return;
      const value = nonNegativeNumber(input.value);
      if (value > 0) {
        totalPygValue += value;
        lineItems.push({ label: input.dataset.label || input.parentElement?.textContent?.trim() || "Plan", value });
      }
      if (input.dataset.variableNote) variableItems.push(input.dataset.variableNote);
    });

    if (breakdown) {
      const rows = lineItems.map((item) => {
        const row = document.createElement("div");
        row.className = "summary-line";
        const label = document.createElement("span");
        label.textContent = item.label;
        const amount = document.createElement("strong");
        amount.textContent = item.included ? "Incluida" : formatPyg(item.value);
        row.append(label, amount);
        return row;
      });
      breakdown.replaceChildren(...rows);
    }
    if (variableNotes) {
      const notes = variableItems.map((item) => {
        const note = document.createElement("p");
        note.className = "variable-note";
        note.textContent = item;
        return note;
      });
      variableNotes.replaceChildren(...notes);
    }
    if (totalUsd) totalUsd.textContent = dollarEquivalent(totalPygValue);
    if (totalPyg) totalPyg.textContent = formatPyg(totalPygValue);
    if (whatsappLink) {
      const detailLines = lineItems.map((item) => `- ${item.label}: ${item.included ? "Incluida" : formatPyg(item.value)}`);
      variableItems.forEach((item) => detailLines.push(`- ${item}`));
      detailLines.push(`- Total estimado mensual: ${formatPyg(totalPygValue)} (${dollarEquivalent(totalPygValue)})`);
      detailLines.push("IVA incluido. Pauta publicitaria y consumos variables se abonan por separado.");
      if (rate > 0) {
        detailLines.push(`Conversión referencial histórica del 28/05/2026: 1 USD = Gs. ${rate.toLocaleString("es-PY", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}.`);
      }
      const message = `Me interesa este plan personalizado de Gestión de Redes:\n${detailLines.join("\n")}`;
      whatsappLink.href = `${whatsappBase}${encodeURIComponent(message)}`;
    }
  };

  quantityInputs.forEach((input, index) => {
    input.inputMode = "numeric";
    const help = input.closest("label")?.querySelector("small");
    if (help) {
      if (!help.id) help.id = `quantity-help-${builderIndex}-${index}`;
      input.setAttribute("aria-describedby", help.id);
    }
    input.addEventListener("input", updateTotal);
    input.addEventListener("change", () => {
      input.value = String(readQuantity(input));
      updateTotal();
    });
  });
  addons.forEach((input) => input.addEventListener("change", updateTotal));
  choices.forEach((input) => input.addEventListener("change", updateTotal));
  if (builderForm) {
    builderForm.addEventListener("submit", (event) => event.preventDefault());
    builderForm.addEventListener("reset", () => queueMicrotask(updateTotal));
    if (summary && !builder.querySelector("[data-builder-reset]")) {
      const resetButton = document.createElement("button");
      resetButton.type = "button";
      resetButton.className = "button secondary builder-reset";
      resetButton.dataset.builderReset = "";
      resetButton.textContent = "Restablecer plan";
      resetButton.addEventListener("click", () => builderForm.reset());
      summary.append(resetButton);
    }
  }
  updateTotal();
});

const analyticsMeasurementId = document.documentElement.dataset.ga4Id || "";
const analyticsIdPattern = /^G-[A-Z0-9]{6,}$/;
const analyticsConfigured = analyticsIdPattern.test(analyticsMeasurementId);
let analyticsEnabled = false;

const analyticsServices = new Set([
  "gestion-redes",
  "meta-ads",
  "google-ads",
  "chatbots-ia",
  "paginas-web",
  "apps-sistemas",
  "campanias-creativas",
  "automatizaciones-bi",
  "multiple",
  "unknown",
]);
const contactServices = {
  "Gestión de redes sociales": "gestion-redes",
  "Chatbot con IA / CloserAI": "chatbots-ia",
  "Página web": "paginas-web",
  "App o sistema": "apps-sistemas",
  "Campaña creativa": "campanias-creativas",
  "Google Ads": "google-ads",
  "Automatización o BI": "automatizaciones-bi",
  "Necesito orientación / varios servicios": "multiple",
};

const analyticsPageData = () => {
  const canonicalElement = document.querySelector('link[rel="canonical"]');
  let canonical;
  try {
    const candidate = new URL(canonicalElement?.href || window.location.href, window.location.href);
    canonical = candidate.origin === window.location.origin ? candidate : new URL(window.location.href);
  } catch {
    canonical = new URL(window.location.href);
  }
  canonical.search = "";
  canonical.hash = "";

  let pageReferrer = "";
  try {
    const referrer = new URL(document.referrer);
    pageReferrer = referrer.origin === window.location.origin
      ? `${referrer.origin}${referrer.pathname.replace(/\.html$/, "")}`
      : `${referrer.origin}/`;
  } catch {
    // An empty or malformed referrer is deliberately omitted.
  }

  return {
    page_location: canonical.href,
    page_path: canonical.pathname,
    page_referrer: pageReferrer,
  };
};

const analyticsServiceForPage = () => {
  const page = analyticsPageData().page_path.replace(/^\/+|\/+$/g, "");
  if (analyticsServices.has(page)) return page;
  if (page.startsWith("plan-redes")) return "gestion-redes";
  if (page.startsWith("plan-chatbot")) return "chatbots-ia";
  if (page.startsWith("plan-campana")) return "campanias-creativas";
  return "unknown";
};

const analyticsPlacementFor = (element) => {
  if (element.closest(".site-header")) return "header";
  if (element.closest(".site-footer")) return "footer";
  if (element.closest(".home-hero, .page-hero")) return "hero";
  if (element.closest("[data-contact-form]")) return "contact_form";
  if (element.closest("[data-builder]")) return "quote";
  return "body";
};

const emitAnalytics = (name, details = {}) => {
  if (!analyticsEnabled || !window.gtag) return;
  const allowedEvents = new Set(["page_view", "quote_start", "contact_prepare", "whatsapp_click", "email_click"]);
  if (!allowedEvents.has(name)) return;
  const payload = analyticsPageData();
  if (name !== "page_view" && analyticsServices.has(details.service)) payload.service = details.service;
  if (name !== "page_view" && ["header", "footer", "hero", "body", "contact_form", "quote"].includes(details.placement)) {
    payload.placement = details.placement;
  }
  window.gtag("event", name, payload);
};

const loadAnalytics = () => {
  if (!analyticsConfigured || window.closerAnalyticsLoaded) return;
  window.closerAnalyticsLoaded = true;
  analyticsEnabled = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() { window.dataLayer.push(arguments); };
  window.gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "granted",
  });
  window.gtag("js", new Date());
  const pageData = analyticsPageData();
  window.gtag("config", analyticsMeasurementId, {
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
    send_page_view: false,
    ...pageData,
  });
  emitAnalytics("page_view");
  const script = document.createElement("script");
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(analyticsMeasurementId)}`;
  document.head.append(script);
};

if (analyticsConfigured) loadAnalytics();

document.addEventListener("closer:contact-prepared", (event) => {
  emitAnalytics("contact_prepare", {
    service: contactServices[event.detail?.service] || "unknown",
    placement: "contact_form",
  });
});

builders.forEach((builder) => {
  let started = false;
  const startQuote = (event) => {
    if (started || !event.isTrusted) return;
    started = true;
    emitAnalytics("quote_start", { service: "gestion-redes", placement: "quote" });
  };
  builder.querySelectorAll("input:not([disabled]), select:not([disabled])").forEach((control) => {
    ["pointerdown", "keydown", "input", "change"].forEach((type) => control.addEventListener(type, startQuote));
  });
});

document.addEventListener("click", (event) => {
  if (!event.isTrusted) return;
  const link = event.target.closest("a[href]");
  if (!link) return;
  if (link.href.startsWith("https://wa.me/595972187822")) {
    emitAnalytics("whatsapp_click", {
      service: link.dataset.analyticsService || analyticsServiceForPage(),
      placement: analyticsPlacementFor(link),
    });
  } else if (link.href === "mailto:closer@closer.com.py") {
    emitAnalytics("email_click", { placement: analyticsPlacementFor(link) });
  }
});
