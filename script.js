const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");
const contactForm = document.querySelector("[data-contact-form]");
const formNote = document.querySelector("[data-form-note]");
const builders = document.querySelectorAll("[data-builder]");
const whatsappBase = "https://wa.me/595972187822?text=";

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const isOpen = siteNav.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
    document.body.classList.toggle("no-scroll", isOpen);
  });

  siteNav.addEventListener("click", (event) => {
    if (event.target.matches("a")) {
      siteNav.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("no-scroll");
    }
  });
}

if (contactForm && formNote) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(contactForm);
    const name = data.get("name") || "genial";

    formNote.textContent = `Gracias, ${name}. La consulta quedó registrada en esta demo visual.`;
    contactForm.reset();
  });
}

builders.forEach((builder) => {
  const rate = Number(builder.dataset.rate || 0);
  const basePyg = Number(builder.dataset.basePyg || 0);
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

  const formatUsd = (value) => `USD ${Math.round(value).toLocaleString("en-US")}`;
  const formatPyg = (value) => `Gs. ${Math.round(value).toLocaleString("es-PY")}`;

  const updateConditionalInputs = () => {
    const publications = Math.max(0, Number(publicationsInput?.value || 0));
    const hasContent = publications > 0;

    if (marketingAuto) {
      marketingAuto.checked = hasContent;
    }

    if (creativeAuto) {
      creativeAuto.checked = hasContent;
    }
  };

  const updateTotal = () => {
    let totalPygValue = basePyg;
    const lineItems = [
      { label: "Base operativa mensual (Instagram + Facebook)", value: basePyg },
    ];
    const variableItems = [];
    const publications = Math.max(0, Number(publicationsInput?.value || 0));
    const hasContent = publications > 0;

    quantityInputs.forEach((input) => {
      const quantity = Math.max(0, Number(input.value || 0));
      const unitPyg = Number(input.dataset.unitPyg || 0);
      const minQty = Number(input.dataset.minQty || 0);
      const effectiveQuantity = minQty && quantity > 0 ? Math.max(quantity, minQty) : quantity;

      if (effectiveQuantity > 0) {
        const value = effectiveQuantity * unitPyg;
        totalPygValue += value;

        const baseLabel = input.dataset.label || input.closest("label")?.querySelector("span")?.textContent || "Item";
        const suffix = minQty && quantity > 0 && quantity < minQty ? ` x ${effectiveQuantity} (minimo aplicado)` : ` x ${effectiveQuantity}`;
        lineItems.push({ label: `${baseLabel}${suffix}`, value });
      }
    });

    if (hasContent) {
      lineItems.push({ label: "Campana de Marketing basica para redes", value: 0, included: true });
      lineItems.push({ label: "Campana creativa", value: 0, included: true });
    }

    addons.forEach((input) => {
      if (input.checked) {
        const value = Number(input.dataset.unitPyg || 0);
        totalPygValue += value;
        lineItems.push({
          label: input.dataset.label || input.parentElement?.textContent?.trim() || "Adicional",
          value,
        });
      }
    });

    choices.forEach((input) => {
      if (input.checked) {
        const value = Number(input.value || 0);
        if (value > 0) {
          totalPygValue += value;
          lineItems.push({
            label: input.dataset.label || input.parentElement?.textContent?.trim() || "Plan",
            value,
          });
        }

        if (input.dataset.variableNote) {
          variableItems.push(input.dataset.variableNote);
        }
      }
    });

    if (breakdown) {
      breakdown.innerHTML = lineItems
        .map((item) => {
          const amount = item.included ? "Incluida" : formatPyg(item.value);
          return `<div class="summary-line"><span>${item.label}</span><strong>${amount}</strong></div>`;
        })
        .join("");
    }

    if (variableNotes) {
      variableNotes.innerHTML = variableItems
        .map((item) => `<p class="variable-note">${item}</p>`)
        .join("");
    }

    if (totalUsd) totalUsd.textContent = formatUsd(totalPygValue / rate);
    if (totalPyg) totalPyg.textContent = formatPyg(totalPygValue);

    if (whatsappLink) {
      const detailLines = lineItems.map((item) => {
        const amount = item.included ? "Incluida" : formatPyg(item.value);
        return `- ${item.label}: ${amount}`;
      });

      variableItems.forEach((item) => {
        detailLines.push(`- ${item}`);
      });

      detailLines.push(`- Total estimado: ${formatPyg(totalPygValue)} (${formatUsd(totalPygValue / rate)})`);

      const message = `Me interesa este plan personalizado de Gestion de Redes:\n${detailLines.join("\n")}`;
      whatsappLink.href = `${whatsappBase}${encodeURIComponent(message)}`;
    }
  };

  quantityInputs.forEach((input) => input.addEventListener("input", () => {
    updateConditionalInputs();
    updateTotal();
  }));
  addons.forEach((input) => input.addEventListener("change", updateTotal));
  choices.forEach((input) => input.addEventListener("change", () => {
    updateConditionalInputs();
    updateTotal();
  }));

  updateConditionalInputs();
  updateTotal();
});
