#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

root = Path(__file__).resolve().parents[1]
docs = root / "docs"
final = docs / "data" / "final"
validation = docs / "data" / "validation"
errors = []

summary = json.loads((final / "integrity_summary.json").read_text(encoding="utf-8"))
expected = {
    "integrity_status": "VALID",
    "publication_gate": "OPEN",
    "calculated_saci": 100.0,
    "declared_nodes": 99,
    "rendered_nodes": 99,
    "edges": 171,
    "observed_edges": 171,
    "missing_edges": 0,
}
for key, value in expected.items():
    if summary.get(key) != value:
        errors.append(f"canonical {key}: expected {value!r}, got {summary.get(key)!r}")

counts = summary.get("finding_counts", {})
if any(int(counts.get(k, 0)) for k in ("INCOMPLETE", "INVALID", "WARNING", "INFO")):
    errors.append(f"active finding counts are not zero: {counts}")

page_checks = {
    docs / "index.html": ["CANONICAL_RELEASE_SYNC_START", "99 / 99", "171 / 171", "VALID", "OPEN"],
    docs / "en" / "index.html": ["CANONICAL_RELEASE_SYNC_START", "99 / 99", "171 / 171", "VALID", "OPEN"],
    docs / "integrity.html": ["F01_PORTAL_SYNC_START", "97 beyan / 99 render", "99 beyan / 99 render", "99,000"],
    docs / "en" / "integrity.html": ["F01_PORTAL_SYNC_START", "97 declared / 99 rendered", "99 declared / 99 rendered", "99,000"],
    docs / "methodology.html": ["VALIDATION_EXPERIMENTS_SYNC_START", "99.000"],
    docs / "en" / "methodology.html": ["VALIDATION_EXPERIMENTS_SYNC_START", "99,000"],
    docs / "evidence.html": ["EVIDENCE_CANONICAL_SYNC_START", "Kanonik final", "99/99"],
    docs / "en" / "evidence.html": ["EVIDENCE_CANONICAL_SYNC_START", "Canonical final", "99/99"],
}
for page, terms in page_checks.items():
    if not page.exists():
        errors.append(f"missing page: {page.relative_to(root)}")
        continue
    text = page.read_text(encoding="utf-8", errors="replace")
    for term in terms:
        if term not in text:
            errors.append(f"{page.relative_to(root)} missing marker/text: {term}")

stale_current = {
    docs / "index.html": [
        "Makalenin birincil sonucu <b>final</b> paketidir: 97",
        "edge uçları node tablosunda beyan edilmemiştir",
    ],
    docs / "en" / "index.html": [
        "97 declared nodes,\n          171 edge rows",
        "edge endpoints are not\n          declared in the node table",
    ],
}
for page, phrases in stale_current.items():
    text = page.read_text(encoding="utf-8", errors="replace")
    for phrase in phrases:
        if phrase in text:
            errors.append(f"stale current-state wording in {page.relative_to(root)}: {phrase}")

manifest = json.loads((final / "manifest.json").read_text(encoding="utf-8"))
for item in manifest.get("files", []):
    if item.get("name") == "saci_nodes.csv" and item.get("records_en") != "99 nodes":
        errors.append("manifest saci_nodes.csv record count is not 99 nodes")
    if item.get("name") == "saci_graph.cyjs" and item.get("records_en") != "99 nodes / 171 edges":
        errors.append("manifest graph record count is stale")

fault_path = validation / "integrity_fault_matrix.csv"
scale_path = validation / "integrity_scalability.csv"
for path in [
    fault_path,
    scale_path,
    validation / "benchmark_summary.json",
    validation / "BENCHMARK_PROTOCOL.md",
]:
    if not path.exists():
        errors.append(f"missing validation artifact: {path.relative_to(root)}")

if fault_path.exists():
    rows = list(csv.DictReader(fault_path.open(encoding="utf-8")))
    if len(rows) != 9:
        errors.append(f"fault matrix row count: expected 9, got {len(rows)}")
    if any(str(row.get("pass")) != "1" for row in rows):
        errors.append("fault matrix contains a failed case")

if scale_path.exists():
    rows = list(csv.DictReader(scale_path.open(encoding="utf-8")))
    if len(rows) != 4:
        errors.append(f"scalability row count: expected 4, got {len(rows)}")
    elif rows[-1].get("nodes") != "99000" or rows[-1].get("edge_rows") != "171000":
        errors.append("largest scalability case is not 99,000 nodes / 171,000 edge rows")

if errors:
    print("SACI portal-paper synchronization FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("SACI portal-paper synchronization PASSED")
print("Canonical: 99/99 nodes | 171/171 relations | VALID | OPEN")
print("F-01: preserved as a pre-release regression case")
print("Fault injection: 9/9 expected states matched")
print("Scalability: 99 to 99,000 nodes published")
