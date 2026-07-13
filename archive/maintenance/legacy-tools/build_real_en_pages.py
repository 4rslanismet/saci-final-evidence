#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EN = DOCS / "en"
EN.mkdir(parents=True, exist_ok=True)

PAGES = [
    ("index.html", "Home"),
    ("methodology.html", "Methodology"),
    ("architecture.html", "Architecture"),
    ("evidence.html", "Evidence"),
    ("artifacts.html", "Artifacts"),
    ("graph.html", "Graph"),
    ("explanation.html", "Explanation"),
    ("paper.html", "Paper View"),
]


def nav_html(active_file: str) -> str:
    links = []
    for file_name, label in PAGES:
        cls = ' class="active"' if file_name == active_file else ""
        links.append(f'<a{cls} href="{file_name}">{label}</a>')
    return "\n      ".join(links)


def header_html(active_file: str) -> str:
    return f'''<a class="skip-link" href="#main">Skip to main content</a>

<header class="top">
  <div class="top-inner">
    <a class="brand" href="index.html">SACI Final Evidence</a>

    <nav class="nav" aria-label="Primary navigation">
      {nav_html(active_file)}
    </nav>

    <div class="top-actions" aria-label="Display controls">
      <div class="top-control">
        <span>Language</span>
        <button type="button" id="langTR">TR</button>
        <button type="button" id="langEN">EN</button>
      </div>

      <div class="top-control">
        <span>Font</span>
        <button type="button" id="fontDown">A−</button>
        <button type="button" id="fontReset">A</button>
        <button type="button" id="fontUp">A+</button>
      </div>

      <div class="top-control">
        <span>Theme</span>
        <button type="button" data-theme-btn="dark">Dark</button>
        <button type="button" data-theme-btn="dim">Dim</button>
        <button type="button" data-theme-btn="light">Light</button>
      </div>
    </div>
  </div>
</header>'''


def section_html(title: str, paragraphs: list[str]) -> str:
    ps = "\n".join(f"    <p>{p}</p>" for p in paragraphs)
    return f'''  <section class="section">
    <h2>{title}</h2>
{ps}
  </section>'''


def standard_page(file_name: str, title: str, kicker: str, lead: str, sections: list[tuple[str, list[str]]]) -> str:
    sections_html = "\n\n".join(section_html(t, ps) for t, ps in sections)
    return f'''<!doctype html>
<html lang="en" data-theme="dim" data-font-level="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — SACI Final Evidence</title>
  <link rel="stylesheet" href="../assets/saci-standard.css?v=real-en-fixed-1">
</head>
<body>
{header_html(file_name)}

<main id="main">
  <section>
    <div class="kicker">{kicker}</div>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </section>

{sections_html}

  <footer>
    SACI Final Evidence — English publication view.
  </footer>
</main>

<script src="../assets/saci-ui.js?v=real-en-fixed-1"></script>
</body>
</html>
'''


def architecture_page() -> str:
    sections_html = "\n\n".join([
        section_html(
            "What does the architecture represent?",
            [
                "The SACI architecture does not explain visibility through a single product or a single log source. It combines telemetry-producing assets, Wazuh collection, detection rules, alert generation, MITRE ATT&CK context, CTI/MISP enrichment and graph-based evidence relations.",
                "A log alone is not sufficient. The log must come from the expected source, be processed by the Wazuh pipeline, be linked to the expected detection control, be mapped to the relevant MITRE technique and, when required, be supported by CTI enrichment."
            ]
        ),
        section_html(
            "Lab components",
            [
                "<strong>Windows sources:</strong> DC01 and WS01 provide Security, Sysmon and PowerShell telemetry.",
                "<strong>Linux sources:</strong> uhost provides authlog, syslog and process visibility.",
                "<strong>pfSense / firewall:</strong> FW01 provides firewall and pfsense_syslog evidence.",
                "<strong>MISP / CTI:</strong> CTI01 provides IOC, MISP event, MISP API and enrichment evidence.",
                "<strong>Wazuh:</strong> Wazuh performs ingestion, decoding, rule matching, alert generation and MITRE mapping."
            ]
        ),
        section_html(
            "End-to-end data flow",
            [
                "Telemetry is produced by Windows, Linux, pfSense and MISP sources. Wazuh receives and processes this data through decoders and rules. Detection controls generate alerts and connect them to MITRE techniques and CTI enrichment results.",
                "SACI then evaluates the declared scope through CWLC, CAC, MDC, CTIC and TF metrics. The evidence graph connects assets, log sources, controls, Wazuh rules, MITRE techniques, CTI objects, metrics and reason codes."
            ]
        ),
        section_html(
            "Interpretation note",
            [
                "The architecture diagram does not mean that the final environment is completely secure.",
                "It only shows the architectural flow through which expected telemetry, detection, MITRE/CTI and graph relations are evaluated within the SACI scope."
            ]
        ),
    ])

    return f'''<!doctype html>
<html lang="en" data-theme="dim" data-font-level="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lab architecture and data flow — SACI Final Evidence</title>
  <link rel="stylesheet" href="../assets/saci-standard.css?v=real-en-fixed-1">
</head>
<body>
{header_html("architecture.html")}

<main id="main">
  <section>
    <div class="kicker">ARCHITECTURE</div>
    <h1>Lab architecture and data flow</h1>
    <p class="lead">This page explains the controlled laboratory architecture used in the SACI evaluation and how data flows end to end from telemetry sources to Wazuh, detection logic, MITRE/CTI context, SACI scoring and the evidence graph.</p>
  </section>

  <section class="figure-section">
    <div class="figure-title">
      <h2>Data flow diagram</h2>
      <p>The diagram shows how data from Windows, Linux, pfSense and MISP sources is processed by Wazuh, how detection and enrichment relations are established, and how the result is transformed into SACI scoring and graph output.</p>
    </div>

    <div class="figure-shell" id="figureShell">
      <div class="figure-overlay">
        <button type="button" class="active" data-zoom="fit">Fit</button>
        <button type="button" data-zoom="125">125%</button>
        <button type="button" data-zoom="150">150%</button>
        <a href="../assets/arch-en.png" id="archOpenLink" target="_blank" rel="noopener">Open image</a>
      </div>

      <img
        id="archImage"
        src="../assets/arch-en.png"
        alt="SACI lab architecture and data flow diagram"
      >
    </div>

    <p class="figure-caption">Figure: SACI lab architecture. The diagram does not represent the final score itself; it shows the architectural flow that feeds telemetry, detection, CTI/MITRE, SACI and graph relations.</p>
  </section>

{sections_html}

  <footer>
    SACI Final Evidence — English publication view.
  </footer>
</main>

<script src="../assets/saci-ui.js?v=real-en-fixed-1"></script>
</body>
</html>
'''


PAGES_CONTENT = {
    "index.html": standard_page(
        "index.html",
        "An explainable evidence model for SIEM visibility",
        "FINAL EVIDENCE PACKAGE",
        "SACI combines telemetry coverage, detection-control relations, CTI/MISP enrichment, MITRE ATT&CK mapping and graph closure into a single evidence-oriented model for SIEM visibility assessment.",
        [
            ("Problem and motivation", [
                "Modern SIEM environments collect large volumes of logs, but the presence of logs does not automatically mean that the monitored environment has operational visibility.",
                "A useful assessment must show whether expected telemetry sources are present, whether detection controls are connected to alerts, whether MITRE techniques are represented, whether CTI enrichment is active, and whether the resulting evidence can be explained."
            ]),
            ("What does SACI solve?", [
                "SACI does not replace a SIEM, EDR, CTI platform or maturity model. Instead, it connects their outputs into a structured visibility model.",
                "The model evaluates whether expected relations are observed, missing, stale or outside the declared scope."
            ]),
            ("Contribution", [
                "The main contribution is an explainable scoring framework that combines criticality-weighted log coverage, control and alert coverage, MITRE detection coverage, CTI enrichment coverage and telemetry freshness.",
                "The second contribution is the evidence graph, which shows how assets, log sources, rules, alerts, MITRE techniques, CTI objects, score components and reason codes are connected."
            ]),
            ("Evaluation scope", [
                "The final evaluation is limited to the declared laboratory scope. The scope includes Windows, Linux, firewall/pfSense, Wazuh and MISP/CTI components used during the controlled assessment.",
                "A final score of 100 means that the expected visibility relations in this declared scope were observed and closed. It does not mean that the environment is absolutely secure."
            ]),
            ("How to read the final result", [
                "The final SACI package reports 100 for the active score components in the final closure state.",
                "This result should be interpreted as complete visibility closure for the declared scope and not as a universal security guarantee."
            ]),
        ]
    ),

    "methodology.html": standard_page(
        "methodology.html",
        "How SACI is calculated and interpreted",
        "METHODOLOGY",
        "This page explains the mathematical and operational logic behind SACI. The method evaluates log coverage, detection relations, MITRE mapping, CTI enrichment and telemetry freshness under a single evidence-based scoring framework.",
        [
            ("Methodology at a glance", [
                "SACI is calculated from active metric components. Each component measures a different visibility dimension.",
                "Components that are outside the declared scenario scope are treated as N/A rather than being forced to zero."
            ]),
            ("Core metrics", [
                "<strong>CWLC</strong> measures criticality-weighted log coverage. It evaluates whether expected asset-to-log-source relations are observed.",
                "<strong>CAC</strong> measures control and alert coverage. It evaluates whether expected detection controls are active and observed.",
                "<strong>MDC</strong> measures MITRE ATT&CK detection coverage. It evaluates whether scoped techniques are represented by detection evidence.",
                "<strong>CTIC</strong> measures CTI enrichment coverage. It evaluates whether MISP/CTI context is connected to alert and detection evidence.",
                "<strong>TF</strong> measures telemetry freshness. It evaluates whether observed telemetry remains recent enough to support the scenario."
            ]),
            ("Active-weight normalization", [
                "If a component is not applicable, its weight is removed from the denominator and the remaining active weights are normalized.",
                "This avoids penalizing a scenario for a metric that is intentionally not applicable."
            ]),
            ("Graph closure logic", [
                "The graph contains expected and observed visibility relations. A relation is closed when the expected evidence is present.",
                "Graph closure is therefore the structural explanation behind the numerical score."
            ]),
            ("Explanation layer boundary", [
                "The explanation layer does not calculate or modify the SACI score.",
                "It converts deterministic SACI outputs into readable scenario-level reports."
            ]),
            ("Limitations", [
                "SACI measures the declared monitoring baseline and evidence closure.",
                "It does not claim to discover every unknown asset, every hidden attack path or every possible security weakness."
            ]),
        ]
    ),

    "architecture.html": architecture_page(),

    "evidence.html": standard_page(
        "evidence.html",
        "Final evidence outputs",
        "EVIDENCE",
        "This page summarizes the final SACI evidence package, including score components, graph closure, coverage tables and auditable result files.",
        [
            ("Final score summary", [
                "The final closure state reports full visibility for the active SACI components in the declared laboratory scope.",
                "The final score should be interpreted as evidence closure for the declared scope, not as a universal statement that the environment is fully secure."
            ]),
            ("Graph closure summary", [
                "Graph closure means that expected visibility relations were observed and connected in the evidence graph.",
                "When missing relations are reduced to zero, the graph no longer contains unresolved expected relations for the declared evaluation scope."
            ]),
            ("Coverage tables", [
                "Coverage tables provide the operational evidence behind the final score.",
                "They show which assets, log sources, controls, MITRE techniques and CTI relations were included and observed."
            ]),
            ("Evidence files", [
                "The evidence package should include validation outputs, score files, graph data, coverage tables and final audit notes.",
                "Legacy intermediate files may be kept for traceability, but the publication should cite the final evidence package rather than old partial results."
            ]),
        ]
    ),

    "artifacts.html": standard_page(
        "artifacts.html",
        "Publication package artifacts",
        "ARTIFACTS",
        "This page collects the files, figures, validation outputs and traceability material used in the SACI final evidence package.",
        [
            ("Publication package files", [
                "The publication package should contain the final score output, graph data, validation report, coverage tables and final audit result.",
                "Each artifact should be stable, reproducible and clearly connected to the methodology."
            ]),
            ("Data files", [
                "Data files represent assets, log sources, detection controls, MITRE mappings, CTI enrichment results, score components and graph relations.",
                "The same data should support both the visual portal and the academic paper."
            ]),
            ("Figures", [
                "Figures should explain the architecture, graph structure, score progression and evidence closure without overstating the security meaning of the final score.",
                "Architecture and graph figures are explanatory artifacts, not independent proof of security."
            ]),
            ("Traceability", [
                "Traceability links the final claim to concrete files and validation outputs.",
                "This is important because SACI is intended to be reviewed as an evidence-based method rather than a black-box score."
            ]),
        ]
    ),

    "graph.html": standard_page(
        "graph.html",
        "Interactive evidence graph",
        "GRAPH",
        "This page explains the SACI evidence graph, where assets, log sources, controls, alerts, MITRE techniques, CTI objects, metrics and reason codes are represented as connected evidence.",
        [
            ("Graph interpretation", [
                "The graph is used to explain why a score component is complete, partial or missing.",
                "Nodes represent evidence objects and edges represent expected or observed visibility relations."
            ]),
            ("Selected node / edge", [
                "A selected node or edge should be interpreted according to its role in the SACI model.",
                "Asset nodes represent monitored systems. Log-source nodes represent telemetry channels. Control and rule nodes represent detection logic. MITRE and CTI nodes provide adversary and intelligence context."
            ]),
            ("Scenario view", [
                "Scenario-level graph views allow the reviewer to understand how the score changes when telemetry, detection, CTI or freshness relations are added or closed.",
                "This is the main explainability advantage of the graph-based approach."
            ]),
        ]
    ),

    "explanation.html": standard_page(
        "explanation.html",
        "Policy-guided explanation report",
        "EXPLANATION",
        "This page describes how deterministic SACI outputs are converted into readable operational explanations without changing the score.",
        [
            ("Explanation layer", [
                "The explanation layer is governed by a reporting policy.",
                "The policy defines how score components, graph completeness values, missing visibility relations, CTI closure, MITRE coverage and freshness decay should be interpreted.",
                "The explanation layer does not calculate or modify the SACI score."
            ]),
            ("Scenario interpretations", [
                "Each scenario explanation should describe what changed, which relations were closed, which evidence sources were used and why the score increased or remained limited.",
                "This prevents the score from being interpreted as an isolated number."
            ]),
            ("Boundaries", [
                "The explanation layer must not invent evidence, hide missing relations or turn an out-of-scope metric into a positive result.",
                "Its role is to make deterministic outputs readable, not to replace validation."
            ]),
        ]
    ),

    "paper.html": standard_page(
        "paper.html",
        "Paper view",
        "PAPER VIEW",
        "This page organizes the SACI final evidence package into a publication-oriented view that can support the academic paper.",
        [
            ("Paper view", [
                "The paper view should summarize the method, architecture, evidence graph, score components and final closure result in a compact academic structure.",
                "It should also clearly state that SACI measures declared visibility closure rather than absolute security."
            ]),
            ("Figures", [
                "Recommended figures include the architecture diagram, graph model, scenario score progression and final evidence closure view.",
                "Figures should be readable in both Turkish and English versions of the portal."
            ]),
            ("Tables", [
                "Recommended tables include metric definitions, active weights, coverage results, evidence files and scenario-level closure status.",
                "Tables should connect directly to the validation and audit files."
            ]),
            ("Publication note", [
                "The final paper should cite the final evidence package and avoid relying on old intermediate results.",
                "Legacy outputs may be mentioned only as development history or ablation evidence."
            ]),
        ]
    ),
}


def main() -> None:
    for file_name, html in PAGES_CONTENT.items():
        out = EN / file_name
        out.write_text(html, encoding="utf-8")
        print("[+] wrote", out)


if __name__ == "__main__":
    main()
