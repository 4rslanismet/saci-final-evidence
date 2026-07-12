#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EN = DOCS / "en"
MANIFEST = ROOT / "tools" / "site_manifest.json"

if len(sys.argv) < 5:
    print("Usage: python3 tools/saci_new_page.py <file.html> <Nav Label> <TR Title> <EN Title>")
    print('Example: python3 tools/saci_new_page.py validation.html "Validation" "Doğrulama" "Validation"')
    raise SystemExit(1)

file_name = sys.argv[1]
label = sys.argv[2]
tr_title = sys.argv[3]
en_title = sys.argv[4]

if not file_name.endswith(".html"):
    raise SystemExit("file must end with .html")

DOCS.mkdir(exist_ok=True)
EN.mkdir(exist_ok=True)

pages = json.loads(MANIFEST.read_text(encoding="utf-8"))
if not any(p["file"] == file_name for p in pages):
    pages.append({"file": file_name, "label": label})
    MANIFEST.write_text(json.dumps(pages, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

base_style = '''<!doctype html>
<html lang="{lang}" data-theme="dim" data-font-level="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
</head>
<body>
  <main id="main">
    <section>
      <div class="kicker">{kicker}</div>
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </section>

    <section class="section">
      <h2>{section_title}</h2>
      <p>{body_1}</p>
      <p>{body_2}</p>
    </section>

    <footer>
      SACI Final Evidence — {footer}
    </footer>
  </main>
</body>
</html>
'''

tr_path = DOCS / file_name
en_path = EN / file_name

if not tr_path.exists():
    tr_path.write_text(base_style.format(
        lang="tr",
        title=tr_title,
        kicker=label.upper(),
        lead="Bu sayfa SACI final evidence portalının ilgili bölümünü açıklar.",
        section_title="Genel açıklama",
        body_1="Bu bölümde ilgili sayfanın amacı, kullandığı veri ve SACI modeli içindeki yeri açıklanır.",
        body_2="Yayın paketine eklenecek her sayfa Türkçe ve İngilizce olarak ayrı dosyalarda tutulur.",
        footer=label
    ), encoding="utf-8")

if not en_path.exists():
    en_path.write_text(base_style.format(
        lang="en",
        title=en_title,
        kicker=label.upper(),
        lead="This page explains the corresponding section of the SACI final evidence portal.",
        section_title="Overview",
        body_1="This section explains the purpose of the page, the data it uses, and its role within the SACI model.",
        body_2="Each page added to the publication package is maintained as a separate Turkish and English file.",
        footer=label
    ), encoding="utf-8")

subprocess.run(["python3", str(ROOT / "tools" / "saci_sync_headers.py")], check=True)
print("[+] created page pair:", tr_path, en_path)
