#!/usr/bin/env python3
from pathlib import Path
import json
import copy

ROOT = Path.cwd()
DOCS = ROOT / "docs"
EN = DOCS / "en"

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

def header(en=False):
    nav = []
    for file, label in PAGES:
        cls = ' class="active"' if file == "graph.html" else ""
        nav.append(f'<a{cls} href="{file}">{label}</a>')
    nav_html = "\n      ".join(nav)
    skip = "Skip to main content" if en else "Ana içeriğe geç"

    return f'''<a class="skip-link" href="#main">{skip}</a>

<header class="top">
  <div class="top-inner">
    <a class="brand" href="index.html">SACI Final Evidence</a>

    <nav class="nav" aria-label="Primary navigation">
      {nav_html}
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

STYLE = r'''
  <style>
    .graph-page {
      width: min(100% - (var(--page-pad, 56px) * 2), 118rem) !important;
      margin-inline: auto !important;
      padding-block: clamp(34px, 4.5vw, 58px) clamp(48px, 6vw, 76px) !important;
    }

    .graph-hero {
      margin-bottom: 20px;
    }

    .graph-hero .kicker {
      margin-bottom: 16px;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: .14em;
      font-size: 13px;
      font-weight: 720;
    }

    .graph-hero h1 {
      max-width: 86rem;
      margin: 0 0 14px;
      font-size: clamp(48px, 5.8vw, 88px);
      line-height: 1.04;
      letter-spacing: -0.055em;
      font-weight: 640;
    }

    .graph-hero .lead {
      max-width: 78rem;
      color: var(--muted);
      font-size: clamp(16.5px, .45vw + 15px, 20px);
      line-height: 1.72;
    }

    .graph-toolbar {
      display: grid;
      grid-template-columns: minmax(260px, 1.15fr) minmax(240px, 1fr) minmax(180px, 260px) auto auto auto;
      gap: 10px;
      align-items: center;
      margin: 16px 0 14px;
      padding: 10px;
      border: 1px solid color-mix(in srgb, var(--line) 70%, transparent);
      border-radius: 18px;
      background: color-mix(in srgb, var(--surface-2, #111827) 76%, transparent);
    }

    .toolbar-field {
      min-width: 0;
    }

    .toolbar-field label {
      display: block;
      margin: 0 0 6px;
      color: var(--muted);
      font-size: 11.5px;
      font-weight: 760;
      letter-spacing: .02em;
    }

    .graph-toolbar select,
    .graph-toolbar input {
      width: 100%;
      height: 40px;
      border: 1px solid color-mix(in srgb, var(--line) 82%, transparent);
      border-radius: 12px;
      background: color-mix(in srgb, var(--bg) 78%, #000 22%);
      color: var(--text);
      padding: 0 12px;
      outline: none;
      font: inherit;
      font-size: 13px;
    }

    .graph-toolbar button {
      align-self: end;
      height: 40px;
      border: 1px solid color-mix(in srgb, var(--line) 82%, transparent);
      border-radius: 999px;
      background: color-mix(in srgb, var(--surface, #0f172a) 82%, transparent);
      color: var(--text);
      cursor: pointer;
      font: inherit;
      font-size: 12.5px;
      font-weight: 750;
      padding: 0 14px;
      white-space: nowrap;
    }

    .graph-metrics {
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 14px;
    }

    .graph-metric {
      min-height: 78px;
      padding: 12px 13px;
      border: 1px solid color-mix(in srgb, var(--line) 70%, transparent);
      border-radius: 16px;
      background: color-mix(in srgb, var(--surface-2, #111827) 76%, transparent);
    }

    .graph-metric span {
      display: block;
      margin-bottom: 7px;
      color: var(--muted);
      font-size: 11.5px;
      font-weight: 780;
    }

    .graph-metric strong {
      display: block;
      color: var(--text);
      font-size: 27px;
      line-height: 1;
      font-weight: 720;
    }

    .graph-frame {
      position: relative;
      width: 100%;
      min-height: 760px;
      height: 78vh;
      max-height: 1040px;
      border: 1px solid color-mix(in srgb, var(--line) 72%, transparent);
      border-radius: 24px;
      background:
        radial-gradient(circle at 18% 18%, color-mix(in srgb, var(--accent) 13%, transparent), transparent 34%),
        color-mix(in srgb, var(--bg) 91%, #000 9%);
      overflow: hidden;
    }

    #cy {
      width: 100%;
      height: 100%;
      min-height: inherit;
    }

    .graph-status {
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 5;
      max-width: min(820px, calc(100% - 28px));
      padding: 8px 11px;
      border: 1px solid color-mix(in srgb, var(--line) 76%, transparent);
      border-radius: 999px;
      background: color-mix(in srgb, var(--bg) 82%, transparent);
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
      backdrop-filter: blur(8px);
    }

    .graph-status.err {
      color: #fecaca;
      border-color: color-mix(in srgb, #f87171 62%, var(--line));
    }

    .graph-analysis {
      display: grid;
      grid-template-columns: minmax(0, .62fr) minmax(320px, .38fr);
      gap: 14px;
      margin-top: 14px;
      align-items: stretch;
    }

    .analysis-card {
      border: 1px solid color-mix(in srgb, var(--line) 70%, transparent);
      border-radius: 18px;
      background: color-mix(in srgb, var(--surface-2, #111827) 76%, transparent);
      padding: 16px 18px;
    }

    .analysis-card h2 {
      margin: 0 0 10px;
      font-size: clamp(24px, 2.2vw, 34px);
      line-height: 1.15;
    }

    .analysis-card p {
      color: var(--muted);
      font-size: 14.5px;
      line-height: 1.65;
    }

    #interpretation .interpretation-head {
      display: flex;
      justify-content: space-between;
      gap: 14px;
      align-items: flex-start;
      margin-bottom: 8px;
    }

    #interpretation .scenario-title {
      margin: 0;
      font-size: 18px;
      line-height: 1.25;
    }

    #interpretation .scenario-subtitle {
      margin-top: 4px;
      color: var(--muted);
      font-size: 13px;
    }

    #interpretation .metric-cards {
      display: none !important;
    }

    #interpretation .explain-box {
      margin-top: 8px;
      padding: 11px 12px;
      border: 1px solid color-mix(in srgb, var(--line) 58%, transparent);
      border-radius: 14px;
      background: color-mix(in srgb, var(--bg) 74%, transparent);
      color: var(--muted);
      font-size: 14px;
      line-height: 1.62;
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      border: 1px solid color-mix(in srgb, var(--line) 65%, transparent);
      border-radius: 999px;
      padding: 5px 9px;
      font-size: 12px;
      font-weight: 780;
      white-space: nowrap;
    }

    .status-pill.good {
      color: #bbf7d0;
      border-color: color-mix(in srgb, #22c55e 65%, var(--line));
    }

    .status-pill.warn {
      color: #fed7aa;
      border-color: color-mix(in srgb, #f97316 65%, var(--line));
    }

    .mitre-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }

    .mitre-chip {
      border: 1px solid color-mix(in srgb, var(--accent) 45%, var(--line));
      border-radius: 999px;
      padding: 6px 9px;
      color: var(--text);
      background: color-mix(in srgb, var(--bg) 72%, transparent);
      font-size: 12.5px;
      line-height: 1.2;
    }

    .mitre-chip small {
      color: var(--muted);
      margin-left: 4px;
    }

    .node-detail-backdrop {
      position: fixed;
      inset: 0;
      z-index: 180;
      background: rgba(0,0,0,.44);
      opacity: 0;
      pointer-events: none;
      transition: opacity .18s ease;
    }

    .node-detail-backdrop.open {
      opacity: 1;
      pointer-events: auto;
    }

    .node-detail-drawer {
      position: fixed;
      top: 0;
      right: 0;
      z-index: 190;
      width: min(560px, 92vw);
      height: 100vh;
      transform: translateX(105%);
      transition: transform .22s ease;
      border-left: 1px solid color-mix(in srgb, var(--line) 80%, transparent);
      background: color-mix(in srgb, var(--bg) 96%, #000 4%);
      padding: 22px;
      overflow: auto;
    }

    .node-detail-drawer.open {
      transform: translateX(0);
    }

    .drawer-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }

    .drawer-head h2 {
      margin: 0;
      font-size: 24px;
    }

    .drawer-head button {
      border: 1px solid color-mix(in srgb, var(--line) 76%, transparent);
      border-radius: 999px;
      background: transparent;
      color: var(--text);
      padding: 7px 10px;
      cursor: pointer;
      font: inherit;
      font-size: 12px;
    }

    .selected-card h3 {
      margin: 0 0 8px;
      font-size: 22px;
    }

    .selected-card p {
      margin: 0 0 12px;
      color: var(--muted);
    }

    .kv {
      display: grid;
      grid-template-columns: minmax(120px, .34fr) minmax(0, 1fr);
      gap: 8px 12px;
      font-size: 13px;
      line-height: 1.5;
    }

    .kv b {
      color: var(--text);
    }

    .kv span {
      color: var(--muted);
      word-break: break-word;
    }

    @media (max-width: 1100px) {
      .graph-toolbar,
      .graph-analysis {
        grid-template-columns: 1fr;
      }

      .graph-metrics {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }

      .graph-frame {
        min-height: 640px;
        height: 72vh;
      }
    }

    @media (max-width: 720px) {
      .graph-toolbar,
      .graph-metrics {
        grid-template-columns: 1fr;
      }

      .graph-frame {
        min-height: 560px;
        height: 70vh;
      }

      .graph-hero h1 {
        font-size: clamp(38px, 12vw, 58px);
      }
    }
  </style>
'''

def page(en=False):
    prefix = "../" if en else ""
    lang = "en" if en else "tr"

    if en:
        title = "Interactive evidence graph"
        kicker = "GRAPH EXPLORER"
        lead = "Select a scenario from the menu, load its graph, inspect MITRE mappings, and double-click nodes or edges for their SACI role."
        scenario_label = "Scenario"
        scenario_loading = "Loading scenarios..."
        search_label = "Search"
        search_ph = "Search node, edge, MITRE, Wazuh, CTI..."
        type_label = "Node type"
        all_types = "All node types"
        fit = "Fit"
        reset = "Reset"
        focus = "Focus"
        rendered = "Rendered nodes"
        declared = "Declared nodes"
        edges = "Edges"
        observed = "Observed"
        missing = "Missing"
        saci = "SACI"
        loading = "Loading graph..."
        interpretation = "Graph interpretation"
        interpretation_hint = "Select a scenario from the menu. The graph, interpretation and MITRE mappings will update dynamically."
        mitre_title = "MITRE ATT&CK mappings"
        mitre_hint = "MITRE techniques detected in the selected graph will appear here."
        drawer_title = "Selected node / edge"
        drawer_empty = "Double-click a node or edge to inspect its SACI role, scenario context and attributes."
        close = "Close"
    else:
        title = "Etkileşimli kanıt grafı"
        kicker = "GRAPH EXPLORER"
        lead = "Menüden bir senaryo seç, grafı yükle, MITRE eşleşmelerini gör ve node/edge üzerine çift tıklayarak SACI içindeki görevini incele."
        scenario_label = "Senaryo"
        scenario_loading = "Senaryolar yükleniyor..."
        search_label = "Arama"
        search_ph = "Node, edge, MITRE, Wazuh, CTI ara..."
        type_label = "Node tipi"
        all_types = "Tüm node tipleri"
        fit = "Sığdır"
        reset = "Sıfırla"
        focus = "Odak"
        rendered = "Gösterilen node"
        declared = "Beyan edilen node"
        edges = "Edge"
        observed = "Observed"
        missing = "Missing"
        saci = "SACI"
        loading = "Graph yükleniyor..."
        interpretation = "Graph yorumlaması"
        interpretation_hint = "Menüden bir senaryo seçildiğinde graph, yorum ve MITRE eşleşmeleri dinamik güncellenir."
        mitre_title = "MITRE ATT&CK eşleşmeleri"
        mitre_hint = "Seçili graph içindeki MITRE teknikleri burada listelenir."
        drawer_title = "Seçili node / edge"
        drawer_empty = "Bir node veya edge üzerine çift tıklayınca SACI rolü, senaryo içindeki görevi ve öznitelikleri burada gösterilir."
        close = "Kapat"

    return f'''<!doctype html>
<html lang="{lang}" data-theme="dim" data-font-level="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — SACI Final Evidence</title>
  <link rel="stylesheet" href="{prefix}assets/saci-standard.css?v=graph-dropdown-layout-1">
{STYLE}
</head>

<body data-page="graph">
{header(en=en)}

<main id="main" class="graph-page">
  <section class="graph-hero">
    <div class="kicker">{kicker}</div>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </section>

  <section class="graph-toolbar" aria-label="Graph controls">
    <div class="toolbar-field">
      <label for="scenarioSelect">{scenario_label}</label>
      <select id="scenarioSelect" aria-label="{scenario_label}">
        <option>{scenario_loading}</option>
      </select>
    </div>

    <div class="toolbar-field">
      <label for="q">{search_label}</label>
      <input id="q" type="search" placeholder="{search_ph}" autocomplete="off">
    </div>

    <div class="toolbar-field">
      <label for="typeFilter">{type_label}</label>
      <select id="typeFilter" aria-label="{type_label}">
        <option value="">{all_types}</option>
      </select>
    </div>

    <button type="button" id="fitBtn">{fit}</button>
    <button type="button" id="resetBtn">{reset}</button>
    <button type="button" id="fullBtn">{focus}</button>
  </section>

  <section class="graph-metrics" aria-label="Graph metrics">
    <div class="graph-metric"><span>{declared}</span><strong id="declaredNodeCount">-</strong></div>
    <div class="graph-metric"><span>{rendered}</span><strong id="nodeCount">-</strong></div>
    <div class="graph-metric"><span>{edges}</span><strong id="edgeCount">-</strong></div>
    <div class="graph-metric"><span>{observed}</span><strong id="observedCount">-</strong></div>
    <div class="graph-metric"><span>{missing}</span><strong id="missingCount">-</strong></div>
    <div class="graph-metric"><span>{saci}</span><strong id="saciScore">-</strong></div>
  </section>

  <section class="graph-frame" id="graphShell">
    <div id="status" class="graph-status">{loading}</div>
    <div id="cy" role="img" aria-label="SACI evidence graph"></div>
  </section>

  <section class="graph-analysis">
    <article class="analysis-card">
      <h2>{interpretation}</h2>
      <div id="interpretation">
        <p>{interpretation_hint}</p>
      </div>
    </article>

    <article class="analysis-card">
      <h2>{mitre_title}</h2>
      <div id="mitrePanel">
        <p>{mitre_hint}</p>
      </div>
    </article>
  </section>
</main>

<div class="node-detail-backdrop" id="nodeDetailBackdrop"></div>

<aside class="node-detail-drawer" id="nodeDetailDrawer" aria-hidden="true">
  <div class="drawer-head">
    <h2>{drawer_title}</h2>
    <button type="button" id="nodeDetailClose">{close}</button>
  </div>
  <div id="details">
    <p>{drawer_empty}</p>
  </div>
</aside>

<script src="https://unpkg.com/cytoscape@3.29.2/dist/cytoscape.min.js"></script>
<script src="{prefix}assets/graph.js?v=graph-dropdown-layout-1"></script>
<script src="{prefix}assets/saci-ui.js?v=graph-dropdown-layout-1"></script>
</body>
</html>
'''

def make_en_manifest():
    src = DOCS / "data" / "scenarios" / "manifest.json"
    dst = EN / "data" / "scenarios" / "manifest.json"
    if not src.exists():
        return

    data = json.loads(src.read_text(encoding="utf-8"))
    out = copy.deepcopy(data)

    for s in out.get("scenarios", []):
        for k, v in list(s.items()):
            if isinstance(v, str) and (v.startswith("evidence/") or v.startswith("data/") or v.startswith("assets/")):
                s[k] = "../" + v

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    EN.mkdir(parents=True, exist_ok=True)
    (DOCS / "graph.html").write_text(page(en=False), encoding="utf-8")
    (EN / "graph.html").write_text(page(en=True), encoding="utf-8")
    make_en_manifest()
    print("[+] Graph pages rebuilt with dropdown scenario selector.")

if __name__ == "__main__":
    main()
