SACI DATA PAGE — EN PATH FIX

Problem:
docs/en/data.html resolved data/final/... as docs/en/data/final/... and received HTTP 404.

Fix:
- English page now loads ../data/final/manifest.json.
- All dynamic file download paths are resolved from docs root.
- English fallback links use ../data/final/.
- Turkish paths remain unchanged.
- Shared asset cache version was increased.

Install:
cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_data_downloads_en_path_fix.zip -d .

Test:
python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/data.html?data_path=2
http://127.0.0.1:8000/en/data.html?data_path=2
