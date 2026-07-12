SACI EXPLANATION REPORT

Kurulum:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_explanation_report_page.zip -d .

Test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/explanation.html?report=1
http://127.0.0.1:8000/en/explanation.html?report=1

Sayfa mevcut docs/data/scenarios/manifest.json ve docs/en/data/scenarios/manifest.json
dosyalarını kullanır. Final ve S0-S18 açıklamalarını dinamik olarak üretir.
