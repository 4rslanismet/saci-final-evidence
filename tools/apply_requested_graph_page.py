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

def header(active="graph.html", en=False):
    links = []
    for file, label in PAGES:
        cls = ' class="active"' if file == active else ""
        links.append(f'<a{cls} href="{file}">{label}</a>')
    nav = "\n      ".join(links)
    skip = "Skip to main content" if en else "Ana içeriğe geç"

    return f'''<a class="skip-link" href="#main">{skip}</a>

<header class="top">
  <div class="top-inner">
    <a class="brand" href="index.html">SACI Final Evidence</a>

    <nav class="nav" aria-label="Primary navigation">
      {nav}
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

CSS = r'''
  <style>
    body[data-page="graph"] {
      overflow-x: hidden;
    }

    body[data-page="graph"] .top {
      position: sticky;
      top: 0;
      z-index: 80;
    }

    .graph-page {
      width: min(100% - (var(--page-pad, 56px) * 2), 112rem) !important;
      margin-inline: auto !important;
      padding-block: clamp(34px, 4.5vw, 58px) clamp(48px, 6vw, 76px) !important;
    }

    .graph-hero {
      margin-bottom: 18px;
    }

    .graph-hero .kicker {
      margin-bottom: 18px;
      color: var(--accent);
      letter-spacing: .14em;
      text-transform: uppercase;
      font-size: 13px;
      font-weight: 700;
    }

    .graph-hero h1 {
      max-width: 84rem;
      margin: 0 0 14px;
      font-size: clamp(48px, 5.8vw, 86px);
      line-height: 1.04;
      letter-spacing: -0.055em;
      font-weight: 640;
    }

    .graph-hero .lead {
      max-width: 76rem;
      font-size: clamp(16.5px, .45vw + 15px, 20px);
      line-height: 1.72;
      color: var(--muted);
    }

    .graph-note-strip {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(280px, 360px);
      gap: 14px;
      margin: 18px 0 16px;
    }

    .scope-card,
    .alt-card {
      border: 1px solid color-mix(in srgb, var(--line) 70%, transparent);
      border-radius: 18px;
      background: color-mix(in srgb, var(--surface-2, #111827) 76%, transparent);
      padding: 15px 17px;
    }

    .scope-card h2 {
      margin: 0 0 8px;
      font-size: clamp(22px, 2vw, 32px);
      line-height: 1.15;
    }

    .scope-card p,
    .alt-card p {
      margin: 8px 0 0;
      color: var(--muted);
      font-size: 14.5px;
      line-height: 1.62;
    }

    .alt-card strong {
      display: block;
      color: var(--text);
      font-size: 13px;
      margin-bottom: 8px;
    }

    .alt-card a {
      color: var(--accent);
      border-bottom: 1px solid color-mix(in srgb, var(--accent) 55%, transparent);
    }

    .graph-workbench {
      display: grid;
      grid-template-columns: minmax(270px, 320px) minmax(0, 1fr);
      gap: 14px;
      align-items: stretch;
    }

    .graph-sidebar {
      display: flex;
      flex-direction: column;
      gap: 10px;
      min-width: 0;
    }

    .control-card,
    .metric-card-side {
      border: 1px solid color-mix(in srgb, var(--line) 70%, transparent);
      border-radius: 18px;
      background: color-mix(in srgb, var(--surface-2, #111827) 76%, transparent);
      padding: 13px;
    }

    .control-card label {
      display: block;
      margin: 0 0 7px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.2;
      font-weight: 750;
      letter-spacing: .02em;
    }

    .control-card select,
    .control-card input {
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

    .graph-button-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .graph-button-grid button,
    .focus-button {
      height: 38px;
      border: 1px solid color-mix(in srgb, var(--line) 82%, transparent);
      border-radius: 999px;
      background: color-mix(in srgb, var(--surface, #0f172a) 82%, transparent);
      color: var(--text);
      cursor: pointer;
      font: inherit;
      font-size: 12.5px;
      font-weight: 750;
    }

    .focus-button {
      width: 100%;
      margin-top: 8px;
    }

    .metric-stack {
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
    }

    .metric-card-side {
      min-height: 72px;
    }

    .metric-card-side span {
      display: block;
      margin-bottom: 5px;
      color: var(--muted);
      font-size: 11.5px;
      font-weight: 760;
    }

    .metric-card-side strong {
      display: block;
      color: var(--text);
      font-size: 27px;
      line-height: 1;
      font-weight: 700;
    }

    .graph-main {
      min-width: 0;
      display: grid;
      grid-template-rows: minmax(720px, 78vh) auto;
      gap: 12px;
    }

    .graph-frame {
      position: relative;
      min-height: 720px;
      height: 78vh;
      max-height: 980px;
      border: 1px solid color-mix(in srgb, var(--line) 72%, transparent);
      border-radius: 22px;
      background:
        radial-gradient(circle at 18% 18%, color-mix(in srgb, var(--accent) 13%, transparent), transparent 32%),
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
      max-width: min(780px, calc(100% - 28px));
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

    .graph-bottom {
      border: 1px solid color-mix(in srgb, var(--line) 70%, transparent);
      border-radius: 18px;
      background: color-mix(in srgb, var(--surface-2, #111827) 76%, transparent);
      padding: 15px 17px;
    }

    .graph-bottom h2 {
      margin: 0 0 10px;
      font-size: clamp(24px, 2.2vw, 34px);
      line-height: 1.15;
    }

    .graph-bottom #interpretation {
      margin-top: 8px;
    }

    .graph-bottom #interpretation .interpretation-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 14px;
      margin-bottom: 8px;
    }

    .graph-bottom #interpretation .scenario-title {
      margin: 0;
      font-size: 18px;
      line-height: 1.25;
    }

    .graph-bottom #interpretation .scenario-subtitle {
      margin-top: 4px;
      font-size: 13px;
      color: var(--muted);
    }

    .graph-bottom #interpretation .metric-cards {
      display: none !important;
    }

    .graph-bottom #interpretation .explain-box {
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

    .drawer-hint {
      margin-top: 8px;
      color: var(--muted);
      font-size: 12.5px;
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
      width: min(540px, 92vw);
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
      grid-template-columns: minmax(110px, .34fr) minmax(0, 1fr);
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

    @media (max-width: 1180px) {
      .graph-note-strip,
      .graph-workbench {
        grid-template-columns: 1fr;
      }

      .graph-sidebar {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .metric-stack {
        grid-template-columns: repeat(5, minmax(0, 1fr));
      }

      .graph-main {
        grid-template-rows: minmax(620px, 72vh) auto;
      }

      .graph-frame {
        min-height: 620px;
        height: 72vh;
      }
    }

    @media (max-width: 780px) {
      .graph-sidebar,
      .metric-stack {
        grid-template-columns: 1fr;
      }

      .graph-main {
        grid-template-rows: minmax(560px, 70vh) auto;
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

def make_page(en=False):
    prefix = "../" if en else ""
    lang = "en" if en else "tr"

    if en:
        title = "Interactive evidence graph"
        kicker = "GRAPH EXPLORER"
        lead = "Explore the SACI evidence graph by scenario, node type, observed relations and selected node or edge details."
        scope_title = "Scope and integrity note"
        scope_p1 = '<strong>final-v2:</strong> 97 declared nodes, 171 edge rows and 171 observed relations. Edge endpoints such as <code>LOGSOURCE:Wazuh</code> and <code>MITRE:T1071.001</code> may be referenced in the edge table even when they are not declared in the node table; the explorer displays them as <code>undeclared_endpoint</code> nodes.'
        scope_p2 = "<strong>Historical S8:</strong> a separate controlled-validation scenario with 95 nodes and 173 edge rows. It is not equivalent to the final-v2 publication snapshot."
        alt_head = "Text alternatives"
        alt_text = '<a href="../evidence/lab/final_v2/saci_nodes_v2.csv">node table</a>, <a href="../evidence/lab/final_v2/saci_edges_v2.csv">edge table</a>, <a href="../evidence/lab/final_v2/saci_graph_v2.cyjs">CYJS graph</a>.'
        scenario = "Scenario"
        search_label = "Search"
        search_ph = "Search node, edge, MITRE, Wazuh, CTI..."
        node_type = "Node type"
        all_types = "All node types"
        view = "View"
        fit = "Fit"
        reset = "Reset"
        focus = "Focus mode"
        metric_node = "Nodes"
        metric_edge = "Edges"
        metric_observed = "Observed"
        metric_missing = "Missing"
        metric_score = "SACI"
        loading = "Loading graph..."
        bottom_title = "Graph interpretation"
        bottom_hint = "The graph is the main object on this page. Double-click a node or edge to inspect its SACI role, relations and attributes."
        drawer_title = "Selected node / edge"
        drawer_empty = "Double-click a node or edge in the graph to inspect its SACI role, relations and attributes."
        close = "Close"
    else:
        title = "Etkileşimli kanıt grafı"
        kicker = "GRAPH EXPLORER"
        lead = "SACI kanıt grafını senaryo, node tipi, observed ilişkiler ve seçili node/edge ayrıntıları üzerinden incele."
        scope_title = "Kapsam ve bütünlük notu"
        scope_p1 = '<strong>final-v2:</strong> 97 beyan edilmiş node, 171 edge satırı ve 171 observed ilişki içerir. <code>LOGSOURCE:Wazuh</code> ve <code>MITRE:T1071.001</code> gibi edge uçları edge tablosunda referans edilip node tablosunda beyan edilmemiş olabilir; gezgin bunları <code>undeclared_endpoint</code> node olarak gösterir.'
        scope_p2 = "<strong>Tarihsel S8:</strong> 95 node ve 173 edge satırıyla ayrı bir kontrollü doğrulama senaryosudur. final-v2 yayın anlık görüntüsüyle eşdeğer değildir."
        alt_head = "Metinsel alternatifler"
        alt_text = '<a href="evidence/lab/final_v2/saci_nodes_v2.csv">node tablosu</a>, <a href="evidence/lab/final_v2/saci_edges_v2.csv">edge tablosu</a>, <a href="evidence/lab/final_v2/saci_graph_v2.cyjs">CYJS graph</a>.'
        scenario = "Senaryo"
        search_label = "Arama"
        search_ph = "Node, edge, MITRE, Wazuh, CTI ara..."
        node_type = "Node tipi"
        all_types = "Tüm node tipleri"
        view = "Görünüm"
        fit = "Sığdır"
        reset = "Sıfırla"
        focus = "Odak modu"
        metric_node = "Node"
        metric_edge = "Edge"
        metric_observed = "Observed"
        metric_missing = "Missing"
        metric_score = "SACI"
        loading = "Graph yükleniyor..."
        bottom_title = "Graph yorumlaması"
        bottom_hint = "Bu sayfanın ana nesnesi graph’tır. Bir node veya edge üzerine çift tıklayarak SACI içindeki görevini, ilişkilerini ve özniteliklerini inceleyebilirsin."
        drawer_title = "Seçili node / edge"
        drawer_empty = "Graph üzerinde bir node veya edge’e çift tıklayınca SACI rolü, ilişkileri ve öznitelikleri burada gösterilir."
        close = "Kapat"

    return f'''<!doctype html>
<html lang="{lang}" data-theme="dim" data-font-level="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — SACI Final Evidence</title>
  <link rel="stylesheet" href="{prefix}assets/saci-standard.css?v=requested-graph-layout-1">
{CSS}
</head>

<body data-page="graph">
{header("graph.html", en=en)}

<main id="main" class="graph-page">
  <section class="graph-hero">
    <div class="kicker">{kicker}</div>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </section>

  <section class="graph-note-strip" aria-label="{scope_title}">
    <aside class="scope-card">
      <h2>{scope_title}</h2>
      <p>{scope_p1}</p>
      <p>{scope_p2}</p>
    </aside>

    <aside class="alt-card">
      <strong>{alt_head}</strong>
      <p>{alt_text}</p>
    </aside>
  </section>

  <section class="graph-workbench" aria-label="SACI graph explorer">
    <aside class="graph-sidebar">
      <div class="control-card">
        <label for="scenarioSelect">{scenario}</label>
        <select id="scenarioSelect" aria-label="{scenario}">
          <option>{loading}</option>
        </select>
      </div>

      <div class="control-card">
        <label for="q">{search_label}</label>
        <input id="q" type="search" placeholder="{search_ph}" autocomplete="off">
      </div>

      <div class="control-card">
        <label for="typeFilter">{node_type}</label>
        <select id="typeFilter" aria-label="{node_type}">
          <option value="">{all_types}</option>
        </select>
      </div>

      <div class="control-card">
        <label>{view}</label>
        <div class="graph-button-grid">
          <button type="button" id="fitBtn">{fit}</button>
          <button type="button" id="resetBtn">{reset}</button>
        </div>
        <button type="button" class="focus-button" id="fullBtn">{focus}</button>
      </div>

      <div class="metric-stack" aria-label="Graph metrics">
        <div class="metric-card-side">
          <span>{metric_node}</span>
          <strong id="nodeCount">-</strong>
        </div>
        <div class="metric-card-side">
          <span>{metric_edge}</span>
          <strong id="edgeCount">-</strong>
        </div>
        <div class="metric-card-side">
          <span>{metric_observed}</span>
          <strong id="observedCount">-</strong>
        </div>
        <div class="metric-card-side">
          <span>{metric_missing}</span>
          <strong id="missingCount">-</strong>
        </div>
        <div class="metric-card-side">
          <span>{metric_score}</span>
          <strong id="saciScore">-</strong>
        </div>
      </div>
    </aside>

    <div class="graph-main">
      <div class="graph-frame" id="graphShell">
        <div id="status" class="graph-status">{loading}</div>
        <div id="cy" role="img" aria-label="SACI evidence graph"></div>
      </div>

      <section class="graph-bottom">
        <h2>{bottom_title}</h2>
        <div id="interpretation">
          <p>{bottom_hint}</p>
        </div>
        <p class="drawer-hint">{drawer_empty}</p>
      </section>
    </div>
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
<script src="{prefix}assets/graph.js?v=requested-graph-layout-1"></script>
<script src="{prefix}assets/saci-ui.js?v=requested-graph-layout-1"></script>
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
    (DOCS / "graph.html").write_text(make_page(en=False), encoding="utf-8")
    (EN / "graph.html").write_text(make_page(en=True), encoding="utf-8")
    make_en_manifest()
    print("[+] Requested TR/EN graph pages rebuilt.")
    print("[+] TR: docs/graph.html")
    print("[+] EN: docs/en/graph.html")

if __name__ == "__main__":
    main()
