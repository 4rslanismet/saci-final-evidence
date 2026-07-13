#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.cwd()
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
CSS_PATH = ASSETS / "saci-copy-width-remaining.css"

if not DOCS.exists():
    raise SystemExit("[!] docs/ bulunamadı. Scripti repo kökünde çalıştır.")

targets = [
    DOCS / "index.html",
    DOCS / "methodology.html",
    DOCS / "graph.html",
    DOCS / "en" / "index.html",
    DOCS / "en" / "methodology.html",
    DOCS / "en" / "graph.html",
]

existing = [path for path in targets if path.exists()]
if not existing:
    raise SystemExit("[!] Hedef sayfalar bulunamadı.")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_root = ROOT / "backups" / f"remaining_copy_width_{stamp}"
backup_root.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

CSS = r'''
/*
 * SACI — Remaining copy-width correction
 * Yalnızca Home, Methodology ve Graph sayfalarını etkiler.
 * Başlık ölçülerine dokunmaz.
 */

/* ---------------------------------------------------------
   HOME
   --------------------------------------------------------- */

body[data-page="home"] .lead,
body[data-page="home"] .micro-lead {
  width: 100% !important;
  max-width: min(1240px, 100%) !important;
}

body[data-page="home"] .editorial-flow,
body[data-page="home"] .scenario-section,
body[data-page="home"] .portal-links {
  width: 100% !important;
  max-width: none !important;
}

body[data-page="home"] .editorial-block {
  width: 100% !important;
  max-width: none !important;
  grid-template-columns: 220px minmax(0, 1fr) !important;
}

body[data-page="home"] .editorial-body,
body[data-page="home"] .editorial-body p,
body[data-page="home"] .compact-list {
  width: 100% !important;
  max-width: min(1220px, 100%) !important;
}

body[data-page="home"] .section-intro,
body[data-page="home"] .final-statement {
  width: 100% !important;
  max-width: min(1180px, 100%) !important;
}

/* ---------------------------------------------------------
   METHODOLOGY
   --------------------------------------------------------- */

body[data-page="methodology"] .lead {
  width: 100% !important;
  max-width: min(1280px, 100%) !important;
}

body[data-page="methodology"] .section,
body[data-page="methodology"] .method-added,
body[data-page="methodology"] .method-extra {
  width: 100% !important;
  max-width: 1360px !important;
}

body[data-page="methodology"] .section p,
body[data-page="methodology"] .method-added p,
body[data-page="methodology"] .method-extra p,
body[data-page="methodology"] .method-note,
body[data-page="methodology"] .source-line,
body[data-page="methodology"] .metric-definition,
body[data-page="methodology"] .method-summary {
  width: 100% !important;
  max-width: min(1280px, 100%) !important;
}

body[data-page="methodology"] :is(
  .method-points,
  .method-steps,
  .plain-list,
  .compact-list
) {
  width: 100% !important;
  max-width: min(1280px, 100%) !important;
}

body[data-page="methodology"] :is(
  .soft-formula,
  .formula-block,
  .worked-example
) {
  max-width: min(1280px, 100%) !important;
}

/* ---------------------------------------------------------
   GRAPH
   --------------------------------------------------------- */

body[data-page="graph"] .hero {
  width: 100% !important;
  max-width: none !important;
}

body[data-page="graph"] .hero > div {
  width: 100% !important;
  max-width: none !important;
}

body[data-page="graph"] .hero p,
body[data-page="graph"] #graph-instructions {
  width: 100% !important;
  max-width: min(1320px, 100%) !important;
}

body[data-page="graph"] .explain-box {
  width: 100% !important;
  max-width: none !important;
}

body[data-page="graph"] .explain-box p {
  width: 100% !important;
  max-width: min(1460px, 100%) !important;
}

/* Metinler kelime ortasında bölünmesin */
body[data-page="home"] p,
body[data-page="methodology"] p,
body[data-page="graph"] p,
body[data-page="home"] li,
body[data-page="methodology"] li,
body[data-page="graph"] li {
  word-break: normal !important;
  overflow-wrap: normal !important;
  hyphens: none !important;
}

/* Tablet ve mobil */
@media (max-width: 900px) {
  body[data-page="home"] .editorial-block {
    grid-template-columns: 1fr !important;
  }

  body[data-page="home"] .lead,
  body[data-page="home"] .micro-lead,
  body[data-page="home"] .editorial-body p,
  body[data-page="home"] .section-intro,
  body[data-page="methodology"] .lead,
  body[data-page="methodology"] .section p,
  body[data-page="graph"] .hero p {
    max-width: 100% !important;
  }
}
'''

CSS_PATH.write_text(CSS.strip() + "\n", encoding="utf-8")

for path in existing:
    rel = path.relative_to(ROOT)
    backup = backup_root / rel
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup)

    html = path.read_text(encoding="utf-8", errors="replace")

    html = re.sub(
        r'\s*<link[^>]+saci-copy-width-remaining\.css[^>]*>\s*',
        '\n',
        html,
        flags=re.I,
    )

    prefix = "../" if path.parent.name == "en" else ""
    link = (
        f'  <link rel="stylesheet" '
        f'href="{prefix}assets/saci-copy-width-remaining.css?v=1">\n'
    )

    html = html.replace("</head>", link + "</head>", 1)
    path.write_text(html, encoding="utf-8")

print("=== HOME / METHODOLOGY / GRAPH COPY WIDTH FIX ===")
print(f"CSS: {CSS_PATH.relative_to(ROOT)}")
print(f"Updated pages: {len(existing)}")
print(f"Backups: {backup_root}")
for path in existing:
    print(f"  - {path.relative_to(ROOT)}")
