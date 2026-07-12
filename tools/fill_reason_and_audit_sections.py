#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import py_compile
import re
import shutil
import subprocess
import sys

ROOT = Path.cwd()
BUILDER = ROOT / "tools" / "build_final_evidence_page.py"

if not BUILDER.exists():
    raise SystemExit(
        "[!] tools/build_final_evidence_page.py bulunamadı."
    )

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = ROOT / "backups" / f"reason_audit_{stamp}"
backup_dir.mkdir(parents=True, exist_ok=True)

shutil.copy2(
    BUILDER,
    backup_dir / "build_final_evidence_page.py",
)

source = BUILDER.read_text(
    encoding="utf-8",
    errors="replace",
)


EXTRA_CSS = r'''
/* SACI_REASON_AUDIT_START */

.reason-summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin: 0 0 14px;
}

.reason-summary-card,
.audit-check {
  padding: 13px 14px;
  border:
    1px solid
    color-mix(in srgb, var(--line) 58%, transparent);
  border-radius: 13px;
  background:
    color-mix(
      in srgb,
      var(--surface, var(--bg)) 80%,
      transparent
    );
}

.reason-summary-card span,
.audit-check-copy > span {
  display: block;
  margin-bottom: 6px;
  color: var(--muted);
  font-size: 11.5px;
  font-weight: 680;
}

.reason-summary-card strong {
  color: var(--text);
  font-size: 19px;
  line-height: 1.3;
}

.reason-explanation {
  margin: 0 0 18px;
  padding: 14px 15px;
  border-left: 2px solid var(--accent);
  border-radius: 0 12px 12px 0;
  background:
    color-mix(
      in srgb,
      var(--accent) 6%,
      transparent
    );
  color: var(--muted);
  font-size: 14px;
  line-height: 1.68;
}

.reason-explanation strong {
  color: var(--text);
}

.reason-catalog {
  display: grid;
  gap: 8px;
  margin-top: 14px;
}

.reason-catalog-item {
  display: grid;
  grid-template-columns:
    minmax(210px, .85fr)
    minmax(90px, .3fr)
    minmax(0, 1.6fr);
  gap: 12px;
  align-items: start;

  padding: 11px 12px;

  border:
    1px solid
    color-mix(in srgb, var(--line) 50%, transparent);

  border-radius: 12px;

  background:
    color-mix(
      in srgb,
      var(--bg) 77%,
      transparent
    );
}

.reason-catalog-item code {
  color: var(--accent);
  font-size: 12px;
  overflow-wrap: anywhere;
}

.reason-catalog-item b {
  color: var(--text);
  font-size: 12.5px;
}

.reason-catalog-item p {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.55;
}

.audit-checklist {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 16px;
}

.audit-check {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  align-items: center;
}

.audit-check-copy {
  min-width: 0;
}

.audit-check-copy p {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.55;
}

.audit-check .status {
  justify-self: end;
}

.audit-integrity-note {
  margin-top: 14px;
  padding: 13px 14px;

  border:
    1px solid
    color-mix(
      in srgb,
      var(--yellow, #eab308) 30%,
      var(--line)
    );

  border-radius: 13px;

  background:
    color-mix(
      in srgb,
      var(--yellow, #eab308) 6%,
      var(--surface, var(--bg))
    );

  color: var(--muted);
  font-size: 13.5px;
  line-height: 1.65;
}

.audit-integrity-note strong {
  color: var(--text);
}

.audit-integrity-note code {
  display: inline-block;
  margin-top: 6px;
  color: var(--accent);
  overflow-wrap: anywhere;
}

@media (max-width: 900px) {
  .reason-summary-grid,
  .audit-checklist {
    grid-template-columns: 1fr;
  }

  .reason-catalog-item {
    grid-template-columns: 1fr;
    gap: 5px;
  }
}

/* SACI_REASON_AUDIT_END */
'''


REASON_AND_GRAPH_JS = r'''
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
'''


AUDIT_JS = r'''
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
'''


source = re.sub(
    r'/\* SACI_REASON_AUDIT_START \*/'
    r'.*?'
    r'/\* SACI_REASON_AUDIT_END \*/',
    '',
    source,
    flags=re.S,
)


css_marker = "\n'''\n\n\nEVIDENCE_JS = r'''"

if css_marker not in source:
    raise SystemExit(
        "[!] EVIDENCE_CSS sonu bulunamadı."
    )

source = source.replace(
    css_marker,
    "\n"
    + EXTRA_CSS
    + "\n'''\n\n\nEVIDENCE_JS = r'''",
    1,
)


reason_pattern = re.compile(
    r'  function renderReasons\([^)]*\) \{'
    r'.*?'
    r'\n  function renderAudit\([^)]*\) \{',
    re.S,
)

if not reason_pattern.search(source):
    raise SystemExit(
        "[!] renderReasons / graphStats alanı bulunamadı."
    )

source = reason_pattern.sub(
    REASON_AND_GRAPH_JS.rstrip()
    + "\n\n"
    + "  function renderAudit("
    + "scores, assets, logs, controls, mitre, ctic, graph"
    + ") {",
    source,
    count=1,
)


audit_pattern = re.compile(
    r'  function renderAudit\([^)]*\) \{'
    r'.*?'
    r'\n  \}'
    r'\n\n\n  function datasetList',
    re.S,
)

if not audit_pattern.search(source):
    raise SystemExit(
        "[!] renderAudit alanı bulunamadı."
    )

source = audit_pattern.sub(
    AUDIT_JS.rstrip()
    + "\n\n\n"
    + "  function datasetList",
    source,
    count=1,
)


source = re.sub(
    r'renderReasons\(\s*reasons'
    r'(?:\s*,\s*graph)?'
    r'\s*\);',
    'renderReasons(reasons, graph);',
    source,
)


source = re.sub(
    r'renderAudit\('
    r'\s*scoreMap\s*,'
    r'\s*assets\s*,'
    r'\s*logs\s*,'
    r'\s*controls\s*,'
    r'\s*mitre\s*,'
    r'\s*ctic\s*,'
    r'(?:\s*reasons\s*,)?'
    r'\s*graph\s*'
    r'\);',
    (
        'renderAudit('
        'scoreMap, assets, logs, controls, '
        'mitre, ctic, reasons, graph'
        ');'
    ),
    source,
)


source = re.sub(
    r'VERSION\s*=\s*"[^"]+"',
    'VERSION = "final-evidence-reason-audit-3"',
    source,
    count=1,
)


BUILDER.write_text(
    source,
    encoding="utf-8",
)


py_compile.compile(
    str(BUILDER),
    doraise=True,
)


subprocess.run(
    [
        sys.executable,
        str(BUILDER),
    ],
    cwd=ROOT,
    check=True,
)


print()
print("=== REASON CODE AND AUDIT SECTIONS FILLED ===")
print(f"Builder backup: {backup_dir}")
print("TR: docs/evidence.html")
print("EN: docs/en/evidence.html")
