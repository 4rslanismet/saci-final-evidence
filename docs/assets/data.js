
(() => {
  const $ = id => document.getElementById(id);
  const en = (document.documentElement.lang || "").toLowerCase().startsWith("en");
  const pageRoot = en ? "../" : "";
  const resolvePath = path => `${pageRoot}${String(path).replace(/^\.\//, "")}`;

  const text = (tr, enValue) => en ? enValue : tr;
  const esc = value => String(value ?? "").replace(/[<>&"]/g, ch => ({
    "<": "&lt;",
    ">": "&gt;",
    "&": "&amp;",
    '"': "&quot;"
  }[ch]));

  const groupLabels = {
    results: ["Skor sonuçları", "Score results"],
    graph: ["Graph verileri", "Graph data"],
    coverage: ["Kapsama ve durum kanıtları", "Coverage and status evidence"],
    explainability: ["Açıklanabilirlik çıktıları", "Explainability outputs"],
    audit: ["Doğrulama ve audit", "Validation and audit"]
  };

  async function init() {
    try {
      const response = await fetch(resolvePath("data/final/manifest.json"), {
        cache: "no-store"
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const manifest = await response.json();
      const summary = manifest.summary;

      $("fileCount").textContent = summary.files;
      $("finalScore").textContent = summary.saci;
      $("relationClosure").textContent =
        `${summary.observed_edges}/${summary.edges}`;
      $("activeReasons").textContent = summary.active_reason_codes;

      const bundle = $("downloadBundle");
      bundle.href = resolvePath(manifest.bundle.path);
      bundle.querySelector("span").textContent =
        text("Tüm dosyaları indir", "Download all files") +
        ` · ${manifest.bundle.size}`;

      $("checksumLink").href = resolvePath("data/final/SHA256SUMS.txt");

      const groups = [
        "results",
        "graph",
        "coverage",
        "explainability",
        "audit"
      ];

      const rows = [];

      for (const group of groups) {
        const files = manifest.files.filter(item => item.group === group);
        if (!files.length) continue;

        const label = groupLabels[group];
        rows.push(`
          <tr class="data-group-row">
            <td colspan="6">${esc(en ? label[1] : label[0])}</td>
          </tr>
        `);

        for (const file of files) {
          const description = en
            ? file.description_en
            : file.description_tr;

          const records = en
            ? file.records_en
            : file.records_tr;

          rows.push(`
            <tr>
              <td>
                <div class="data-file-name">
                  <span class="data-format">${esc(file.format)}</span>
                  <strong>${esc(file.name)}</strong>
                </div>
              </td>
              <td class="data-description">${esc(description)}</td>
              <td class="data-records">${esc(records)}</td>
              <td class="data-size">${esc(file.size)}</td>
              <td class="data-hash">
                <code title="${esc(file.sha256)}">${esc(file.sha256.slice(0, 12))}…</code>
              </td>
              <td>
                <a class="data-download"
                   href="${esc(resolvePath(file.path))}"
                   download>
                  ${text("İndir", "Download")}
                </a>
              </td>
            </tr>
          `);
        }
      }

      $("dataRows").innerHTML = rows.join("");

      $("auditEdges").textContent =
        `${summary.observed_edges}/${summary.edges}`;

      $("auditLogs").textContent =
        `${summary.asset_log_pairs}/${summary.asset_log_pairs}`;

      $("auditControls").textContent =
        summary.enabled_controls;

      $("auditMitreCti").textContent =
        `${summary.mitre} · ${summary.ctic}`;

      $("endpointList").textContent =
        summary.undeclared_endpoints.join(", ");

      $("loadingState").hidden = true;
      $("dataContent").hidden = false;

    } catch (error) {
      console.error(error);
      $("loadingState").textContent = text(
        `Veri manifesti yüklenemedi: ${error.message}`,
        `Data manifest could not be loaded: ${error.message}`
      );
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
