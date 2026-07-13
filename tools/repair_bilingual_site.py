#!/usr/bin/env python3
from pathlib import Path
import re
import json
import shutil

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
    ("validation.html", "Validation"),
    ("data.html", "Data"),
]

TR_EMPTY = {
    "homeKicker": "CANONICAL PUBLICATION SNAPSHOT",
    "homeTitle": "SACI Final Evidence Portal",
    "homeLead": "SACI, SIEM görünürlüğünü telemetri, detection kontrolleri, MITRE ATT&CK kapsamı ve CTI/MISP enrichment üzerinden ölçen açıklanabilir, graph tabanlı bir modeldir.",
    "methodologyKicker": "METHODOLOGY",
    "methodologyTitle": "SACI nasıl hesaplanır ve yorumlanır?",
    "methodologyLead": "Bu sayfa SACI ölçüm modelini; CWLC, CAC, MDC, CTIC ve TF formüllerini, değerlendirme tasarımını, varsayımları, doğrulama kontrollerini ve yorumlama sınırlarını açıklar.",
    "graphTitle": "Etkileşimli kanıt grafı",
}

EN_EMPTY = {
    "homeKicker": "CANONICAL PUBLICATION SNAPSHOT",
    "homeTitle": "SACI Final Evidence Portal",
    "homeLead": "SACI is an explainable, graph-based model for measuring SIEM visibility across telemetry, detection controls, MITRE ATT&CK coverage and CTI/MISP enrichment.",
    "methodologyKicker": "METHODOLOGY",
    "methodologyTitle": "How SACI is calculated and interpreted",
    "methodologyLead": "This page explains the SACI measurement model, including CWLC, CAC, MDC, CTIC and TF formulas, evaluation design, assumptions, validation checks and interpretation boundaries.",
    "graphTitle": "Interactive evidence graph",
}

def is_en(path: Path) -> bool:
    return path.parent.name == "en"

def fix_empty_i18n(path: Path):
    html = path.read_text(encoding="utf-8", errors="replace")
    mapping = EN_EMPTY if is_en(path) else TR_EMPTY

    for key, val in mapping.items():
        # <h1 data-i18n="x"></h1> gibi boş alanları doldur
        html = re.sub(
            rf'<(?P<tag>h1|h2|p|div)(?P<attrs>[^>]*)data-i18n="{re.escape(key)}"(?P<attrs2>[^>]*)>\s*</(?P=tag)>',
            lambda m: f'<{m.group("tag")}{m.group("attrs")}{m.group("attrs2")}>{val}</{m.group("tag")}>',
            html,
            flags=re.I
        )

    # Graph özel boş h1
    if path.name == "graph.html":
        if is_en(path):
            html = re.sub(r'<h1[^>]*data-i18n="graphTitle"[^>]*>\s*</h1>', '<h1>Interactive evidence graph</h1>', html, flags=re.I)
            html = html.replace(
                'Varsayılan görünüm kanonik final-v2 yayın anlık görüntüsüdür. Tarihsel S0–S18 senaryoları ayrı veri kümeleri olarak seçilebilir; node ve edge sayıları veri kümeleri arasında birleştirilmez.',
                'The default view is the canonical final-v2 publication snapshot. Historical S0–S18 scenarios can be selected as separate datasets; node and edge counts are not merged across datasets.'
            )
            html = html.replace('Kapsam ve bütünlük notu', 'Scope and integrity note')
            html = html.replace('Graph yükleniyor...', 'Loading graph...')
            html = html.replace('Veri kümesi veya senaryo seç', 'Select dataset or scenario')
            html = html.replace('Graf içinde ara', 'Search graph')
            html = html.replace('Node tipine göre filtrele', 'Filter by node type')
            html = html.replace('All node types', 'All node types')
            html = html.replace('Declared / model nodes', 'Declared / model nodes')
            html = html.replace('Edge rows', 'Edge rows')
            html = html.replace('Rows observed=1', 'Rows observed=1')
            html = html.replace('Rows observed=0', 'Rows observed=0')
            html = html.replace('SACI score', 'SACI score')
        else:
            html = re.sub(r'<h1[^>]*data-i18n="graphTitle"[^>]*>\s*</h1>', '<h1>Etkileşimli kanıt grafı</h1>', html, flags=re.I)

    path.write_text(html, encoding="utf-8")

def fix_paths(path: Path):
    html = path.read_text(encoding="utf-8", errors="replace")

    if is_en(path):
        # CSS/JS
        html = re.sub(r'href="assets/', 'href="../assets/', html)
        html = re.sub(r'src="assets/', 'src="../assets/', html)

        # Zaten ../ olanları bozma
        html = html.replace('../../assets/', '../assets/')
        html = html.replace('../../evidence/', '../evidence/')
        html = html.replace('../../data/', '../data/')

        # EN graph kendi manifestini kullansın
        if path.name == "graph.html":
            html = html.replace('../data/scenarios/manifest.json', 'data/scenarios/manifest.json')
            html = html.replace('"data/scenarios/manifest.json"', '"data/scenarios/manifest.json"')
            html = html.replace("'data/scenarios/manifest.json'", "'data/scenarios/manifest.json'")

            # Statik evidence linkleri EN klasöründen bir üst dizine gitmeli
            html = re.sub(r'href="evidence/', 'href="../evidence/', html)
            html = re.sub(r'href="data/', 'href="../data/', html)
        else:
            html = re.sub(r'(?<!\.\./)href="evidence/', 'href="../evidence/', html)
            html = re.sub(r'(?<!\.\./)src="evidence/', 'src="../evidence/', html)

    else:
        html = html.replace('../assets/', 'assets/')
        html = html.replace('../evidence/', 'evidence/')
        html = html.replace('../data/', 'data/')

    path.write_text(html, encoding="utf-8")

def relink_css_js(path: Path):
    html = path.read_text(encoding="utf-8", errors="replace")
    css = "../assets/saci-standard.css?v=repair-bilingual-1" if is_en(path) else "assets/saci-standard.css?v=repair-bilingual-1"
    js = "../assets/saci-ui.js?v=repair-bilingual-1" if is_en(path) else "assets/saci-ui.js?v=repair-bilingual-1"

    html = re.sub(r'\s*<link rel="stylesheet" href="(\.\./)?assets/saci-standard\.css[^"]*">\s*', '\n', html)
    html = re.sub(r'\s*<script src="(\.\./)?assets/saci-ui\.js[^"]*"></script>\s*', '\n', html)

    if "</head>" in html:
        html = html.replace("</head>", f'  <link rel="stylesheet" href="{css}">\n</head>', 1)
    if "</body>" in html:
        html = html.replace("</body>", f'  <script src="{js}"></script>\n</body>', 1)

    path.write_text(html, encoding="utf-8")

def arch_main(lang: str) -> str:
    en = lang == "en"
    img = "../assets/arch-en.png" if en else "assets/arch-tr.png"
    open_text = "Open image" if en else "Görseli aç"

    if en:
        return f'''<main id="main">
  <section>
    <div class="kicker">ARCHITECTURE</div>
    <h1>Lab architecture and data flow</h1>
    <p class="lead">This page explains the controlled laboratory architecture used in the SACI evaluation and how data flows end to end from telemetry sources to Wazuh, detection logic, MITRE/CTI context, SACI scoring and the evidence graph.</p>
    <p class="note"><span>Scope distinction:</span> The primary publication snapshot is final-v2 with 97 declared nodes and 171 edge rows. The S8 closure point in the historical S0–S18 validation series uses a separate graph with 95 nodes and 173 edges. These two artifacts must not be interpreted as the same snapshot.</p>
  </section>

  <section class="figure-section arch-figure-section">
    <div class="figure-title">
      <h2>Data flow diagram</h2>
      <p>The diagram shows how Windows, Linux, pfSense and MISP sources feed Wazuh, detection, enrichment, SACI scoring and the final evidence graph.</p>
    </div>

    <div class="figure-shell" id="figureShell">
      <div class="figure-overlay">
        <button type="button" class="active" data-zoom="fit">Fit</button>
        <button type="button" data-zoom="125">125%</button>
        <button type="button" data-zoom="150">150%</button>
        <a href="{img}" id="archOpenLink" target="_blank" rel="noopener">{open_text}</a>
      </div>
      <img id="archImage" src="{img}" alt="SACI lab architecture and data flow diagram">
    </div>
    <p class="figure-caption">Figure: SACI lab architecture. The diagram is not the final score itself; it shows the architectural flow that feeds telemetry, detection, CTI/MITRE, SACI and graph relations.</p>
  </section>

  <section class="section">
    <h2>What does the architecture represent?</h2>
    <p>The SACI architecture does not explain security visibility through a single product or a single log source. It combines telemetry-producing assets, Wazuh collection, detection rule and alert generation, MITRE ATT&CK context, CTI/MISP enrichment and the evidence graph.</p>
    <p>The core idea is that a log alone is not sufficient. The log must come from the expected source, be processed by the Wazuh pipeline, be linked to a detection control, be mapped to the relevant MITRE technique and, when required, be supported by CTI enrichment.</p>
  </section>

  <section class="section">
    <h2>Lab components</h2>
    <div class="component-flow">
      <div class="component-item"><span class="name">Windows sources</span><span class="desc">DC01 and WS01 produce Security, Sysmon and PowerShell telemetry.</span></div>
      <div class="component-item"><span class="name">Linux sources</span><span class="desc">uhost provides authlog, syslog and process visibility.</span></div>
      <div class="component-item"><span class="name">pfSense / firewall sources</span><span class="desc">FW01 provides firewall and pfsense_syslog evidence for network visibility.</span></div>
      <div class="component-item"><span class="name">MISP / CTI sources</span><span class="desc">CTI01 provides IOC, MISP event, MISP API and enrichment outputs.</span></div>
      <div class="component-item"><span class="name">Wazuh collection and detection layer</span><span class="desc">Wazuh performs ingestion, decoding, rule matching, alert generation and MITRE mapping.</span></div>
    </div>
  </section>

  <section class="section">
    <h2>End-to-end data flow</h2>
    <ul class="flow-list">
      <li><span class="term">Telemetry</span><span class="desc">Raw logs, events and IOC information are produced by Windows, Linux, pfSense and MISP sources.</span></li>
      <li><span class="term">Wazuh</span><span class="desc">Incoming logs are collected and processed through decoder and rule layers.</span></li>
      <li><span class="term">Detection</span><span class="desc">Rules generate alerts; alert relations are linked to detection controls and MITRE techniques.</span></li>
      <li><span class="term">MITRE / CTI</span><span class="desc">MITRE ATT&CK techniques and MISP enrichment strengthen the alert context.</span></li>
      <li><span class="term">SACI</span><span class="desc">CWLC, CAC, MDC, CTIC and TF metrics are calculated from declared scope and observed/missing relations.</span></li>
      <li><span class="term">Graph</span><span class="desc">Assets, log sources, controls, rules, MITRE techniques, CTI objects, metrics and reason codes are merged into the evidence graph.</span></li>
    </ul>
  </section>

  <section class="section">
    <h2>Telemetry → Wazuh → Detection → MITRE/CTI → SACI → Graph relation</h2>
    <p>Each stage in this chain feeds a different aspect of the SACI score. Telemetry feeds log visibility, Wazuh and detection feed control/alert coverage, MITRE/CTI feeds technical and intelligence context, SACI calculates metrics and the graph explains these relations as observed or missing.</p>
    <p>The Architecture page should be read as the bridge between the Methodology and Graph pages.</p>
    <p class="note"><span>Interpretation note:</span> The architecture diagram does not mean that the final environment is completely secure. It only shows the flow through which expected telemetry, detection, MITRE/CTI and graph relations are evaluated within SACI scope.</p>
  </section>

  <footer>SACI Architecture — telemetry flow, Wazuh detection pipeline, MITRE/CTI enrichment and evidence graph output.</footer>
</main>'''

    return f'''<main id="main">
  <section>
    <div class="kicker">MİMARİ / ARCHITECTURE</div>
    <h1>Lab mimarisi ve veri akışı</h1>
    <p class="lead">Bu sayfa, SACI değerlendirmesinde kullanılan kontrollü laboratuvar mimarisini ve verinin uçtan uca nasıl aktığını açıklar. Amaç, telemetri kaynaklarından başlayarak Wazuh toplama ve detection katmanına, MITRE/CTI bağlamına, SACI skorlamasına ve evidence graph çıktısına kadar olan ilişkiyi sade biçimde göstermektir.</p>
    <p class="note"><span>Kapsam ayrımı:</span> Birincil yayın anlık görüntüsü final-v2'dir: 97 beyan edilmiş node ve 171 edge satırı. S0–S18 tarihsel doğrulama serisinin S8 kapanışı ayrı bir graph kullanır: 95 node ve 173 edge. Bu iki artefakt aynı anlık görüntü gibi yorumlanmamalıdır.</p>
  </section>

  <section class="figure-section arch-figure-section">
    <div class="figure-title">
      <h2>Veri akış diyagramı</h2>
      <p>Diyagram; Windows, Linux, pfSense ve MISP kaynaklarından gelen verinin Wazuh üzerinde işlenmesini, detection ve enrichment ilişkilerinin kurulmasını, ardından SACI skor ve graph çıktısına dönüşmesini gösterir.</p>
    </div>

    <div class="figure-shell" id="figureShell">
      <div class="figure-overlay">
        <button type="button" class="active" data-zoom="fit">Fit</button>
        <button type="button" data-zoom="125">125%</button>
        <button type="button" data-zoom="150">150%</button>
        <a href="{img}" id="archOpenLink" target="_blank" rel="noopener">{open_text}</a>
      </div>
      <img id="archImage" src="{img}" alt="SACI lab mimarisi ve veri akışı diyagramı">
    </div>
    <p class="figure-caption">Şekil: SACI lab mimarisi. Diyagram final skorun kendisini değil; final skorun beslendiği telemetri, detection, CTI/MITRE, SACI ve graph ilişkilerinin mimari akışını gösterir.</p>
  </section>

  <section class="section">
    <h2>Mimari neyi temsil eder?</h2>
    <p>SACI mimarisi, güvenlik görünürlüğünü tek bir ürün veya tek bir log kaynağı üzerinden açıklamaz. Bunun yerine, telemetri üreten varlıkları, Wazuh toplama sürecini, detection rule ve alert üretimini, MITRE ATT&CK bağlamını, CTI/MISP enrichment zincirini ve bunların evidence graph modeline nasıl taşındığını birlikte ele alır.</p>
    <p>Bu yaklaşımın nedeni şudur: Bir logun var olması tek başına yeterli değildir. Logun doğru kaynaktan gelmesi, Wazuh pipeline içinde işlenmesi, beklenen detection kontrolüne bağlanması, ilgili MITRE tekniğiyle ilişkilendirilmesi ve gerektiğinde CTI enrichment zinciriyle desteklenmesi gerekir.</p>
  </section>

  <section class="section">
    <h2>Lab bileşenleri</h2>
    <div class="component-flow">
      <div class="component-item"><span class="name">Windows kaynakları</span><span class="desc">DC01 ve WS01 üzerinden Security, Sysmon ve PowerShell telemetrisi üretilir.</span></div>
      <div class="component-item"><span class="name">Linux kaynakları</span><span class="desc">uhost üzerinden authlog, syslog ve process kayıtları alınır.</span></div>
      <div class="component-item"><span class="name">pfSense / firewall kaynakları</span><span class="desc">FW01 üzerinden firewall ve pfsense_syslog olayları toplanır.</span></div>
      <div class="component-item"><span class="name">MISP / CTI kaynakları</span><span class="desc">CTI01 üzerinde IOC, MISP event, misp_api ve misp_enrichment çıktıları kullanılır.</span></div>
      <div class="component-item"><span class="name">Wazuh toplama ve detection katmanı</span><span class="desc">Wazuh; log ve event ingestion, decoder/rule eşleşmeleri, alert üretimi ve MITRE mapping adımlarını yürütür.</span></div>
    </div>
  </section>

  <section class="section">
    <h2>Uçtan uca veri akışı</h2>
    <ul class="flow-list">
      <li><span class="term">Telemetry</span><span class="desc">Windows, Linux, pfSense ve MISP kaynaklarından ham log, event ve IOC bilgisi üretilir.</span></li>
      <li><span class="term">Wazuh</span><span class="desc">Gelen loglar Wazuh tarafından alınır, decoder ve rule katmanlarından geçirilir.</span></li>
      <li><span class="term">Detection</span><span class="desc">Kurallar alert üretir; alertlerin detection control ve MITRE technique ilişkileri kurulur.</span></li>
      <li><span class="term">MITRE / CTI</span><span class="desc">MITRE ATT&CK teknikleri ve MISP enrichment çıktıları alert bağlamını güçlendirir.</span></li>
      <li><span class="term">SACI</span><span class="desc">CWLC, CAC, MDC, CTIC ve TF metrikleri declared scope ve observed/missing ilişkiler üzerinden hesaplanır.</span></li>
      <li><span class="term">Graph</span><span class="desc">Asset, log source, control, Wazuh rule, MITRE technique, CTI object, metric ve reason code ilişkileri evidence graph içinde birleşir.</span></li>
    </ul>
  </section>

  <section class="section">
    <h2>Telemetry → Wazuh → Detection → MITRE/CTI → SACI → Graph ilişkisi</h2>
    <p>Bu zincirdeki her aşama SACI skorunun başka bir yönünü besler. Telemetry katmanı log görünürlüğünü, Wazuh ve detection katmanı control/alert coverage değerini, MITRE/CTI katmanı teknik ve istihbarat bağlamını, SACI katmanı metrik hesaplamasını, graph katmanı ise bu ilişkilerin observed veya missing olarak açıklanmasını sağlar.</p>
    <p>Architecture sayfası, Methodology ve Graph sayfaları arasındaki köprü olarak okunmalıdır.</p>
    <p class="note"><span>Yorumlama notu:</span> Diyagram final ortamın tamamen güvenli olduğunu göstermez. Yalnızca SACI kapsamındaki beklenen telemetri, detection, MITRE/CTI ve graph ilişkilerinin hangi mimari akış üzerinden değerlendirildiğini gösterir.</p>
  </section>

  <footer>SACI Architecture — lab topology, telemetry flow, Wazuh detection pipeline, MITRE/CTI enrichment and evidence graph output.</footer>
</main>'''

def patch_architecture(path: Path, lang: str):
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8", errors="replace")
    html = re.sub(r'<main[\s\S]*?</main>', arch_main(lang), html, count=1, flags=re.I)
    path.write_text(html, encoding="utf-8")

def find_file(base: Path, names):
    for n in names:
        if (base / n).exists():
            return n
    return None

def scenario_entry(base_rel, base_abs, sid, title, en_prefix=""):
    nodes = find_file(base_abs, ["saci_nodes_v2.csv", "saci_nodes.csv"])
    edges = find_file(base_abs, ["saci_edges_v2.csv", "saci_edges.csv"])
    graph = find_file(base_abs, ["saci_graph_v2.cyjs", "saci_graph.cyjs"])
    scores = find_file(base_abs, ["saci_scores_v2.csv", "saci_scores.csv", "saci_scores.json"])
    summary = find_file(base_abs, ["saci_graph_summary_v2.md", "saci_graph_summary.md"])

    def p(x):
        return en_prefix + base_rel + "/" + x if x else ""

    return {
        "id": sid,
        "name": title,
        "label": title,
        "title": title,
        "dir": en_prefix + base_rel,
        "base": en_prefix + base_rel,
        "nodes": p(nodes),
        "node_csv": p(nodes),
        "nodes_csv": p(nodes),
        "edges": p(edges),
        "edge_csv": p(edges),
        "edges_csv": p(edges),
        "graph": p(graph),
        "cyjs": p(graph),
        "graph_cyjs": p(graph),
        "scores": p(scores),
        "score": p(scores),
        "summary": p(summary),
        "graph_summary": p(summary)
    }

def write_manifests():
    scenarios_tr = []

    final_v2 = DOCS / "evidence" / "lab" / "final_v2"
    final = DOCS / "evidence" / "lab" / "final"

    if final_v2.exists():
        scenarios_tr.append(scenario_entry("evidence/lab/final_v2", final_v2, "final_v2", "final-v2 canonical publication snapshot"))
    elif final.exists():
        scenarios_tr.append(scenario_entry("evidence/lab/final", final, "final", "final lab closure snapshot"))

    data_root = DOCS / "evidence" / "data"
    if data_root.exists():
        for d in sorted(data_root.iterdir()):
            if d.is_dir() and (d / "saci_graph.cyjs").exists():
                sid = d.name.split("_", 1)[0]
                scenarios_tr.append(scenario_entry(f"evidence/data/{d.name}", d, sid, d.name.replace("_", " ")))

    if not scenarios_tr:
        return

    (DOCS / "data" / "scenarios").mkdir(parents=True, exist_ok=True)
    (EN / "data" / "scenarios").mkdir(parents=True, exist_ok=True)

    tr_manifest = {
        "default": scenarios_tr[0]["id"],
        "default_scenario": scenarios_tr[0]["id"],
        "scenarios": scenarios_tr
    }

    scenarios_en = []
    for s in scenarios_tr:
        se = dict(s)
        for k, v in list(se.items()):
            if isinstance(v, str) and (v.startswith("evidence/") or v.startswith("data/")):
                se[k] = "../" + v
        scenarios_en.append(se)

    en_manifest = {
        "default": scenarios_en[0]["id"],
        "default_scenario": scenarios_en[0]["id"],
        "scenarios": scenarios_en
    }

    (DOCS / "data" / "scenarios" / "manifest.json").write_text(json.dumps(tr_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (EN / "data" / "scenarios" / "manifest.json").write_text(json.dumps(en_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

def write_ui():
    js = r'''(function () {
  const FONT_KEY = "saci-font-level";
  const THEME_KEY = "saci-graph-theme";
  const ARCH_ZOOM_KEY = "saci-arch-zoom";

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function isEnglishPage() {
    return /\/en\//.test(window.location.pathname);
  }

  function currentFile() {
    return window.location.pathname.split("/").pop() || "index.html";
  }

  function initLanguageControls() {
    const tr = document.getElementById("langTR");
    const en = document.getElementById("langEN");
    const inEn = isEnglishPage();
    const file = currentFile();

    if (tr) tr.classList.toggle("active", !inEn);
    if (en) en.classList.toggle("active", inEn);

    if (tr) tr.onclick = () => { if (inEn) window.location.href = "../" + file; };
    if (en) en.onclick = () => { if (!inEn) window.location.href = "en/" + file; };
  }

  function initFontControls() {
    let level = Number(localStorage.getItem(FONT_KEY) || "0");
    if (!Number.isFinite(level)) level = 0;

    function apply() {
      level = clamp(level, -2, 2);
      document.documentElement.setAttribute("data-font-level", String(level));
      localStorage.setItem(FONT_KEY, String(level));
    }

    const down = document.getElementById("fontDown");
    const reset = document.getElementById("fontReset");
    const up = document.getElementById("fontUp");

    if (down) down.onclick = () => { level -= 1; apply(); };
    if (reset) reset.onclick = () => { level = 0; apply(); };
    if (up) up.onclick = () => { level += 1; apply(); };
    apply();
  }

  function initThemeControls() {
    const saved = localStorage.getItem(THEME_KEY) || "dim";
    document.documentElement.setAttribute("data-theme", saved);

    document.querySelectorAll("[data-theme-btn]").forEach(btn => {
      const theme = btn.getAttribute("data-theme-btn");
      btn.classList.toggle("active", theme === saved);
      btn.onclick = () => {
        localStorage.setItem(THEME_KEY, theme);
        document.documentElement.setAttribute("data-theme", theme);
        document.querySelectorAll("[data-theme-btn]").forEach(b => {
          b.classList.toggle("active", b.getAttribute("data-theme-btn") === theme);
        });
      };
    });
  }

  function applyArchZoom(mode) {
    const img = document.getElementById("archImage");
    if (!img) return;
    const safe = ["fit", "125", "150"].includes(mode) ? mode : "fit";
    if (safe === "fit") {
      img.style.width = "100%";
      img.style.maxWidth = "100%";
    } else {
      img.style.width = safe + "%";
      img.style.maxWidth = "none";
    }
    localStorage.setItem(ARCH_ZOOM_KEY, safe);
    document.querySelectorAll("[data-zoom]").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-zoom") === safe);
    });
  }

  function initArchZoom() {
    document.querySelectorAll("[data-zoom]").forEach(btn => {
      btn.onclick = () => applyArchZoom(btn.getAttribute("data-zoom"));
    });
    applyArchZoom(localStorage.getItem(ARCH_ZOOM_KEY) || "fit");
  }

  function init() {
    initLanguageControls();
    initFontControls();
    initThemeControls();
    initArchZoom();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();'''
    (DOCS / "assets" / "saci-ui.js").write_text(js, encoding="utf-8")

def main():
    write_ui()

    html_files = list(DOCS.glob("*.html")) + list(EN.glob("*.html"))
    for p in html_files:
        fix_empty_i18n(p)
        fix_paths(p)
        relink_css_js(p)

    patch_architecture(DOCS / "architecture.html", "tr")
    patch_architecture(EN / "architecture.html", "en")

    # EN graph kendi manifestini kullansın.
    en_graph = EN / "graph.html"
    if en_graph.exists():
        html = en_graph.read_text(encoding="utf-8", errors="replace")
        html = html.replace("../data/scenarios/manifest.json", "data/scenarios/manifest.json")
        html = html.replace('"../data/scenarios/manifest.json"', '"data/scenarios/manifest.json"')
        html = html.replace("'../data/scenarios/manifest.json'", "'data/scenarios/manifest.json'")
        html = html.replace("href=\"evidence/", "href=\"../evidence/")
        en_graph.write_text(html, encoding="utf-8")

    write_manifests()
    print("[+] Bilingual portal repaired: TR headings, EN paths, architecture sections, graph manifests.")

if __name__ == "__main__":
    main()
