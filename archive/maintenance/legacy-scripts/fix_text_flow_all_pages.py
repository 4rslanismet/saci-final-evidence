#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.cwd()
DOCS = ROOT / "docs"
GLOBAL_CSS = DOCS / "assets" / "saci-global-ui.css"

if not DOCS.exists():
    raise SystemExit("[!] docs/ bulunamadı. Scripti repo kökünde çalıştır.")
if not GLOBAL_CSS.exists():
    raise SystemExit(f"[!] Dosya bulunamadı: {GLOBAL_CSS}")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_root = ROOT / "backups" / f"text_flow_all_pages_{stamp}"
backup_root.mkdir(parents=True, exist_ok=True)

def backup(path: Path):
    rel = path.relative_to(ROOT)
    target = backup_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)

backup(GLOBAL_CSS)

START = "/* SACI_GLOBAL_TEXT_FLOW_START */"
END = "/* SACI_GLOBAL_TEXT_FLOW_END */"

PATCH = r'''
/* SACI_GLOBAL_TEXT_FLOW_START */

/*
 * Site genelinde başlık ve açıklama metinlerinin gereksiz dar alanlarda
 * parçalanmasını önler. Uzun metinler yalnızca ekran gerçekten daraldığında
 * doğal biçimde satır kırar.
 */

html {
  text-rendering: optimizeLegibility;
}

body {
  overflow-wrap: normal;
  word-break: normal;
  hyphens: none;
}

/* Ana içerik alanlarını gereksiz yere daraltma */
:is(
  .page,
  .home-page,
  .methodology-page,
  .architecture-page,
  .evidence-page,
  .scenarios-page,
  .artifacts-page,
  .graph-page,
  .explanation-page,
  .paper-page,
  .data-page
) {
  width: min(
    calc(100% - clamp(28px, 6vw, 96px)),
    1520px
  ) !important;

  max-width: none !important;
  margin-inline: auto !important;
}

/* Hero başlıkları masaüstünde yapay karakter sınırına takılmasın */
:is(
  .hero,
  .home-hero,
  .methodology-hero,
  .architecture-hero,
  .evidence-hero,
  .scenario-hero,
  .scenarios-hero,
  .artifacts-hero,
  .graph-hero,
  .explanation-hero,
  .paper-hero,
  .data-hero
) h1 {
  width: auto !important;
  max-width: none !important;
  margin-right: 0 !important;
  overflow-wrap: normal !important;
  word-break: normal !important;
  hyphens: none !important;
  text-wrap: pretty;
}

/* Hero açıklamalarını daha geniş ve doğal okut */
:is(
  .hero,
  .home-hero,
  .methodology-hero,
  .architecture-hero,
  .evidence-hero,
  .scenario-hero,
  .scenarios-hero,
  .artifacts-hero,
  .graph-hero,
  .explanation-hero,
  .paper-hero,
  .data-hero
) :is(
  .lead,
  .hero-lead,
  .hero-copy,
  .subtitle,
  .description,
  .paper-scope,
  .data-scope
) {
  width: auto !important;
  max-width: 112ch !important;
  overflow-wrap: normal !important;
  word-break: normal !important;
  hyphens: none !important;
  text-wrap: pretty;
  line-height: 1.68 !important;
}

/* Sayfa içindeki bölüm açıklamalarını da gereksiz daraltma */
:is(
  .section-head,
  .page-section-head,
  .paper-section-head,
  .data-section-head,
  .explanation-section-head,
  .scenario-section-head,
  .evidence-section-head,
  .architecture-section-head,
  .methodology-section-head,
  .artifacts-section-head
) p {
  width: auto !important;
  max-width: 112ch !important;
  overflow-wrap: normal !important;
  word-break: normal !important;
  hyphens: none !important;
  text-wrap: pretty;
}

/* Kart ve rapor paragraflarında aşırı dar karakter sınırlarını kaldır */
:is(
  .academic-note,
  .report-block,
  .policy-card,
  .pipeline-step,
  .paper-summary-card,
  .paper-scenario-panel,
  .data-description,
  .structural-note,
  .structural-review,
  .explanation-boundary,
  .paper-boundary
) p {
  max-width: 100% !important;
  overflow-wrap: normal !important;
  word-break: normal !important;
  hyphens: none !important;
  text-wrap: pretty;
}

/* Başlıkların kelime ortasından veya yapay dar kolon yüzünden kırılmasını önle */
main :is(h1, h2, h3, h4) {
  overflow-wrap: normal !important;
  word-break: normal !important;
  hyphens: none !important;
  text-wrap: pretty;
}

/* Dosya adı, hash ve uzun teknik değerlerde taşma kontrollü kalsın */
:is(
  code,
  pre,
  .data-file-name strong,
  .data-hash,
  .technical-value,
  .path-value
) {
  overflow-wrap: anywhere;
  word-break: break-word;
}

/* Düğmelerin etiketleri iki satıra bölünmesin */
:is(
  .data-actions,
  .paper-actions,
  .selector-actions,
  .paper-scenario-actions,
  .figure-tools,
  .top-actions
) :is(a, button) {
  white-space: nowrap;
}

@media (max-width: 980px) {
  :is(
    .page,
    .home-page,
    .methodology-page,
    .architecture-page,
    .evidence-page,
    .scenarios-page,
    .artifacts-page,
    .graph-page,
    .explanation-page,
    .paper-page,
    .data-page
  ) {
    width: min(calc(100% - 32px), 1520px) !important;
  }

  :is(
    .hero,
    .home-hero,
    .methodology-hero,
    .architecture-hero,
    .evidence-hero,
    .scenario-hero,
    .scenarios-hero,
    .artifacts-hero,
    .graph-hero,
    .explanation-hero,
    .paper-hero,
    .data-hero
  ) :is(
    .lead,
    .hero-lead,
    .hero-copy,
    .subtitle,
    .description,
    .paper-scope,
    .data-scope
  ) {
    max-width: 100% !important;
  }
}

@media (max-width: 620px) {
  :is(
    .page,
    .home-page,
    .methodology-page,
    .architecture-page,
    .evidence-page,
    .scenarios-page,
    .artifacts-page,
    .graph-page,
    .explanation-page,
    .paper-page,
    .data-page
  ) {
    width: min(calc(100% - 24px), 1520px) !important;
  }

  :is(
    .hero,
    .home-hero,
    .methodology-hero,
    .architecture-hero,
    .evidence-hero,
    .scenario-hero,
    .scenarios-hero,
    .artifacts-hero,
    .graph-hero,
    .explanation-hero,
    .paper-hero,
    .data-hero
  ) h1 {
    max-width: 100% !important;
    text-wrap: pretty;
  }

  :is(
    .data-actions,
    .paper-actions,
    .selector-actions,
    .paper-scenario-actions,
    .figure-tools
  ) :is(a, button) {
    white-space: normal;
  }
}

/* SACI_GLOBAL_TEXT_FLOW_END */
'''

css = GLOBAL_CSS.read_text(encoding="utf-8", errors="replace")

css = re.sub(
    re.escape(START) + r".*?" + re.escape(END),
    "",
    css,
    flags=re.S
)

GLOBAL_CSS.write_text(
    css.rstrip() + "\n\n" + PATCH.strip() + "\n",
    encoding="utf-8"
)

html_files = sorted(DOCS.glob("*.html")) + sorted((DOCS / "en").glob("*.html"))
changed = []

for path in html_files:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    text = re.sub(
        r'(saci-global-ui\.css)(?:\?v=[^"\']*)?',
        r'\1?v=text-flow-1',
        text
    )

    if "saci-global-ui.css" not in text:
        prefix = "../" if path.parent.name == "en" else ""
        link = (
            f'  <link rel="stylesheet" '
            f'href="{prefix}assets/saci-global-ui.css?v=text-flow-1">\n'
        )
        text = text.replace("</head>", link + "</head>", 1)

    if text != original:
        backup(path)
        path.write_text(text, encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)))

print("=== SACI GLOBAL TEXT FLOW FIX ===")
print(f"Updated CSS: {GLOBAL_CSS.relative_to(ROOT)}")
print(f"Updated HTML files: {len(changed)}")
print(f"Backups: {backup_root}")
for item in changed:
    print(f"  - {item}")
