SACI PAPER VIEW

Kurulum:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_paper_view_page.zip -d .

Lokal test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/paper.html?paper_view=1
http://127.0.0.1:8000/en/paper.html?paper_view=1

Sayfa şunları içerir:

- Final SACI score card
- Graph closure card
- MITRE ATT&CK coverage card
- CTI/MISP coverage card
- Final component profile figure
- Evidence graph closure figure
- MITRE/CTI coverage figure
- SVG export buttons
- Print / Save as PDF
- Short academic interpretation paragraphs
- Structural graph-integrity note
- Turkish and English pages

Veriler docs/data/scenarios/manifest.json ile final veri kümesindeki
score CSV, graph CYJS, MITRE coverage CSV ve CTI coverage CSV dosyalarından
dinamik olarak yüklenir.
