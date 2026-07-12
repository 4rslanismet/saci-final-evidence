(function () {
  const FONT_KEY = "saci-font-level";
  const THEME_KEY = "saci-graph-theme";
  const ARCH_ZOOM_KEY = "saci-arch-zoom";

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function isEnglishPage() {
    return /\/en\//.test(window.location.pathname);
  }

  function currentFile() {
    return window.location.pathname.split("/").pop() || "index.html";
  }

  function initLanguageControls() {
    const tr = document.getElementById("langTR");
    const en = document.getElementById("langEN");
    const inEn = isEnglishPage();
    const file = currentFile();

    if (tr) tr.classList.toggle("active", !inEn);
    if (en) en.classList.toggle("active", inEn);

    if (tr) tr.onclick = () => { if (inEn) window.location.href = "../" + file; };
    if (en) en.onclick = () => { if (!inEn) window.location.href = "en/" + file; };
  }

  function initFontControls() {
    let level = Number(localStorage.getItem(FONT_KEY) || "0");
    if (!Number.isFinite(level)) level = 0;

    function apply() {
      level = clamp(level, -2, 2);
      document.documentElement.setAttribute("data-font-level", String(level));
      localStorage.setItem(FONT_KEY, String(level));
    }

    const down = document.getElementById("fontDown");
    const reset = document.getElementById("fontReset");
    const up = document.getElementById("fontUp");

    if (down) down.onclick = () => { level -= 1; apply(); };
    if (reset) reset.onclick = () => { level = 0; apply(); };
    if (up) up.onclick = () => { level += 1; apply(); };
    apply();
  }

  function initThemeControls() {
    const saved = localStorage.getItem(THEME_KEY) || "dim";
    document.documentElement.setAttribute("data-theme", saved);

    document.querySelectorAll("[data-theme-btn]").forEach(btn => {
      const theme = btn.getAttribute("data-theme-btn");
      btn.classList.toggle("active", theme === saved);
      btn.onclick = () => {
        localStorage.setItem(THEME_KEY, theme);
        document.documentElement.setAttribute("data-theme", theme);
        document.querySelectorAll("[data-theme-btn]").forEach(b => {
          b.classList.toggle("active", b.getAttribute("data-theme-btn") === theme);
        });
      };
    });
  }

  function applyArchZoom(mode) {
    const img = document.getElementById("archImage");
    if (!img) return;
    const safe = ["fit", "125", "150"].includes(mode) ? mode : "fit";
    if (safe === "fit") {
      img.style.width = "100%";
      img.style.maxWidth = "100%";
    } else {
      img.style.width = safe + "%";
      img.style.maxWidth = "none";
    }
    localStorage.setItem(ARCH_ZOOM_KEY, safe);
    document.querySelectorAll("[data-zoom]").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-zoom") === safe);
    });
  }

  function initArchZoom() {
    document.querySelectorAll("[data-zoom]").forEach(btn => {
      btn.onclick = () => applyArchZoom(btn.getAttribute("data-zoom"));
    });
    applyArchZoom(localStorage.getItem(ARCH_ZOOM_KEY) || "fit");
  }

  function init() {
    initLanguageControls();
    initFontControls();
    initThemeControls();
    initArchZoom();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();

/* SACI_RESPONSIVE_HEADER_JS_START */
(function () {
  "use strict";

  const COLLAPSE_SAFETY_PX = 52;
  const FORCE_COLLAPSE_BELOW_PX = 980;

  function isEnglishDocument() {
    return (document.documentElement.lang || "").toLowerCase().startsWith("en");
  }

  function cloneNaturalWidth(element) {
    if (!element) return 0;

    const clone = element.cloneNode(true);
    clone.querySelectorAll("[id]").forEach(node => node.removeAttribute("id"));
    clone.querySelectorAll("[aria-controls]").forEach(node => node.removeAttribute("aria-controls"));

    Object.assign(clone.style, {
      position: "fixed",
      left: "-100000px",
      top: "0",
      width: "max-content",
      minWidth: "max-content",
      maxWidth: "none",
      display: "flex",
      flexWrap: "nowrap",
      visibility: "hidden",
      pointerEvents: "none",
      contain: "layout style size"
    });

    document.body.appendChild(clone);
    const width = Math.ceil(clone.getBoundingClientRect().width);
    clone.remove();
    return width;
  }

  function initHeader(top, index) {
    if (!top || top.dataset.saciResponsiveNav === "1") return;

    const inner = top.querySelector(":scope > .top-inner") || top.querySelector(".top-inner");
    const brand = inner && inner.querySelector(":scope > .brand");
    const nav = inner && inner.querySelector(":scope > .nav");
    const actions = inner && inner.querySelector(":scope > .top-actions");

    if (!inner || !brand || !nav || !actions) return;

    top.dataset.saciResponsiveNav = "1";
    inner.classList.add("saci-nav-enhanced");

    const panel = document.createElement("div");
    panel.className = "saci-nav-panel";
    panel.id = `saci-nav-panel-${index}`;

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "nav-toggle";
    toggle.setAttribute("aria-controls", panel.id);
    toggle.setAttribute("aria-expanded", "false");

    const label = isEnglishDocument() ? "Menu" : "Menü";
    const openLabel = isEnglishDocument() ? "Open navigation menu" : "Gezinme menüsünü aç";
    toggle.setAttribute("aria-label", openLabel);
    toggle.innerHTML = `
      <span class="nav-toggle-icon" aria-hidden="true"><span></span></span>
      <span class="nav-toggle-label">${label}</span>
    `;

    inner.insertBefore(toggle, nav);
    panel.appendChild(nav);
    panel.appendChild(actions);
    inner.appendChild(panel);

    let scheduled = 0;

    function setOpen(open) {
      const safeOpen = Boolean(open && top.classList.contains("saci-nav-collapsed"));
      top.classList.toggle("saci-nav-open", safeOpen);
      toggle.setAttribute("aria-expanded", String(safeOpen));
      toggle.setAttribute(
        "aria-label",
        safeOpen
          ? (isEnglishDocument() ? "Close navigation menu" : "Gezinme menüsünü kapat")
          : (isEnglishDocument() ? "Open navigation menu" : "Gezinme menüsünü aç")
      );
      document.documentElement.classList.toggle("saci-nav-lock", safeOpen && window.innerWidth <= 860);
    }

    function evaluate() {
      scheduled = 0;

      const innerWidth = Math.floor(inner.getBoundingClientRect().width);
      const brandWidth = Math.ceil(brand.getBoundingClientRect().width);
      const navWidth = cloneNaturalWidth(nav);
      const actionsWidth = cloneNaturalWidth(actions);
      const requiredWidth = brandWidth + navWidth + actionsWidth + COLLAPSE_SAFETY_PX;
      const collapse = window.innerWidth <= FORCE_COLLAPSE_BELOW_PX || requiredWidth > innerWidth;

      top.classList.toggle("saci-nav-collapsed", collapse);

      if (!collapse) {
        setOpen(false);
      }
    }

    function scheduleEvaluate() {
      if (scheduled) cancelAnimationFrame(scheduled);
      scheduled = requestAnimationFrame(evaluate);
    }

    toggle.addEventListener("click", () => {
      setOpen(!top.classList.contains("saci-nav-open"));
    });

    nav.addEventListener("click", event => {
      if (event.target.closest("a")) setOpen(false);
    });

    document.addEventListener("pointerdown", event => {
      if (top.classList.contains("saci-nav-open") && !top.contains(event.target)) {
        setOpen(false);
      }
    });

    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && top.classList.contains("saci-nav-open")) {
        setOpen(false);
        toggle.focus();
      }
    });

    window.addEventListener("resize", scheduleEvaluate, { passive: true });
    window.addEventListener("orientationchange", scheduleEvaluate, { passive: true });

    if ("ResizeObserver" in window) {
      const observer = new ResizeObserver(scheduleEvaluate);
      observer.observe(inner);
      observer.observe(brand);
      observer.observe(nav);
      observer.observe(actions);
    }

    const attrObserver = new MutationObserver(scheduleEvaluate);
    attrObserver.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-font-level", "data-theme", "lang"]
    });

    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(scheduleEvaluate).catch(() => {});
    }

    scheduleEvaluate();
  }

  function initResponsiveHeaders() {
    document.querySelectorAll(".top").forEach(initHeader);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initResponsiveHeaders, { once: true });
  } else {
    initResponsiveHeaders();
  }
})();
/* SACI_RESPONSIVE_HEADER_JS_END */
