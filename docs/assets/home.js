
(function () {
  function initThemeSwitcher() {
    const saved = localStorage.getItem("saci-graph-theme") || "dim";
    document.documentElement.setAttribute("data-theme", saved);

    document.querySelectorAll("[data-theme-btn]").forEach(btn => {
      const t = btn.getAttribute("data-theme-btn");
      btn.classList.toggle("active", t === saved);

      btn.addEventListener("click", () => {
        localStorage.setItem("saci-graph-theme", t);
        document.documentElement.setAttribute("data-theme", t);

        document.querySelectorAll("[data-theme-btn]").forEach(b => {
          b.classList.toggle("active", b.getAttribute("data-theme-btn") === t);
        });
      });
    });
  }

  function initFontControls() {
    let scale = Number(localStorage.getItem("saci-font-scale") || "1");
    if (Number.isNaN(scale)) scale = 1;

    function apply() {
      scale = Math.max(0.9, Math.min(1.35, scale));
      document.documentElement.style.setProperty("--saci-font-scale", String(scale));
      localStorage.setItem("saci-font-scale", String(scale));
    }

    const down = document.getElementById("fontDown");
    const up = document.getElementById("fontUp");
    const reset = document.getElementById("fontReset");

    if (down) down.onclick = () => { scale -= 0.05; apply(); };
    if (up) up.onclick = () => { scale += 0.05; apply(); };
    if (reset) reset.onclick = () => { scale = 1; apply(); };

    apply();
  }

  document.addEventListener("DOMContentLoaded", () => {
    initThemeSwitcher();
    initFontControls();
  });
})();
