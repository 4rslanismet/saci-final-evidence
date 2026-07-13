SACI ARTIFACTS HOTFIX

Problem found in the uploaded site:
- docs/artifacts.html was missing.
- Only docs/en/artifacts.html existed.
- Turkish navigation therefore opened a missing page.
- The English Artifacts page was also an older version with legacy final_v2 links.

This hotfix installs:
- docs/artifacts.html
- docs/en/artifacts.html
- docs/assets/artifacts.css

Install from the repository root:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_artifacts_hotfix.zip -d .

Test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/artifacts.html?hotfix=1
http://127.0.0.1:8000/en/artifacts.html?hotfix=1

Verification:

test -f docs/artifacts.html && echo "TR artifacts OK"
test -f docs/en/artifacts.html && echo "EN artifacts OK"
test -f docs/assets/artifacts.css && echo "Artifacts CSS OK"
