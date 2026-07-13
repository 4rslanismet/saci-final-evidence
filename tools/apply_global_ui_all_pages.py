#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import os
import re
import shutil

ROOT = Path.cwd()
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
CSS_FILE = ASSETS / "saci-global-ui.css"

VERSION = "global-ui-20260711-1"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "backups" / f"global_ui_all_pages_{STAMP}"

if not DOCS.exists():
    raise SystemExit(
        "[!] docs/ bulunamadı. Script repo kökünde çalıştırılmalı."
    )

HTML_FILES = sorted(
    path
    for path in DOCS.rglob("*.html")
    if "backup" not in path.as_posix().lower()
)

GLOBAL_CSS = r'''
/*
 * SACI Global Page Standard
 * Applies to every Turkish and English page.
 */

/* =========================================================
   BASE
   ========================================================= */

html {
  scroll-behavior: smooth;
  scroll-padding-top: 96px;
}

body {
  margin: 0 !important;
  overflow-x: hidden;
}

body,
button,
input,
select,
textarea {
  font-family:
    Inter,
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif !important;
}

.skip-link {
  position: fixed !important;
  top: 10px !important;
  left: 10px !important;
  z-index: 9999 !important;
  transform: translateY(-180%) !important;
  padding: 9px 12px !important;
  border-radius: 8px !important;
  background: var(--text) !important;
  color: var(--bg) !important;
  text-decoration: none !important;
}

.skip-link:focus {
  transform: translateY(0) !important;
}


/* =========================================================
   GLOBAL TOP HEADER
   ========================================================= */

.top {
  position: sticky !important;
  top: 0 !important;
  z-index: 100 !important;

  width: 100% !important;
  min-height: 76px !important;

  border-bottom:
    1px solid
    color-mix(
      in srgb,
      var(--line) 76%,
      transparent
    ) !important;

  background:
    color-mix(
      in srgb,
      var(--bg) 91%,
      transparent
    ) !important;

  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
}

.top-inner {
  width: min(calc(100% - 48px), 1460px) !important;
  max-width: none !important;
  min-height: 76px !important;

  margin-inline: auto !important;
  padding: 0 !important;

  display: grid !important;
  grid-template-columns:
    max-content
    minmax(0, 1fr)
    max-content !important;

  align-items: center !important;
  gap: clamp(20px, 2.2vw, 38px) !important;
}


/* Brand */

.brand {
  display: inline-flex !important;
  align-items: center !important;

  margin: 0 !important;
  padding: 0 !important;

  color: var(--text) !important;
  text-decoration: none !important;
  white-space: nowrap !important;

  font-size: 16px !important;
  font-weight: 750 !important;
  line-height: 1.2 !important;
  letter-spacing: -0.015em !important;
}


/* Main navigation */

.nav {
  min-width: 0 !important;

  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-wrap: nowrap !important;

  gap: clamp(13px, 1.45vw, 24px) !important;

  margin: 0 !important;
  padding: 0 !important;
}

.nav a {
  position: relative !important;

  display: inline-flex !important;
  align-items: center !important;

  min-height: 38px !important;
  margin: 0 !important;
  padding: 0 !important;

  color: var(--muted) !important;
  text-decoration: none !important;
  white-space: nowrap !important;

  font-size: 14px !important;
  font-weight: 580 !important;
  line-height: 1.2 !important;

  transition:
    color .15s ease,
    opacity .15s ease !important;
}

.nav a:hover {
  color: var(--text) !important;
}

.nav a.active {
  color: var(--text) !important;
  font-weight: 680 !important;
}

.nav a.active::after {
  content: "" !important;

  position: absolute !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 1px !important;

  height: 1px !important;

  background:
    color-mix(
      in srgb,
      var(--accent) 76%,
      var(--text)
    ) !important;
}


/* Header controls */

.top-actions {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  flex-wrap: nowrap !important;

  gap: 13px !important;

  margin: 0 !important;
  padding: 0 !important;

  white-space: nowrap !important;
}

.top-control {
  display: inline-flex !important;
  align-items: center !important;

  gap: 6px !important;

  margin: 0 !important;
  padding: 0 !important;

  color: var(--muted) !important;
  font-size: 12px !important;
  line-height: 1 !important;
}

.top-control > span {
  margin-right: 1px !important;
  color: var(--muted) !important;
  font-size: 12px !important;
  font-weight: 540 !important;
}

.top-control button {
  appearance: none !important;

  min-width: 22px !important;
  min-height: 28px !important;

  margin: 0 !important;
  padding: 3px 4px !important;

  border: 0 !important;
  border-radius: 5px !important;

  background: transparent !important;
  color: var(--muted) !important;

  font: inherit !important;
  font-size: 12px !important;
  font-weight: 580 !important;
  line-height: 1 !important;

  cursor: pointer !important;
}

.top-control button:hover {
  color: var(--text) !important;
  background:
    color-mix(
      in srgb,
      var(--text) 6%,
      transparent
    ) !important;
}

.top-control button.active,
.top-control button[aria-pressed="true"] {
  color: var(--text) !important;

  background:
    color-mix(
      in srgb,
      var(--accent) 8%,
      transparent
    ) !important;

  outline:
    1px solid
    color-mix(
      in srgb,
      var(--accent) 42%,
      var(--line)
    ) !important;
}


/* =========================================================
   GLOBAL CONTENT WIDTH AND TOP SPACING
   ========================================================= */

main,
.page,
.page-main,
.page-wrap,
.content,
.content-wrap {
  margin-top: 0 !important;
}

main,
main.page,
main.page-main,
.page-main {
  width:
    min(
      calc(100% - clamp(40px, 8vw, 128px)),
      1340px
    ) !important;

  max-width: none !important;

  margin-inline: auto !important;

  padding-top: clamp(34px, 4.2vw, 58px) !important;
  padding-bottom: clamp(56px, 7vw, 96px) !important;
}


/*
 * Graph uses a wider working surface.
 */

body[data-page="graph"] main {
  width:
    min(
      calc(100% - clamp(32px, 6vw, 96px)),
      1760px
    ) !important;
}


/* =========================================================
   GLOBAL HERO / PAGE INTRO
   ========================================================= */

.graph-hero,
.page-hero,
.hero,
.hero-section,
.page-intro,
.page-header,
.page-header-block,
.content-hero,
.intro-section,
main > section:first-child {
  margin-top: 0 !important;
}


/* Kicker / eyebrow */

.kicker,
.eyebrow,
.overline,
.page-kicker,
.page-eyebrow,
.hero-kicker,
.section-kicker,
.intro-kicker,
.page-label,
.graph-hero .kicker,
main > section:first-child > .kicker,
main > section:first-child > .eyebrow {
  display: inline-flex !important;
  align-items: center !important;

  margin: 0 0 17px 0 !important;
  padding: 0 !important;

  border: 0 !important;
  background: transparent !important;

  color: var(--accent) !important;

  font-size: 12px !important;
  font-weight: 740 !important;
  line-height: 1.25 !important;
  letter-spacing: .14em !important;
  text-transform: uppercase !important;

  opacity: .96 !important;
}


/* Main title */

.graph-hero h1,
.page-hero h1,
.hero h1,
.hero-section h1,
.page-intro h1,
.page-header h1,
.page-header-block h1,
.content-hero h1,
.intro-section h1,
main > section:first-child > h1 {
  max-width: 19ch !important;

  margin: 0 0 20px 0 !important;

  color: var(--text) !important;

  font-size:
    clamp(
      46px,
      5.6vw,
      78px
    ) !important;

  font-weight: 720 !important;
  line-height: 1.01 !important;
  letter-spacing: -.05em !important;

  text-wrap: balance !important;
}


/* Lead / intro paragraphs */

.graph-hero .lead,
.page-hero .lead,
.hero .lead,
.hero-section .lead,
.page-intro .lead,
.page-header .lead,
.page-header-block .lead,
.content-hero .lead,
.intro-section .lead,
.page-summary,
.page-lead,
main > section:first-child > p {
  max-width: 78ch !important;

  margin: 0 0 15px 0 !important;

  color: var(--muted) !important;

  font-size:
    clamp(
      17px,
      .5vw + 15px,
      21px
    ) !important;

  line-height: 1.72 !important;
  letter-spacing: 0 !important;

  overflow-wrap: normal !important;
  word-break: normal !important;
}


/* Scope note or smaller paragraph in hero */

.scope-note,
.hero-note,
.intro-note,
.architecture-scope-note,
.graph-scope-note {
  max-width: 78ch !important;

  margin-top: 19px !important;

  color: var(--muted) !important;

  font-size: 14.5px !important;
  line-height: 1.72 !important;
}


/* Prevent old oversized empty hero containers */

.graph-hero,
.page-hero,
.hero,
.hero-section,
.page-intro,
.page-header,
.page-header-block,
.content-hero,
.intro-section {
  min-height: 0 !important;
  height: auto !important;

  padding-top: 0 !important;
  padding-bottom: clamp(18px, 2.8vw, 32px) !important;
}


/* =========================================================
   HEADINGS AND PARAGRAPHS
   ========================================================= */

main h2 {
  max-width: 30ch;

  margin-top: clamp(48px, 6vw, 82px);
  margin-bottom: 18px;

  color: var(--text);

  font-size: clamp(30px, 3.2vw, 44px);
  font-weight: 680;
  line-height: 1.1;
  letter-spacing: -.035em;
}

main h3 {
  color: var(--text);
  line-height: 1.25;
}

main p {
  overflow-wrap: normal;
  word-break: normal;
}


/* =========================================================
   GRAPH PAGE SPECIFIC TOP AREA
   ========================================================= */

body[data-page="graph"] .graph-hero {
  margin-bottom: 8px !important;
}

body[data-page="graph"] .graph-hero h1 {
  max-width: 20ch !important;
}

body[data-page="graph"] .graph-toolbar {
  margin-top: 12px !important;
}


/* =========================================================
   ARCHITECTURE PAGE SPECIFIC TOP AREA
   ========================================================= */

body[data-page="architecture"] .page-hero h1,
body[data-page="architecture"] .hero h1,
body[data-page="architecture"] .page-intro h1,
body[data-page="architecture"] main > section:first-child > h1 {
  max-width: 22ch !important;
}

body[data-page="architecture"] .architecture-final-intro {
  max-width: 86ch !important;
}

body[data-page="architecture"] .architecture-final-intro p {
  max-width: 82ch !important;
  line-height: 1.76 !important;
}


/* =========================================================
   RESPONSIVE HEADER
   ========================================================= */

@media (max-width: 1280px) {
  .top-inner {
    grid-template-columns:
      max-content
      minmax(0, 1fr) !important;

    gap:
      8px
      24px !important;

    padding-block: 12px !important;
  }

  .top-actions {
    grid-column: 1 / -1 !important;
    justify-self: end !important;
  }

  .nav {
    justify-content: flex-end !important;
  }
}


@media (max-width: 900px) {
  .top {
    position: relative !important;
  }

  .top-inner {
    width: min(calc(100% - 30px), 1460px) !important;

    grid-template-columns: 1fr !important;

    gap: 8px !important;

    padding-block: 14px !important;
  }

  .brand {
    justify-self: start !important;
  }

  .nav {
    width: 100% !important;

    justify-content: flex-start !important;

    overflow-x: auto !important;
    overscroll-behavior-inline: contain !important;

    padding-bottom: 3px !important;

    scrollbar-width: thin;
  }

  .top-actions {
    grid-column: auto !important;
    justify-self: start !important;

    width: 100% !important;

    overflow-x: auto !important;

    padding-bottom: 3px !important;
  }

  main,
  main.page,
  main.page-main,
  .page-main,
  body[data-page="graph"] main {
    width: min(calc(100% - 34px), 1340px) !important;
    padding-top: 28px !important;
  }

  .graph-hero h1,
  .page-hero h1,
  .hero h1,
  .hero-section h1,
  .page-intro h1,
  .page-header h1,
  .page-header-block h1,
  .content-hero h1,
  .intro-section h1,
  main > section:first-child > h1 {
    max-width: 100% !important;

    font-size:
      clamp(
        38px,
        9vw,
        58px
      ) !important;
  }
}


@media (max-width: 600px) {
  .top-control > span {
    display: none !important;
  }

  .top-actions {
    gap: 9px !important;
  }

  main,
  main.page,
  main.page-main,
  .page-main,
  body[data-page="graph"] main {
    width: min(calc(100% - 24px), 1340px) !important;
    padding-top: 22px !important;
  }

  .kicker,
  .eyebrow,
  .overline,
  .page-kicker,
  .page-eyebrow,
  .hero-kicker,
  .section-kicker,
  .intro-kicker,
  .page-label,
  .graph-hero .kicker {
    margin-bottom: 13px !important;

    font-size: 11px !important;
    letter-spacing: .12em !important;
  }

  .graph-hero .lead,
  .page-hero .lead,
  .hero .lead,
  .hero-section .lead,
  .page-intro .lead,
  .page-header .lead,
  .page-header-block .lead,
  .content-hero .lead,
  .intro-section .lead,
  .page-summary,
  .page-lead,
  main > section:first-child > p {
    font-size: 16px !important;
    line-height: 1.66 !important;
  }
}
'''


def backup_file(path: Path) -> None:
    target = BACKUP / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def infer_page_name(path: Path) -> str:
    name = path.stem.lower()

    if name == "index":
        return "home"

    return re.sub(r"[^a-z0-9_-]+", "-", name)


def add_body_page_attribute(html: str, page_name: str) -> str:
    body_match = re.search(
        r"<body\b([^>]*)>",
        html,
        flags=re.I,
    )

    if not body_match:
        return html

    attrs = body_match.group(1)

    if re.search(r"\bdata-page\s*=", attrs, flags=re.I):
        attrs = re.sub(
            r'\bdata-page\s*=\s*["\'][^"\']*["\']',
            f'data-page="{page_name}"',
            attrs,
            flags=re.I,
        )
    else:
        attrs = attrs.rstrip() + f' data-page="{page_name}"'

    replacement = f"<body{attrs}>"

    return (
        html[:body_match.start()]
        + replacement
        + html[body_match.end():]
    )


def relative_asset_href(page: Path) -> str:
    relative = os.path.relpath(
        CSS_FILE,
        start=page.parent,
    )

    return Path(relative).as_posix()


def patch_html(page: Path) -> None:
    html = page.read_text(
        encoding="utf-8",
        errors="replace",
    )

    html = re.sub(
        r'\s*<link[^>]+saci-global-ui\.css[^>]*>\s*',
        "\n",
        html,
        flags=re.I,
    )

    page_name = infer_page_name(page)
    html = add_body_page_attribute(
        html,
        page_name,
    )

    href = relative_asset_href(page)

    link = (
        f'<link rel="stylesheet" '
        f'href="{href}?v={VERSION}">'
    )

    if "</head>" not in html:
        raise RuntimeError(
            f"</head> bulunamadı: {page}"
        )

    html = html.replace(
        "</head>",
        f"  {link}\n</head>",
        1,
    )

    page.write_text(
        html,
        encoding="utf-8",
    )


ASSETS.mkdir(parents=True, exist_ok=True)

if CSS_FILE.exists():
    backup_file(CSS_FILE)

CSS_FILE.write_text(
    GLOBAL_CSS.strip() + "\n",
    encoding="utf-8",
)

updated = 0

for page in HTML_FILES:
    backup_file(page)
    patch_html(page)
    updated += 1
    print(f"[+] Güncellendi: {page.relative_to(ROOT)}")

print()
print("=== GLOBAL UI APPLIED TO ALL PAGES ===")
print(f"HTML pages: {updated}")
print(f"Global CSS: {CSS_FILE}")
print(f"Backup: {BACKUP}")
