(() => {
  const wanted = new URLSearchParams(location.search).get("scenario") || "";
  if (!wanted) return;
  let attempts = 0;
  const timer = setInterval(() => {
    attempts++;
    const select = document.getElementById("scenarioSelect");
    if (!select || !select.options.length) {
      if (attempts > 80) clearInterval(timer);
      return;
    }
    const upper = wanted.toUpperCase();
    const option = [...select.options].find(o => String(o.value).toUpperCase() === upper || String(o.value).toUpperCase().startsWith(upper + "_") || String(o.textContent).toUpperCase().startsWith(upper + " "));
    if (option) {
      select.value = option.value;
      select.dispatchEvent(new Event("change", { bubbles: true }));
    }
    clearInterval(timer);
  }, 100);
})();
