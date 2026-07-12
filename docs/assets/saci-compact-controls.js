(() => {
  "use strict";

  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];

  function closeMenus(except = null) {
    $$(".saci-compact-menu").forEach(menu => {
      if (menu === except) return;
      menu.hidden = true;
      const trigger = document.querySelector(
        `[aria-controls="${menu.id}"]`
      );
      trigger?.setAttribute("aria-expanded", "false");
    });
  }

  function openOrClose(trigger, menu) {
    const willOpen = menu.hidden;
    closeMenus(willOpen ? menu : null);
    menu.hidden = !willOpen;
    trigger.setAttribute("aria-expanded", String(willOpen));
  }

  function currentLanguage() {
    return (document.documentElement.lang || "tr")
      .toLowerCase()
      .startsWith("en") ? "EN" : "TR";
  }

  function currentTheme() {
    return (
      document.documentElement.dataset.theme ||
      localStorage.getItem("saci-theme") ||
      "dark"
    ).toLowerCase();
  }

  function updateState() {
    const language = currentLanguage();
    const languageButton = $("#saciLanguageCompact");

    if (languageButton) {
      languageButton.querySelector(".label").textContent = language;
      languageButton.title =
        language === "TR" ? "Switch to English" : "Türkçeye geç";
    }

    const theme = currentTheme();

    $$("[data-theme-proxy]").forEach(button => {
      button.setAttribute(
        "aria-current",
        String(button.dataset.themeProxy === theme)
      );
    });
  }

  function triggerOriginal(target) {
    const original = $(target);
    if (!original) return false;
    original.click();
    return true;
  }

  function init() {
    const languageButton = $("#saciLanguageCompact");
    const fontButton = $("#saciFontCompact");
    const themeButton = $("#saciThemeCompact");
    const fontMenu = $("#saciFontMenu");
    const themeMenu = $("#saciThemeMenu");

    languageButton?.addEventListener("click", () => {
      const target =
        currentLanguage() === "TR" ? "#langEN" : "#langTR";
      triggerOriginal(target);
    });

    fontButton?.addEventListener("click", () => {
      openOrClose(fontButton, fontMenu);
    });

    themeButton?.addEventListener("click", () => {
      openOrClose(themeButton, themeMenu);
    });

    $$("[data-font-proxy]").forEach(button => {
      button.addEventListener("click", () => {
        triggerOriginal(`#${button.dataset.fontProxy}`);
        closeMenus();
      });
    });

    $$("[data-theme-proxy]").forEach(button => {
      button.addEventListener("click", () => {
        triggerOriginal(
          `[data-theme-btn="${button.dataset.themeProxy}"]`
        );
        requestAnimationFrame(updateState);
        closeMenus();
      });
    });

    document.addEventListener("pointerdown", event => {
      if (!event.target.closest(".saci-compact-control")) {
        closeMenus();
      }
    });

    document.addEventListener("keydown", event => {
      if (event.key === "Escape") {
        closeMenus();
      }
    });

    const observer = new MutationObserver(updateState);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme", "lang"]
    });

    window.addEventListener("storage", updateState);
    updateState();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();

/* SACI_COMPACT_CONTROLS_I18N_START */
(() => {
  "use strict";

  function localizeCompactControls() {
    const english = (document.documentElement.lang || "")
      .toLowerCase()
      .startsWith("en");

    const themeTrigger = document.querySelector(
      "#saciThemeCompact > span:first-child"
    );

    const fontTrigger = document.querySelector("#saciFontCompact");
    const languageTrigger = document.querySelector("#saciLanguageCompact");

    if (themeTrigger) {
      themeTrigger.textContent = english ? "Theme" : "Tema";
    }

    if (fontTrigger) {
      fontTrigger.setAttribute(
        "aria-label",
        english ? "Font size" : "Yazı boyutu"
      );
      fontTrigger.title = english ? "Font size" : "Yazı boyutu";
    }

    const fontLabels = {
      fontDown: english ? "Smaller" : "Küçült",
      fontReset: english ? "Reset" : "Sıfırla",
      fontUp: english ? "Larger" : "Büyüt"
    };

    document
      .querySelectorAll("[data-font-proxy]")
      .forEach(button => {
        const label = button.querySelector("span:first-child");
        const key = button.dataset.fontProxy;

        if (label && fontLabels[key]) {
          label.textContent = fontLabels[key];
        }
      });

    const themeButton = document.querySelector("#saciThemeCompact");

    if (themeButton) {
      themeButton.setAttribute(
        "aria-label",
        english ? "Theme" : "Tema"
      );
      themeButton.title = english ? "Theme" : "Tema";
    }

    if (languageTrigger) {
      languageTrigger.setAttribute(
        "aria-label",
        english ? "Switch to Turkish" : "İngilizceye geç"
      );
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      localizeCompactControls,
      { once: true }
    );
  } else {
    localizeCompactControls();
  }

  new MutationObserver(localizeCompactControls).observe(
    document.documentElement,
    {
      attributes: true,
      attributeFilter: ["lang"]
    }
  );
})();
/* SACI_COMPACT_CONTROLS_I18N_END */
