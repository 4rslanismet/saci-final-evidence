#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / "docs"
EN = DOCS / "en"
ASSETS = DOCS / "assets"
SCENARIO_DST = DOCS / "evidence" / "data"
FINAL_DST = DOCS / "evidence" / "lab" / "final"
TR_MANIFEST = DOCS / "data" / "scenarios" / "manifest.json"
EN_MANIFEST = EN / "data" / "scenarios" / "manifest.json"

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

TR_SCENARIO_NAMES = {
    "S0_no_siem": "S0 — SIEM yok",
    "S1_siem_deployed": "S1 — SIEM kuruldu",
    "S2_inventory_defined": "S2 — Envanter tanımlandı",
    "S3_log_sources_connected": "S3 — Log kaynakları bağlandı",
    "S4_detection_controls_enabled": "S4 — Detection kontrolleri etkin",
    "S5_mitre_scope_defined": "S5 — MITRE kapsamı tanımlı",
    "S6_cti_enrichment_enabled": "S6 — CTI enrichment etkin",
    "S7_partial_closure": "S7 — Kısmi kapanış",
    "S7A_critical_dc01_sysmon_loss": "S7A — Kritik DC01 Sysmon kaybı",
    "S7B_noncritical_ws01_sysmon_loss": "S7B — Kritik olmayan WS01 Sysmon kaybı",
    "S8_final_closure": "S8 — Final kapanış",
    "S9_critical_dc01_security_loss": "S9 — Kritik DC01 Security kaybı",
    "S10_endpoint_powershell_loss": "S10 — Endpoint PowerShell kaybı",
    "S11_linux_authlog_loss": "S11 — Linux authlog kaybı",
    "S12_firewall_ioc_without_cti": "S12 — CTI olmadan firewall IOC",
    "S13_misp_lookup_without_ioc_hit": "S13 — IOC hit olmadan MISP lookup",
    "S14_mitre_scope_expansion_gap": "S14 — MITRE kapsam genişleme boşluğu",
    "S15_freshness_decay": "S15 — Freshness düşüşü",
    "S16_detection_rule_gap": "S16 — Detection rule boşluğu",
    "S17_recovery_after_fix": "S17 — Düzeltme sonrası toparlanma",
    "S18_legacy_control_out_of_scope": "S18 — Legacy kontrol kapsam dışı",
}

EN_SCENARIO_NAMES = {
    "S0_no_siem": "S0 — No SIEM",
    "S1_siem_deployed": "S1 — SIEM deployed",
    "S2_inventory_defined": "S2 — Inventory defined",
    "S3_log_sources_connected": "S3 — Log sources connected",
    "S4_detection_controls_enabled": "S4 — Detection controls enabled",
    "S5_mitre_scope_defined": "S5 — MITRE scope defined",
    "S6_cti_enrichment_enabled": "S6 — CTI enrichment enabled",
    "S7_partial_closure": "S7 — Partial closure",
    "S7A_critical_dc01_sysmon_loss": "S7A — Critical DC01 Sysmon loss",
    "S7B_noncritical_ws01_sysmon_loss": "S7B — Non-critical WS01 Sysmon loss",
    "S8_final_closure": "S8 — Final closure",
    "S9_critical_dc01_security_loss": "S9 — Critical DC01 Security loss",
    "S10_endpoint_powershell_loss": "S10 — Endpoint PowerShell loss",
    "S11_linux_authlog_loss": "S11 — Linux authlog loss",
    "S12_firewall_ioc_without_cti": "S12 — Firewall IOC without CTI",
    "S13_misp_lookup_without_ioc_hit": "S13 — MISP lookup without IOC hit",
    "S14_mitre_scope_expansion_gap": "S14 — MITRE scope expansion gap",
    "S15_freshness_decay": "S15 — Freshness decay",
    "S16_detection_rule_gap": "S16 — Detection rule gap",
    "S17_recovery_after_fix": "S17 — Recovery after fix",
    "S18_legacy_control_out_of_scope": "S18 — Legacy control out of scope",
}


def natural_scenario_key(name: str):
    m = re.match(r"^S(\d+)([A-Za-z]?)_", name)
    if not m:
        return (999, "", name)
    return (int(m.group(1)), m.group(2).upper(), name)


def find_scenario_source() -> Path | None:
    candidates = []

    if SCENARIO_DST.exists():
        count = len([p for p in SCENARIO_DST.iterdir() if p.is_dir() and (p / "saci_graph.cyjs").exists()])
        if count:
            candidates.append((count, SCENARIO_DST))

    for pattern in [
        "docs_backup_*/evidence/data",
        "backups/**/evidence/data",
        "_local_backups/**/evidence/data",
    ]:
        for p in ROOT.glob(pattern):
            if not p.is_dir():
                continue
            count = len([x for x in p.iterdir() if x.is_dir() and (x / "saci_graph.cyjs").exists()])
            if count:
                candidates.append((count, p))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def restore_scenarios() -> int:
    source = find_scenario_source()
    if source is None:
        return 0

    SCENARIO_DST.mkdir(parents=True, exist_ok=True)
    copied = 0

    for src in sorted(source.iterdir(), key=lambda p: natural_scenario_key(p.name)):
        if not src.is_dir() or not re.match(r"^S\d+[A-Za-z]?_", src.name):
            continue
        if not (src / "saci_graph.cyjs").exists():
            continue

        dst = SCENARIO_DST / src.name
        if src.resolve() != dst.resolve():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        copied += 1

    return copied


def restore_final() -> None:
    candidates = [
        ROOT / "_saci_final_seed" / "data" / "final",
        DOCS / "evidence" / "lab" / "final_v2",
        DOCS / "evidence" / "lab" / "final",
    ]

    source = next(
        (
            p for p in candidates
            if p.exists()
            and ((p / "saci_graph.cyjs").exists() or (p / "saci_graph_v2.cyjs").exists())
        ),
        None,
    )
    if source is None:
        raise SystemExit(
            "[!] Final graph kaynağı bulunamadı. "
            "_saci_final_seed/data/final veya docs/evidence/lab/final(_v2) gerekli."
        )

    FINAL_DST.mkdir(parents=True, exist_ok=True)

    mapping = {
        "saci_graph.cyjs": ["saci_graph.cyjs", "saci_graph_v2.cyjs"],
        "saci_nodes.csv": ["saci_nodes.csv", "saci_nodes_v2.csv"],
        "saci_edges.csv": ["saci_edges.csv", "saci_edges_v2.csv"],
        "saci_scores.csv": ["saci_scores.csv", "saci_scores_v2.csv"],
        "mitre_coverage.csv": ["mitre_coverage.csv", "mitre_coverage_v2.csv"],
        "saci_graph_summary.md": ["saci_graph_summary.md", "saci_graph_summary_v2.md"],
        "control_coverage.csv": ["control_coverage.csv", "control_coverage_v2.csv"],
        "asset_log_coverage.csv": ["asset_log_coverage.csv", "asset_log_coverage_v2.csv"],
        "ctic_coverage.csv": ["ctic_coverage.csv", "ctic_coverage_v2.csv"],
        "log_source_status.csv": ["log_source_status.csv"],
        "reason_codes.csv": ["reason_codes.csv", "reason_codes_v2.csv"],
        "reason_codes.json": ["reason_codes.json", "reason_codes_v2.json"],
    }

    for dst_name, src_names in mapping.items():
        src = next((source / n for n in src_names if (source / n).exists()), None)
        if src is not None:
            shutil.copy2(src, FINAL_DST / dst_name)


def rel(path: Path) -> str:
    return path.relative_to(DOCS).as_posix()


def dataset_entry(base: Path, sid: str, label_tr: str, label_en: str, kind: str):
    if not (base / "saci_graph.cyjs").exists():
        return None

    def maybe(name: str):
        p = base / name
        return rel(p) if p.exists() else ""

    return {
        "id": sid,
        "label_tr": label_tr,
        "label_en": label_en,
        "kind": kind,
        "graph": maybe("saci_graph.cyjs"),
        "nodes": maybe("saci_nodes.csv"),
        "edges": maybe("saci_edges.csv"),
        "scores": maybe("saci_scores.csv"),
        "mitre": maybe("mitre_coverage.csv"),
        "summary": maybe("saci_graph_summary.md"),
        "controls": maybe("control_coverage.csv"),
        "assets": maybe("asset_log_coverage.csv"),
        "ctic": maybe("ctic_coverage.csv"),
    }


def make_manifests() -> int:
    entries = []

    final = dataset_entry(
        FINAL_DST,
        "final_v2",
        "final-v2 — Kanonik yayın anlık görüntüsü",
        "final-v2 — Canonical publication snapshot",
        "canonical",
    )
    if final:
        entries.append(final)

    if SCENARIO_DST.exists():
        for d in sorted(
            [p for p in SCENARIO_DST.iterdir() if p.is_dir()],
            key=lambda p: natural_scenario_key(p.name),
        ):
            if not re.match(r"^S\d+[A-Za-z]?_", d.name):
                continue
            tr = TR_SCENARIO_NAMES.get(d.name, d.name.replace("_", " "))
            en = EN_SCENARIO_NAMES.get(d.name, d.name.replace("_", " "))
            e = dataset_entry(d, d.name.split("_", 1)[0], tr, en, "historical")
            if e:
                entries.append(e)

    if not entries:
        raise SystemExit("[!] Manifest için kullanılabilir graph dataset bulunamadı.")

    tr_manifest = {
        "default": "final_v2" if any(x["id"] == "final_v2" for x in entries) else entries[0]["id"],
        "datasets": entries,
    }

    en_entries = []
    for item in entries:
        x = dict(item)
        for k, v in list(x.items()):
            if isinstance(v, str) and (
                v.startswith("evidence/")
                or v.startswith("data/")
                or v.startswith("assets/")
            ):
                x[k] = "../" + v
        en_entries.append(x)

    en_manifest = {
        "default": tr_manifest["default"],
        "datasets": en_entries,
    }

    TR_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    EN_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    TR_MANIFEST.write_text(json.dumps(tr_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    EN_MANIFEST.write_text(json.dumps(en_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(entries)


def header(en: bool) -> str:
    skip = "Skip to main content" if en else "Ana içeriğe geç"
    links = []
    for filename, label in PAGES:
        active = ' class="active"' if filename == "graph.html" else ""
        links.append(f'<a{active} href="{filename}">{label}</a>')
    nav = "\n      ".join(links)

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
        <button type="button" id="fontDown">A-</button>
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


GRAPH_STYLE = r'''
<style>
  body[data-page="graph"] { overflow-x: hidden; }

  .graph-page {
    width: min(100% - (var(--page-pad, 56px) * 2), 112rem) !important;
    margin-inline: auto !important;
    padding-block: clamp(34px, 4.5vw, 58px) clamp(54px, 6vw, 84px) !important;
  }

  .graph-hero { margin-bottom: 20px; }
  .graph-hero h1 {
    margin: 0 0 14px;
    max-width: 82rem;
    font-size: clamp(46px, 5.5vw, 82px);
    line-height: 1.04;
    letter-spacing: -.052em;
  }
  .graph-hero .lead {
    max-width: 76rem !important;
    font-size: clamp(17px, .45vw + 15px, 20px) !important;
  }

  .graph-toolbar {
    position: sticky;
    top: 74px;
    z-index: 30;
    display: grid;
    grid-template-columns: minmax(280px, 1.25fr) minmax(240px, 1fr) minmax(190px, 260px) auto auto auto;
    gap: 10px;
    align-items: end;
    padding: 11px;
    margin: 18px 0 12px;
    border: 1px solid color-mix(in srgb, var(--line) 68%, transparent);
    border-radius: 18px;
    background: color-mix(in srgb, var(--bg) 88%, transparent);
    backdrop-filter: blur(14px);
  }

  .toolbar-field { min-width: 0; }
  .toolbar-field label {
    display: block;
    margin: 0 0 6px;
    color: var(--muted);
    font-size: 12px;
    font-weight: 650;
  }
  .graph-toolbar select,
  .graph-toolbar input,
  .graph-toolbar button {
    height: 42px;
    border: 1px solid color-mix(in srgb, var(--line) 82%, transparent);
    border-radius: 12px;
    background: color-mix(in srgb, var(--bg) 78%, #000 22%);
    color: var(--text);
    font: inherit;
    font-size: 13px;
  }
  .graph-toolbar select,
  .graph-toolbar input {
    width: 100%;
    padding: 0 12px;
    outline: none;
  }
  .graph-toolbar button {
    border-radius: 999px;
    padding: 0 14px;
    cursor: pointer;
    font-weight: 650;
    white-space: nowrap;
  }

  .graph-stats {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 12px;
  }
  .graph-stat {
    min-height: 78px;
    padding: 12px 13px;
    border: 1px solid color-mix(in srgb, var(--line) 68%, transparent);
    border-radius: 16px;
    background: color-mix(in srgb, var(--surface-2, var(--bg)) 76%, transparent);
  }
  .graph-stat span {
    display: block;
    color: var(--muted);
    font-size: 11.5px;
    font-weight: 650;
    margin-bottom: 7px;
  }
  .graph-stat strong {
    display: block;
    color: var(--text);
    font-size: 27px;
    line-height: 1;
  }

  .graph-frame {
    position: relative;
    width: 100%;
    height: clamp(700px, 78vh, 980px);
    border: 1px solid color-mix(in srgb, var(--line) 72%, transparent);
    border-radius: 22px;
    background:
      radial-gradient(circle at 16% 18%, color-mix(in srgb, var(--accent) 10%, transparent), transparent 34%),
      color-mix(in srgb, var(--bg) 94%, #000 6%);
    overflow: hidden;
  }
  #cy { width: 100%; height: 100%; }
  .graph-status {
    position: absolute;
    left: 14px;
    top: 14px;
    z-index: 5;
    max-width: min(800px, calc(100% - 28px));
    padding: 8px 11px;
    border: 1px solid color-mix(in srgb, var(--line) 76%, transparent);
    border-radius: 999px;
    background: color-mix(in srgb, var(--bg) 84%, transparent);
    color: var(--muted);
    font-size: 12px;
    backdrop-filter: blur(8px);
  }
  .graph-status.err { color: #fca5a5; }

  .graph-analysis {
    display: grid;
    grid-template-columns: minmax(0, 1.08fr) minmax(380px, .92fr);
    gap: 14px;
    margin-top: 14px;
  }
  .analysis-panel {
    padding: 18px;
    border: 1px solid color-mix(in srgb, var(--line) 68%, transparent);
    border-radius: 18px;
    background: color-mix(in srgb, var(--surface-2, var(--bg)) 76%, transparent);
  }
  .analysis-panel h2 {
    margin: 0 0 12px !important;
    font-size: clamp(25px, 2.2vw, 34px) !important;
  }
  .analysis-panel p {
    max-width: none !important;
    color: var(--muted);
    font-size: 15px !important;
    line-height: 1.66 !important;
  }

  .interpretation-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 10px;
  }
  .scenario-title { margin: 0; font-size: 19px; }
  .scenario-subtitle { margin-top: 4px; color: var(--muted); font-size: 13px; }
  .status-pill {
    display: inline-flex;
    padding: 5px 9px;
    border: 1px solid color-mix(in srgb, var(--line) 66%, transparent);
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
  }
  .status-pill.good { color: #86efac; }
  .status-pill.warn { color: #fde68a; }

  .score-strip {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 8px;
    margin: 10px 0;
  }
  .score-chip {
    padding: 10px;
    border: 1px solid color-mix(in srgb, var(--line) 58%, transparent);
    border-radius: 13px;
    background: color-mix(in srgb, var(--bg) 76%, transparent);
  }
  .score-chip b {
    display: block;
    color: var(--muted) !important;
    font-size: 11.5px;
  }
  .score-chip strong {
    display: block;
    margin-top: 4px;
    color: var(--text);
    font-size: 21px;
  }
  .interpretation-text {
    padding: 12px 13px;
    border: 1px solid color-mix(in srgb, var(--line) 54%, transparent);
    border-radius: 14px;
    background: color-mix(in srgb, var(--bg) 76%, transparent);
  }

  .mitre-groups {
    display: grid;
    gap: 10px;
  }
  .mitre-group {
    padding: 12px;
    border: 1px solid color-mix(in srgb, var(--line) 58%, transparent);
    border-radius: 14px;
    background: color-mix(in srgb, var(--bg) 76%, transparent);
  }
  .mitre-group h3 {
    margin: 0 0 9px;
    font-size: 16px;
  }
  .mitre-group h3 a {
    color: var(--accent);
    border-bottom: 1px solid color-mix(in srgb, var(--accent) 48%, transparent);
  }
  .tech-list { display: grid; gap: 7px; }
  .tech-item {
    display: grid;
    grid-template-columns: 92px minmax(0, 1fr) auto;
    gap: 8px;
    align-items: center;
    padding: 8px 9px;
    border: 1px solid color-mix(in srgb, var(--line) 50%, transparent);
    border-radius: 12px;
  }
  .tech-item a { color: inherit; text-decoration: none; }
  .tech-id {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 12px;
    color: var(--accent);
  }
  .tech-name { color: var(--muted); font-size: 13px; }
  .tech-state {
    padding: 4px 7px;
    border-radius: 999px;
    border: 1px solid color-mix(in srgb, var(--line) 58%, transparent);
    font-size: 11px;
    font-weight: 700;
  }
  .tech-state.covered { color: #86efac; }
  .tech-state.missing { color: #fca5a5; }

  .node-detail-backdrop {
    position: fixed;
    inset: 0;
    z-index: 180;
    background: rgba(2,6,23,.48);
    opacity: 0;
    pointer-events: none;
    transition: opacity .18s ease;
  }
  .node-detail-backdrop.open { opacity: 1; pointer-events: auto; }
  .node-detail-drawer {
    position: fixed;
    top: 0;
    right: 0;
    z-index: 190;
    width: min(620px, 94vw);
    height: 100vh;
    padding: 22px;
    border-left: 1px solid color-mix(in srgb, var(--line) 80%, transparent);
    background: var(--bg);
    transform: translateX(105%);
    transition: transform .2s ease;
    overflow: auto;
  }
  .node-detail-drawer.open { transform: translateX(0); }
  .drawer-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 16px;
  }
  .drawer-head h2 { margin: 0 !important; font-size: 24px !important; }
  .drawer-head button {
    padding: 7px 10px;
    border: 1px solid color-mix(in srgb, var(--line) 70%, transparent);
    border-radius: 999px;
    background: transparent;
    color: var(--text);
    cursor: pointer;
  }
  .role-card {
    padding: 13px;
    margin: 10px 0 14px;
    border: 1px solid color-mix(in srgb, var(--accent) 40%, var(--line));
    border-radius: 14px;
    background: color-mix(in srgb, var(--accent) 7%, var(--bg));
  }
  .kv {
    display: grid;
    grid-template-columns: minmax(130px, .34fr) minmax(0, 1fr);
    gap: 8px 12px;
    font-size: 13px;
    line-height: 1.55;
  }
  .kv b { color: var(--text) !important; }
  .kv span { color: var(--muted); overflow-wrap: anywhere; }

  @media (max-width: 1180px) {
    .graph-toolbar { grid-template-columns: 1fr 1fr 1fr; position: static; }
    .graph-stats, .score-strip { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .graph-analysis { grid-template-columns: 1fr; }
  }
  @media (max-width: 720px) {
    .graph-toolbar, .graph-stats, .score-strip { grid-template-columns: 1fr; }
    .graph-frame { height: 70vh; min-height: 560px; }
  }
</style>
'''


def page(en: bool) -> str:
    prefix = "../" if en else ""
    lang = "en" if en else "tr"

    if en:
        title = "Interactive evidence graph"
        lead = "Select a dataset or historical scenario, inspect the graph, open node or edge details, and review MITRE ATT&CK mappings below."
        dataset_label = "Dataset / scenario"
        search_label = "Search"
        type_label = "Node type"
        all_types = "All node types"
        fit = "Fit"
        reset = "Reset"
        focus = "Focus"
        loading = "Loading graph..."
        labels = ["Declared nodes", "Rendered nodes", "Edges", "Observed", "Missing", "SACI"]
        interpretation = "Graph interpretation"
        mitre = "MITRE ATT&CK tactics and techniques"
        drawer = "Selected node / edge"
        close = "Close"
        empty = "Double-click a node or edge to inspect its role in the selected scenario."
    else:
        title = "Etkileşimli kanıt grafı"
        lead = "Veri kümesi veya tarihsel senaryoyu seç; grafı incele, node/edge ayrıntılarını aç ve alttaki MITRE ATT&CK eşleşmelerini değerlendir."
        dataset_label = "Veri kümesi / senaryo"
        search_label = "Arama"
        type_label = "Node tipi"
        all_types = "Tüm node tipleri"
        fit = "Sığdır"
        reset = "Sıfırla"
        focus = "Odak"
        loading = "Graph yükleniyor..."
        labels = ["Beyan edilen node", "Gösterilen node", "Edge", "Observed", "Missing", "SACI"]
        interpretation = "Graph yorumlaması"
        mitre = "MITRE ATT&CK taktik ve teknik eşleşmeleri"
        drawer = "Seçili node / edge"
        close = "Kapat"
        empty = "Seçili senaryodaki görevini görmek için bir node veya edge üzerine çift tıkla."

    stat_ids = [
        "declaredNodeCount", "nodeCount", "edgeCount",
        "observedCount", "missingCount", "saciScore"
    ]
    stats = "\n".join(
        f'<div class="graph-stat"><span>{label}</span><strong id="{sid}">-</strong></div>'
        for label, sid in zip(labels, stat_ids)
    )

    return f'''<!doctype html>
<html lang="{lang}" data-theme="dim" data-font-level="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — SACI Final Evidence</title>
  <link rel="stylesheet" href="{prefix}assets/saci-standard.css?v=graph-explorer-restore-1">
  {GRAPH_STYLE}
</head>
<body data-page="graph">
{header(en)}
<main id="main" class="graph-page">
  <section class="graph-hero">
    <div class="kicker">GRAPH EXPLORER</div>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </section>

  <section class="graph-toolbar" aria-label="Graph controls">
    <div class="toolbar-field">
      <label for="scenarioSelect">{dataset_label}</label>
      <select id="scenarioSelect"><option>{loading}</option></select>
    </div>
    <div class="toolbar-field">
      <label for="q">{search_label}</label>
      <input id="q" type="search" placeholder="DC01, Wazuh, T1071, MISP...">
    </div>
    <div class="toolbar-field">
      <label for="typeFilter">{type_label}</label>
      <select id="typeFilter"><option value="">{all_types}</option></select>
    </div>
    <button type="button" id="fitBtn">{fit}</button>
    <button type="button" id="resetBtn">{reset}</button>
    <button type="button" id="fullBtn">{focus}</button>
  </section>

  <section class="graph-stats">
    {stats}
  </section>

  <section class="graph-frame" id="graphShell">
    <div id="status" class="graph-status">{loading}</div>
    <div id="cy" role="img" aria-label="SACI evidence graph"></div>
  </section>

  <section class="graph-analysis">
    <article class="analysis-panel">
      <h2>{interpretation}</h2>
      <div id="interpretation"><p>{loading}</p></div>
    </article>
    <article class="analysis-panel">
      <h2>{mitre}</h2>
      <div id="mitrePanel"><p>{loading}</p></div>
    </article>
  </section>
</main>

<div class="node-detail-backdrop" id="nodeDetailBackdrop"></div>
<aside class="node-detail-drawer" id="nodeDetailDrawer" aria-hidden="true">
  <div class="drawer-head">
    <h2>{drawer}</h2>
    <button type="button" id="nodeDetailClose">{close}</button>
  </div>
  <div id="details"><p>{empty}</p></div>
</aside>

<script src="https://unpkg.com/cytoscape@3.29.2/dist/cytoscape.min.js"></script>
<script src="{prefix}assets/graph.js?v=graph-explorer-restore-1"></script>
<script src="{prefix}assets/saci-ui.js?v=graph-explorer-restore-1"></script>
</body>
</html>
'''


GRAPH_JS = r'''(() => {
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
        `Kanonik final-v2 görünümünde ${declaredNodes} beyan edilmiş node, ${nodes.length} gösterilen node ve ${edges.length} edge vardır. ${obs} edge observed=1, ${miss} edge observed=0 durumundadır. ${coveredMitre}/${allMitre} MITRE tekniği kapsanır. Bu sonuç tanımlı yayın kapsamındaki kanıt kapanışını gösterir; mutlak güvenlik garantisi değildir.`,
        `The canonical final-v2 view contains ${declaredNodes} declared nodes, ${nodes.length} rendered nodes and ${edges.length} edges. ${obs} edges are observed=1 and ${miss} edges are observed=0. ${coveredMitre}/${allMitre} MITRE techniques are covered. This indicates evidence closure within the declared publication scope; it is not an absolute security guarantee.`
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
})();'''


def write_site_files() -> None:
    EN.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS / "graph.html").write_text(page(False), encoding="utf-8")
    (EN / "graph.html").write_text(page(True), encoding="utf-8")
    (ASSETS / "graph.js").write_text(GRAPH_JS, encoding="utf-8")


def main() -> None:
    if not DOCS.exists():
        raise SystemExit("[!] docs/ klasörü bulunamadı. Script repo kökünde çalıştırılmalı.")

    restored = restore_scenarios()
    restore_final()
    count = make_manifests()
    write_site_files()

    print("=== SACI GRAPH EXPLORER RESTORED ===")
    print("Historical scenario folders restored:", restored)
    print("Datasets in dropdown:", count)
    print("TR page:", DOCS / "graph.html")
    print("EN page:", EN / "graph.html")
    print("TR manifest:", TR_MANIFEST)
    print("EN manifest:", EN_MANIFEST)

    if restored == 0:
        print()
        print("[!] Tarihsel S0-S18 klasörleri bulunamadı.")
        print("[!] Dropdown yine final-v2 ile çalışır; çoklu senaryo için")
        print("[!] docs_backup_*/evidence/data/S*_*/ klasörleri repo içinde bulunmalı.")


if __name__ == "__main__":
    main()
