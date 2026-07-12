(() => {
  const $ = (id) => document.getElementById(id);
  const isEn = /\/en\//.test(location.pathname);

  const el = {
    scenario: $("scenarioSelect"),
    q: $("q"),
    type: $("typeFilter"),
    fit: $("fitBtn"),
    reset: $("resetBtn"),
    full: $("fullBtn"),
    cy: $("cy"),
    shell: $("graphShell"),
    status: $("status"),
    declared: $("declaredNodeCount"),
    nodes: $("nodeCount"),
    edges: $("edgeCount"),
    observed: $("observedCount"),
    missing: $("missingCount"),
    saci: $("saciScore"),
    interpretation: $("interpretation"),
    mitre: $("mitrePanel"),
    details: $("details"),
    drawer: $("nodeDetailDrawer"),
    backdrop: $("nodeDetailBackdrop"),
    close: $("nodeDetailClose"),
  };

  let cy = null;
  let manifest = null;
  let current = null;
  let declaredNodes = 0;

  const tacticIds = {
    "Reconnaissance": "TA0043",
    "Resource Development": "TA0042",
    "Initial Access": "TA0001",
    "Execution": "TA0002",
    "Persistence": "TA0003",
    "Privilege Escalation": "TA0004",
    "Defense Evasion": "TA0005",
    "Credential Access": "TA0006",
    "Discovery": "TA0007",
    "Lateral Movement": "TA0008",
    "Collection": "TA0009",
    "Command and Control": "TA0011",
    "Exfiltration": "TA0010",
    "Impact": "TA0040",
  };

  const t = (tr, en) => isEn ? en : tr;
  const safe = (v) => String(v ?? "").replace(/[<>&"]/g, c => ({
    "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;"
  }[c]));

  function setStatus(message, error = false) {
    el.status.textContent = message;
    el.status.className = error ? "graph-status err" : "graph-status";
  }

  async function fetchText(url) {
    const r = await fetch(url, { cache: "no-store" });
    if (!r.ok) throw new Error(`${url} HTTP ${r.status}`);
    return await r.text();
  }

  async function fetchJson(url) {
    return JSON.parse(await fetchText(url));
  }

  function parseCSV(text) {
    const rows = [];
    let row = [], field = "", quoted = false;

    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      const next = text[i + 1];

      if (quoted) {
        if (c === '"' && next === '"') {
          field += '"';
          i++;
        } else if (c === '"') {
          quoted = false;
        } else {
          field += c;
        }
      } else if (c === '"') {
        quoted = true;
      } else if (c === ",") {
        row.push(field);
        field = "";
      } else if (c === "\n") {
        row.push(field.replace(/\r$/, ""));
        rows.push(row);
        row = [];
        field = "";
      } else {
        field += c;
      }
    }
    if (field.length || row.length) {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
    }
    if (!rows.length) return [];

    const headers = rows.shift().map(x => x.trim());
    return rows
      .filter(r => r.some(x => String(x).trim() !== ""))
      .map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
  }

  function datasets(m) {
    if (Array.isArray(m)) return m;
    return m.datasets || m.scenarios || [];
  }

  function label(item) {
    return isEn
      ? (item.label_en || item.label || item.id)
      : (item.label_tr || item.label || item.id);
  }

  function normalizeCyjs(raw) {
    if (Array.isArray(raw)) return raw;
    if (Array.isArray(raw.elements)) return raw.elements;
    if (raw.elements?.nodes && raw.elements?.edges) {
      return [...raw.elements.nodes, ...raw.elements.edges];
    }
    if (raw.nodes && raw.edges) return [...raw.nodes, ...raw.edges];
    return [];
  }

  function isEdge(item) {
    const d = item.data || {};
    return Boolean(d.source && d.target);
  }

  function nodeType(d) {
    return d.type || d.node_type || d.group || d.kind || "node";
  }

  function normalizeElements(items) {
    return items.map((item, i) => {
      const out = item.data ? item : { data: item };
      const d = out.data;
      if (!d.id) d.id = d.source && d.target ? `edge_${i}` : `node_${i}`;
      if (!d.label) d.label = d.name || d.technique_name || d.id;
      return out;
    });
  }

  function addUndeclaredEndpoints(items) {
    const ids = new Set(
      items.filter(x => !isEdge(x)).map(x => String(x.data.id))
    );
    const missing = new Set();

    items.filter(isEdge).forEach(x => {
      const d = x.data;
      if (!ids.has(String(d.source))) missing.add(String(d.source));
      if (!ids.has(String(d.target))) missing.add(String(d.target));
    });

    return items.concat([...missing].map(id => ({
      data: {
        id,
        label: id,
        type: "undeclared_endpoint",
        undeclared: true,
        description: t(
          "Edge tablosunda referans edilen fakat node tablosunda beyan edilmeyen uç.",
          "Endpoint referenced in the edge table but not declared in the node table."
        )
      }
    })));
  }

  function observed(v) {
    return v === 1 || v === "1" || v === true || String(v).toLowerCase() === "true";
  }

  function techniqueUrl(id) {
    const clean = String(id).replace(/^MITRE:/i, "");
    const [base, sub] = clean.split(".");
    return `https://attack.mitre.org/techniques/${base}/${sub ? sub + "/" : ""}`;
  }

  function tacticUrl(name) {
    const id = tacticIds[name.trim()];
    return id ? `https://attack.mitre.org/tactics/${id}/` : "https://attack.mitre.org/tactics/enterprise/";
  }

  async function loadScores(item) {
    const result = {};
    if (!item.scores) return result;
    const rows = parseCSV(await fetchText(item.scores));
    rows.forEach(r => {
      const key = r.metric || r.name || "";
      if (key) result[key] = r.score ?? "";
    });
    return result;
  }

  async function loadMitre(item, elements) {
    if (item.mitre) {
      try {
        return parseCSV(await fetchText(item.mitre));
      } catch (_) {}
    }

    return elements
      .filter(x => !isEdge(x) && nodeType(x.data) === "mitre_technique")
      .map(x => ({
        technique_id: String(x.data.id || "").replace(/^MITRE:/, ""),
        technique_name: x.data.technique_name || x.data.label || x.data.id,
        tactic: x.data.tactic || "Unknown",
        covered: x.data.covered ?? 1,
      }));
  }

  function graphStyle() {
    return [
      {
        selector: "node",
        style: {
          label: "data(label)",
          "font-size": 10,
          "text-wrap": "wrap",
          "text-max-width": 100,
          color: "#e5e7eb",
          "text-outline-width": 2,
          "text-outline-color": "#020617",
          "background-color": "#60a5fa",
          "border-color": "#bfdbfe",
          "border-width": 1,
          width: 31,
          height: 31
        }
      },
      { selector: 'node[type = "asset"]', style: { "background-color": "#38bdf8" } },
      { selector: 'node[type = "log_source"]', style: { "background-color": "#22c55e" } },
      { selector: 'node[type = "control"]', style: { "background-color": "#a78bfa" } },
      { selector: 'node[type = "wazuh_rule"]', style: { "background-color": "#f97316" } },
      { selector: 'node[type = "mitre_technique"]', style: { "background-color": "#facc15", color: "#f8fafc" } },
      { selector: 'node[type = "cti_object"]', style: { "background-color": "#fb7185" } },
      { selector: 'node[type = "metric"]', style: { "background-color": "#14b8a6" } },
      { selector: 'node[type = "platform"]', style: { "background-color": "#0ea5e9", shape: "round-rectangle" } },
      { selector: 'node[type = "score"]', style: { "background-color": "#10b981", shape: "hexagon" } },
      { selector: 'node[type = "integration"]', style: { "background-color": "#8b5cf6", shape: "round-rectangle" } },
      { selector: 'node[type = "reason_code"]', style: { "background-color": "#e879f9" } },
      { selector: 'node[type = "undeclared_endpoint"]', style: { "background-color": "#ef4444", shape: "diamond" } },
      {
        selector: "edge",
        style: {
          "curve-style": "bezier",
          width: 1.2,
          "line-color": "#64748b",
          "target-arrow-shape": "triangle",
          "target-arrow-color": "#64748b",
          opacity: .72,
          label: "data(relationship)",
          "font-size": 7,
          color: "#cbd5e1",
          "text-background-color": "#020617",
          "text-background-opacity": .55,
          "text-background-padding": 2
        }
      },
      {
        selector: 'edge[observed = "0"], edge[observed = 0]',
        style: {
          "line-color": "#fca5a5",
          "target-arrow-color": "#fca5a5",
          "line-style": "dashed",
          opacity: .95
        }
      },
      { selector: ".hidden", style: { display: "none" } },
      {
        selector: ":selected",
        style: {
          "border-width": 4,
          "border-color": "#ffffff",
          "line-color": "#ffffff",
          "target-arrow-color": "#ffffff"
        }
      }
    ];
  }

  function renderMitre(rows) {
    if (!rows.length) {
      el.mitre.innerHTML = `<p>${t("Bu senaryoda MITRE tekniği yok.", "No MITRE techniques are present in this scenario.")}</p>`;
      return;
    }

    const groups = new Map();
    rows.forEach(r => {
      const raw = r.tactic || "Unknown";
      raw.split("/").map(x => x.trim()).filter(Boolean).forEach(tactic => {
        if (!groups.has(tactic)) groups.set(tactic, []);
        groups.get(tactic).push(r);
      });
    });

    el.mitre.innerHTML = `<div class="mitre-groups">${
      [...groups.entries()].map(([tactic, items]) => `
        <section class="mitre-group">
          <h3><a href="${tacticUrl(tactic)}" target="_blank" rel="noopener">${safe(tactic)}</a></h3>
          <div class="tech-list">
            ${items.map(r => {
              const id = r.technique_id || r.technique || "";
              const name = r.technique_name || id;
              const covered = observed(r.covered);
              return `
                <div class="tech-item">
                  <a class="tech-id" href="${techniqueUrl(id)}" target="_blank" rel="noopener">${safe(id)}</a>
                  <a class="tech-name" href="${techniqueUrl(id)}" target="_blank" rel="noopener">${safe(name)}</a>
                  <span class="tech-state ${covered ? "covered" : "missing"}">${covered ? t("kapsanıyor", "covered") : t("eksik", "missing")}</span>
                </div>
              `;
            }).join("")}
          </div>
        </section>
      `).join("")
    }</div>`;
  }

  function renderInterpretation(item, elements, scores, mitreRows) {
    const nodes = elements.filter(x => !isEdge(x));
    const edges = elements.filter(isEdge);
    const obs = edges.filter(x => observed(x.data.observed)).length;
    const miss = edges.length - obs;
    const coveredMitre = mitreRows.filter(x => observed(x.covered)).length;
    const allMitre = mitreRows.length;

    const metrics = ["CWLC", "CAC", "MDC", "CTIC", "TF", "SACI"];
    const metricHtml = metrics.map(k => `
      <div class="score-chip">
        <b>${k}</b>
        <strong>${safe(scores[k] ?? "-")}</strong>
      </div>
    `).join("");

    let explanation;
    if (item.kind === "canonical") {
      explanation = t(
        `Kanonik final görünümünde ${declaredNodes} beyan edilmiş node, ${nodes.length} gösterilen node ve ${edges.length} edge vardır. ${obs} edge observed=1, ${miss} edge observed=0 durumundadır. ${coveredMitre}/${allMitre} MITRE tekniği kapsanır. Bu sonuç tanımlı yayın kapsamındaki kanıt kapanışını gösterir; mutlak güvenlik garantisi değildir.`,
        `The canonical final view contains ${declaredNodes} declared nodes, ${nodes.length} rendered nodes and ${edges.length} edges. ${obs} edges are observed=1 and ${miss} edges are observed=0. ${coveredMitre}/${allMitre} MITRE techniques are covered. This indicates evidence closure within the declared publication scope; it is not an absolute security guarantee.`
      );
    } else if (miss > 0) {
      explanation = t(
        `Seçili tarihsel senaryoda ${miss} eksik ilişki vardır. Graph, eksikliğin asset, log source, control, Wazuh rule, MITRE veya CTI zincirinin hangi noktasında oluştuğunu görünür kılar. MITRE kapsamı ${coveredMitre}/${allMitre}, SACI skoru ${scores.SACI ?? "-"} düzeyindedir.`,
        `The selected historical scenario contains ${miss} missing relationships. The graph shows whether the gap occurs in the asset, log-source, control, Wazuh-rule, MITRE or CTI chain. MITRE coverage is ${coveredMitre}/${allMitre}, and the SACI score is ${scores.SACI ?? "-"}.`
      );
    } else {
      explanation = t(
        `Seçili tarihsel senaryoda missing edge yoktur. ${coveredMitre}/${allMitre} MITRE tekniği kapsanır ve SACI skoru ${scores.SACI ?? "-"} düzeyindedir. Bu görünüm yalnızca ilgili senaryonun tanımlı kapsamını açıklar.`,
        `The selected historical scenario has no missing edges. ${coveredMitre}/${allMitre} MITRE techniques are covered and the SACI score is ${scores.SACI ?? "-"}. This view explains only the declared scope of the selected scenario.`
      );
    }

    el.interpretation.innerHTML = `
      <div class="interpretation-head">
        <div>
          <h3 class="scenario-title">${safe(label(item))}</h3>
          <p class="scenario-subtitle">${safe(item.graph)}</p>
        </div>
        <span class="status-pill ${miss === 0 ? "good" : "warn"}">${miss === 0 ? t("kapalı", "closed") : t("eksik var", "open gaps")}</span>
      </div>
      <div class="score-strip">${metricHtml}</div>
      <div class="interpretation-text">${explanation}</div>
    `;
  }

  function roleDescription(d, edge = false) {
    if (edge) {
      return t(
        "Bu ilişki, seçili senaryoda iki kanıt nesnesi arasındaki görünürlük zincirini temsil eder. observed değeri ilişkinin kanıtla doğrulanıp doğrulanmadığını gösterir.",
        "This relation represents a visibility link between two evidence objects in the selected scenario. The observed value indicates whether the relation was validated by evidence."
      );
    }

    const roles = {
      asset: ["İzlenen varlık; beklenen telemetrinin ve kontrol kapsamının başlangıç noktasıdır.", "Monitored asset; the starting point for expected telemetry and control coverage."],
      log_source: ["Varlıktan üretilmesi ve Wazuh tarafından toplanması beklenen telemetri kanalıdır.", "Telemetry channel expected to be produced by the asset and collected by Wazuh."],
      control: ["Belirli saldırı davranışını görünür kılmak için tanımlanan detection kontrolüdür.", "Detection control defined to make a specific attack behavior visible."],
      wazuh_rule: ["Telemetriyi alert kanıtına dönüştüren Wazuh kuralıdır.", "Wazuh rule that converts telemetry into alert evidence."],
      mitre_technique: ["Detection kanıtının bağlandığı MITRE ATT&CK tekniğidir.", "MITRE ATT&CK technique linked to the detection evidence."],
      cti_object: ["IOC, event veya enrichment bağlamını temsil eden typed CTI nesnesidir.", "Typed CTI object representing IOC, event or enrichment context."],
      platform: ["Kanıt zincirindeki operasyonel platformdur.", "Operational platform in the evidence chain."],
      metric: ["SACI skor bileşenlerinden biridir.", "One of the SACI score components."],
      score: ["Aktif metriklerin normalize edilmiş ağırlıklarıyla üretilen final görünürlük skorudur.", "Final visibility score produced from normalized active metric weights."],
      integration: ["Wazuh ile CTI platformu arasındaki enrichment entegrasyonudur.", "Enrichment integration between Wazuh and the CTI platform."],
      undeclared_endpoint: ["Edge tablosunda referans edilen fakat node tablosunda beyan edilmeyen uçtur.", "Endpoint referenced in the edge table but not declared in the node table."],
    };
    return (roles[nodeType(d)] || [d.description || "Kanıt grafı düğümü.", d.description || "Evidence graph node."])[isEn ? 1 : 0];
  }

  function openDetails(target) {
    const d = target.data();
    const edge = Boolean(d.source && d.target);
    const rows = Object.entries(d).map(([k, v]) => `
      <b>${safe(k)}</b>
      <span>${safe(typeof v === "object" ? JSON.stringify(v) : v)}</span>
    `).join("");

    let mitreLink = "";
    const possibleId = String(d.technique_id || d.id || "").replace(/^MITRE:/, "");
    if (/^T\d{4}(?:\.\d{3})?$/.test(possibleId)) {
      mitreLink = `<p><a href="${techniqueUrl(possibleId)}" target="_blank" rel="noopener">${t("MITRE ATT&CK sayfasını aç", "Open MITRE ATT&CK page")}</a></p>`;
    }

    el.details.innerHTML = `
      <h3>${safe(d.label || d.name || d.id || (edge ? "Edge" : "Node"))}</h3>
      <div class="role-card">${roleDescription(d, edge)}</div>
      ${mitreLink}
      <div class="kv">${rows}</div>
    `;

    el.backdrop.classList.add("open");
    el.drawer.classList.add("open");
    el.drawer.setAttribute("aria-hidden", "false");
  }

  function closeDetails() {
    el.backdrop.classList.remove("open");
    el.drawer.classList.remove("open");
    el.drawer.setAttribute("aria-hidden", "true");
  }

  function fillTypes(elements) {
    const types = [...new Set(
      elements.filter(x => !isEdge(x)).map(x => nodeType(x.data)).filter(Boolean)
    )].sort();
    el.type.innerHTML = `<option value="">${t("Tüm node tipleri", "All node types")}</option>` +
      types.map(x => `<option value="${safe(x)}">${safe(x)}</option>`).join("");
  }

  function applyFilters() {
    if (!cy) return;
    const q = (el.q.value || "").trim().toLowerCase();
    const type = el.type.value;

    cy.batch(() => {
      cy.elements().removeClass("hidden");
      cy.nodes().forEach(n => {
        const d = n.data();
        const hidden = (type && nodeType(d) !== type) || (q && !JSON.stringify(d).toLowerCase().includes(q));
        if (hidden) n.addClass("hidden");
      });
      cy.edges().forEach(e => {
        const hidden = e.source().hasClass("hidden") || e.target().hasClass("hidden");
        const qMiss = q && !JSON.stringify(e.data()).toLowerCase().includes(q)
          && !JSON.stringify(e.source().data()).toLowerCase().includes(q)
          && !JSON.stringify(e.target().data()).toLowerCase().includes(q);
        if (hidden || qMiss) e.addClass("hidden");
      });
    });
  }

  async function loadDataset(item) {
    current = item;
    el.scenario.value = item.id;
    setStatus(t("Graph yükleniyor...", "Loading graph..."));

    const raw = await fetchJson(item.graph);
    let elements = normalizeElements(normalizeCyjs(raw));
    declaredNodes = elements.filter(x => !isEdge(x)).length;
    elements = addUndeclaredEndpoints(elements);

    const [scores, mitreRows] = await Promise.all([
      loadScores(item),
      loadMitre(item, elements),
    ]);

    const nodes = elements.filter(x => !isEdge(x));
    const edges = elements.filter(isEdge);
    const obs = edges.filter(x => observed(x.data.observed)).length;
    const miss = edges.length - obs;

    el.declared.textContent = declaredNodes;
    el.nodes.textContent = nodes.length;
    el.edges.textContent = edges.length;
    el.observed.textContent = obs;
    el.missing.textContent = miss;
    el.saci.textContent = scores.SACI ?? "-";

    fillTypes(elements);
    renderInterpretation(item, elements, scores, mitreRows);
    renderMitre(mitreRows);

    if (!window.cytoscape) throw new Error("Cytoscape could not be loaded.");
    if (cy) cy.destroy();

    cy = cytoscape({
      container: el.cy,
      elements,
      style: graphStyle(),
      wheelSensitivity: .16,
      minZoom: .05,
      maxZoom: 4,
    });

    cy.on("dbltap", "node, edge", ev => openDetails(ev.target));
    cy.on("tap", "node, edge", ev => ev.target.select());

    cy.layout({
      name: "cose",
      animate: false,
      fit: true,
      padding: 70,
      idealEdgeLength: 110,
      nodeRepulsion: 9800,
      gravity: .16,
      numIter: 1300,
    }).run();

    setTimeout(() => cy && cy.resize().fit(undefined, 70), 240);
    setStatus(t("Graph yüklendi. Ayrıntı için node veya edge üzerine çift tıkla.", "Graph loaded. Double-click a node or edge for details."));
  }

  async function init() {
    try {
      manifest = await fetchJson("data/scenarios/manifest.json");
      const items = datasets(manifest);
      if (!items.length) throw new Error("Manifest contains no datasets.");

      el.scenario.innerHTML = items.map(item =>
        `<option value="${safe(item.id)}">${safe(label(item))}</option>`
      ).join("");

      el.scenario.onchange = () => {
        const item = items.find(x => x.id === el.scenario.value);
        if (item) loadDataset(item).catch(e => setStatus(t("Graph yüklenemedi: ", "Graph failed: ") + e.message, true));
      };
      el.q.oninput = applyFilters;
      el.type.onchange = applyFilters;
      el.fit.onclick = () => cy && cy.fit(undefined, 70);
      el.reset.onclick = () => current && loadDataset(current);
      el.full.onclick = () => {
        const expanded = el.shell.dataset.focus === "1";
        el.shell.dataset.focus = expanded ? "0" : "1";
        el.shell.style.height = expanded ? "" : "92vh";
        el.shell.style.maxHeight = expanded ? "" : "none";
        setTimeout(() => cy && cy.resize().fit(undefined, 70), 80);
      };
      el.close.onclick = closeDetails;
      el.backdrop.onclick = closeDetails;

      const defaultId = manifest.default || items[0].id;
      const first = items.find(x => x.id === defaultId) || items[0];
      await loadDataset(first);
    } catch (e) {
      console.error(e);
      setStatus(t("Graph yüklenemedi: ", "Graph failed: ") + e.message, true);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();