#!/usr/bin/env python3
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EN = DOCS / "en"
EN.mkdir(parents=True, exist_ok=True)

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

def make_header(active_file: str, lang: str) -> str:
    skip = "Skip to main content" if lang == "en" else "Ana içeriğe geç"

    nav = []
    for file, label in PAGES:
        cls = ' class="active"' if file == active_file else ""
        nav.append(f'<a{cls} href="{file}">{label}</a>')

    nav_html = "\n      ".join(nav)

    return f'''<a class="skip-link" href="#main">{skip}</a>

<header class="top">
  <div class="top-inner">
    <a class="brand" href="index.html">SACI Final Evidence</a>

    <nav class="nav" aria-label="Primary navigation">
      {nav_html}
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
</header>'''

def strip_old_header(html: str) -> str:
    html = re.sub(r'\s*<a[^>]*class="[^"]*skip[^"]*"[^>]*>[\s\S]*?</a>\s*', '\n', html, flags=re.I)
    html = re.sub(r'\s*<header class="top">[\s\S]*?</header>\s*', '\n', html, flags=re.I)
    html = re.sub(r'\s*<div class="utility">[\s\S]*?</div>\s*', '\n', html, flags=re.I)
    html = re.sub(r'\s*<nav class="primary-links">[\s\S]*?</nav>\s*', '\n', html, flags=re.I)
    return html

def ensure_main(html: str) -> str:
    return re.sub(r'<main(?![^>]*id=)', '<main id="main"', html, count=1, flags=re.I)

def fix_common_links(html: str, lang: str) -> str:
    is_en = lang == "en"

    # CSS / JS linklerini temizle
    html = re.sub(r'\s*<link rel="stylesheet" href="(\.\./)?assets/saci-standard\.css[^"]*">\s*', '\n', html)
    html = re.sub(r'\s*<script src="(\.\./)?assets/saci-ui\.js[^"]*"></script>\s*', '\n', html)

    css = "../assets/saci-standard.css?v=preserve-en-1" if is_en else "assets/saci-standard.css?v=preserve-en-1"
    js = "../assets/saci-ui.js?v=preserve-en-1" if is_en else "assets/saci-ui.js?v=preserve-en-1"

    html = html.replace("</head>", f'  <link rel="stylesheet" href="{css}">\n</head>', 1)
    html = html.replace("</body>", f'  <script src="{js}"></script>\n</body>', 1)

    return html

def fix_en_paths(html: str) -> str:
    # EN klasörü bir seviye aşağıda olduğu için asset/data yollarını yukarı al.
    # Zaten ../ ile başlayanları tekrar bozmaz.
    html = re.sub(r'(?<!\.\./)(["\'`])assets/', r'\1../assets/', html)
    html = re.sub(r'(?<!\.\./)(["\'`])data/', r'\1../data/', html)
    html = re.sub(r'(?<!\.\./)(["\'`])evidence/', r'\1../evidence/', html)

    # CSS url(...) pathleri
    html = re.sub(r'url\((["\']?)(?!\.\./)assets/', r'url(\1../assets/', html)
    html = re.sub(r'url\((["\']?)(?!\.\./)data/', r'url(\1../data/', html)

    # Architecture görseli EN’de İngilizce görsele dönsün
    html = html.replace("../assets/arch-tr.png", "../assets/arch-en.png")
    html = html.replace("assets/arch-tr.png", "../assets/arch-en.png")

    return html

def set_lang(html: str, lang: str) -> str:
    if re.search(r'<html[^>]*lang=', html, flags=re.I):
        html = re.sub(r'<html([^>]*)lang="[^"]*"', f'<html\\1lang="{lang}"', html, count=1, flags=re.I)
    else:
        html = re.sub(r'<html', f'<html lang="{lang}"', html, count=1, flags=re.I)
    return html

def sync_page(path: Path, active_file: str, lang: str) -> None:
    html = path.read_text(encoding="utf-8", errors="replace")
    html = strip_old_header(html)
    html = set_lang(html, lang)

    header = make_header(active_file, lang)
    html = re.sub(r'(<body[^>]*>)', r'\1\n' + header, html, count=1, flags=re.I)

    html = ensure_main(html)
    html = fix_common_links(html, lang)

    if lang == "en":
        html = fix_en_paths(html)

    path.write_text(html, encoding="utf-8")

def main() -> None:
    for file, _label in PAGES:
        tr_path = DOCS / file
        en_path = EN / file

        if not tr_path.exists():
            print("[!] missing TR page:", tr_path)
            continue

        # EN sayfa TR sayfanın birebir kopyasından başlar
        shutil.copy2(tr_path, en_path)

        # TR header temiz
        sync_page(tr_path, file, "tr")

        # EN header + path temiz
        sync_page(en_path, file, "en")

        print("[+] rebuilt pair:", tr_path, en_path)

if __name__ == "__main__":
    main()
