#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a clean GitHub Pages site for the SACI Final Evidence Package.
Run from repository root after extracting saci_final_seed_current.zip to _saci_final_seed.

Expected source:
  _saci_final_seed/data/final/*.csv|*.json|*.cyjs|*.md
  _saci_final_seed/code/*.py|*.sh

Output:
  docs/ clean static site
"""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path.cwd()
SOURCE = ROOT / "_saci_final_seed" / "data" / "final"
SOURCE_CODE = ROOT / "_saci_final_seed" / "code"
DOCS = ROOT / "docs"
BACKUP_ROOT = ROOT / "_local_backups"

REQUIRED = [
    "asset_log_coverage.csv",
    "control_coverage.csv",
    "ctic_coverage.csv",
    "log_source_status.csv",
    "mitre_coverage.csv",
    "reason_codes.csv",
    "reason_codes.json",
    "saci_edges.csv",
    "saci_graph.cyjs",
    "saci_graph.mmd",
    "saci_graph_summary.md",
    "saci_nodes.csv",
    "saci_scores.csv",
    "saci_scores.json",
]


def fail(message: str) -> None:
    raise SystemExit("[!] " + message)


def ensure_source() -> None:
    if not SOURCE.exists():
        fail(
            f"Final veri klasörü yok: {SOURCE}\n"
            "Önce şu komutu çalıştır:\n"
            "  rm -rf _saci_final_seed && mkdir -p _saci_final_seed\n"
            "  unzip -o saci_final_seed_current.zip -d _saci_final_seed"
        )
    missing = [name for name in REQUIRED if not (SOURCE / name).exists()]
    if missing:
        fail("Eksik final dosyalar:\n" + "\n".join("  - " + m for m in missing))


def read_csv(name: str) -> List[Dict[str, str]]:
    with (SOURCE / name).open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def esc(value) -> str:
    return str("" if value is None else value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def fmt(value) -> str:
    try:
        f = float(value)
        return str(int(f)) if f.is_integer() else f"{f:.2f}"
    except Exception:
        return str("" if value is None else value)


def get_score(scores: List[Dict[str, str]], metric: str) -> str:
    for row in scores:
        if row.get("metric") == metric:
            return row.get("score", "")
    return ""


def tr_en(tr: str, en: str) -> str:
    return f'<span data-tr="{esc(tr)}" data-en="{esc(en)}">{esc(tr)}</span>'


def status_pill(value: str) -> str:
    s = str(value).strip()
    if s in {"1", "1.0", "100", "100.0", "true", "True"}:
        return '<span class="pill ok">OK</span>'
    if s in {"0", "0.0", "", "false", "False"}:
        return '<span class="pill no">NO</span>'
    return esc(value)


def make_table(rows: List[Dict[str, str]], columns: Iterable[str]) -> str:
    columns = list(columns)
    out = ['<div class="table-wrap"><table><thead><tr>']
    for col in columns:
        out.append(f"<th>{esc(col)}</th>")
    out.append("</tr></thead><tbody>")
    bool_columns = {
        "observed", "seen", "covered", "enabled", "expected",
        "lookup_executed", "misp_hit", "wazuh_alert", "mapped_to_mitre",
        "applicable", "coverage_applicable", "expected_lookup",
    }
    numeric_columns = {
        "score", "weight", "coverage_percent", "criticality", "priority",
        "asset_criticality", "source_weight", "impact",
    }
    for row in rows:
        out.append("<tr>")
        for col in columns:
            val = row.get(col, "")
            if col in bool_columns:
                out.append(f"<td>{status_pill(val)}</td>")
            elif col in numeric_columns:
                out.append(f"<td><b>{esc(fmt(val))}</b></td>")
            else:
                out.append(f"<td>{esc(val)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def nav(prefix: str = "") -> str:
    return f'''
<header class="topbar">
  <nav class="nav">
    <a class="brand" href="{prefix}index.html"><span class="dot"></span><span>SACI Final Evidence</span></a>
    <div class="nav-right">
      <div class="nav-links">
        <a href="{prefix}index.html">{tr_en("Ana Portal", "Main Portal")}</a>
        <a href="{prefix}methodology.html">{tr_en("Yöntem", "Methodology")}</a>
        <a href="{prefix}architecture.html">{tr_en("Mimari", "Architecture")}</a>
        <a href="{prefix}evidence.html">{tr_en("Kanıt", "Evidence")}</a>
        <a href="{prefix}graph.html">{tr_en("Graf", "Graph")}</a>
        <a href="{prefix}paper.html">{tr_en("Makale", "Paper")}</a>
        <a href="{prefix}explanation.html">{tr_en("Açıklama", "Explanation")}</a>
      </div>
      <div class="lang"><button type="button" data-lang="tr">TR</button><button type="button" data-lang="en">EN</button></div>
    </div>
  </nav>
</header>
'''


def page(title: str, body: str, prefix: str = "") -> str:
    return f'''<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{prefix}assets/app.css">
</head>
<body>
{nav(prefix)}
<main class="shell">
{body}
<footer class="footer">
  {tr_en("SACI=100 güvenlik garantisi değildir; yalnızca beyan edilen kapsam içindeki beklenen görünürlük ilişkilerinin kapandığını ifade eder.", "SACI=100 is not a security guarantee; it only indicates that expected visibility relationships within the declared scope were closed.")}
</footer>
</main>
<script src="{prefix}assets/app.js"></script>
</body>
</html>
'''


CSS = r'''
:root{--bg:#060a18;--panel:#111827;--panel2:#182235;--line:#334155;--text:#e5e7eb;--muted:#b8d6ff;--soft:#94a3b8;--blue:#60a5fa;--green:#86efac;--red:#fca5a5;--yellow:#fde68a}*{box-sizing:border-box}body{margin:0;color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;line-height:1.6;background:radial-gradient(circle at top left,rgba(37,99,235,.20),transparent 32rem),linear-gradient(135deg,#050816,#070b1a 50%,#020617)}a{text-decoration:none;color:#93c5fd}.topbar{position:sticky;top:0;z-index:50;background:rgba(7,11,26,.92);backdrop-filter:blur(12px);border-bottom:1px solid rgba(71,85,105,.65)}.nav{max-width:1240px;margin:0 auto;padding:14px 22px;display:flex;justify-content:space-between;align-items:center;gap:18px}.brand{display:flex;align-items:center;gap:10px;color:var(--text);font-weight:900}.dot{width:12px;height:12px;border-radius:999px;background:#22c55e;box-shadow:0 0 18px rgba(34,197,94,.9)}.nav-right{display:flex;gap:12px;align-items:center;flex-wrap:wrap;justify-content:flex-end}.nav-links{display:flex;gap:8px;flex-wrap:wrap}.nav-links a,.lang button{border:1px solid rgba(96,165,250,.35);background:rgba(15,23,42,.82);color:#dbeafe;padding:8px 12px;border-radius:999px;font-size:13px;font-weight:800}.lang{display:flex;gap:6px;border:1px solid rgba(96,165,250,.28);padding:4px;border-radius:999px;background:rgba(15,23,42,.70)}.lang button{cursor:pointer;padding:7px 11px}.lang button.active{background:#2563eb;color:#fff;border-color:#60a5fa}.shell{max-width:1240px;margin:0 auto;padding:38px 22px 76px}.hero{padding:18px 0 30px;margin-bottom:26px;border-bottom:1px solid rgba(71,85,105,.58)}.badge{display:inline-flex;padding:7px 14px;border:1px solid rgba(96,165,250,.55);background:rgba(37,99,235,.13);color:#dbeafe;border-radius:999px;font-size:13px;font-weight:900}h1{font-size:clamp(38px,5vw,66px);line-height:1.04;letter-spacing:-.055em;margin:18px 0 16px}h2{font-size:clamp(25px,3vw,36px);letter-spacing:-.03em;margin:34px 0 14px}h3{margin:0 0 10px;color:#93c5fd;font-size:21px;line-height:1.2}.lead{max-width:920px;color:var(--muted);font-size:20px;margin:0}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:18px}.card,.panel,.note,.stat,.score-card,.table-wrap{border:1px solid rgba(71,85,105,.78);background:rgba(17,24,39,.88);border-radius:20px;box-shadow:0 18px 50px rgba(0,0,0,.16)}.card{min-height:174px;padding:22px;color:var(--text);display:flex;flex-direction:column}.card p{margin:0;color:var(--muted)}.card:hover{border-color:rgba(96,165,250,.95);background:rgba(30,41,59,.93);transform:translateY(-2px)}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:22px 0}.stat{padding:20px}.stat strong{display:block;color:var(--green);font-size:34px;line-height:1;margin-bottom:8px}.stat span{color:var(--muted);font-size:14px}.panel,.note{padding:22px;margin:20px 0}.note{border-color:rgba(251,191,36,.55);background:rgba(251,191,36,.08)}.mini-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.mini{border:1px solid rgba(96,165,250,.32);border-radius:16px;padding:14px;background:rgba(15,23,42,.88)}.mini b{display:block;color:#93c5fd;margin-bottom:6px}.mini span{color:var(--muted)}.flow{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px}.flow div{border:1px solid rgba(96,165,250,.32);border-radius:16px;padding:16px;background:rgba(15,23,42,.88)}.flow b{display:block;color:#93c5fd;font-size:28px}.flow span{color:var(--muted)}.score-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:22px 0}.score-card{padding:18px}.score-card b{display:block;color:#93c5fd}.score-card span{display:block;color:var(--muted);font-size:13px}.score-card strong{display:block;color:var(--green);font-size:34px;margin:10px 0}.bar{height:10px;background:rgba(71,85,105,.8);border-radius:999px;overflow:hidden}.bar i{display:block;height:100%;background:linear-gradient(90deg,#2563eb,#22c55e)}.table-wrap{padding:16px;overflow-x:auto;margin:16px 0 28px}table{width:100%;border-collapse:collapse;min-width:760px}th,td{padding:10px 12px;border-bottom:1px solid rgba(71,85,105,.65);text-align:left;vertical-align:top}th{color:#bfdbfe;text-transform:uppercase;font-size:12px;letter-spacing:.06em}td{color:#dbeafe}.pill{display:inline-flex;border-radius:999px;padding:3px 9px;font-size:12px;font-weight:900}.pill.ok{color:#bbf7d0;border:1px solid rgba(34,197,94,.45);background:rgba(34,197,94,.14)}.pill.no{color:#fecaca;border:1px solid rgba(248,113,113,.45);background:rgba(248,113,113,.13)}.graph-controls{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}.graph-controls input,.graph-controls select,.graph-controls button{background:rgba(15,23,42,.95);border:1px solid rgba(96,165,250,.35);color:var(--text);border-radius:999px;padding:10px 13px}#cy{width:100%;height:760px;border:1px solid rgba(71,85,105,.85);border-radius:20px;background:#030712}pre{background:#020617;border:1px solid rgba(71,85,105,.85);border-radius:16px;color:#dbeafe;padding:16px;overflow:auto;white-space:pre-wrap}.footer{margin-top:42px;padding-top:18px;border-top:1px solid rgba(71,85,105,.55);color:var(--soft);font-size:13px}@media(max-width:900px){.nav{align-items:flex-start;flex-direction:column}.nav-right{align-items:flex-start;justify-content:flex-start}#cy{height:620px}}
'''

JS = r'''
(function(){function setLang(lang){localStorage.setItem("saci-lang",lang);document.documentElement.lang=lang==="en"?"en":"tr";document.querySelectorAll("[data-tr][data-en]").forEach(el=>{el.textContent=lang==="en"?el.getAttribute("data-en"):el.getAttribute("data-tr")});document.querySelectorAll("[data-lang]").forEach(btn=>{btn.classList.toggle("active",btn.getAttribute("data-lang")===lang)})}document.addEventListener("DOMContentLoaded",()=>{document.querySelectorAll("[data-lang]").forEach(btn=>btn.addEventListener("click",()=>setLang(btn.getAttribute("data-lang"))));setLang(localStorage.getItem("saci-lang")||"tr")})})();
'''

GRAPH_JS = r'''
function colorFor(type){return{asset:"#60a5fa",log_source:"#22c55e",control:"#fbbf24",wazuh_rule:"#a78bfa",mitre_technique:"#fb7185",cti_object:"#2dd4bf",platform:"#93c5fd",integration:"#c084fc",metric:"#86efac",score:"#34d399",reason_code:"#f97316",external:"#94a3b8"}[type]||"#94a3b8"}const details=document.getElementById("details");let cy;fetch("data/final/saci_graph.cyjs").then(r=>r.json()).then(data=>{const nodes=data.elements.nodes||[];const edges=data.elements.edges||[];const ids=new Set(nodes.map(n=>n.data.id));edges.forEach(e=>["source","target"].forEach(k=>{const id=e.data[k];if(id&&!ids.has(id)){ids.add(id);nodes.push({data:{id,label:id,type:"external"}})}}));const typeFilter=document.getElementById("typeFilter");[...new Set(nodes.map(n=>n.data.type||"unknown"))].sort().forEach(t=>{const o=document.createElement("option");o.value=t;o.textContent=t;typeFilter.appendChild(o)});cy=cytoscape({container:document.getElementById("cy"),elements:[...nodes,...edges],wheelSensitivity:.18,style:[{selector:"node",style:{"background-color":e=>colorFor(e.data("type")),label:e=>e.data("label")||e.data("id"),color:"#e5e7eb","font-size":10,"text-outline-width":2,"text-outline-color":"#020617",width:23,height:23}},{selector:"edge",style:{width:1.4,"line-color":e=>Number(e.data("observed"))===1?"#64748b":"#ef4444","target-arrow-color":e=>Number(e.data("observed"))===1?"#64748b":"#ef4444","target-arrow-shape":"triangle","curve-style":"bezier",label:e=>e.data("relationship")||"","font-size":8,color:"#bfdbfe","text-background-color":"#020617","text-background-opacity":.85,"text-background-padding":2}},{selector:".faded",style:{opacity:.12}},{selector:":selected",style:{"border-width":3,"border-color":"#fff","line-color":"#60a5fa","target-arrow-color":"#60a5fa"}}],layout:{name:"cose",animate:false,idealEdgeLength:115,nodeRepulsion:6500,edgeElasticity:80,numIter:1200}});cy.on("tap","node, edge",evt=>details.textContent=JSON.stringify(evt.target.data(),null,2));function applyFilter(){const q=document.getElementById("q").value.toLowerCase().trim();const t=document.getElementById("typeFilter").value;cy.elements().removeClass("faded");if(!q&&!t)return;cy.nodes().forEach(n=>{const hay=JSON.stringify(n.data()).toLowerCase();const okQ=!q||hay.includes(q);const okT=!t||n.data("type")===t;if(!(okQ&&okT))n.addClass("faded")});cy.edges().forEach(e=>{if(e.source().hasClass("faded")||e.target().hasClass("faded"))e.addClass("faded")})}document.getElementById("q").addEventListener("input",applyFilter);document.getElementById("typeFilter").addEventListener("change",applyFilter);document.getElementById("fitBtn").onclick=()=>cy.fit(null,40);document.getElementById("resetBtn").onclick=()=>{document.getElementById("q").value="";document.getElementById("typeFilter").value="";cy.elements().removeClass("faded");cy.fit(null,40)};cy.fit(null,40)}).catch(err=>details.textContent="Graph yüklenemedi: "+err);
'''


def build() -> None:
    ensure_source()

    scores = read_csv("saci_scores.csv")
    nodes = read_csv("saci_nodes.csv")
    edges = read_csv("saci_edges.csv")
    assets = read_csv("asset_log_coverage.csv")
    logs = read_csv("log_source_status.csv")
    controls = read_csv("control_coverage.csv")
    mitre = read_csv("mitre_coverage.csv")
    ctic = read_csv("ctic_coverage.csv")
    reasons = read_csv("reason_codes.csv")

    saci = get_score(scores, "SACI")
    cwlc = get_score(scores, "CWLC")
    cac = get_score(scores, "CAC")
    mdc = get_score(scores, "MDC")
    ctic_score = get_score(scores, "CTIC")
    tf = get_score(scores, "TF")

    node_count = len(nodes)
    edge_count = len(edges)
    observed_edges = sum(1 for e in edges if str(e.get("observed", "")).strip() in {"1", "1.0"})
    missing_edges = edge_count - observed_edges

    if DOCS.exists():
        BACKUP_ROOT.mkdir(exist_ok=True)
        backup = BACKUP_ROOT / f"docs_before_clean_rebuild_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree(DOCS, backup)
        shutil.rmtree(DOCS)
    else:
        backup = None

    (DOCS / "assets").mkdir(parents=True, exist_ok=True)
    (DOCS / "data" / "final").mkdir(parents=True, exist_ok=True)
    (DOCS / "code").mkdir(parents=True, exist_ok=True)

    for name in REQUIRED:
        shutil.copy2(SOURCE / name, DOCS / "data" / "final" / name)
    if SOURCE_CODE.exists():
        for p in SOURCE_CODE.iterdir():
            if p.is_file():
                shutil.copy2(p, DOCS / "code" / p.name)

    score_cards = "".join(
        f'<div class="score-card"><b>{esc(r.get("metric"))}</b><span>{esc(r.get("name"))}</span><strong>{fmt(r.get("score"))}</strong><div class="bar"><i style="width:{fmt(r.get("score"))}%"></i></div></div>'
        for r in scores
    )
    stats = f'''
<section class="stats">
  <div class="stat"><strong>{fmt(saci)}</strong><span>SACI</span></div>
  <div class="stat"><strong>{fmt(cwlc)}</strong><span>CWLC</span></div>
  <div class="stat"><strong>{observed_edges}/{edge_count}</strong><span>Observed Graph Relations</span></div>
  <div class="stat"><strong>{missing_edges}</strong><span>Missing Edges</span></div>
</section>'''

    index = f'''
<section class="hero"><span class="badge">SACI Final Evidence Package</span><h1>{tr_en("SACI Final Evidence Portalı", "SACI Final Evidence Portal")}</h1><p class="lead">{tr_en("Bu portal, SIEM telemetrisi, CTI entegrasyonu, MITRE ATT&CK kapsamı ve kanıt grafı kapanışını ölçen açıklanabilir SACI görünürlük skorlama modelinin final kanıt paketini yayınlar.", "This portal publishes the final evidence package for the explainable SACI visibility scoring model, which evaluates SIEM telemetry, CTI integration, MITRE ATT&CK coverage and evidence graph closure.")}</p></section>{stats}
<section class="cards">
<a class="card" href="methodology.html"><h3>{tr_en("Yöntem ve Hesaplama", "Methodology and Calculation")}</h3><p>{tr_en("Düzeltilmiş SACI yöntemi, N/A metrik normalizasyonu, CWLC, CTIC closure ve graph completeness mantığı.", "Corrected SACI method, N/A metric normalization, CWLC, CTIC closure and graph completeness logic.")}</p></a>
<a class="card" href="architecture.html"><h3>{tr_en("Mimari", "Architecture")}</h3><p>{tr_en("Wazuh, Windows, Linux, pfSense, MISP ve SACI katmanlarının sade mimari görünümü.", "Clean architecture view of Wazuh, Windows, Linux, pfSense, MISP and SACI layers.")}</p></a>
<a class="card" href="evidence.html"><h3>{tr_en("Final Kanıt", "Final Evidence")}</h3><p>{tr_en(f"SACI {saci}, {observed_edges}/{edge_count} observed relation ve {missing_edges} missing edge ile final kapanış.", f"Final closure with SACI {saci}, {observed_edges}/{edge_count} observed relations and {missing_edges} missing edges.")}</p></a>
<a class="card" href="graph.html"><h3>{tr_en("Etkileşimli Graf", "Interactive Graph")}</h3><p>{tr_en("Final kanıt grafını node, edge, ilişki ve tip filtreleriyle inceleme.", "Inspect the final evidence graph with node, edge, relationship and type filtering.")}</p></a>
<a class="card" href="paper.html"><h3>{tr_en("Makale Görünümü", "Paper View")}</h3><p>{tr_en("Makale için sade skor kartları ve kapsam tabloları.", "Clean score cards and coverage tables for the paper.")}</p></a>
<a class="card" href="explanation.html"><h3>{tr_en("Açıklama Raporu", "Explanation Report")}</h3><p>{tr_en("Serbest LLM yerine deterministik SACI sonuçlarını açıklayan policy-guided rapor.", "A policy-guided report explaining deterministic SACI results instead of free-form LLM text.")}</p></a>
</section>
<section class="note"><h2>{tr_en("Önemli yorumlama notu", "Important interpretation note")}</h2><p>{tr_en("SACI=100 ortamın güvenli olduğu anlamına gelmez. Yalnızca tanımlı değerlendirme kapsamındaki beklenen görünürlük ilişkilerinin gözlemlendiğini ve kapandığını ifade eder.", "SACI=100 does not mean that the environment is secure. It only means that expected visibility relationships within the declared evaluation scope were observed and closed.")}</p></section>'''

    methodology = f'''
<section class="hero"><span class="badge">Methodology</span><h1>{tr_en("Yöntem ve Hesaplama", "Methodology and Calculation")}</h1><p class="lead">{tr_en("Bu sayfa, final sitedeki verilerin hangi hesaplama mantığına dayandığını açıklar. Site hesaplamayı yeniden yapmaz; final SACI engine çıktısını yayımlar.", "This page explains the calculation logic behind the final data. The site does not recompute the score; it publishes the final SACI engine output.")}</p></section>
<section class="panel"><h2>SACI Formula</h2><pre>SACI = weighted_score(CWLC, CAC, MDC, CTIC, TF)

CWLC = criticality-weighted log coverage
CAC  = control / alert coverage
MDC  = MITRE detection coverage
CTIC = CTI / MISP enrichment closure
TF   = telemetry freshness</pre></section>
<section class="panel"><h2>{tr_en("Hakem eleştirilerine karşı düzeltmeler", "Fixes addressing reviewer concerns")}</h2><div class="mini-grid"><div class="mini"><b>N/A Metrics</b><span>{tr_en("Paydası 0 olan metrikler cezalandırılmaz; aktif ağırlıklarla normalize edilir.", "Metrics with zero denominator are not penalized; active weights are normalized.")}</span></div><div class="mini"><b>CWLC</b><span>{tr_en("Log kapsaması asset criticality ve log source ağırlığıyla hesaplanır.", "Log coverage is calculated using asset criticality and log source weights.")}</span></div><div class="mini"><b>CTIC</b><span>{tr_en("IOC lookup, MISP hit, Wazuh alert ve MITRE mapping zinciri ayrı izlenir.", "IOC lookup, MISP hit, Wazuh alert and MITRE mapping are tracked as staged closure.")}</span></div><div class="mini"><b>Graph Closure</b><span>{tr_en("Observed + missing = total edge ilişkisi kontrol edilir.", "The observed + missing = total edge relation is checked.")}</span></div><div class="mini"><b>Explanation</b><span>{tr_en("Açıklama katmanı skoru değiştirmez; deterministik çıktıyı açıklar.", "The explanation layer does not change the score; it explains deterministic outputs.")}</span></div></div></section>{stats}<section class="panel"><h2>Score Components</h2><div class="score-grid">{score_cards}</div></section>'''

    architecture = f'''
<section class="hero"><span class="badge">Architecture</span><h1>{tr_en("SACI Mimari Görünümü", "SACI Architecture View")}</h1><p class="lead">{tr_en("Bu sayfa, final kanıt paketinin veri kaynaklarını ve SACI değerlendirme akışını gösterir.", "This page shows the data sources and SACI evaluation flow of the final evidence package.")}</p></section><section class="panel"><h2>{tr_en("Uç Sistemler ve Kaynaklar", "Endpoints and Sources")}</h2><div class="mini-grid"><div class="mini"><b>DC01</b><span>Windows Security + Sysmon</span></div><div class="mini"><b>WS01</b><span>Security + Sysmon + PowerShell</span></div><div class="mini"><b>uhost</b><span>authlog + syslog + process</span></div><div class="mini"><b>pfSense</b><span>firewall syslog + IOC traffic</span></div><div class="mini"><b>MISP</b><span>IOC lookup + enrichment</span></div><div class="mini"><b>Wazuh</b><span>manager + rules + alerts</span></div></div></section><section class="panel"><h2>{tr_en("Ana Veri Akışı", "Main Data Flow")}</h2><div class="flow"><div><b>1</b><span>{tr_en("Telemetri üretimi", "Telemetry generation")}</span></div><div><b>2</b><span>Wazuh ingestion</span></div><div><b>3</b><span>{tr_en("Detection control eşleşmesi", "Detection control matching")}</span></div><div><b>4</b><span>SACI scoring</span></div><div><b>5</b><span>Evidence graph closure</span></div></div></section>'''

    evidence = f'''
<section class="hero"><span class="badge">Final Evidence</span><h1>{tr_en("Final Kanıt", "Final Evidence")}</h1><p class="lead">{tr_en("Bu sayfa final SACI çıktılarını, coverage tablolarını ve closure durumunu yayımlar.", "This page publishes final SACI outputs, coverage tables and closure status.")}</p></section>{stats}<section class="panel"><h2>Score Components</h2><div class="score-grid">{score_cards}</div></section><h2>Asset / Log Source Coverage</h2>{make_table(assets,["asset_id","hostname","expected_sources","received_sources","coverage_percent","criticality","coverage_applicable"])}<h2>Log Source Status</h2>{make_table(logs,["asset_id","hostname","log_source","expected","observed","asset_criticality","source_weight","last_seen"])}<h2>Control / Alert Coverage</h2>{make_table(controls,["control_id","asset_id","source","rule_id","mitre_technique","enabled","seen","weight","description"])}<h2>MITRE Coverage</h2>{make_table(mitre,["technique_id","technique_name","tactic","covered","priority"])}<h2>CTI Coverage</h2>{make_table(ctic,["indicator","type","lookup_executed","misp_hit","wazuh_alert","mapped_to_mitre","expected_alert_rule","mitre_technique"])}'''

    graph = f'''
<section class="hero"><span class="badge">Interactive Graph</span><h1>{tr_en("Etkileşimli Kanıt Grafı", "Interactive Evidence Graph")}</h1><p class="lead">{tr_en("Final kanıt grafındaki düğüm ve ilişkileri etkileşimli olarak inceleyebilirsin.", "You can interactively inspect nodes and relationships in the final evidence graph.")}</p></section>{stats}<div class="graph-controls"><input id="q" placeholder="DC01, Wazuh, T1071, MISP..." /><select id="typeFilter"><option value="">All node types</option></select><button id="fitBtn">Fit</button><button id="resetBtn">Reset</button></div><div id="cy"></div><pre id="details">Select a node or edge.</pre><script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script><script src="assets/graph.js"></script>'''

    paper = f'''
<section class="hero"><span class="badge">Paper View</span><h1>{tr_en("Makale Görünümü", "Paper View")}</h1><p class="lead">{tr_en("Bu sayfa, makale için kullanılabilecek sade ve tutarlı çıktı özetlerini içerir.", "This page contains clean and consistent output summaries for the paper.")}</p></section><section class="panel"><h2>Figure 1 — SACI Score Components</h2><div class="score-grid">{score_cards}</div></section><section class="panel"><h2>Figure 2 — Evidence Graph Closure</h2>{stats}</section><section class="panel"><h2>Figure 3 — Asset Coverage</h2>{make_table(assets,["asset_id","hostname","expected_sources","received_sources","coverage_percent","criticality"])}</section><section class="panel"><h2>Figure 4 — CTI Closure</h2>{make_table(ctic,["indicator","type","lookup_executed","misp_hit","wazuh_alert","mapped_to_mitre"])}</section>'''

    reason_part = make_table(reasons, ["reason_code", "metric", "impact", "fields_json"]) if reasons else f'<section class="note"><p>{tr_en("Final kapanışta aktif reason code yoktur; final kapsam içinde aktif metrik boşluğu raporlanmamıştır.", "There are no active reason codes in final closure; no active metric gap is reported within the final scope.")}</p></section>'
    explanation = f'''
<section class="hero"><span class="badge">Policy-Guided Explanation</span><h1>{tr_en("Açıklama Raporu", "Explanation Report")}</h1><p class="lead">{tr_en("Bu rapor serbest LLM çıktısı değildir. Deterministik SACI sonuçlarını policy-guided açıklama katmanına dönüştürür.", "This report is not a free-form LLM output. It transforms deterministic SACI results into a policy-guided explanation layer.")}</p></section>{stats}<section class="panel"><h2>Metric Explanation</h2>{make_table(scores,["metric","name","weight","score","applicable"])}</section><section class="panel"><h2>Reason Codes</h2>{reason_part}</section><section class="panel"><h2>Controlled Wording</h2><pre>SACI=100 sonucu kurumun güvenli olduğunu göstermez.
Bu sonuç, yalnızca tanımlı değerlendirme kapsamındaki beklenen görünürlük ilişkilerinin gözlemlendiğini ve kanıt grafında kapandığını ifade eder.
Açıklama katmanı skoru değiştirmez; deterministic SACI çıktısını açıklanabilir rapora dönüştürür.</pre></section>'''

    write(DOCS / "assets" / "app.css", CSS)
    write(DOCS / "assets" / "app.js", JS)
    write(DOCS / "assets" / "graph.js", GRAPH_JS)
    write(DOCS / ".nojekyll", "")

    write(DOCS / "index.html", page("SACI Final Evidence Portal", index))
    write(DOCS / "methodology.html", page("SACI Methodology", methodology))
    write(DOCS / "architecture.html", page("SACI Architecture", architecture))
    write(DOCS / "evidence.html", page("SACI Evidence", evidence))
    write(DOCS / "graph.html", page("SACI Graph", graph))
    write(DOCS / "paper.html", page("SACI Paper View", paper))
    write(DOCS / "explanation.html", page("SACI Explanation", explanation))

    validation = f"""SACI Final Evidence Validation

SACI: {saci}
CWLC: {cwlc}
CAC: {cac}
MDC: {mdc}
CTIC: {ctic_score}
TF: {tf}

Nodes: {node_count}
Edges: {edge_count}
Observed edges: {observed_edges}
Missing edges: {missing_edges}

SACI=100 does not indicate that the monitored environment is fully secure.
It indicates that all expected visibility relations defined within the declared evaluation scope were observed and closed.
"""
    write(DOCS / "data" / "VALIDATION.txt", validation)

    audit = f"""# SACI Final Audit Result

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

SACI=100 is not a security guarantee.
"""
    write(DOCS / "data" / "FINAL_AUDIT_RESULT.md", audit)

    readme = f"""# SACI Final Evidence Package

SACI is an explainable, graph-based SIEM visibility scoring model.

Public portal:

https://4rslanismet.github.io/saci-final-evidence/

## Final Evidence Summary

| Metric | Value |
|---|---:|
| CWLC | {cwlc} |
| CAC | {cac} |
| MDC | {mdc} |
| CTIC | {ctic_score} |
| TF | {tf} |
| SACI | {saci} |

## Final Graph Closure

| Item | Value |
|---|---:|
| Nodes | {node_count} |
| Edges | {edge_count} |
| Observed edges | {observed_edges} |
| Missing edges | {missing_edges} |

SACI=100 does not mean that the environment is fully secure. It means that all expected visibility relationships defined within the declared evaluation scope were observed and closed.
"""
    write(ROOT / "README.md", readme)

    print("=== CLEAN SACI SITE BUILD DONE ===")
    print("Source:", SOURCE)
    print("Backup:", backup if backup else "no previous docs")
    print("SACI:", saci)
    print("CWLC:", cwlc, "CAC:", cac, "MDC:", mdc, "CTIC:", ctic_score, "TF:", tf)
    print("Nodes:", node_count)
    print("Edges:", edge_count)
    print("Observed:", observed_edges)
    print("Missing:", missing_edges)


if __name__ == "__main__":
    build()
