#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
DOCS = ROOT / "docs"
BACKUP = ROOT / "_local_backups" / datetime.now().strftime("docs_%Y%m%d_%H%M%S")

SOURCE_CANDIDATES = [
    ROOT / "docs" / "data" / "final",
    ROOT / "docs" / "data" / "v2",
    ROOT / "saci_v2_final",
    ROOT,
]

FILE_MAP = {
    "asset_log_coverage.csv": ["asset_log_coverage.csv", "asset_log_coverage_v2.csv"],
    "control_coverage.csv": ["control_coverage.csv", "control_coverage_v2.csv"],
    "ctic_coverage.csv": ["ctic_coverage.csv", "ctic_coverage_v2.csv"],
    "log_source_status.csv": ["log_source_status.csv"],
    "mitre_coverage.csv": ["mitre_coverage.csv", "mitre_coverage_v2.csv"],
    "reason_codes.csv": ["reason_codes.csv", "reason_codes_v2.csv"],
    "reason_codes.json": ["reason_codes.json", "reason_codes_v2.json"],
    "saci_edges.csv": ["saci_edges.csv", "saci_edges_v2.csv"],
    "saci_graph_summary.md": ["saci_graph_summary.md", "saci_graph_summary_v2.md"],
    "saci_graph.cyjs": ["saci_graph.cyjs", "saci_graph_v2.cyjs"],
    "saci_graph.mmd": ["saci_graph.mmd", "saci_graph_v2.mmd"],
    "saci_nodes.csv": ["saci_nodes.csv", "saci_nodes_v2.csv"],
    "saci_scores.csv": ["saci_scores.csv", "saci_scores_v2.csv"],
    "saci_scores.json": ["saci_scores.json", "saci_scores_v2.json"],
}

REQUIRED = [
    "asset_log_coverage.csv",
    "control_coverage.csv",
    "ctic_coverage.csv",
    "log_source_status.csv",
    "mitre_coverage.csv",
    "saci_edges.csv",
    "saci_graph_summary.md",
    "saci_graph.cyjs",
    "saci_nodes.csv",
    "saci_scores.csv",
    "saci_scores.json",
]

def find_file(canonical):
    names = FILE_MAP[canonical]
    for base in SOURCE_CANDIDATES:
        for name in names:
            p = base / name
            if p.exists():
                return p
    return None

def read_csv(path):
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))

def read_json(path):
    with path.open(encoding="utf-8", errors="replace") as f:
        return json.load(f)

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def esc(v):
    if v is None:
        return ""
    return str(v).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def metric_score(scores, metric):
    for r in scores:
        if r.get("metric") == metric:
            return str(r.get("score", ""))
    return ""

def fmt_num(v):
    try:
        f = float(v)
        if f.is_integer():
            return str(int(f))
        return f"{f:.2f}"
    except Exception:
        return str(v)

def pill(value):
    s = str(value).strip()
    if s in ("1", "1.0", "100", "100.0", "true", "True", "OK", "ok"):
        return '<span class="pill ok">OK</span>'
    if s in ("0", "0.0", "false", "False", "NO", "no", ""):
        return '<span class="pill bad">NO</span>'
    return esc(value)

def table(rows, columns, limit=None):
    if limit:
        rows = rows[:limit]

    out = ['<div class="table-card"><table><thead><tr>']
    for col in columns:
        out.append(f"<th>{esc(col)}</th>")
    out.append("</tr></thead><tbody>")

    for r in rows:
        out.append("<tr>")
        for col in columns:
            val = r.get(col, "")
            if col in {
                "observed", "seen", "covered", "enabled", "expected",
                "lookup_executed", "misp_hit", "wazuh_alert",
                "mapped_to_mitre", "applicable", "coverage_applicable"
            }:
                out.append(f"<td>{pill(val)}</td>")
            elif col in {"score", "coverage_percent", "weight", "criticality", "priority", "asset_criticality", "source_weight"}:
                out.append(f"<td><b>{esc(fmt_num(val))}</b></td>")
            else:
                out.append(f"<td>{esc(val)}</td>")
        out.append("</tr>")

    out.append("</tbody></table></div>")
    return "".join(out)

def lang_span(tr, en):
    return f'<span data-tr="{esc(tr)}" data-en="{esc(en)}">{esc(tr)}</span>'

def nav(prefix=""):
    return f"""
<header class="topbar">
  <nav class="nav">
    <a class="brand" href="{prefix}index.html">
      <span class="brand-dot"></span>
      <span>SACI Final Evidence</span>
    </a>

    <div class="nav-right">
      <div class="nav-links">
        <a href="{prefix}index.html">{lang_span("Ana Portal", "Main Portal")}</a>
        <a href="{prefix}lab_topology.html">{lang_span("Lab Mimarisi", "Lab Architecture")}</a>
        <a href="{prefix}evidence/lab/index.html">{lang_span("Final Kanıt", "Final Evidence")}</a>
        <a href="{prefix}graph.html">{lang_span("Kanıt Grafı", "Evidence Graph")}</a>
        <a href="{prefix}evidence/paper_clean/index.html">{lang_span("Makale Görünümü", "Paper View")}</a>
        <a href="{prefix}evidence/explanation_report.html">{lang_span("Açıklama Raporu", "Explanation Report")}</a>
      </div>

      <div class="lang-switch" aria-label="Language switch">
        <button type="button" data-lang="tr">TR</button>
        <button type="button" data-lang="en">EN</button>
      </div>
    </div>
  </nav>
</header>
"""

def page(title, body, prefix=""):
    return f"""<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body>
{nav(prefix)}
<main class="shell">
{body}
<footer class="footer">
  {lang_span("SACI=100 güvenlik garantisi değildir; yalnızca beyan edilen kapsam içindeki beklenen görünürlük ilişkilerinin kapandığını ifade eder.", "SACI=100 is not a security guarantee; it only indicates that expected visibility relationships within the declared scope were closed.")}
</footer>
</main>
<script src="{prefix}assets/site.js"></script>
</body>
</html>
"""

def main():
    resolved = {}
    missing = []

    for canonical in REQUIRED:
        p = find_file(canonical)
        if not p:
            missing.append(canonical)
        else:
            resolved[canonical] = p

    optional = ["reason_codes.csv", "reason_codes.json", "saci_graph.mmd"]
    for canonical in optional:
        p = find_file(canonical)
        if p:
            resolved[canonical] = p

    if missing:
        print("[!] Eksik final veri dosyaları:")
        for m in missing:
            print("   -", m)
        print("\nKaynak aranan yerler:")
        for c in SOURCE_CANDIDATES:
            print("   -", c)
        raise SystemExit(1)

    if DOCS.exists():
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(DOCS, BACKUP)
        shutil.rmtree(DOCS)
        print(f"[+] Eski docs yedeklendi: {BACKUP}")

    final_data = DOCS / "data" / "final"
    final_data.mkdir(parents=True, exist_ok=True)

    for canonical, src in resolved.items():
        shutil.copy2(src, final_data / canonical)

    if not (final_data / "reason_codes.csv").exists():
        write(final_data / "reason_codes.csv", "reason_code,metric,impact,fields_json\n")
    if not (final_data / "reason_codes.json").exists():
        write(final_data / "reason_codes.json", "[]\n")
    if not (final_data / "saci_graph.mmd").exists():
        write(final_data / "saci_graph.mmd", "graph LR\n")

    scores = read_csv(final_data / "saci_scores.csv")
    assets = read_csv(final_data / "asset_log_coverage.csv")
    controls = read_csv(final_data / "control_coverage.csv")
    ctic = read_csv(final_data / "ctic_coverage.csv")
    logs = read_csv(final_data / "log_source_status.csv")
    mitre = read_csv(final_data / "mitre_coverage.csv")
    nodes = read_csv(final_data / "saci_nodes.csv")
    edges = read_csv(final_data / "saci_edges.csv")
    reasons = read_csv(final_data / "reason_codes.csv")

    saci = metric_score(scores, "SACI")
    cwlc = metric_score(scores, "CWLC")
    cac = metric_score(scores, "CAC")
    mdc = metric_score(scores, "MDC")
    ctic_score = metric_score(scores, "CTIC")
    tf = metric_score(scores, "TF")

    node_count = len(nodes)
    edge_count = len(edges)
    observed_edges = sum(1 for e in edges if str(e.get("observed", "")).strip() in ("1", "1.0"))
    missing_edges = edge_count - observed_edges

    # static assets
    write(DOCS / "assets" / "site.css", CSS)
    write(DOCS / "assets" / "site.js", JS)
    write(DOCS / ".nojekyll", "")

    # validation files
    write(DOCS / "data" / "VALIDATION.txt", f"""SACI Final Evidence Validation

Final SACI score: {saci}
CWLC: {cwlc}
CAC: {cac}
MDC: {mdc}
CTIC: {ctic_score}
TF: {tf}

Graph closure:
- Nodes: {node_count}
- Edges: {edge_count}
- Observed edges: {observed_edges}
- Missing edges: {missing_edges}

Interpretation:
SACI=100 does not indicate that the monitored environment is fully secure.
It indicates that all expected visibility relations defined within the declared evaluation scope were observed and closed.
""")

    write(DOCS / "data" / "FINAL_AUDIT_RESULT.md", f"""# SACI Final Audit Result

| Item | Value |
|---|---:|
| SACI | {saci} |
| CWLC | {cwlc} |
| CAC | {cac} |
| MDC | {mdc} |
| CTIC | {ctic_score} |
| TF | {tf} |
| Nodes | {node_count} |
| Edges | {edge_count} |
| Observed edges | {observed_edges} |
| Missing edges | {missing_edges} |

SACI=100 is not a security guarantee. It indicates that the expected visibility relationships in the declared evaluation scope were observed and closed.
""")

    # README
    write(ROOT / "README.md", f"""# SACI Final Evidence Package

**SACI (Security Attack Surface Coverage Index)** is an explainable, graph-based SIEM visibility scoring model. It evaluates whether expected security visibility relationships are observed and closed within a declared SOC evaluation scope.

## Public Evidence Portal

https://4rslanismet.github.io/saci-final-evidence/

## Türkçe Özet

SACI, bir kurumun tamamen güvenli olup olmadığını ölçen bir güvenlik garantisi modeli değildir. SACI, tanımlı değerlendirme kapsamı içinde beklenen görünürlük ilişkilerinin SIEM, CTI, MITRE ATT&CK ve kanıt grafı üzerinden gözlemlenip gözlemlenmediğini ölçen açıklanabilir bir görünürlük skorlama modelidir.

## Final Evidence Summary

| Metric | Meaning | Final Value |
|---|---|---:|
| CWLC | Criticality-weighted log coverage | {cwlc} |
| CAC | Control / alert coverage | {cac} |
| MDC | MITRE ATT&CK detection coverage | {mdc} |
| CTIC | CTI / MISP enrichment coverage | {ctic_score} |
| TF | Telemetry freshness | {tf} |
| SACI | Overall SACI visibility score | {saci} |

## Final Graph Closure

| Item | Value |
|---|---:|
| Nodes | {node_count} |
| Edges | {edge_count} |
| Observed edges | {observed_edges} |
| Missing edges | {missing_edges} |

## Important Interpretation Note

**SACI=100 does not mean that the environment is fully secure.**

It means that all expected visibility relationships defined within the declared evaluation scope were observed and closed.

## Evidence Pages

- Main portal: https://4rslanismet.github.io/saci-final-evidence/
- Lab architecture: https://4rslanismet.github.io/saci-final-evidence/lab_topology.html
- Final evidence: https://4rslanismet.github.io/saci-final-evidence/evidence/lab/
- Interactive graph: https://4rslanismet.github.io/saci-final-evidence/graph.html
- Paper view: https://4rslanismet.github.io/saci-final-evidence/evidence/paper_clean/
- Explanation report: https://4rslanismet.github.io/saci-final-evidence/evidence/explanation_report.html
""")

    # pages
    index_cards = f"""
<section class="cards">
  <a class="card" href="lab_topology.html">
    <h3>{lang_span("Kontrollü Lab Mimarisi", "Controlled Lab Architecture")}</h3>
    <p>{lang_span("Wazuh, Sysmon, Linux logları, pfSense, MISP ve SACI değerlendirme katmanının temiz mimari görünümü.", "Clean architecture view of Wazuh, Sysmon, Linux logs, pfSense, MISP and the SACI evaluation layer.")}</p>
  </a>

  <a class="card" href="evidence/lab/index.html">
    <h3>{lang_span("Final Kanıt Paketi", "Final Evidence Package")}</h3>
    <p>{lang_span(f"SACI {saci}, {observed_edges}/{edge_count} observed graph relation ve {missing_edges} missing edge ile final kapanış.", f"Final closure with SACI {saci}, {observed_edges}/{edge_count} observed graph relations and {missing_edges} missing edges.")}</p>
  </a>

  <a class="card" href="graph.html">
    <h3>{lang_span("Etkileşimli Kanıt Grafı", "Interactive Evidence Graph")}</h3>
    <p>{lang_span("Asset, log source, detection control, Wazuh rule, MITRE, CTI object ve metric düğümlerini etkileşimli inceleme.", "Interactive inspection of asset, log source, detection control, Wazuh rule, MITRE, CTI object and metric nodes.")}</p>
  </a>

  <a class="card" href="evidence/paper_clean/index.html">
    <h3>{lang_span("Makale Görünümü", "Paper View")}</h3>
    <p>{lang_span("IDAP makalesi için sade skor kartları, kapsam tabloları ve görsel özetler.", "Clean score cards, coverage tables and visual summaries for the IDAP paper.")}</p>
  </a>

  <a class="card" href="evidence/explanation_report.html">
    <h3>{lang_span("Açıklama Raporu", "Explanation Report")}</h3>
    <p>{lang_span("Serbest LLM çıktısı değil; deterministik SACI sonuçlarını açıklayan policy-guided rapor.", "Not a free-form LLM output; a policy-guided report explaining deterministic SACI results.")}</p>
  </a>

  <a class="card" href="data/VALIDATION.txt">
    <h3>{lang_span("Doğrulama Dosyası", "Validation File")}</h3>
    <p>{lang_span("Final sonucun nasıl yorumlanacağını açıklayan doğrulama notu.", "Validation note explaining how the final result should be interpreted.")}</p>
  </a>
</section>
"""

    stats = f"""
<section class="stats">
  <div class="stat"><strong>{fmt_num(saci)}</strong><span>SACI</span></div>
  <div class="stat"><strong>{fmt_num(cwlc)}</strong><span>CWLC</span></div>
  <div class="stat"><strong>{observed_edges}/{edge_count}</strong><span>Observed Graph Relations</span></div>
  <div class="stat"><strong>{missing_edges}</strong><span>Missing Edges</span></div>
</section>
"""

    index_body = f"""
<section class="hero">
  <span class="badge">SACI Final Evidence Package</span>
  <h1>{lang_span("SACI Final Evidence Portalı", "SACI Final Evidence Portal")}</h1>
  <p class="lead">{lang_span("Bu portal, SIEM telemetrisi, CTI entegrasyonu, MITRE ATT&CK kapsamı ve kanıt grafı kapanışını ölçen açıklanabilir SACI görünürlük skorlama modelinin final kanıt paketini yayınlar.", "This portal publishes the final evidence package for the explainable SACI visibility scoring model, which evaluates SIEM telemetry, CTI integration, MITRE ATT&CK coverage and evidence graph closure.")}</p>
</section>
{stats}
{index_cards}
<section class="note">
  <h2>{lang_span("Önemli yorumlama notu", "Important Interpretation Note")}</h2>
  <p>{lang_span("SACI=100 ortamın güvenli olduğu anlamına gelmez. Yalnızca tanımlı değerlendirme kapsamındaki beklenen visibility ilişkilerinin gözlemlendiğini ve kapandığını ifade eder.", "SACI=100 does not mean that the environment is secure. It only means that expected visibility relationships within the declared evaluation scope were observed and closed.")}</p>
</section>
"""
    write(DOCS / "index.html", page("SACI Final Evidence Portal", index_body))

    topology_body = f"""
<section class="hero">
  <span class="badge">Controlled SOC Lab</span>
  <h1>{lang_span("SACI Lab Mimarisi ve Veri Akışı", "SACI Lab Architecture and Data Flow")}</h1>
  <p class="lead">{lang_span("Bu sayfa, SACI final kanıt paketinin hangi sistemlerden veri aldığını, Wazuh üzerinde nasıl toplandığını ve graf tabanlı skora nasıl dönüştüğünü gösterir.", "This page shows which systems feed the SACI final evidence package, how data is collected in Wazuh and how it becomes graph-based scoring.")}</p>
</section>

<section class="panel">
  <h2>{lang_span("Uç Sistemler ve Kaynaklar", "Endpoints and Sources")}</h2>
  <div class="mini-grid">
    <div class="mini"><b>DC01</b><span>Windows Security + Sysmon</span></div>
    <div class="mini"><b>WS01</b><span>Security + Sysmon + PowerShell</span></div>
    <div class="mini"><b>uhost</b><span>authlog + syslog + process</span></div>
    <div class="mini"><b>pfSense</b><span>firewall syslog + IOC traffic</span></div>
    <div class="mini"><b>MISP</b><span>IOC lookup + enrichment</span></div>
    <div class="mini"><b>Wazuh</b><span>manager + rules + alerts</span></div>
  </div>
</section>

<section class="panel">
  <h2>{lang_span("Ana Veri Akışı", "Main Data Flow")}</h2>
  <div class="flow">
    <div><b>1</b><span>{lang_span("Telemetri üretimi", "Telemetry generation")}</span></div>
    <div><b>2</b><span>Wazuh ingestion</span></div>
    <div><b>3</b><span>{lang_span("Detection control eşleşmesi", "Detection control matching")}</span></div>
    <div><b>4</b><span>SACI scoring</span></div>
    <div><b>5</b><span>Evidence graph closure</span></div>
  </div>
</section>

<section class="panel">
  <h2>{lang_span("SACI Metrikleri", "SACI Metrics")}</h2>
  <div class="mini-grid">
    <div class="mini"><b>CWLC</b><span>Criticality-weighted log coverage</span></div>
    <div class="mini"><b>CAC</b><span>Control / alert coverage</span></div>
    <div class="mini"><b>MDC</b><span>MITRE detection coverage</span></div>
    <div class="mini"><b>CTIC</b><span>CTI / MISP enrichment closure</span></div>
    <div class="mini"><b>TF</b><span>Telemetry freshness</span></div>
    <div class="mini"><b>SACI</b><span>Overall visibility score</span></div>
  </div>
</section>
"""
    write(DOCS / "lab_topology.html", page("SACI Lab Architecture", topology_body))

    score_cards = "".join([
        f"""<div class="score-card">
  <div><b>{esc(r.get("metric"))}</b><span>{esc(r.get("name"))}</span></div>
  <strong>{fmt_num(r.get("score"))}</strong>
  <div class="bar"><i style="width:{fmt_num(r.get("score"))}%"></i></div>
</div>"""
        for r in scores
    ])

    lab_body = f"""
<section class="hero">
  <span class="badge">Final Evidence</span>
  <h1>{lang_span("Final Kanıt Paketi", "Final Evidence Package")}</h1>
  <p class="lead">{lang_span(f"Final kanıt paketinde SACI {saci}, graph closure {observed_edges}/{edge_count} ve missing edge {missing_edges} olarak doğrulanmıştır.", f"The final evidence package verifies SACI {saci}, graph closure {observed_edges}/{edge_count} and {missing_edges} missing edges.")}</p>
</section>

<section class="score-grid">{score_cards}</section>

<h2>Asset / Log Source Coverage</h2>
{table(assets, ["asset_id","hostname","expected_sources","received_sources","coverage_percent","criticality","coverage_applicable"])}

<h2>Log Source Status</h2>
{table(logs, ["asset_id","hostname","log_source","expected","observed","asset_criticality","source_weight","last_seen"])}

<h2>Control / Alert Coverage</h2>
{table(controls, ["control_id","asset_id","source","rule_id","mitre_technique","enabled","seen","weight","description"])}

<h2>MITRE Coverage</h2>
{table(mitre, ["technique_id","technique_name","tactic","covered","priority"])}

<h2>CTI Coverage</h2>
{table(ctic, ["indicator","type","lookup_executed","misp_hit","wazuh_alert","mapped_to_mitre","expected_alert_rule","mitre_technique"])}
"""
    write(DOCS / "evidence" / "lab" / "index.html", page("Final Evidence", lab_body, "../../"))

    graph_body = f"""
<section class="hero">
  <span class="badge">Interactive Graph</span>
  <h1>{lang_span("Etkileşimli Kanıt Grafı", "Interactive Evidence Graph")}</h1>
  <p class="lead">{lang_span("Final kanıt grafındaki tüm düğüm ve ilişkileri etkileşimli olarak inceleyebilirsin.", "You can interactively inspect all nodes and relationships in the final evidence graph.")}</p>
</section>

<section class="stats">
  <div class="stat"><strong>{node_count}</strong><span>Nodes</span></div>
  <div class="stat"><strong>{edge_count}</strong><span>Edges</span></div>
  <div class="stat"><strong>{observed_edges}</strong><span>Observed</span></div>
  <div class="stat"><strong>{missing_edges}</strong><span>Missing</span></div>
</section>

<div class="graph-controls">
  <input id="q" placeholder="DC01, Wazuh, T1071, MISP..." />
  <select id="typeFilter"><option value="">All node types</option></select>
  <button id="fitBtn">Fit</button>
  <button id="resetBtn">Reset</button>
</div>

<div id="cy"></div>
<pre id="details">Select a node or edge.</pre>

<script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script>
<script src="assets/graph.js"></script>
"""
    write(DOCS / "graph.html", page("Evidence Graph", graph_body))

    write(DOCS / "assets" / "graph.js", GRAPH_JS)

    paper_body = f"""
<section class="hero">
  <span class="badge">Paper View</span>
  <h1>{lang_span("Makale Görünümü", "Paper View")}</h1>
  <p class="lead">{lang_span("Bu sayfa, makaleye aktarılabilecek sade ve tutarlı çıktı özetlerini içerir.", "This page contains clean and consistent output summaries that can be used in the paper.")}</p>
</section>

<section class="panel">
  <h2>Figure 1 — SACI Score Components</h2>
  <div class="score-grid">{score_cards}</div>
</section>

<section class="panel">
  <h2>Figure 2 — Evidence Graph Closure</h2>
  <section class="stats">
    <div class="stat"><strong>{node_count}</strong><span>Nodes</span></div>
    <div class="stat"><strong>{edge_count}</strong><span>Edges</span></div>
    <div class="stat"><strong>{observed_edges}</strong><span>Observed</span></div>
    <div class="stat"><strong>{missing_edges}</strong><span>Missing</span></div>
  </section>
</section>

<section class="panel">
  <h2>Figure 3 — Asset Coverage</h2>
  {table(assets, ["asset_id","hostname","expected_sources","received_sources","coverage_percent","criticality"])}
</section>
"""
    write(DOCS / "evidence" / "paper_clean" / "index.html", page("Paper View", paper_body, "../../"))

    if reasons:
        reason_part = table(reasons, ["reason_code","metric","impact","fields_json"])
    else:
        reason_part = f'<section class="note"><p>{lang_span("Final kapanışta aktif reason code yoktur; bu, final kapsam içinde aktif metrik boşluğu raporlanmadığı anlamına gelir.", "There are no active reason codes in final closure; this means no active metric gap is reported within the final scope.")}</p></section>'

    exp_body = f"""
<section class="hero">
  <span class="badge">Policy-Guided Explanation</span>
  <h1>{lang_span("Açıklama Raporu", "Explanation Report")}</h1>
  <p class="lead">{lang_span("Bu rapor serbest LLM çıktısı değildir. Deterministik SACI sonuçlarını policy-guided açıklama katmanına dönüştürür.", "This report is not a free-form LLM output. It transforms deterministic SACI results into a policy-guided explanation layer.")}</p>
</section>

<section class="panel">
  <h2>Executive Summary</h2>
  <p>{lang_span(f"Final skor {saci}; graph closure {observed_edges}/{edge_count}; missing edge {missing_edges}.", f"Final score is {saci}; graph closure is {observed_edges}/{edge_count}; missing edges: {missing_edges}.")}</p>
</section>

<section class="panel">
  <h2>Metric Explanation</h2>
  {table(scores, ["metric","name","weight","score","applicable"])}
</section>

<section class="panel">
  <h2>Reason Codes</h2>
  {reason_part}
</section>

<section class="panel">
  <h2>Controlled Wording</h2>
  <pre>SACI=100 sonucu kurumun güvenli olduğunu göstermez.
Bu sonuç, yalnızca tanımlı değerlendirme kapsamındaki beklenen görünürlük ilişkilerinin gözlemlendiğini ve kanıt grafında kapandığını ifade eder.
Açıklama katmanı skoru değiştirmez; deterministic SACI çıktısını açıklanabilir rapora dönüştürür.</pre>
</section>
"""
    write(DOCS / "evidence" / "explanation_report.html", page("Explanation Report", exp_body, "../"))

    print("=== CLEAN SACI FINAL SITE GENERATED ===")
    print("SACI:", saci)
    print("CWLC:", cwlc, "CAC:", cac, "MDC:", mdc, "CTIC:", ctic_score, "TF:", tf)
    print("Nodes:", node_count)
    print("Edges:", edge_count)
    print("Observed:", observed_edges)
    print("Missing:", missing_edges)
    print("Docs:", DOCS)

CSS = r'''
:root {
  --bg: #060a18;
  --panel: #111827;
  --panel2: #162033;
  --line: #334155;
  --text: #e5e7eb;
  --muted: #b8d6ff;
  --soft: #94a3b8;
  --blue: #60a5fa;
  --green: #86efac;
  --red: #fca5a5;
  --yellow: #fde68a;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background:
    radial-gradient(circle at top left, rgba(37,99,235,.20), transparent 34rem),
    linear-gradient(135deg, #050816 0%, #070b1a 50%, #020617 100%);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  line-height: 1.6;
}

a { color: #93c5fd; text-decoration: none; }

.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(7, 11, 26, .92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(71,85,105,.6);
}

.nav {
  max-width: 1220px;
  margin: 0 auto;
  padding: 14px 22px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text);
  font-weight: 900;
}

.brand-dot {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  background: #22c55e;
  box-shadow: 0 0 18px rgba(34,197,94,.9);
}

.nav-right {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.nav-links {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.nav-links a, .lang-switch button {
  border: 1px solid rgba(96,165,250,.35);
  background: rgba(15,23,42,.82);
  color: #dbeafe;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 800;
}

.lang-switch {
  display: flex;
  gap: 6px;
  border: 1px solid rgba(96,165,250,.28);
  padding: 4px;
  border-radius: 999px;
  background: rgba(15,23,42,.70);
}

.lang-switch button {
  cursor: pointer;
  padding: 7px 11px;
}

.lang-switch button.active {
  background: #2563eb;
  color: #fff;
  border-color: #60a5fa;
}

.shell {
  max-width: 1220px;
  margin: 0 auto;
  padding: 34px 22px 70px;
}

.hero {
  padding: 18px 0 30px;
  margin-bottom: 28px;
  border-bottom: 1px solid rgba(71,85,105,.55);
}

.badge {
  display: inline-flex;
  padding: 7px 14px;
  border: 1px solid rgba(96,165,250,.55);
  background: rgba(37,99,235,.13);
  color: #dbeafe;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 900;
}

h1 {
  margin: 18px 0 16px;
  font-size: clamp(36px, 5vw, 64px);
  line-height: 1.05;
  letter-spacing: -.05em;
}

h2 {
  margin: 30px 0 14px;
  font-size: clamp(24px, 3vw, 36px);
  letter-spacing: -.03em;
}

h3 {
  margin: 0 0 10px;
  color: #93c5fd;
  font-size: 21px;
  line-height: 1.2;
}

.lead {
  max-width: 900px;
  color: var(--muted);
  font-size: 20px;
  margin: 0;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 18px;
}

.card, .panel, .note, .table-card, .score-card, .stat {
  border: 1px solid rgba(71,85,105,.78);
  background: rgba(17,24,39,.88);
  border-radius: 20px;
  box-shadow: 0 18px 50px rgba(0,0,0,.16);
}

.card {
  display: flex;
  flex-direction: column;
  min-height: 170px;
  padding: 22px;
  color: var(--text);
}

.card p {
  margin: 0;
  color: var(--muted);
}

.card:hover {
  border-color: rgba(96,165,250,.95);
  background: rgba(30,41,59,.92);
  transform: translateY(-2px);
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 14px;
  margin: 22px 0;
}

.stat {
  padding: 20px;
}

.stat strong {
  display: block;
  color: var(--green);
  font-size: 32px;
  line-height: 1;
  margin-bottom: 8px;
}

.stat span {
  color: var(--muted);
  font-size: 14px;
}

.note, .panel {
  padding: 22px;
  margin: 20px 0;
}

.note {
  border-color: rgba(251,191,36,.55);
  background: rgba(251,191,36,.08);
}

.mini-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px,1fr));
  gap: 14px;
}

.mini {
  border: 1px solid rgba(96,165,250,.32);
  border-radius: 16px;
  padding: 14px;
  background: rgba(15,23,42,.88);
}

.mini b {
  display: block;
  color: #93c5fd;
  margin-bottom: 6px;
}

.mini span {
  color: var(--muted);
}

.flow {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px,1fr));
  gap: 14px;
}

.flow div {
  border: 1px solid rgba(96,165,250,.32);
  border-radius: 16px;
  padding: 16px;
  background: rgba(15,23,42,.88);
}

.flow b {
  display: block;
  color: #93c5fd;
  font-size: 28px;
}

.flow span {
  color: var(--muted);
}

.score-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px,1fr));
  gap: 14px;
  margin: 22px 0;
}

.score-card {
  padding: 18px;
}

.score-card div:first-child {
  min-height: 58px;
}

.score-card b {
  display: block;
  color: #93c5fd;
}

.score-card span {
  display: block;
  color: var(--muted);
  font-size: 13px;
}

.score-card strong {
  display: block;
  color: var(--green);
  font-size: 34px;
  margin: 10px 0;
}

.bar {
  height: 10px;
  background: rgba(71,85,105,.8);
  border-radius: 999px;
  overflow: hidden;
}

.bar i {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #22c55e);
}

.table-card {
  padding: 16px;
  overflow-x: auto;
  margin: 16px 0 28px;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 760px;
}

th, td {
  padding: 10px 12px;
  border-bottom: 1px solid rgba(71,85,105,.65);
  text-align: left;
  vertical-align: top;
}

th {
  color: #bfdbfe;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: .06em;
}

td {
  color: #dbeafe;
}

.pill {
  display: inline-flex;
  border-radius: 999px;
  padding: 3px 9px;
  font-size: 12px;
  font-weight: 900;
}

.pill.ok {
  color: #bbf7d0;
  border: 1px solid rgba(34,197,94,.45);
  background: rgba(34,197,94,.14);
}

.pill.bad {
  color: #fecaca;
  border: 1px solid rgba(248,113,113,.45);
  background: rgba(248,113,113,.13);
}

.graph-controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 18px 0;
}

.graph-controls input, .graph-controls select, .graph-controls button {
  background: rgba(15,23,42,.95);
  border: 1px solid rgba(96,165,250,.35);
  color: var(--text);
  border-radius: 999px;
  padding: 10px 13px;
}

#cy {
  width: 100%;
  height: 760px;
  border: 1px solid rgba(71,85,105,.85);
  border-radius: 20px;
  background: #030712;
}

pre {
  background: #020617;
  border: 1px solid rgba(71,85,105,.85);
  border-radius: 16px;
  color: #dbeafe;
  padding: 16px;
  overflow: auto;
  white-space: pre-wrap;
}

.footer {
  margin-top: 42px;
  padding-top: 18px;
  border-top: 1px solid rgba(71,85,105,.55);
  color: var(--soft);
  font-size: 13px;
}

@media (max-width: 900px) {
  .nav {
    align-items: flex-start;
    flex-direction: column;
  }

  .nav-right {
    align-items: flex-start;
    justify-content: flex-start;
  }

  #cy {
    height: 620px;
  }
}
'''

JS = r'''
(function () {
  function setLang(lang) {
    localStorage.setItem("saci-lang", lang);
    document.documentElement.lang = lang === "en" ? "en" : "tr";

    document.querySelectorAll("[data-tr][data-en]").forEach(function (el) {
      el.textContent = lang === "en" ? el.getAttribute("data-en") : el.getAttribute("data-tr");
    });

    document.querySelectorAll("[data-lang]").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-lang") === lang);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-lang]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        setLang(btn.getAttribute("data-lang"));
      });
    });

    setLang(localStorage.getItem("saci-lang") || "tr");
  });
})();
'''

GRAPH_JS = r'''
function colorFor(type) {
  return {
    asset: "#60a5fa",
    log_source: "#22c55e",
    control: "#fbbf24",
    wazuh_rule: "#a78bfa",
    mitre_technique: "#fb7185",
    cti_object: "#2dd4bf",
    platform: "#93c5fd",
    integration: "#c084fc",
    metric: "#86efac",
    score: "#34d399",
    reason_code: "#f97316",
    external: "#94a3b8"
  }[type] || "#94a3b8";
}

const details = document.getElementById("details");
let cy;

fetch("data/final/saci_graph.cyjs")
  .then(r => r.json())
  .then(data => {
    const nodes = data.elements.nodes || [];
    const edges = data.elements.edges || [];
    const ids = new Set(nodes.map(n => n.data.id));

    edges.forEach(e => {
      ["source", "target"].forEach(k => {
        const id = e.data[k];
        if (id && !ids.has(id)) {
          ids.add(id);
          nodes.push({data: {id, label: id, type: "external"}});
        }
      });
    });

    const types = [...new Set(nodes.map(n => n.data.type || "unknown"))].sort();
    const typeFilter = document.getElementById("typeFilter");
    types.forEach(t => {
      const o = document.createElement("option");
      o.value = t;
      o.textContent = t;
      typeFilter.appendChild(o);
    });

    cy = cytoscape({
      container: document.getElementById("cy"),
      elements: [...nodes, ...edges],
      wheelSensitivity: 0.18,
      style: [
        {
          selector: "node",
          style: {
            "background-color": ele => colorFor(ele.data("type")),
            "label": ele => ele.data("label") || ele.data("id"),
            "color": "#e5e7eb",
            "font-size": 10,
            "text-outline-width": 2,
            "text-outline-color": "#020617",
            "width": 23,
            "height": 23
          }
        },
        {
          selector: "edge",
          style: {
            "width": 1.4,
            "line-color": ele => Number(ele.data("observed")) === 1 ? "#64748b" : "#ef4444",
            "target-arrow-color": ele => Number(ele.data("observed")) === 1 ? "#64748b" : "#ef4444",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            "label": ele => ele.data("relationship") || "",
            "font-size": 8,
            "color": "#bfdbfe",
            "text-background-color": "#020617",
            "text-background-opacity": 0.85,
            "text-background-padding": 2
          }
        },
        { selector: ".faded", style: { opacity: .12 } },
        { selector: ":selected", style: { "border-width": 3, "border-color": "#fff", "line-color": "#60a5fa", "target-arrow-color": "#60a5fa" } }
      ],
      layout: { name: "cose", animate: false, idealEdgeLength: 115, nodeRepulsion: 6500, edgeElasticity: 80, numIter: 1200 }
    });

    cy.on("tap", "node, edge", evt => {
      details.textContent = JSON.stringify(evt.target.data(), null, 2);
    });

    function applyFilter() {
      const q = document.getElementById("q").value.toLowerCase().trim();
      const t = document.getElementById("typeFilter").value;

      cy.elements().removeClass("faded");

      if (!q && !t) return;

      cy.nodes().forEach(n => {
        const hay = JSON.stringify(n.data()).toLowerCase();
        const okQ = !q || hay.includes(q);
        const okT = !t || n.data("type") === t;
        if (!(okQ && okT)) n.addClass("faded");
      });

      cy.edges().forEach(e => {
        if (e.source().hasClass("faded") || e.target().hasClass("faded")) e.addClass("faded");
      });
    }

    document.getElementById("q").addEventListener("input", applyFilter);
    document.getElementById("typeFilter").addEventListener("change", applyFilter);
    document.getElementById("fitBtn").onclick = () => cy.fit(null, 40);
    document.getElementById("resetBtn").onclick = () => {
      document.getElementById("q").value = "";
      document.getElementById("typeFilter").value = "";
      cy.elements().removeClass("faded");
      cy.fit(null, 40);
    };

    cy.fit(null, 40);
  })
  .catch(err => {
    details.textContent = "Graph yüklenemedi: " + err;
  });
'''

if __name__ == "__main__":
    main()
