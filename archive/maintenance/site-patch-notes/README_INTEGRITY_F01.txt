SACI FINDING F-01 AND INDEPENDENT INTEGRITY GATE

Install:
cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_integrity_f01_phase.zip -d .
python3 apply_integrity_f01.py

Validate:
python3 tools/validate_integrity.py --data-dir docs/data/final --check
python3 tools/validate_all.py

Exit codes:
0 VALID
1 VALID_WITH_WARNINGS
2 INVALID
3 INCOMPLETE

The first run may intentionally return INVALID or VALID_WITH_WARNINGS.
That means the gate captured the existing structural finding; it is not an installation failure.

Web:
python3 -m http.server 8000 --directory docs
http://127.0.0.1:8000/integrity.html
http://127.0.0.1:8000/en/integrity.html
