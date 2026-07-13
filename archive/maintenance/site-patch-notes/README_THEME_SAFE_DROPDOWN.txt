SACI PAPER VIEW — THEME-SAFE SCENARIO DROPDOWN

Bu sürüm native HTML select açılır listesini tamamen kaldırır.
Windows/Chromium tarafından beyaz çizilen işletim sistemi menüsü artık kullanılmaz.

Yerine:
- tema değişkenlerini kullanan özel açılır menü,
- senaryo arama alanı,
- sınırlı yükseklik ve iç kaydırma,
- dışarı tıklayınca kapanma,
- Escape ile kapanma,
- Dark / Dim / Light tema uyumu
eklenmiştir.

Kurulum:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_paper_view_theme_safe_dropdown.zip -d .

Test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/paper.html?scenario=FINAL&dropdown=5
http://127.0.0.1:8000/en/paper.html?scenario=S15&dropdown=5
