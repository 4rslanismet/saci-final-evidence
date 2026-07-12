SACI REMAINING COPY WIDTH FIX

Yalnızca şu sayfaları etkiler:
- docs/index.html
- docs/methodology.html
- docs/graph.html
- docs/en/index.html
- docs/en/methodology.html
- docs/en/graph.html

Düzeltmeler:
- Home giriş paragrafları 1240 px'e kadar genişler.
- Home editorial metinleri 1220 px'e kadar genişler.
- Methodology section ve paragrafları 1280–1360 px'e kadar genişler.
- Graph giriş paragrafı 1320 px'e kadar genişler.
- Başlık ölçüleri değiştirilmez.
- Diğer sayfalar etkilenmez.
- Mobil ve tablet davranışı korunur.

Kurulum:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_remaining_copy_width_fix.zip -d .
python3 fix_remaining_copy_width.py

Test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/index.html?copy_width=1
http://127.0.0.1:8000/methodology.html?copy_width=1
http://127.0.0.1:8000/graph.html?copy_width=1
http://127.0.0.1:8000/en/index.html?copy_width=1

Tarayıcıda Ctrl+Shift+R yap.
