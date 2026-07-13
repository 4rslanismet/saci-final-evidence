SACI DATA AND DOWNLOADABLE FILES PAGE

Files installed:
- docs/data.html
- docs/en/data.html
- docs/assets/data.css
- docs/assets/data.js
- docs/data/final/*

Canonical downloadable files:
- saci_scores.csv
- saci_scores.json
- saci_nodes.csv
- saci_edges.csv
- saci_graph.cyjs
- asset_log_coverage.csv
- control_coverage.csv
- mitre_coverage.csv
- ctic_coverage.csv
- log_source_status.csv
- reason_codes.csv
- reason_codes.json
- VALIDATION.txt
- FINAL_AUDIT_RESULT.md

Additional package files:
- SHA256SUMS.txt
- README_DATA_PACKAGE.txt
- saci_final_data_package.zip
- manifest.json

Installation:
1. Extract this ZIP into the repository root.
2. Run: python3 patch_data_nav.py
3. Test: python3 -m http.server 8000 --directory docs

URLs:
- http://127.0.0.1:8000/data.html
- http://127.0.0.1:8000/en/data.html

Canonical checks:
- SACI: 100.0
- Declared nodes: 97
- Rendered nodes: 99
- Edges: 171
- Observed: 171
- Missing: 0
- Asset-log pairs: 12/12
- Enabled controls seen: 25/25
- MITRE: 13/13
- CTI/MISP: 2/2
- Active reason codes: 0
