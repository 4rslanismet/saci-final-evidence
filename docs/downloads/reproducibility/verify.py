#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

base = Path(sys.argv[1] if len(sys.argv) > 1 else "/opt/saci-final")
required = [
    "saci_scores.csv", "saci_nodes.csv", "saci_edges.csv",
    "saci_graph.cyjs", "asset_log_coverage.csv", "control_coverage.csv",
    "mitre_coverage.csv", "ctic_coverage.csv", "VALIDATION.txt"
]
missing = [name for name in required if not (base / name).exists()]
if missing:
    raise SystemExit("Missing canonical artifacts: " + ", ".join(missing))
with (base / "saci_scores.csv").open(newline="", encoding="utf-8-sig") as f:
    scores = {r["metric"]: r["score"] for r in csv.DictReader(f)}
with (base / "saci_edges.csv").open(newline="", encoding="utf-8-sig") as f:
    edges = list(csv.DictReader(f))
observed = sum(str(r.get("observed", "")).lower() in {"1","true","yes"} for r in edges)
print(f"SACI={scores.get('SACI')} edges={len(edges)} observed={observed} missing={len(edges)-observed}")
print("Canonical evidence verification passed.")
