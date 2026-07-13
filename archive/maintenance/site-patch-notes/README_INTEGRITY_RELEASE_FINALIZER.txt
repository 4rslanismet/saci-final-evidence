SACI INTEGRITY RELEASE FINALIZER

Purpose:
- Make validate_integrity.py --check read-only.
- Keep integrity_summary.json hash stable.
- Update academic validator to the 99/99 canonical graph.
- Remove the old undeclared-endpoint expectation.
- Rebuild SHA256SUMS.txt without circular self-references.
- Rebuild saci_final_data_package.zip with SHA256SUMS.txt included.
- Refresh manifest bundle metadata.
- Run all validators twice to prove repeatability.

Install:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_integrity_release_finalizer.zip -d .
python3 finalize_integrity_release.py

Expected result:

Integrity status : VALID
Publication gate : OPEN
Final graph: 99 declared / 99 rendered nodes
171/171 observed relations
Canonical ZIP includes SHA256SUMS.txt
All validators pass twice.
