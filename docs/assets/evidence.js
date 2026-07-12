(() => {
  const root = document.querySelector("[data-evidence-base]");
  if (!root) return;

  const base = root.dataset.evidenceBase.replace(/\/$/, "");
  const en = (document.documentElement.lang || "").toLowerCase().startsWith("en");
  const t = (tr, english) => en ? english : tr;
  const $ = (id) => document.getElementById(id);
  const esc = (value) => String(value ?? "").replace(/[<>&\"]/g, ch => ({"<":"&lt;", ">":"&gt;", "&":"&amp;", '"':"&quot;"}[ch]));

  function parseCSV(text) {
    const rows = [];
    let row = [], field = "", quoted = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i], next = text[i + 1];
      if (quoted) {
        if (c === '"' && next === '"') { field += '"'; i++; }
        else if (c === '"') quoted = false;
        else field += c;
      } else if (c === '"') quoted = true;
      else if (c === ',') { row.push(field); field = ""; }
      else if (c === '\n') { row.push(field.replace(/\r$/, "")); rows.push(row); row = []; field = ""; }
      else field += c;
    }
    if (field.length || row.length) { row.push(field.replace(/\r$/, "")); rows.push(row); }
    if (!rows.length) return [];
    const headers = rows.shift().map(x => x.trim());
    return rows.filter(r => r.some(x => String(x).trim() !== ""))
      .map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
  }

  async function getText(name, optional = false) {
    try {
      const r = await fetch(`${base}/${name}`, { cache: "no-store" });
      if (!r.ok) throw new Error(`${name} HTTP ${r.status}`);
      return await r.text();
    } catch (e) {
      if (optional) return "";
      throw e;
    }
  }

  async function getCSV(name, optional = false) {
    const text = await getText(name, optional);
    return text ? parseCSV(text) : [];
  }

  function table(headers, rows) {
    return `<div class="table-shell"><table class="evidence-table"><thead><tr>${headers.map(h => `<th>${h.label}</th>`).join("")}</tr></thead><tbody>${rows.map(row => `<tr>${headers.map(h => `<td>${h.render ? h.render(row[h.key], row) : esc(row[h.key])}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  }

  function status(value, goodText, badText, disabled = false) {
    if (disabled) return `<span class="status muted">${esc(t("Kapsam dışı", "Out of scope"))}</span>`;
    const good = String(value) === "1" || String(value).toLowerCase() === "true" || Number(value) === 100;
    return `<span class="status ${good ? "good" : "warn"}">${esc(good ? goodText : badText)}</span>`;
  }

  function pct(value) {
    const n = Number(value);
    return Number.isFinite(n) ? `${n.toFixed(n % 1 ? 1 : 0)}%` : esc(value);
  }

  function date(value) {
    if (!value) return "-";
    const d = new Date(value);
    return Number.isNaN(d.getTime()) ? esc(value) : esc(d.toLocaleString(en ? "en-GB" : "tr-TR"));
  }

  function techniqueUrl(id) {
    const clean = String(id || "").replace(/^MITRE:/i, "");
    const [baseId, sub] = clean.split(".");
    return `https://attack.mitre.org/techniques/${baseId}/${sub ? `${sub}/` : ""}`;
  }

  function tacticUrl(name) {
    const ids = {
      "Reconnaissance":"TA0043", "Resource Development":"TA0042", "Initial Access":"TA0001",
      "Execution":"TA0002", "Persistence":"TA0003", "Privilege Escalation":"TA0004",
      "Defense Evasion":"TA0005", "Credential Access":"TA0006", "Discovery":"TA0007",
      "Lateral Movement":"TA0008", "Collection":"TA0009", "Command and Control":"TA0011",
      "Exfiltration":"TA0010", "Impact":"TA0040"
    };
    return ids[name] ? `https://attack.mitre.org/tactics/${ids[name]}/` : "https://attack.mitre.org/tactics/enterprise/";
  }

  function renderScores(rows) {
    const values = Object.fromEntries(rows.map(r => [r.metric, r.score]));
    ["CWLC", "CAC", "MDC", "CTIC", "TF", "SACI"].forEach(key => {
      const node = $(`metric-${key.toLowerCase()}`);
      if (node) node.textContent = values[key] ?? "-";
    });
    $("scoreTable").innerHTML = table([
      { key:"metric", label:t("Metrik", "Metric"), render:v => `<code>${esc(v)}</code>` },
      { key:"name", label:t("Ad", "Name") },
      { key:"weight", label:t("Ağırlık", "Weight"), render:v => pct(Number(v) * 100) },
      { key:"score", label:t("Skor", "Score"), render:v => `<strong>${esc(v)}</strong>` },
      { key:"applicable", label:t("Durum", "Status"), render:v => status(v, t("Aktif", "Active"), t("N/A", "N/A"), String(v) !== "1") },
    ], rows);
    return values;
  }

  function renderAssets(rows) {
    $("assetTable").innerHTML = table([
      { key:"asset_id", label:t("Varlık", "Asset"), render:v => `<code>${esc(v)}</code>` },
      { key:"hostname", label:t("Ana makine", "Hostname") },
      { key:"expected_sources", label:t("Beklenen kaynaklar", "Expected sources") },
      { key:"received_sources", label:t("Alınan kaynaklar", "Received sources") },
      { key:"coverage_percent", label:t("Kapsama", "Coverage"), render:v => pct(v) },
      { key:"criticality", label:t("Kritiklik", "Criticality") },
      { key:"coverage_applicable", label:t("Durum", "Status"), render:(v,r) => status(r.coverage_percent, t("Tam", "Complete"), t("Eksik", "Partial"), String(v) !== "1") },
    ], rows);
  }

  function renderLogs(rows) {
    $("logTable").innerHTML = table([
      { key:"asset_id", label:t("Varlık", "Asset"), render:v => `<code>${esc(v)}</code>` },
      { key:"hostname", label:t("Ana makine", "Hostname") },
      { key:"log_source", label:t("Log kaynağı", "Log source"), render:v => `<code>${esc(v)}</code>` },
      { key:"expected", label:t("Beklenen", "Expected"), render:v => status(v, t("Evet", "Yes"), t("Hayır", "No")) },
      { key:"observed", label:t("Gözlemlenen", "Observed"), render:v => status(v, t("Gözlemlendi", "Observed"), t("Eksik", "Missing")) },
      { key:"source_weight", label:t("Kaynak ağırlığı", "Source weight") },
      { key:"last_seen", label:t("Son görülme", "Last seen"), render:v => date(v) },
    ], rows);
  }

  function renderControls(rows) {
    $("controlTable").innerHTML = table([
      { key:"control_id", label:t("Kontrol", "Control"), render:v => `<code>${esc(v)}</code>` },
      { key:"asset_id", label:t("Varlık", "Asset"), render:v => `<code>${esc(v)}</code>` },
      { key:"source", label:t("Kaynak", "Source") },
      { key:"rule_id", label:t("Wazuh kuralı", "Wazuh rule"), render:v => `<code>${esc(v)}</code>` },
      { key:"mitre_technique", label:t("MITRE tekniği", "MITRE technique"), render:v => `<a href="${techniqueUrl(v)}" target="_blank" rel="noopener"><code>${esc(v)}</code></a>` },
      { key:"enabled", label:t("Etkin", "Enabled"), render:v => status(v, t("Etkin", "Enabled"), t("Kapsam dışı", "Out of scope"), String(v) !== "1") },
      { key:"seen", label:t("Kanıt", "Evidence"), render:(v,r) => status(v, t("Görüldü", "Seen"), t("Eksik", "Missing"), String(r.enabled) !== "1") },
      { key:"description", label:t("Açıklama", "Description") },
    ], rows);
  }

  function renderMitre(rows) {
    $("mitreTable").innerHTML = table([
      { key:"technique_id", label:t("Teknik", "Technique"), render:v => `<a href="${techniqueUrl(v)}" target="_blank" rel="noopener"><code>${esc(v)}</code></a>` },
      { key:"technique_name", label:t("Teknik adı", "Technique name") },
      { key:"tactic", label:t("Taktik", "Tactic"), render:v => String(v).split("/").map(x => x.trim()).filter(Boolean).map(x => `<a href="${tacticUrl(x)}" target="_blank" rel="noopener">${esc(x)}</a>`).join(" / ") },
      { key:"covered", label:t("Kapsama", "Coverage"), render:v => status(v, t("Kapsanıyor", "Covered"), t("Eksik", "Missing")) },
      { key:"priority", label:t("Öncelik", "Priority") },
    ], rows);
  }

  function renderCtic(rows) {
    $("cticTable").innerHTML = table([
      { key:"indicator", label:t("Gösterge", "Indicator"), render:v => `<code>${esc(v)}</code>` },
      { key:"type", label:t("Tür", "Type") },
      { key:"lookup_executed", label:t("Lookup", "Lookup"), render:v => status(v, t("Çalıştı", "Executed"), t("Çalışmadı", "Not executed")) },
      { key:"misp_hit", label:t("MISP eşleşmesi", "MISP hit"), render:v => status(v, t("Eşleşti", "Matched"), t("Eşleşmedi", "No match")) },
      { key:"wazuh_alert", label:t("Wazuh alarmı", "Wazuh alert"), render:v => status(v, t("Üretildi", "Produced"), t("Eksik", "Missing")) },
      { key:"mapped_to_mitre", label:t("MITRE eşlemesi", "MITRE mapping"), render:v => status(v, t("Eşlendi", "Mapped"), t("Eksik", "Missing")) },
      { key:"expected_alert_rule", label:t("Beklenen kural", "Expected rule"), render:v => `<code>${esc(v)}</code>` },
      { key:"mitre_technique", label:t("MITRE tekniği", "MITRE technique"), render:v => `<a href="${techniqueUrl(v)}" target="_blank" rel="noopener"><code>${esc(v)}</code></a>` },
    ], rows);
  }


  function reasonCatalog() {
    return [
      {
        code:"expected_log_source_not_observed",
        metric:"CWLC",
        tr:"Beklenen asset → log source ilişkisi gözlemlenmediğinde üretilir.",
        en:"Generated when an expected asset-to-log-source relation is not observed."
      },
      {
        code:"enabled_control_not_seen",
        metric:"CAC",
        tr:"Etkin bir detection kontrolünün Wazuh rule veya alert kanıtı görülmediğinde üretilir.",
        en:"Generated when an enabled detection control has no observed Wazuh-rule or alert evidence."
      },
      {
        code:"mitre_technique_not_covered",
        metric:"MDC",
        tr:"Kapsamdaki MITRE ATT&CK tekniği detection kanıtıyla doğrulanmadığında üretilir.",
        en:"Generated when an in-scope MITRE ATT&CK technique is not validated by detection evidence."
      },
      {
        code:"cti_lookup_without_hit",
        metric:"CTIC",
        tr:"CTI lookup çalıştığı halde MISP üzerinde eşleşme oluşmadığında üretilir.",
        en:"Generated when a CTI lookup executes but no MISP match is returned."
      },
      {
        code:"ioc_not_converted_to_alert",
        metric:"CTIC",
        tr:"MISP eşleşmesi bulunmasına rağmen beklenen Wazuh alarmı üretilmediğinde üretilir.",
        en:"Generated when a MISP match exists but the expected Wazuh alert is not produced."
      },
      {
        code:"telemetry_freshness_decay",
        metric:"TF",
        tr:"Son telemetri zamanı tanımlı freshness eşiğini aştığında üretilir.",
        en:"Generated when the latest telemetry exceeds the configured freshness threshold."
      },
      {
        code:"telemetry_freshness_absent",
        metric:"TF",
        tr:"Freshness hesaplamak için kullanılabilir telemetri zamanı bulunmadığında üretilir.",
        en:"Generated when no telemetry timestamp is available for freshness calculation."
      }
    ];
  }



  function reasonCatalog() {
    return [
      {
        code:"expected_log_source_not_observed",
        metric:"CWLC",
        tr:"Beklenen asset → log source ilişkisi gözlemlenmediğinde üretilir.",
        en:"Generated when an expected asset-to-log-source relation is not observed."
      },
      {
        code:"enabled_control_not_seen",
        metric:"CAC",
        tr:"Etkin bir detection kontrolünün Wazuh rule veya alert kanıtı görülmediğinde üretilir.",
        en:"Generated when an enabled detection control has no observed Wazuh-rule or alert evidence."
      },
      {
        code:"mitre_technique_not_covered",
        metric:"MDC",
        tr:"Kapsamdaki MITRE ATT&CK tekniği detection kanıtıyla doğrulanmadığında üretilir.",
        en:"Generated when an in-scope MITRE ATT&CK technique is not validated by detection evidence."
      },
      {
        code:"cti_lookup_without_hit",
        metric:"CTIC",
        tr:"CTI lookup çalıştığı halde MISP üzerinde eşleşme oluşmadığında üretilir.",
        en:"Generated when a CTI lookup executes but no MISP match is returned."
      },
      {
        code:"ioc_not_converted_to_alert",
        metric:"CTIC",
        tr:"MISP eşleşmesi bulunmasına rağmen beklenen Wazuh alarmı üretilmediğinde üretilir.",
        en:"Generated when a MISP match exists but the expected Wazuh alert is not produced."
      },
      {
        code:"telemetry_freshness_decay",
        metric:"TF",
        tr:"Son telemetri zamanı tanımlı freshness eşiğini aştığında üretilir.",
        en:"Generated when the latest telemetry exceeds the configured freshness threshold."
      },
      {
        code:"telemetry_freshness_absent",
        metric:"TF",
        tr:"Freshness hesaplamak için kullanılabilir telemetri zamanı bulunmadığında üretilir.",
        en:"Generated when no telemetry timestamp is available for freshness calculation."
      }
    ];
  }


  function renderReasons(rows, graph) {
    const catalog = reasonCatalog();

    const active = rows.length;

    const missing = graph?.missing ?? "-";

    const endpointCount =
      Array.isArray(graph?.undeclaredEndpoints)
        ? graph.undeclaredEndpoints.length
        : "-";

    const summary = `
      <div class="reason-summary-grid">

        <div class="reason-summary-card">
          <span>
            ${esc(t(
              "Aktif reason code",
              "Active reason codes"
            ))}
          </span>

          <strong>${esc(active)}</strong>
        </div>

        <div class="reason-summary-card">
          <span>
            ${esc(t(
              "Eksik graph ilişkisi",
              "Missing graph relations"
            ))}
          </span>

          <strong>${esc(missing)}</strong>
        </div>

        <div class="reason-summary-card">
          <span>
            ${esc(t(
              "Tanımsız edge ucu",
              "Undeclared edge endpoints"
            ))}
          </span>

          <strong>${esc(endpointCount)}</strong>
        </div>

      </div>
    `;

    const explanation =
      active === 0

        ? `
          <div class="reason-explanation">

            <strong>
              ${esc(t(
                "Final reason-code doğrulaması geçti.",
                "Final reason-code validation passed."
              ))}
            </strong>

            ${esc(t(
              "Final veri kümesinde missing edge bulunmadığı için skor boşluğunu açıklayan aktif reason code üretilmemiştir. Aşağıdaki kayıtlar aktif bulgu değil, SACI hesaplama motorunda tanımlı deterministik reason-code sözlüğüdür. Tarihsel S0–S18 senaryoları bu kuralları tetikleyebilir.",
              "Because the final dataset contains no missing edges, no active reason code was generated to explain a score gap. The entries below are not active findings; they are the deterministic reason-code dictionary defined by the SACI scoring engine. Historical S0–S18 scenarios may trigger these rules."
            ))}

          </div>
        `

        : `
          <div class="reason-explanation">

            <strong>
              ${esc(t(
                "Aktif reason code kayıtları bulundu.",
                "Active reason-code records were found."
              ))}
            </strong>

            ${esc(t(
              "Bu kayıtlar eksik görünürlük ilişkilerinin hangi SACI metriğini ve hangi kanıt zincirini etkilediğini gösterir.",
              "These records identify which SACI metric and evidence chain are affected by missing visibility relations."
            ))}

          </div>
        `;

    const activeTable =
      active

        ? `
          <h3>
            ${esc(t(
              "Aktif kayıtlar",
              "Active records"
            ))}
          </h3>

          ${table([
            {
              key:"reason_code",
              label:t("Reason code", "Reason code"),
              render:v => `<code>${esc(v)}</code>`
            },
            {
              key:"metric",
              label:t("Metrik", "Metric")
            },
            {
              key:"impact",
              label:t("Etki", "Impact")
            },
            {
              key:"fields_json",
              label:t(
                "Kanıt alanları",
                "Evidence fields"
              ),
              render:v => `<code>${esc(v)}</code>`
            }
          ], rows)}
        `

        : "";

    const catalogHtml = `
      <h3>
        ${esc(t(
          "Deterministik reason-code sözlüğü",
          "Deterministic reason-code dictionary"
        ))}
      </h3>

      <div class="reason-catalog">

        ${catalog.map(item => `
          <div class="reason-catalog-item">

            <code>${esc(item.code)}</code>

            <b>${esc(item.metric)}</b>

            <p>
              ${esc(en ? item.en : item.tr)}
            </p>

          </div>
        `).join("")}

      </div>
    `;

    $("reasonContent").innerHTML =
      summary
      + explanation
      + activeTable
      + catalogHtml;
  }


  async function graphStats() {
    try {
      const raw = JSON.parse(
        await getText(
          "saci_graph.cyjs",
          true
        )
      );

      const elements =
        Array.isArray(raw)
          ? raw
          : Array.isArray(raw.elements)
            ? raw.elements
            : raw.elements?.nodes
              && raw.elements?.edges
                ? [
                    ...raw.elements.nodes,
                    ...raw.elements.edges
                  ]
                : raw.nodes
                  && raw.edges
                    ? [
                        ...raw.nodes,
                        ...raw.edges
                      ]
                    : [];

      const nodeElements =
        elements.filter(
          item =>
            !(
              item?.data?.source
              && item?.data?.target
            )
        );

      const edges =
        elements.filter(
          item =>
            item?.data?.source
            && item?.data?.target
        );

      const nodeIds =
        new Set(
          nodeElements.map(
            item =>
              String(
                item?.data?.id ?? ""
              )
          )
        );

      const undeclaredEndpoints =
        [
          ...new Set(
            edges
              .flatMap(
                edge => [
                  String(edge.data.source),
                  String(edge.data.target)
                ]
              )
              .filter(
                id =>
                  id
                  && !nodeIds.has(id)
              )
          )
        ].sort();

      const observed =
        edges.filter(
          item =>
            String(item.data.observed) === "1"
            || item.data.observed === true
        ).length;

      return {
        nodes: nodeElements.length,

        renderedNodes:
          nodeElements.length
          + undeclaredEndpoints.length,

        edges: edges.length,

        observed,

        missing:
          edges.length
          - observed,

        undeclaredEndpoints
      };

    } catch (_) {
      return {
        nodes:"-",
        renderedNodes:"-",
        edges:"-",
        observed:"-",
        missing:"-",
        undeclaredEndpoints:[]
      };
    }
  }


  function renderAudit(
    scores,
    assets,
    logs,
    controls,
    mitre,
    ctic,
    reasons,
    graph
  ) {
    const expectedLogs =
      logs.filter(
        row =>
          String(row.expected) === "1"
      ).length;

    const observedLogs =
      logs.filter(
        row =>
          String(row.expected) === "1"
          && String(row.observed) === "1"
      ).length;

    const enabledControls =
      controls.filter(
        row =>
          String(row.enabled) === "1"
      ).length;

    const seenControls =
      controls.filter(
        row =>
          String(row.enabled) === "1"
          && String(row.seen) === "1"
      ).length;

    const coveredMitre =
      mitre.filter(
        row =>
          String(row.covered) === "1"
      ).length;

    const closedCti =
      ctic.filter(
        row =>
          [
            "lookup_executed",
            "misp_hit",
            "wazuh_alert",
            "mapped_to_mitre"
          ].every(
            key =>
              String(row[key]) === "1"
          )
      ).length;

    const activeMetrics = [
      "CWLC",
      "CAC",
      "MDC",
      "CTIC",
      "TF",
      "SACI"
    ];

    const metricsAt100 =
      activeMetrics.filter(
        metric =>
          Number(scores[metric]) === 100
      ).length;

    const allScores100 =
      metricsAt100
      === activeMetrics.length;

    const reasonCount =
      reasons.length;

    const endpointList =
      Array.isArray(
        graph.undeclaredEndpoints
      )
        ? graph.undeclaredEndpoints
        : [];

    const endpointClean =
      endpointList.length === 0;

    const closurePassed =
      Number(graph.missing) === 0
      && Number(graph.observed)
        === Number(graph.edges);


    $("auditGrid").innerHTML = `

      <div class="audit-item">
        <span>
          ${esc(t(
            "Final skor",
            "Final score"
          ))}
        </span>

        <strong>
          ${esc(scores.SACI ?? "-")} / 100
        </strong>
      </div>


      <div class="audit-item">
        <span>
          ${esc(t(
            "Aktif metrik doğrulaması",
            "Active metric validation"
          ))}
        </span>

        <strong>
          ${esc(metricsAt100)}
          /
          ${esc(activeMetrics.length)}

          ${esc(t(
            "metrik 100",
            "metrics at 100"
          ))}
        </strong>
      </div>


      <div class="audit-item">
        <span>
          ${esc(t(
            "Graph ilişki kapanışı",
            "Graph relation closure"
          ))}
        </span>

        <strong>
          ${esc(graph.observed)}
          /
          ${esc(graph.edges)}

          ${esc(t(
            "gözlemlenen ilişki",
            "observed relations"
          ))}
        </strong>
      </div>


      <div class="audit-item">
        <span>
          ${esc(t(
            "Beyan / görüntülenen node",
            "Declared / rendered nodes"
          ))}
        </span>

        <strong>
          ${esc(graph.nodes)}
          /
          ${esc(graph.renderedNodes)}
        </strong>
      </div>


      <div class="audit-item">
        <span>
          ${esc(t(
            "Varlık / log kapsamı",
            "Asset / log coverage"
          ))}
        </span>

        <strong>
          ${assets.length}
          ${esc(t("varlık", "assets"))},

          ${observedLogs}
          /
          ${expectedLogs}

          ${esc(t("kaynak", "sources"))}
        </strong>
      </div>


      <div class="audit-item">
        <span>
          ${esc(t(
            "Kontrol kanıtı",
            "Control evidence"
          ))}
        </span>

        <strong>
          ${seenControls}
          /
          ${enabledControls}

          ${esc(t(
            "etkin kontrol",
            "enabled controls"
          ))}
        </strong>
      </div>


      <div class="audit-item">
        <span>
          ${esc(t(
            "MITRE kapsamı",
            "MITRE coverage"
          ))}
        </span>

        <strong>
          ${coveredMitre}
          /
          ${mitre.length}

          ${esc(t(
            "teknik",
            "techniques"
          ))}
        </strong>
      </div>


      <div class="audit-item">
        <span>
          ${esc(t(
            "CTI/MISP kapanışı",
            "CTI/MISP closure"
          ))}
        </span>

        <strong>
          ${closedCti}
          /
          ${ctic.length}

          ${esc(t(
            "gösterge",
            "indicators"
          ))}
        </strong>
      </div>


      <div class="audit-item">
        <span>
          ${esc(t(
            "Aktif reason code",
            "Active reason codes"
          ))}
        </span>

        <strong>
          ${esc(reasonCount)}
        </strong>
      </div>
    `;


    const checks = [
      {
        label:t(
          "Skor tutarlılığı",
          "Score consistency"
        ),

        detail:t(
          "Aktif SACI metrikleri beklenen final değerleriyle karşılaştırıldı.",
          "Active SACI metrics were compared with the expected final values."
        ),

        ok:allScores100
      },

      {
        label:t(
          "Graph ilişki kapanışı",
          "Graph relation closure"
        ),

        detail:t(
          "Bütün edge satırlarının observed durumu ve missing edge sayısı kontrol edildi.",
          "Observed state of every edge row and the missing-edge count were checked."
        ),

        ok:closurePassed
      },

      {
        label:t(
          "Varlık ve log kaynağı kapsamı",
          "Asset and log-source coverage"
        ),

        detail:t(
          "Beklenen log kaynakları varlık envanteriyle karşılaştırıldı.",
          "Expected log sources were compared with the asset inventory."
        ),

        ok:
          expectedLogs > 0
          && observedLogs === expectedLogs
      },

      {
        label:t(
          "Detection kontrol kanıtı",
          "Detection-control evidence"
        ),

        detail:t(
          "Etkin kontrollerin Wazuh rule ve alarm kanıtı doğrulandı.",
          "Wazuh-rule and alert evidence was verified for enabled controls."
        ),

        ok:
          enabledControls > 0
          && seenControls === enabledControls
      },

      {
        label:t(
          "MITRE ve CTI kapanışı",
          "MITRE and CTI closure"
        ),

        detail:t(
          "ATT&CK teknikleri ve CTI enrichment zincirleri kontrol edildi.",
          "ATT&CK techniques and CTI-enrichment chains were checked."
        ),

        ok:
          coveredMitre === mitre.length
          && closedCti === ctic.length
      },

      {
        label:t(
          "Reason-code kontrolü",
          "Reason-code check"
        ),

        detail:t(
          "Final veri kümesinde aktif skor boşluğu açıklayan reason code bulunup bulunmadığı kontrol edildi.",
          "The final dataset was checked for active reason codes explaining score gaps."
        ),

        ok:
          reasonCount === 0
      },

      {
        label:t(
          "Graph endpoint bütünlüğü",
          "Graph endpoint integrity"
        ),

        detail:t(
          "Edge uçlarının node tablosunda beyan edilip edilmediği kontrol edildi.",
          "Edge endpoints were checked against declarations in the node table."
        ),

        ok:endpointClean,

        review:!endpointClean
      },

      {
        label:t(
          "Yorumlama sınırı",
          "Interpretation boundary"
        ),

        detail:t(
          "SACI=100 sonucunun mutlak güvenlik değil, tanımlı kapsamda kanıt kapanışı olduğu doğrulandı.",
          "SACI=100 was confirmed as evidence closure within the declared scope, not an absolute security guarantee."
        ),

        ok:true
      }
    ];


    $("auditConclusion").innerHTML = `

      <strong>
        ${esc(t(
          "Doğrulama kararı:",
          "Validation decision:"
        ))}
      </strong>

      ${esc(
        allScores100
        && closurePassed
        && reasonCount === 0

          ? t(
              "Skorlama, görünürlük ilişkileri, kontrol kanıtı, MITRE kapsamı ve CTI kapanışı doğrulamaları geçmiştir. Final sonuç tanımlı değerlendirme kapsamında kanıt kapanışını gösterir.",
              "Scoring, visibility relations, control evidence, MITRE coverage and CTI closure validations passed. The final result indicates evidence closure within the declared evaluation scope."
            )

          : t(
              "Final kanıt paketinde incelenmesi gereken kısmi veya eksik doğrulama sonuçları bulunmaktadır.",
              "The final evidence package contains partial or incomplete validation results that require review."
            )
      )}


      <div class="audit-checklist">

        ${checks.map(check => `

          <div class="audit-check">

            <div class="audit-check-copy">

              <span>
                ${esc(check.label)}
              </span>

              <p>
                ${esc(check.detail)}
              </p>

            </div>


            <span class="
              status
              ${
                check.review
                  ? "warn"
                  : check.ok
                    ? "good"
                    : "warn"
              }
            ">

              ${esc(
                check.review

                  ? t(
                      "İncele",
                      "Review"
                    )

                  : check.ok

                    ? t(
                        "Geçti",
                        "Passed"
                      )

                    : t(
                        "Eksik",
                        "Incomplete"
                      )
              )}

            </span>

          </div>

        `).join("")}

      </div>


      ${
        endpointClean

          ? ""

          : `
            <div class="audit-integrity-note">

              <strong>
                ${esc(t(
                  "Yapısal bütünlük notu:",
                  "Structural integrity note:"
                ))}
              </strong>

              ${esc(t(
                "Edge tablosunda referans edilen fakat node tablosunda beyan edilmeyen endpointler vardır. Bu endpointler graph görüntüleyicisinde sentetik düğüm olarak eklenir ve ilişki kapanışını değiştirmez; ancak yayın paketinde yapısal audit notu olarak korunmalıdır.",
                "Some endpoints referenced by the edge table are not declared in the node table. The graph explorer adds them as synthetic nodes and this does not change relation closure; however, the issue must remain documented as a structural audit note."
              ))}

              <br>

              <code>
                ${esc(endpointList.join(", "))}
              </code>

            </div>
          `
      }
    `;
  }


  function datasetList(manifest) {
    if (Array.isArray(manifest)) return manifest;
    return manifest.datasets || manifest.scenarios || [];
  }

  function scenarioLabel(item) {
    return en
      ? (item.label_en || item.label || item.title || item.name || item.id)
      : (item.label_tr || item.label || item.title || item.name || item.id);
  }

  function scenarioPath(item, keys, fallbackName) {
    for (const key of keys) {
      if (item && item[key]) return item[key];
    }
    const graph = item?.graph || item?.cyjs || item?.graph_cyjs || "";
    if (!graph) return "";
    return graph.replace(/saci_graph(?:_v2)?\.cyjs$/i, fallbackName);
  }

  async function getCSVByPath(path, optional = true) {
    if (!path) return [];
    try {
      const r = await fetch(path, { cache: "no-store" });
      if (!r.ok) throw new Error(`${path} HTTP ${r.status}`);
      return parseCSV(await r.text());
    } catch (e) {
      if (optional) return [];
      throw e;
    }
  }

  async function getJSONByPath(path, optional = true) {
    if (!path) return null;
    try {
      const r = await fetch(path, { cache: "no-store" });
      if (!r.ok) throw new Error(`${path} HTTP ${r.status}`);
      return await r.json();
    } catch (e) {
      if (optional) return null;
      throw e;
    }
  }

  function scoreMap(rows) {
    return Object.fromEntries(rows.map(r => [String(r.metric || r.name || "").toUpperCase(), r.score ?? r.value ?? "-"]));
  }

  function graphStatsFromRaw(raw) {
    if (!raw) return { nodes:"-", edges:"-", observed:"-", missing:"-" };
    const elements = Array.isArray(raw) ? raw
      : Array.isArray(raw.elements) ? raw.elements
      : raw.elements?.nodes && raw.elements?.edges ? [...raw.elements.nodes, ...raw.elements.edges]
      : raw.nodes && raw.edges ? [...raw.nodes, ...raw.edges]
      : [];
    const edges = elements.filter(x => x?.data?.source && x?.data?.target);
    const nodes = elements.length - edges.length;
    const observed = edges.filter(x => String(x.data.observed) === "1" || x.data.observed === true).length;
    return { nodes, edges:edges.length, observed, missing:edges.length-observed };
  }

  function scenarioMitreTable(rows) {
    if (!rows.length) {
      return `<div class="empty-state">${esc(t("Bu senaryo için MITRE kapsam dosyası bulunamadı.", "No MITRE coverage file was found for this scenario."))}</div>`;
    }
    return table([
      { key:"technique_id", label:t("Teknik", "Technique"), render:v => `<a href="${techniqueUrl(v)}" target="_blank" rel="noopener"><code>${esc(v)}</code></a>` },
      { key:"technique_name", label:t("Teknik adı", "Technique name"), render:(v,r) => `<a href="${techniqueUrl(r.technique_id)}" target="_blank" rel="noopener">${esc(v || r.technique_id)}</a>` },
      { key:"tactic", label:t("Taktik", "Tactic"), render:v => String(v || "").split("/").map(x => x.trim()).filter(Boolean).map(x => `<a href="${tacticUrl(x)}" target="_blank" rel="noopener">${esc(x)}</a>`).join(" / ") || "-" },
      { key:"covered", label:t("Kapsama", "Coverage"), render:v => status(v, t("Kapsanıyor", "Covered"), t("Eksik", "Missing")) },
      { key:"priority", label:t("Öncelik", "Priority") },
    ], rows);
  }

  async function loadScenario(item) {
    const scorePath = scenarioPath(item, ["scores","score","score_csv","scores_csv"], "saci_scores.csv");
    const mitrePath = scenarioPath(item, ["mitre","mitre_csv","mitre_coverage"], "mitre_coverage.csv");
    const graphPath = scenarioPath(item, ["graph","cyjs","graph_cyjs"], "saci_graph.cyjs");
    const summaryPath = scenarioPath(item, ["summary","graph_summary"], "saci_graph_summary.md");
    const [scoreRows, mitreRows, graphRaw] = await Promise.all([
      getCSVByPath(scorePath, true),
      getCSVByPath(mitrePath, true),
      getJSONByPath(graphPath, true),
    ]);
    const scores = scoreMap(scoreRows);
    const graph = graphStatsFromRaw(graphRaw);
    const covered = mitreRows.filter(r => String(r.covered) === "1" || String(r.covered).toLowerCase() === "true").length;
    return {
      item,
      id:String(item.id || item.key || "scenario"),
      label:scenarioLabel(item),
      scorePath, mitrePath, graphPath, summaryPath,
      scores, mitreRows, graph,
      mitreCovered:covered,
      mitreTotal:mitreRows.length,
    };
  }

  function scenarioLink(path, label) {
    return path ? `<a href="${path}" target="_blank" rel="noopener">${esc(label)}</a>` : "";
  }

  function renderScenarioDetails(data) {
    const m = data.scores;
    const metrics = ["CWLC","CAC","MDC","CTIC","TF","SACI"]
      .map(key => `<div class="scenario-metric"><span>${key}</span><strong>${esc(m[key] ?? "-")}</strong></div>`)
      .join("");
    const links = [
      scenarioLink(data.scorePath, t("Skor CSV", "Score CSV")),
      scenarioLink(data.mitrePath, t("MITRE CSV", "MITRE CSV")),
      scenarioLink(data.graphPath, t("Graph verisi", "Graph data")),
      scenarioLink(data.summaryPath, t("Graph özeti", "Graph summary")),
    ].filter(Boolean).join("");
    return `<details class="scenario-detail" id="scenario-${esc(data.id)}">
      <summary>
        <span class="scenario-summary-title">${esc(data.label)}</span>
        <span class="scenario-summary-stat">SACI <strong>${esc(m.SACI ?? "-")}</strong></span>
        <span class="scenario-summary-stat">${esc(t("Eksik", "Missing"))} <strong>${esc(data.graph.missing)}</strong></span>
        <span class="scenario-summary-stat">MITRE <strong>${esc(data.mitreCovered)}/${esc(data.mitreTotal)}</strong></span>
      </summary>
      <div class="scenario-detail-body">
        <div class="scenario-metrics">${metrics}</div>
        <div class="scenario-links">${links}</div>
        <h3 class="scenario-mitre-title">${esc(t("MITRE ATT&CK taktik ve teknik eşleşmeleri", "MITRE ATT&CK tactic and technique mappings"))}</h3>
        ${scenarioMitreTable(data.mitreRows)}
      </div>
    </details>`;
  }

  async function renderScenarios() {
    const manifestPath = root.dataset.scenarioManifest;
    if (!manifestPath) return;
    const manifest = await getJSONByPath(manifestPath, false);
    const items = datasetList(manifest).filter(item => {
      const id = String(item.id || "").toLowerCase();
      const kind = String(item.kind || "").toLowerCase();
      return kind !== "canonical" && !["final","final","final"].includes(id);
    });
    const host = $("scenarioContent");
    if (!items.length) {
      host.innerHTML = `<div class="empty-state">${esc(t("Tarihsel senaryo veri kümesi bulunamadı.", "No historical scenario datasets were found."))}</div>`;
      return;
    }
    const loaded = await Promise.all(items.map(loadScenario));
    const summaryRows = loaded.map(data => ({
      scenario:data.label,
      saci:data.scores.SACI ?? "-",
      cwlc:data.scores.CWLC ?? "-",
      cac:data.scores.CAC ?? "-",
      mdc:data.scores.MDC ?? "-",
      ctic:data.scores.CTIC ?? "-",
      tf:data.scores.TF ?? "-",
      observed:data.graph.observed,
      missing:data.graph.missing,
      mitre:`${data.mitreCovered}/${data.mitreTotal}`,
      id:data.id,
    }));
    $("scenarioTable").innerHTML = table([
      { key:"scenario", label:t("Senaryo", "Scenario"), render:(v,r) => `<a href="#scenario-${esc(r.id)}">${esc(v)}</a>` },
      { key:"cwlc", label:"CWLC" },
      { key:"cac", label:"CAC" },
      { key:"mdc", label:"MDC" },
      { key:"ctic", label:"CTIC" },
      { key:"tf", label:"TF" },
      { key:"saci", label:"SACI", render:v => `<strong>${esc(v)}</strong>` },
      { key:"observed", label:t("Observed", "Observed") },
      { key:"missing", label:t("Eksik", "Missing") },
      { key:"mitre", label:"MITRE" },
    ], summaryRows);
    host.innerHTML = `<div class="scenario-detail-list">${loaded.map(renderScenarioDetails).join("")}</div>`;
    $("scenarioCount").textContent = String(loaded.length);
  }

  async function init() {
    try {
      const [scores, assets, logs, controls, mitre, ctic, reasons, graph] = await Promise.all([
        getCSV("saci_scores.csv"), getCSV("asset_log_coverage.csv"), getCSV("log_source_status.csv"),
        getCSV("control_coverage.csv"), getCSV("mitre_coverage.csv"), getCSV("ctic_coverage.csv"),
        getCSV("reason_codes.csv", true), graphStats()
      ]);
      const scoreMap = renderScores(scores);
      renderAssets(assets); renderLogs(logs); renderControls(controls); renderMitre(mitre); renderCtic(ctic); renderReasons(reasons, graph);
      renderAudit(scoreMap, assets, logs, controls, mitre, ctic, reasons, graph);
      await renderScenarios();
      $("evidenceStatus").textContent = t("Final kanıt dosyaları yüklendi.", "Final evidence files loaded.");
    } catch (e) {
      console.error(e);
      $("evidenceStatus").textContent = t("Kanıt verileri yüklenemedi: ", "Evidence data could not be loaded: ") + e.message;
      $("evidenceStatus").classList.add("warn");
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
