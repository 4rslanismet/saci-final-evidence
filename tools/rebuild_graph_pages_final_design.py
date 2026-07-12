#!/usr/bin/env python3
from pathlib import Path

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
    nav = []
    for file, label in PAGES:
        cls = ' class="active"' if file == active else ""
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

def graph_page(en=False):
    css_path = "../assets/saci-standard.css?v=graph-final-design-1" if en else "assets/saci-standard.css?v=graph-final-design-1"
    ui_path = "../assets/saci-ui.js?v=graph-final-design-1" if en else "assets/saci-ui.js?v=graph-final-design-1"
    graph_path = "../assets/graph.js?v=graph-final-design-1" if en else "assets/graph.js?v=graph-final-design-1"

    if en:
        lang = "en"
        title = "Interactive evidence graph"
        kicker = "GRAPH EXPLORER"
        lead = "Explore the SACI evidence graph by scenario, node type, observed relations and selected node or edge details."
        scope_title = "Scope and integrity note"
        scope_p1 = "<strong>final-v2:</strong> 97 declared nodes, 171 edge rows and 171 observed relations. Edge endpoints such as <code>LOGSOURCE:Wazuh</code> and <code>MITRE:T1071.001</code> may be referenced in the edge table even when they are not declared in the node table; the explorer displays them as <code>undeclared_endpoint</code> nodes."
        scope_p2 = "<strong>Historical S8:</strong> a separate controlled-validation scenario with 95 nodes and 173 edge rows. It is not equivalent to the final-v2 publication snapshot."
        select_label = "Scenario"
        search_ph = "Search node, edge, MITRE, Wazuh, CTI..."
        type_label = "Node type"
        all_types = "All node types"
        fit = "Fit"
        reset = "Reset"
        focus = "Focus mode"
        node = "Nodes"
        edge = "Edges"
        observed = "Observed"
        missing = "Missing"
        score = "SACI"
        graph_status = "Loading graph..."
        bottom_title = "Graph interpretation"
        bottom_hint = "The graph is the primary object on this page. Double-click a node or edge to inspect its role in the SACI model."
        drawer_title = "Selected node / edge"
        drawer_empty = "Double-click a node or edge in the graph to inspect its SACI role, relations and attributes."
        close = "Close"
        text_alt = 'Text alternatives: <a href="../evidence/lab/final_v2/saci_nodes_v2.csv">node table</a>, <a href="../evidence/lab/final_v2/saci_edges_v2.csv">edge table</a>, <a href="../evidence/lab/final_v2/saci_graph_v2.cyjs">CYJS graph</a>.'
    else:
        lang = "tr"
        title = "Etkileşimli kanıt grafı"
        kicker = "GRAPH EXPLORER"
        lead = "SACI kanıt grafını senaryo, node tipi, observed ilişkiler ve seçili node/edge ayrıntıları üzerinden incele."
        scope_title = "Kapsam ve bütünlük notu"
        scope_p1 = "<strong>final-v2:</strong> 97 beyan edilmiş node, 171 edge satırı ve 171 observed ilişki içerir. <code>LOGSOURCE:Wazuh</code> ve <code>MITRE:T1071.001</code> gibi edge uçları edge tablosunda referans edilip node tablosunda beyan edilmemiş olabilir; gezgin bunları <code>undeclared_endpoint</code> node olarak gösterir."
        scope_p2 = "<strong>Tarihsel S8:</strong> 95 node ve 173 edge satırıyla ayrı bir kontrollü doğrulama senaryosudur. final-v2 yayın anlık görüntüsüyle eşdeğer değildir."
        select_label = "Senaryo"
        search_ph = "Node, edge, MITRE, Wazuh, CTI ara..."
        type_label = "Node tipi"
        all_types = "Tüm node tipleri"
        fit = "Sığdır"
        reset = "Sıfırla"
        focus = "Odak modu"
        node = "Node"
        edge = "Edge"
        observed = "Observed"
        missing = "Missing"
        score = "SACI"
        graph_status = "Graph yükleniyor..."
        bottom_title = "Graph yorumlaması"
        bottom_hint = "Bu sayfanın ana nesnesi graph’tır. Bir node veya edge üzerine çift tıklayarak SACI içindeki görevini inceleyebilirsin."
        drawer_title = "Seçili node / edge"
        drawer_empty = "Graph üzerinde bir node veya edge’e çift tıklayınca SACI rolü, ilişkileri ve öznitelikleri burada gösterilir."
        close = "Kapat"
        text_alt = 'Metinsel alternatifler: <a href="evidence/lab/final_v2/saci_nodes_v2.csv">node tablosu</a>, <a href="evidence/lab/final_v2/saci_edges_v2.csv">edge tablosu</a>, <a href="evidence/lab/final_v2/saci_graph_v2.cyjs">CYJS graph</a>.'

    return f'''<!doctype html>
<html lang="{lang}" data-theme="dim" data-font-level="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — SACI Final Evidence</title>
  <link rel="stylesheet" href="{css_path}">

  <style>
    body[data-page="graph"] main.graph-page {{
      width: min(100% - (var(--page-pad, 56px) * 2), 104rem);
      margin-inline: auto;
      padding-block: clamp(36px, 5vw, 64px) clamp(48px, 6vw, 80px);
    }}

    .graph-hero {{
      margin-bottom: 22px;
    }}

    .graph-hero .kicker {{
      margin-bottom: 18px;
    }}

    .graph-hero h1 {{
      max-width: 82rem;
      margin: 0 0 16px;
      font-size: clamp(46px, 5.8vw, 86px);
      line-height: 1.04;
      letter-spacing: -0.055em;
    }}

    .graph-hero .lead {{
      max-width: 74rem;
      font-size: clamp(16px, .42vw + 15px, 19px);
      line-height: 1.72;
    }}

    .scope-strip {{
      display: grid;
      grid-template-columns: minmax(0, .72fr) minmax(280px, .28fr);
      gap: 18px;
      align-items: stretch;
      margin: 18px 0 16px;
    }}

    .scope-card,
    .quick-card {{
      border: 1px solid color-mix(in srgb, var(--line) 68%, transparent);
      border-radius: 18px;
      background: color-mix(in srgb, var(--surface-2, #111827) 72%, transparent);
      padding: 16px 18px;
    }}

    .scope-card h2 {{
      font-size: clamp(22px, 2vw, 32px);
      margin: 0 0 8px;
    }}

    .scope-card p,
    .quick-card p {{
      font-size: 14.5px;
      line-height: 1.62;
      margin: 8px 0 0;
      color: var(--muted);
    }}

    .quick-card strong {{
      display: block;
      color: var(--text);
      font-size: 13px;
      margin-bottom: 8px;
    }}

    .quick-card a {{
      color: var(--accent);
      border-bottom: 1px solid color-mix(in srgb, var(--accent) 55%, transparent);
    }}

    .graph-workspace {{
      display: grid;
      grid-template-columns: minmax(250px, 300px) minmax(0, 1fr);
      gap: 14px;
      align-items: stretch;
      margin-top: 14px;
    }}

    .graph-side {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      min-width: 0;
    }}

    .control-card,
    .metric-card-mini {{
      border: 1px solid color-mix(in srgb, var(--line) 68%, transparent);
      border-radius: 18px;
      background: color-mix(in srgb, var(--surface-2, #111827) 74%, transparent);
      padding: 14px;
    }}

    .control-card label {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      font-weight: 650;
      margin: 0 0 7px;
    }}

    .control-card select,
    .control-card input {{
      width: 100%;
      height: 40px;
      border-radius: 12px;
      border: 1px solid color-mix(in srgb, var(--line) 82%, transparent);
      background: color-mix(in srgb, var(--bg) 78%, #000 22%);
      color: var(--text);
      padding: 0 12px;
      outline: none;
      font: inherit;
      font-size: 13px;
    }}

    .control-card + .control-card {{
      margin-top: 0;
    }}

    .button-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}

    .button-row button,
    .focus-button {{
      height: 38px;
      border-radius: 999px;
      border: 1px solid color-mix(in srgb, var(--line) 82%, transparent);
      background: color-mix(in srgb, var(--surface, #0f172a) 82%, transparent);
      color: var(--text);
      cursor: pointer;
      font: inherit;
      font-size: 12.5px;
      font-weight: 650;
    }}

    .focus-button {{
      width: 100%;
      margin-top: 8px;
    }}

    .metric-grid-mini {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
    }}

    .metric-card-mini {{
      min-height: 72px;
    }}

    .metric-card-mini span {{
      display: block;
      color: var(--muted);
      font-size: 11.5px;
      font-weight: 700;
      margin-bottom: 5px;
    }}

    .metric-card-mini strong {{
      display: block;
      color: var(--text);
      font-size: 26px;
      line-height: 1;
    }}

    .graph-main {{
      min-width: 0;
      display: grid;
      grid-template-rows: minmax(720px, 78vh) auto;
      gap: 12px;
    }}

    .graph-frame {{
      position: relative;
      min-height: 720px;
      height: 78vh;
      max-height: 980px;
      border: 1px solid color-mix(in srgb, var(--line) 70%, transparent);
      border-radius: 22px;
      background:
        radial-gradient(circle at 15% 20%, color-mix(in srgb, var(--accent) 12%, transparent), transparent 32%),
        color-mix(in srgb, var(--bg) 90%, #000 10%);
      overflow: hidden;
    }}

    #cy {{
      width: 100%;
      height: 100%;
      min-height: inherit;
    }}

    .graph-note {{
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 5;
      max-width: min(760px, calc(100% - 28px));
      padding: 8px 11px;
      border-radius: 999px;
      border: 1px solid color-mix(in srgb, var(--line) 76%, transparent);
      background: color-mix(in srgb, var(--bg) 82%, transparent);
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
      backdrop-filter: blur(8px);
    }}

    .graph-note.err {{
      color: #fecaca;
      border-color: color-mix(in srgb, #f87171 60%, var(--line));
    }}

    .graph-summary {{
      border: 1px solid color-mix(in srgb, var(--line) 68%, transparent);
      border-radius: 18px;
      background: color-mix(in srgb, var(--surface-2, #111827) 72%, transparent);
      padding: 16px 18px;
    }}

    .graph-summary h2 {{
      font-size: clamp(24px, 2.2vw, 34px);
      margin: 0 0 10px;
    }}

    .graph-summary #interpretation {{
      margin-top: 10px;
    }}

    .graph-summary #interpretation .interpretation-head {{
      display: flex;
      justify-content: space-between;
      gap: 14px;
      align-items: flex-start;
      margin-bottom: 10px;
    }}

    .graph-summary #interpretation .scenario-title {{
      font-size: 18px;
      margin: 0;
    }}

    .graph-summary #interpretation .scenario-subtitle {{
      font-size: 13px;
      margin-top: 4px;
    }}

    .graph-summary #interpretation .metric-cards {{
      display: none !important;
    }}

    .graph-summary #interpretation .explain-box {{
      margin-top: 8px;
      padding: 11px 12px;
      border-radius: 14px;
      border: 1px solid color-mix(in srgb, var(--line) 55%, transparent);
      background: color-mix(in srgb, var(--bg) 72%, transparent);
      font-size: 14px;
      line-height: 1.62;
    }}

    .status-pill {{
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 5px 9px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid color-mix(in srgb, var(--line) 65%, transparent);
    }}

    .status-pill.good {{
      color: #bbf7d0;
      border-color: color-mix(in srgb, #22c55e 65%, var(--line));
    }}

    .status-pill.warn {{
      color: #fed7aa;
      border-color: color-mix(in srgb, #f97316 65%, var(--line));
    }}

    .drawer-hint {{
      margin-top: 8px;
      font-size: 12.5px;
      color: var(--muted);
    }}

    .node-detail-backdrop {{
      position: fixed;
      inset: 0;
      z-index: 180;
      background: rgba(0,0,0,.42);
      opacity: 0;
      pointer-events: none;
      transition: opacity .18s ease;
    }}

    .node-detail-backdrop.open {{
      opacity: 1;
      pointer-events: auto;
    }}

    .node-detail-drawer {{
      position: fixed;
      top: 0;
      right: 0;
      z-index: 190;
      height: 100vh;
      width: min(520px, 92vw);
      transform: translateX(105%);
      transition: transform .22s ease;
      border-left: 1px solid color-mix(in srgb, var(--line) 80%, transparent);
      background: color-mix(in srgb, var(--bg) 96%, #000 4%);
      padding: 22px;
      overflow: auto;
    }}

    .node-detail-drawer.open {{
      transform: translateX(0);
    }}

    .drawer-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }}

    .drawer-head h2 {{
      font-size: 24px;
      margin: 0;
    }}

    .drawer-head button {{
      border-radius: 999px;
      border: 1px solid color-mix(in srgb, var(--line) 76%, transparent);
      background: transparent;
      color: var(--text);
      padding: 7px 10px;
      cursor: pointer;
      font: inherit;
      font-size: 12px;
    }}

    .selected-card h3 {{
      font-size: 22px;
      margin: 0 0 8px;
    }}

    .selected-card p {{
      margin: 0 0 12px;
      color: var(--muted);
    }}

    .kv {{
      display: grid;
      grid-template-columns: minmax(110px, .34fr) minmax(0, 1fr);
      gap: 8px 12px;
      font-size: 13px;
      line-height: 1.5;
    }}

    .kv b {{
      color: var(--text);
    }}

    .kv span {{
      color: var(--muted);
      word-break: break-word;
    }}

    @media (max-width: 1180px) {{
      .scope-strip,
      .graph-workspace {{
        grid-template-columns: 1fr;
      }}

      .graph-side {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .metric-grid-mini {{
        grid-template-columns: repeat(5, minmax(0, 1fr));
      }}

      .graph-main {{
        grid-template-rows: minmax(620px, 72vh) auto;
      }}

      .graph-frame {{
        min-height: 620px;
        height: 72vh;
      }}
    }}

    @media (max-width: 780px) {{
      .graph-side,
      .metric-grid-mini {{
        grid-template-columns: 1fr;
      }}

      .graph-main {{
        grid-template-rows: minmax(560px, 70vh) auto;
      }}

      .graph-frame {{
        min-height: 560px;
        height: 70vh;
      }}

      .graph-hero h1 {{
        font-size: clamp(38px, 12vw, 58px);
      }}
    }}
  </style>
</head>

<body data-page="graph">
{header("graph.html", en=en)}

<main id="main" class="graph-page">
  <section class="graph-hero">
    <div class="kicker">{kicker}</div>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </section>

  <section class="scope-strip" aria-label="{scope_title}">
    <aside class="scope-card">
      <h2>{scope_title}</h2>
      <p>{scope_p1}</p>
      <p>{scope_p2}</p>
    </aside>

    <aside class="quick-card">
      <strong>{bottom_hint}</strong>
      <p>{text_alt}</p>
    </aside>
  </section>

  <section class="graph-workspace" aria-label="SACI graph explorer">
    <aside class="graph-side">
      <div class="control-card">
        <label for="scenarioSelect">{select_label}</label>
        <select id="scenarioSelect" aria-label="{select_label}">
          <option>{graph_status}</option>
        </select>
      </div>

      <div class="control-card">
        <label for="q">Search</label>
        <input id="q" type="search" placeholder="{search_ph}" autocomplete="off">
      </div>

      <div class="control-card">
        <label for="typeFilter">{type_label}</label>
        <select id="typeFilter" aria-label="{type_label}">
          <option value="">{all_types}</option>
        </select>
      </div>

      <div class="control-card">
        <label>View</label>
        <div class="button-row">
          <button type="button" id="fitBtn">{fit}</button>
          <button type="button" id="resetBtn">{reset}</button>
        </div>
        <button type="button" class="focus-button" id="fullBtn">{focus}</button>
      </div>

      <div class="metric-grid-mini" aria-label="Graph metrics">
        <div class="metric-card-mini">
          <span>{node}</span>
          <strong id="nodeCount">-</strong>
        </div>
        <div class="metric-card-mini">
          <span>{edge}</span>
          <strong id="edgeCount">-</strong>
        </div>
        <div class="metric-card-mini">
          <span>{observed}</span>
          <strong id="observedCount">-</strong>
        </div>
        <div class="metric-card-mini">
          <span>{missing}</span>
          <strong id="missingCount">-</strong>
        </div>
        <div class="metric-card-mini">
          <span>{score}</span>
          <strong id="saciScore">-</strong>
        </div>
      </div>
    </aside>

    <div class="graph-main">
      <div class="graph-frame" id="graphShell">
        <div id="status" class="graph-note">{graph_status}</div>
        <div id="cy" role="img" aria-label="SACI evidence graph"></div>
      </div>

      <section class="graph-summary">
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
<script src="{graph_path}"></script>
<script src="{ui_path}"></script>
</body>
</html>
'''

def main():
    (DOCS / "graph.html").write_text(graph_page(en=False), encoding="utf-8")
    (EN / "graph.html").write_text(graph_page(en=True), encoding="utf-8")
    print("[+] graph.html and en/graph.html rebuilt with final explorer layout")

if __name__ == "__main__":
    main()
