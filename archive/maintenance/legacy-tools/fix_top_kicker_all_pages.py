#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.cwd()
CSS = ROOT / "docs" / "assets" / "saci-standard.css"

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT / "backups" / f"top_kicker_fix_{STAMP}"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

if not CSS.exists():
    raise SystemExit(f"CSS bulunamadı: {CSS}")

shutil.copy2(CSS, BACKUP_DIR / CSS.name)

css = CSS.read_text(encoding="utf-8", errors="replace")

start_tag = "/* SACI_TOP_KICKER_NORMALIZE_START */"
end_tag   = "/* SACI_TOP_KICKER_NORMALIZE_END */"

css = re.sub(
    re.escape(start_tag) + r".*?" + re.escape(end_tag),
    "",
    css,
    flags=re.S
)

block = r'''
/* SACI_TOP_KICKER_NORMALIZE_START */

/* Üst menü sonrası içerik başlangıcı */
.page-shell,
.page-wrap,
main,
main.page-main,
body .page-main,
body[data-page] main {
  padding-top: 0 !important;
}

/* Hero / page intro alanı */
.page-hero,
.hero,
.hero-block,
.page-header-block,
.page-intro,
.content-hero,
.section-hero,
main > header:first-of-type,
body[data-page] .hero-section {
  margin-top: 0 !important;
  padding-top: clamp(28px, 4vw, 44px) !important;
  padding-bottom: clamp(18px, 2.6vw, 28px) !important;
}

/* Hero iç genişliği */
.page-hero .container,
.hero .container,
.page-intro .container,
.page-header-block .container,
main > header:first-of-type .container,
.page-hero,
.hero,
.page-intro,
.page-header-block {
  max-width: min(1280px, calc(100vw - 64px)) !important;
}

/* Küçük üst başlık / kicker / eyebrow */
.page-eyebrow,
.eyebrow,
.kicker,
.overline,
.page-kicker,
.section-kicker,
.hero-kicker,
.intro-kicker,
header .eyebrow,
header .kicker,
body[data-page] .page-label {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  margin: 0 0 16px 0 !important;
  padding: 0 !important;
  border: 0 !important;
  background: transparent !important;
  color: var(--accent, #8ec5ff) !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  line-height: 1.25 !important;
  letter-spacing: .14em !important;
  text-transform: uppercase !important;
  opacity: .95 !important;
  max-width: none !important;
}

/* Hero ana başlık */
.page-hero h1,
.hero h1,
.page-intro h1,
.page-header-block h1,
main > header:first-of-type h1,
body[data-page] .page-title {
  margin: 0 0 18px 0 !important;
  max-width: 16ch !important;
  color: var(--text) !important;
  font-size: clamp(42px, 5.8vw, 74px) !important;
  font-weight: 760 !important;
  line-height: .98 !important;
  letter-spacing: -.04em !important;
  text-wrap: balance !important;
}

/* Hero açıklama metni */
.page-hero p,
.hero p,
.page-intro p,
.page-header-block p,
main > header:first-of-type p,
body[data-page] .page-summary,
body[data-page] .page-lead {
  margin: 0 0 14px 0 !important;
  max-width: 78ch !important;
  color: var(--muted) !important;
  font-size: clamp(17px, 1.45vw, 22px) !important;
  line-height: 1.68 !important;
}

/* Graph sayfasında üst boşluk ve etiket */
body[data-page="graph"] .page-hero,
body[data-page="graph"] .hero,
body[data-page="graph"] .page-intro,
body[data-page="graph"] main > header:first-of-type {
  padding-top: clamp(24px, 3.5vw, 36px) !important;
}

body[data-page="graph"] .page-eyebrow,
body[data-page="graph"] .eyebrow,
body[data-page="graph"] .kicker,
body[data-page="graph"] .section-kicker {
  margin-bottom: 14px !important;
}

/* Mobil */
@media (max-width: 900px) {
  .page-hero,
  .hero,
  .page-intro,
  .page-header-block,
  main > header:first-of-type {
    padding-top: 22px !important;
    padding-bottom: 18px !important;
  }

  .page-hero h1,
  .hero h1,
  .page-intro h1,
  .page-header-block h1,
  main > header:first-of-type h1 {
    max-width: 100% !important;
    font-size: clamp(34px, 8vw, 52px) !important;
    line-height: 1.02 !important;
  }

  .page-hero p,
  .hero p,
  .page-intro p,
  .page-header-block p,
  main > header:first-of-type p {
    font-size: 16px !important;
    line-height: 1.65 !important;
  }
}

/* Çok dar ekran */
@media (max-width: 640px) {
  .page-hero,
  .hero,
  .page-intro,
  .page-header-block,
  main > header:first-of-type {
    padding-top: 18px !important;
    padding-bottom: 14px !important;
  }

  .page-eyebrow,
  .eyebrow,
  .kicker,
  .overline,
  .page-kicker,
  .section-kicker {
    font-size: 11px !important;
    letter-spacing: .12em !important;
    margin-bottom: 12px !important;
  }
}

/* SACI_TOP_KICKER_NORMALIZE_END */
'''.strip()

css = css.rstrip() + "\n\n" + block + "\n"
CSS.write_text(css, encoding="utf-8")

print("=== TOP KICKER / HERO NORMALIZATION DONE ===")
print(f"Backup: {BACKUP_DIR / CSS.name}")
print(f"Patched: {CSS}")
