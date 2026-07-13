SACI METHODOLOGY RHYTHM — ALL PAGES

Bu paket önceki genişlik yamalarını temizler ve Methodology sayfasındaki
gerçek metin ölçülerini bütün portalda ortak standart olarak uygular.

Kaynak alınan Methodology değerleri:
- H1 max-width: 1180px
- Lead max-width: 980px
- Narrative section max-width: 1120px
- Body copy max-width: 1040px
- Paragraph: 17px / line-height 1.8
- Paragraph gap: 16px
- Section padding: 54px
- Intro-to-content gap: 72px

Önemli:
- Graph, tablo, kart, figure ve uygulama panelleri daraltılmaz.
- Yalnızca başlık altı metinler, anlatı paragrafları ve section heading copy
  Methodology ritmine alınır.
- Önceki runtime ve width yamaları kaldırılır.
- TR ve EN sayfaları birlikte güncellenir.

Kurulum:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_methodology_rhythm_all_pages.zip -d .
python3 apply_methodology_rhythm.py

Test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/index.html?rhythm=1
http://127.0.0.1:8000/methodology.html?rhythm=1
http://127.0.0.1:8000/architecture.html?rhythm=1
http://127.0.0.1:8000/scenarios.html?rhythm=1
http://127.0.0.1:8000/graph.html?rhythm=1
http://127.0.0.1:8000/en/architecture.html?rhythm=1

Tarayıcıda Ctrl+Shift+R yap.
