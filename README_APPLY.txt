SACI WEB + VAGRANT REPRODUCIBILITY — PHASE 1

Install from repository root:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_web_reproducibility_phase1_patch.zip -d .

Validate syntax and site:

ruby -c Vagrantfile
python3 -m json.tool lab/topology.json >/dev/null
python3 tools/validate_academic_site.py
python3 -m http.server 8000 --directory docs

Open:
http://127.0.0.1:8000/reproducibility.html
http://127.0.0.1:8000/en/reproducibility.html
http://127.0.0.1:8000/artifacts.html

Evidence-only VM:
SACI_LAB_PROFILE=evidence vagrant up --provider=virtualbox
