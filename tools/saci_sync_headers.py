#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MANIFEST = ROOT / "tools" / "site_manifest.json"

pages = json.loads(MANIFEST.read_text(encoding="utf-8"))

HEADER = '''<a class="skip-link" href="#main">Ana içeriğe geç</a>

<header class="top">
  <div class="top-inner">
    <a class="brand" href="index.html">SACI Final Evidence</a>

    <nav class="nav" aria-label="Primary navigation">
      {nav_links}
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
</header>
'''

def nav_for(current_file):
    links = []
    for item in pages:
        f = item["file"]
        label = item["label"]
        if not (DOCS / f).exists() and not (DOCS / "en" / f).exists():
            continue
        cls = ' class="active"' if f == current_file else ""
        links.append(f'<a{cls} href="{f}">{label}</a>')
    return "\n      ".join(links)

def clean_and_sync(path, is_en):
    html = path.read_text(encoding="utf-8", errors="replace")
    current = path.name

    html = re.sub(r'\s*<a[^>]*class="[^"]*skip[^"]*"[^>]*>[\s\S]*?</a>\s*', '\n', html, flags=re.I)
    html = re.sub(r'\s*<header class="top">[\s\S]*?</header>\s*', '\n', html, flags=re.I)
    html = re.sub(r'\s*<div class="utility">[\s\S]*?</div>\s*', '\n', html, flags=re.I)
    html = re.sub(r'\s*<nav class="primary-links">[\s\S]*?</nav>\s*', '\n', html, flags=re.I)

    header = HEADER.format(nav_links=nav_for(current))

    html = re.sub(r'(<body[^>]*>)', r'\1\n' + header, html, count=1, flags=re.I)
    html = re.sub(r'<main(?![^>]*id=)', '<main id="main"', html, count=1, flags=re.I)

    css_path = "../assets/saci-standard.css" if is_en else "assets/saci-standard.css"
    js_path = "../assets/saci-ui.js" if is_en else "assets/saci-ui.js"

    html = re.sub(r'\s*<link rel="stylesheet" href="(\.\./)?assets/saci-standard\.css[^"]*">\s*', '\n', html)
    html = re.sub(r'\s*<script src="(\.\./)?assets/saci-ui\.js[^"]*"></script>\s*', '\n', html)

    if "</head>" in html:
        html = html.replace("</head>", f'  <link rel="stylesheet" href="{css_path}?v=sync-header-1">\n</head>', 1)

    if "</body>" in html:
        html = html.replace("</body>", f'  <script src="{js_path}?v=sync-header-1"></script>\n</body>', 1)

    path.write_text(html, encoding="utf-8")
    print("[+] synced:", path)

for item in pages:
    tr = DOCS / item["file"]
    en = DOCS / "en" / item["file"]

    if tr.exists():
        clean_and_sync(tr, False)

    if en.exists():
        clean_and_sync(en, True)
