SACI REFERENCES PAGE

Files:
- docs/references.html
- docs/en/references.html
- docs/assets/references.css
- patch_references_nav.py

Navigation order:
Home · Methodology · Architecture · Evidence · Scenarios · Artifacts · Data · References · Graph · Explanation · Paper View

Artifacts should remain:
- Artifacts = implementation/reproducibility outputs
- Data = canonical machine-readable datasets
- References = external official/technical/academic sources

Install:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_references_page.zip -d .
python3 patch_references_nav.py

Test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/references.html
http://127.0.0.1:8000/en/references.html
