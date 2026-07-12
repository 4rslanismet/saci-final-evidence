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
for k, v in expected.items():
    if summary.get(k) != v:
        errors.append(f"canonical {k}: expected {v!r}, got {summary.get(k)!r}")

pages = [
    docs / "index.html",
    docs / "en" / "index.html",
    docs / "integrity.html",
    docs / "en" / "integrity.html",
    docs / "methodology.html",
    docs / "en" / "methodology.html",
    docs / "evidence.html",
    docs / "en" / "evidence.html",
]
for page in pages:
    if not page.exists():
        errors.append(f"missing page: {page.relative_to(root)}")

checks = {
    docs / "index.html": ["CANONICAL_RELEASE_SYNC_START", "99 / 99", "171 / 171"],
    docs / "en" / "index.html": ["CANONICAL_RELEASE_SYNC_START", "99 / 99", "171 / 171"],
    docs / "integrity.html": ["F01_PORTAL_SYNC_START", "97 beyan / 99 render", "99 beyan / 99 render", "99.000"],
    docs / "en" / "integrity.html": ["F01_PORTAL_SYNC_START", "97 declared / 99 rendered", "99 declared / 99 rendered", "99,000"],
}
for page, terms in checks.items():
    if not page.exists():
        continue
    text = page.read_text(encoding="utf-8", errors="replace")
    for term in terms:
        if term not in text:
            errors.append(f"{page.relative_to(root)} missing marker/text: {term}")

fault_path = validation / "integrity_fault_matrix.csv"
scale_path = validation / "integrity_scalability.csv"
for path in [fault_path, scale_path, validation / "benchmark_summary.json", validation / "BENCHMARK_PROTOCOL.md"]:
    if not path.exists():
        errors.append(f"missing validation artifact: {path.relative_to(root)}")

if fault_path.exists():
    rows = list(csv.DictReader(fault_path.open(encoding="utf-8")))
    if len(rows) != 9:
        errors.append(f"fault matrix row count: expected 9, got {len(rows)}")
    if any(str(r.get("pass")) != "1" for r in rows):
        errors.append("fault matrix contains a failed case")

if scale_path.exists():
    rows = list(csv.DictReader(scale_path.open(encoding="utf-8")))
    if len(rows) != 4:
        errors.append(f"scalability row count: expected 4, got {len(rows)}")
    elif rows[-1].get("nodes") != "99000" or rows[-1].get("edge_rows") != "171000":
        errors.append("largest scalability case is not 99,000 nodes / 171,000 edge rows")

if errors:
    print("SACI portal-paper synchronization FAILED")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("SACI portal-paper synchronization PASSED")
print("Canonical: 99/99 nodes | 171/171 relations | VALID | OPEN")
print("F-01: preserved as pre-release validation case")
print("Fault injection: 9/9 expected states matched")
print("Scalability: 99 to 99,000 nodes published")
