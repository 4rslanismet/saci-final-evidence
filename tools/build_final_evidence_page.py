#!/usr/bin/env python3
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
EN = DOCS / "en"
FINAL_DST = DOCS / "evidence" / "lab" / "final"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "backups" / f"evidence_page_{STAMP}"
VERSION = "final-evidence-reason-audit-3"

if not DOCS.exists():
    raise SystemExit("[!] docs/ bulunamadı. Script repo kökünde çalıştırılmalı.")


def backup(path: Path) -> None:
    if not path.exists():
        return
    target = BACKUP / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def find_source() -> Path:
    candidates = [
        ROOT / "_saci_final_seed" / "data" / "final",
        DOCS / "evidence" / "lab" / "final",
        DOCS / "evidence" / "lab" / "final_v2",
    ]
    for candidate in candidates:
        if candidate.exists() and any(candidate.glob("saci_scores*.csv")):
            return candidate
    raise SystemExit(
        "[!] Final veri kaynağı bulunamadı. "
        "_saci_final_seed/data/final veya docs/evidence/lab/final(_v2) gerekli."
    )


def first_existing(base: Path, names: list[str]) -> Path | None:
    for name in names:
        path = base / name
        if path.exists():
            return path
    return None


def copy_final_data(source: Path) -> list[str]:
    FINAL_DST.mkdir(parents=True, exist_ok=True)
    mapping = {
        "saci_scores.csv": ["saci_scores.csv", "saci_scores_v2.csv"],
        "asset_log_coverage.csv": ["asset_log_coverage.csv", "asset_log_coverage_v2.csv"],
        "log_source_status.csv": ["log_source_status.csv", "log_source_status_v2.csv"],
        "control_coverage.csv": ["control_coverage.csv", "control_coverage_v2.csv"],
        "mitre_coverage.csv": ["mitre_coverage.csv", "mitre_coverage_v2.csv"],
        "ctic_coverage.csv": ["ctic_coverage.csv", "ctic_coverage_v2.csv"],
        "reason_codes.csv": ["reason_codes.csv", "reason_codes_v2.csv"],
        "reason_codes.json": ["reason_codes.json", "reason_codes_v2.json"],
        "saci_graph.cyjs": ["saci_graph.cyjs", "saci_graph_v2.cyjs"],
        "saci_graph_summary.md": ["saci_graph_summary.md", "saci_graph_summary_v2.md"],
    }
    copied = []
    for target_name, source_names in mapping.items():
        src = first_existing(source, source_names)
        if src:
            dst = FINAL_DST / target_name
            if src.resolve() != dst.resolve():
                shutil.copy2(src, dst)
            copied.append(target_name)
    required = {
        "saci_scores.csv",
        "asset_log_coverage.csv",
        "log_source_status.csv",
        "control_coverage.csv",
        "mitre_coverage.csv",
        "ctic_coverage.csv",
    }
    missing = sorted(required - set(copied))
    if missing:
        raise SystemExit("[!] Eksik final kanıt dosyaları: " + ", ".join(missing))
    return copied


EVIDENCE_CSS = r'''/* SACI Final Evidence page */
body[data-page="evidence"] .evidence-page {
  width: min(100% - clamp(32px, 7vw, 112px), 1380px) !important;
  margin-inline: auto !important;
  padding-block: clamp(36px, 4.8vw, 64px) clamp(64px, 7vw, 104px) !important;
}

.evidence-hero { margin-bottom: clamp(34px, 5vw, 58px); }
.evidence-hero .kicker {
  margin: 0 0 17px;
  color: var(--accent);
  font-size: 12px;
  font-weight: 740;
  letter-spacing: .14em;
  text-transform: uppercase;
}
.evidence-hero h1 {
  max-width: 17ch;
  margin: 0 0 20px;
  color: var(--text);
  font-size: clamp(46px, 5.7vw, 78px);
  line-height: 1.01;
  letter-spacing: -.05em;
}
.evidence-hero .lead {
  max-width: 78ch;
  margin: 0;
  color: var(--muted);
  font-size: clamp(17px, .5vw + 15px, 21px);
  line-height: 1.72;
}

.evidence-summary {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 10px;
  margin: 0 0 clamp(42px, 5vw, 68px);
}
.evidence-metric {
  min-width: 0;
  padding: 15px;
  border: 1px solid color-mix(in srgb, var(--line) 66%, transparent);
  border-radius: 16px;
  background: color-mix(in srgb, var(--surface, var(--bg)) 82%, transparent);
}
.evidence-metric span {
  display: block;
  margin-bottom: 8px;
  color: var(--muted);
  font-size: 11.5px;
  font-weight: 680;
}
.evidence-metric strong {
  display: block;
  color: var(--text);
  font-size: clamp(24px, 2.4vw, 34px);
  line-height: 1;
}

.evidence-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: clamp(42px, 5vw, 68px);
}
.evidence-nav a {
  padding: 8px 11px;
  border: 1px solid color-mix(in srgb, var(--line) 64%, transparent);
  border-radius: 999px;
  color: var(--muted);
  text-decoration: none;
  font-size: 12.5px;
}
.evidence-nav a:hover {
  color: var(--text);
  border-color: color-mix(in srgb, var(--accent) 42%, var(--line));
}

.evidence-section {
  scroll-margin-top: 108px;
  padding-top: clamp(40px, 5.5vw, 72px);
  margin-top: clamp(40px, 5.5vw, 72px);
  border-top: 1px solid color-mix(in srgb, var(--line) 58%, transparent);
}
.evidence-section:first-of-type { margin-top: 0; }
.evidence-section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
}
.evidence-section h2 {
  max-width: 28ch;
  margin: 0;
  color: var(--text);
  font-size: clamp(29px, 3vw, 42px);
  line-height: 1.1;
  letter-spacing: -.035em;
}
.evidence-section .section-copy {
  max-width: 78ch;
  margin: 0 0 18px;
  color: var(--muted);
  font-size: 15.5px;
  line-height: 1.72;
}
.raw-link {
  color: var(--accent);
  text-decoration: none;
  white-space: nowrap;
  font-size: 12.5px;
}
.raw-link:hover { text-decoration: underline; }

.table-shell {
  width: 100%;
  overflow: auto;
  border: 1px solid color-mix(in srgb, var(--line) 66%, transparent);
  border-radius: 16px;
  background: color-mix(in srgb, var(--surface, var(--bg)) 78%, transparent);
}
.evidence-table {
  width: 100%;
  min-width: 760px;
  border-collapse: collapse;
  color: var(--text);
  font-size: 13px;
}
.evidence-table th,
.evidence-table td {
  padding: 11px 12px;
  border-bottom: 1px solid color-mix(in srgb, var(--line) 48%, transparent);
  text-align: left;
  vertical-align: top;
}
.evidence-table th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: color-mix(in srgb, var(--bg) 92%, transparent);
  color: var(--muted);
  font-size: 11.5px;
  font-weight: 720;
  letter-spacing: .02em;
}
.evidence-table tr:last-child td { border-bottom: 0; }
.evidence-table tbody tr:hover {
  background: color-mix(in srgb, var(--accent) 4%, transparent);
}
.evidence-table code {
  color: var(--accent);
  font-size: 12px;
}
.evidence-table a { color: var(--accent); text-decoration: none; }
.evidence-table a:hover { text-decoration: underline; }

.status {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 27px;
  padding: 0 9px;
  border: 1px solid color-mix(in srgb, var(--line) 64%, transparent);
  border-radius: 999px;
  background: color-mix(in srgb, var(--surface, var(--bg)) 82%, transparent);
  color: var(--text);
  font-size: 11.5px;
  font-weight: 700;
  white-space: nowrap;
}
.status::before {
  content: "";
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
}
.status.good {
  color: var(--green, #22c55e);
  border-color: color-mix(in srgb, var(--green, #22c55e) 34%, var(--line));
  background: color-mix(in srgb, var(--green, #22c55e) 7%, var(--surface, var(--bg)));
}
.status.warn {
  color: var(--yellow, #eab308);
  border-color: color-mix(in srgb, var(--yellow, #eab308) 34%, var(--line));
  background: color-mix(in srgb, var(--yellow, #eab308) 7%, var(--surface, var(--bg)));
}
.status.muted { color: var(--muted); }

.audit-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-top: 18px;
}
.audit-item {
  padding: 14px;
  border: 1px solid color-mix(in srgb, var(--line) 60%, transparent);
  border-radius: 14px;
  background: color-mix(in srgb, var(--surface, var(--bg)) 80%, transparent);
}
.audit-item span {
  display: block;
  margin-bottom: 7px;
  color: var(--muted);
  font-size: 11.5px;
  font-weight: 680;
}
.audit-item strong {
  color: var(--text);
  font-size: 17px;
  line-height: 1.4;
}
.validation-note {
  margin-top: 16px;
  padding: 14px 15px;
  border-left: 2px solid var(--accent);
  border-radius: 0 12px 12px 0;
  background: color-mix(in srgb, var(--accent) 6%, transparent);
  color: var(--muted);
  font-size: 14px;
  line-height: 1.68;
}
.validation-note strong { color: var(--text); }
.empty-state {
  padding: 18px;
  border: 1px dashed color-mix(in srgb, var(--line) 66%, transparent);
  border-radius: 14px;
  color: var(--muted);
  line-height: 1.65;
}
.evidence-file-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}
.evidence-file-links a {
  padding: 7px 10px;
  border: 1px solid color-mix(in srgb, var(--line) 58%, transparent);
  border-radius: 999px;
  color: var(--accent);
  text-decoration: none;
  font-size: 12px;
}


/* Historical scenario validation series */
.scenario-summary-note {
  margin: 0 0 18px;
  padding: 13px 14px;
  border-left: 2px solid var(--accent);
  border-radius: 0 12px 12px 0;
  background: color-mix(in srgb, var(--accent) 6%, transparent);
  color: var(--muted);
  font-size: 14px;
  line-height: 1.68;
}
.scenario-detail-list {
  display: grid;
  gap: 10px;
  margin-top: 18px;
}
.scenario-detail {
  border: 1px solid color-mix(in srgb, var(--line) 62%, transparent);
  border-radius: 15px;
  background: color-mix(in srgb, var(--surface, var(--bg)) 80%, transparent);
  overflow: hidden;
}
.scenario-detail summary {
  display: grid;
  grid-template-columns: minmax(230px, 1fr) repeat(3, minmax(90px, auto));
  gap: 12px;
  align-items: center;
  padding: 13px 15px;
  cursor: pointer;
  list-style: none;
  color: var(--text);
}
.scenario-detail summary::-webkit-details-marker { display: none; }
.scenario-detail summary::before {
  content: "›";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  margin-right: 8px;
  border: 1px solid color-mix(in srgb, var(--accent) 40%, var(--line));
  border-radius: 50%;
  color: var(--accent);
  transition: transform .16s ease;
}
.scenario-detail[open] summary::before { transform: rotate(90deg); }
.scenario-summary-title {
  min-width: 0;
  font-weight: 720;
  overflow-wrap: anywhere;
}
.scenario-summary-stat {
  color: var(--muted);
  font-size: 12px;
  white-space: nowrap;
}
.scenario-summary-stat strong { color: var(--text); }
.scenario-detail-body {
  padding: 0 15px 16px;
  border-top: 1px solid color-mix(in srgb, var(--line) 48%, transparent);
}
.scenario-metrics {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 8px;
  margin: 15px 0;
}
.scenario-metric {
  padding: 10px;
  border: 1px solid color-mix(in srgb, var(--line) 52%, transparent);
  border-radius: 12px;
  background: color-mix(in srgb, var(--bg) 76%, transparent);
}
.scenario-metric span {
  display: block;
  margin-bottom: 5px;
  color: var(--muted);
  font-size: 11px;
  font-weight: 680;
}
.scenario-metric strong {
  color: var(--text);
  font-size: 18px;
}
.scenario-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0 15px;
}
.scenario-links a {
  padding: 7px 10px;
  border: 1px solid color-mix(in srgb, var(--line) 56%, transparent);
  border-radius: 999px;
  color: var(--accent);
  text-decoration: none;
  font-size: 12px;
}
.scenario-mitre-title {
  margin: 18px 0 10px;
  color: var(--text);
  font-size: 18px;
}
@media (max-width: 980px) {
  .scenario-detail summary {
    grid-template-columns: minmax(0, 1fr) auto;
  }
  .scenario-summary-stat:nth-of-type(n+2) { display: none; }
  .scenario-metrics { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 620px) {
  .scenario-detail summary { grid-template-columns: 1fr; }
  .scenario-detail summary::before { display: none; }
  .scenario-metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 1100px) {
  .evidence-summary { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .audit-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 720px) {
  body[data-page="evidence"] .evidence-page {
    width: min(100% - 24px, 1380px) !important;
    padding-top: 26px !important;
  }
  .evidence-summary { grid-template-columns: 1fr 1fr; }
  .evidence-section-head { align-items: flex-start; flex-direction: column; }
  .audit-grid { grid-template-columns: 1fr; }
}




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


EVIDENCE_JS = r'''(() => {
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
      return kind !== "canonical" && !["final","final_v2","final-v2"].includes(id);
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
})();'''


def header(en: bool) -> str:
    active = "evidence.html"
    pages = [
        ("index.html", "Home"), ("methodology.html", "Methodology"),
        ("architecture.html", "Architecture"), ("evidence.html", "Evidence"),
        ("artifacts.html", "Artifacts"), ("graph.html", "Graph"),
        ("explanation.html", "Explanation"), ("paper.html", "Paper View"),
    ]
    nav = "\n      ".join(
        f'<a{" class=\"active\"" if file == active else ""} href="{file}">{label}</a>'
        for file, label in pages
    )
    skip = "Skip to main content" if en else "Ana içeriğe geç"
    return f'''<a class="skip-link" href="#main">{skip}</a>
<header class="top">
  <div class="top-inner">
    <a class="brand" href="index.html">SACI Final Evidence</a>
    <nav class="nav" aria-label="Primary navigation">{nav}</nav>
    <div class="top-actions" aria-label="Display controls">
      <div class="top-control"><span>Language</span><button type="button" id="langTR">TR</button><button type="button" id="langEN">EN</button></div>
      <div class="top-control"><span>Font</span><button type="button" id="fontDown">A−</button><button type="button" id="fontReset">A</button><button type="button" id="fontUp">A+</button></div>
      <div class="top-control"><span>Theme</span><button type="button" data-theme-btn="dark">Dark</button><button type="button" data-theme-btn="dim">Dim</button><button type="button" data-theme-btn="light">Light</button></div>
    </div>
  </div>
</header>'''


def page(en: bool, global_css: bool) -> str:
    prefix = "../" if en else ""
    lang = "en" if en else "tr"
    base = "../evidence/lab/final" if en else "evidence/lab/final"
    global_link = f'  <link rel="stylesheet" href="{prefix}assets/saci-global-ui.css?v={VERSION}">\n' if global_css else ""

    if en:
        kicker = "FINAL EVIDENCE"
        title = "Final evidence package"
        lead = "This page brings together the deterministic outputs used to verify the final SACI result: score components, asset and log-source coverage, control evidence, MITRE ATT&CK coverage, CTI/MISP closure, reason codes and audit notes."
        navs = ["Score", "Scenarios", "Assets", "Log sources", "Controls", "MITRE", "CTI/MISP", "Reason codes", "Audit"]
        sections = {
            "score": ("Final SACI score table", "Active SACI components, declared weights and final normalized scores."),
            "scenarios": ("Historical scenario validation series", "All S0–S18 scenario outputs are listed together. Each scenario includes SACI components, graph closure values and linked MITRE ATT&CK tactics and techniques."),
            "assets": ("Asset and log-source coverage", "Expected and received telemetry sources are compared for every asset in the declared scope."),
            "logs": ("Log-source status", "Source-level evidence, observed state, weighting and last-seen timestamps."),
            "controls": ("Control and alert coverage", "Detection controls, Wazuh rules, MITRE mappings and observed alert evidence."),
            "mitre": ("MITRE ATT&CK coverage", "In-scope tactics and techniques are shown with direct links to the official ATT&CK pages."),
            "ctic": ("CTI/MISP coverage", "Indicator lookup, MISP match, Wazuh alert and MITRE-link closure are verified together."),
            "reasons": ("Reason codes", "Reason codes explain why an expected visibility relation is missing or excluded from the active scope."),
            "audit": ("Final audit and validation notes", "A compact audit summary derived directly from the final evidence files."),
        }
        raw = "Open CSV"
    else:
        kicker = "FİNAL KANIT"
        title = "Final kanıt paketi"
        lead = "Bu sayfa final SACI sonucunu doğrulamak için kullanılan deterministik çıktıları bir araya getirir: skor bileşenleri, varlık ve log kaynağı kapsamı, kontrol kanıtları, MITRE ATT&CK kapsamı, CTI/MISP kapanışı, reason code kayıtları ve audit notları."
        navs = ["Skor", "Senaryolar", "Varlıklar", "Log kaynakları", "Kontroller", "MITRE", "CTI/MISP", "Reason code", "Audit"]
        sections = {
            "score": ("Final SACI skor tablosu", "Aktif SACI bileşenleri, tanımlı ağırlıklar ve normalize edilmiş final skorları."),
            "scenarios": ("Tarihsel senaryo doğrulama serisi", "S0–S18 senaryolarının tümü birlikte listelenir. Her senaryoda SACI bileşenleri, graph kapanış değerleri ve bağlantılı MITRE ATT&CK taktik ve teknikleri gösterilir."),
            "assets": ("Varlık ve log kaynağı kapsamı", "Beyan edilen kapsamdaki her varlık için beklenen ve alınan telemetri kaynakları karşılaştırılır."),
            "logs": ("Log kaynağı durumu", "Kaynak düzeyindeki kanıt, gözlemlenme durumu, ağırlık ve son görülme zamanları."),
            "controls": ("Kontrol ve alarm kapsamı", "Detection kontrolleri, Wazuh kuralları, MITRE eşlemeleri ve gözlemlenen alarm kanıtı."),
            "mitre": ("MITRE ATT&CK kapsamı", "Kapsamdaki taktik ve teknikler resmi ATT&CK sayfalarına doğrudan bağlantılarla gösterilir."),
            "ctic": ("CTI/MISP kapsamı", "Indicator lookup, MISP eşleşmesi, Wazuh alarmı ve MITRE bağlantısının kapanışı birlikte doğrulanır."),
            "reasons": ("Reason code kayıtları", "Reason code kayıtları beklenen bir görünürlük ilişkisinin neden eksik veya aktif kapsam dışında olduğunu açıklar."),
            "audit": ("Final audit ve doğrulama notları", "Final kanıt dosyalarından doğrudan türetilen kısa audit özeti."),
        }
        raw = "CSV'yi aç"

    ids = ["score", "scenarios", "assets", "logs", "controls", "mitre", "ctic", "reasons", "audit"]
    nav_html = "".join(f'<a href="#{sid}">{label}</a>' for sid, label in zip(ids, navs))
    file_map = {"score":"saci_scores.csv", "assets":"asset_log_coverage.csv", "logs":"log_source_status.csv", "controls":"control_coverage.csv", "mitre":"mitre_coverage.csv", "ctic":"ctic_coverage.csv", "reasons":"reason_codes.csv"}
    container_map = {"score":"scoreTable", "assets":"assetTable", "logs":"logTable", "controls":"controlTable", "mitre":"mitreTable", "ctic":"cticTable", "reasons":"reasonContent"}
    section_html = []
    for sid in ids[:-1]:
        heading, copy = sections[sid]
        if sid == "scenarios":
            section_html.append(f'''<section id="scenarios" class="evidence-section"><div class="evidence-section-head"><h2>{heading}</h2><span class="status muted"><span id="scenarioCount">-</span>&nbsp;{("scenarios" if en else "senaryo")}</span></div><p class="section-copy">{copy}</p><div class="scenario-summary-note">{("The canonical final evidence remains separate from the historical scenario validation series; counts are not merged across datasets." if en else "Kanonik final kanıtı ile tarihsel senaryo doğrulama serisi ayrı veri kümeleridir; node, edge ve skor değerleri veri kümeleri arasında birleştirilmez.")}</div><div id="scenarioTable"><div class="empty-state">Loading…</div></div><div id="scenarioContent"></div></section>''')
            continue
        heading, copy = sections[sid]
        link = f'<a class="raw-link" href="{base}/{file_map[sid]}" target="_blank" rel="noopener">{raw}</a>'
        section_html.append(f'''<section id="{sid}" class="evidence-section"><div class="evidence-section-head"><h2>{heading}</h2>{link}</div><p class="section-copy">{copy}</p><div id="{container_map[sid]}"><div class="empty-state">Loading…</div></div></section>''')
    audit_heading, audit_copy = sections["audit"]
    section_html.append(f'''<section id="audit" class="evidence-section"><div class="evidence-section-head"><h2>{audit_heading}</h2></div><p class="section-copy">{audit_copy}</p><div id="auditGrid" class="audit-grid"></div><div id="auditConclusion" class="validation-note"></div><div class="evidence-file-links"><a href="{base}/saci_graph.cyjs" target="_blank" rel="noopener">saci_graph.cyjs</a><a href="{base}/saci_graph_summary.md" target="_blank" rel="noopener">saci_graph_summary.md</a></div></section>''')

    return f'''<!doctype html>
<html lang="{lang}" data-theme="dim" data-font-level="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — SACI Final Evidence</title>
  <link rel="stylesheet" href="{prefix}assets/saci-standard.css?v={VERSION}">
{global_link}  <link rel="stylesheet" href="{prefix}assets/evidence.css?v={VERSION}">
</head>
<body data-page="evidence">
{header(en)}
<main id="main" class="evidence-page" data-evidence-base="{base}" data-scenario-manifest="data/scenarios/manifest.json">
  <section class="evidence-hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="lead">{lead}</p></section>
  <div id="evidenceStatus" class="validation-note">Loading final evidence…</div>
  <section class="evidence-summary" aria-label="SACI summary">
    <div class="evidence-metric"><span>CWLC</span><strong id="metric-cwlc">-</strong></div>
    <div class="evidence-metric"><span>CAC</span><strong id="metric-cac">-</strong></div>
    <div class="evidence-metric"><span>MDC</span><strong id="metric-mdc">-</strong></div>
    <div class="evidence-metric"><span>CTIC</span><strong id="metric-ctic">-</strong></div>
    <div class="evidence-metric"><span>TF</span><strong id="metric-tf">-</strong></div>
    <div class="evidence-metric"><span>SACI</span><strong id="metric-saci">-</strong></div>
  </section>
  <nav class="evidence-nav" aria-label="Evidence sections">{nav_html}</nav>
  {''.join(section_html)}
</main>
<script src="{prefix}assets/evidence.js?v={VERSION}"></script>
<script src="{prefix}assets/saci-ui.js?v={VERSION}"></script>
</body>
</html>'''


def main() -> None:
    source = find_source()
    for path in [DOCS / "evidence.html", EN / "evidence.html", ASSETS / "evidence.css", ASSETS / "evidence.js"]:
        backup(path)
    copied = copy_final_data(source)
    ASSETS.mkdir(parents=True, exist_ok=True)
    EN.mkdir(parents=True, exist_ok=True)
    (ASSETS / "evidence.css").write_text(EVIDENCE_CSS.strip() + "\n", encoding="utf-8")
    (ASSETS / "evidence.js").write_text(EVIDENCE_JS.strip() + "\n", encoding="utf-8")
    global_css = (ASSETS / "saci-global-ui.css").exists()
    (DOCS / "evidence.html").write_text(page(False, global_css), encoding="utf-8")
    (EN / "evidence.html").write_text(page(True, global_css), encoding="utf-8")
    print("=== FINAL EVIDENCE PAGE BUILT ===")
    print("Source:", source)
    print("Canonical data:", FINAL_DST)
    print("Copied:", ", ".join(copied))
    print("TR:", DOCS / "evidence.html")
    print("EN:", EN / "evidence.html")
    print("Backup:", BACKUP)


if __name__ == "__main__":
    main()
