SACI PAPER VIEW — SIMPLE PALETTE

Değişiklikler:
- Mor, sarı ve kırmızı grafik renkleri kaldırıldı.
- Grafikler açık mavi, yumuşak mavi-gri ve nötr gri tonlarına indirildi.
- Yalnızca graph closure için düşük yoğunluklu yeşil bırakıldı.
- Kart ve figür yüzeyleri daha nötr hale getirildi.
- Tema davranışı korunur.

Kurulum:
cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_paper_view_simple_palette.zip -d .

Test:
python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/paper.html?palette=2
http://127.0.0.1:8000/en/paper.html?palette=2
