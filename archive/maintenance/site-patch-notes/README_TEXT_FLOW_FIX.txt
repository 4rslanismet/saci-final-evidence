SACI GLOBAL TEXT FLOW FIX

Amaç:
- Hero başlıklarının yapay max-width sınırları nedeniyle bölünmesini kaldırır.
- Açıklama ve section metinlerini 112ch genişliğe kadar doğal akıtır.
- Tüm TR ve EN HTML sayfalarında shared CSS cache sürümünü yeniler.
- Teknik dosya adı/hash gibi değerlerde kontrollü taşmayı korur.
- Mobil görünümde doğal satır kırmayı sürdürür.

Kurulum:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_global_text_flow_fix.zip -d .
python3 fix_text_flow_all_pages.py

Test:

python3 -m http.server 8000 --directory docs

Örnek:
http://127.0.0.1:8000/data.html?text_flow=1
http://127.0.0.1:8000/en/data.html?text_flow=1
http://127.0.0.1:8000/paper.html?text_flow=1
http://127.0.0.1:8000/explanation.html?text_flow=1

Tarayıcıda Ctrl+F5 yap.
