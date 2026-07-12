SACI COMPACT HEADER CONTROLS

Üst menüdeki uzun kontrol grubu şu görünüme dönüşür:

TR · A ▾ · Tema ▾

Davranış:
- TR/EN düğmesi doğrudan diğer dile geçer.
- A düğmesi küçük font menüsü açar.
- Tema düğmesi Dark/Dim/Light menüsü açar.
- Mevcut saci-ui.js ve localStorage davranışları korunur.
- Responsive header fallback çalışmaya devam eder.
- Bütün TR/EN sayfalar güncellenir.
- Yedekler backups/ altında oluşturulur.

Kurulum:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_compact_header_controls.zip -d .
python3 apply_compact_header_controls.py

Kontrol:

node --check docs/assets/saci-compact-controls.js
python3 tools/validate_academic_site.py

Lokal test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/paper.html?compact_controls=1
http://127.0.0.1:8000/reproducibility.html?compact_controls=1
http://127.0.0.1:8000/en/paper.html?compact_controls=1

Tarayıcıda Ctrl+Shift+R yap.
