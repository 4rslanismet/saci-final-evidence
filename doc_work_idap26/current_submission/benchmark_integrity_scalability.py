#!/usr/bin/env python3
"""Synthetic integrity-gate benchmark for the SACI paper.

The benchmark preserves the canonical graph cardinalities per replica
(99 declared nodes, 171 edge rows, 165 unique triples, 6 parallel evidence
rows) but does not replay operational telemetry. It evaluates only the
computational behavior and fault selectivity of a simplified implementation
of the published integrity rules.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
import tracemalloc
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

REQUIRED_EDGE_FIELDS = {"source", "relationship", "target", "observed", "evidence_id"}
DIRECT_MAPPING_REL = "detects_technique"

@dataclass
class Finding:
    severity: str
    code: str


def canonical_replica(replica: int = 0) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str], list[dict[str, Any]]]:
    p = f"R{replica}:"
    special = [
        "RULE:110203", "MITRE:T1071.001", "MITRE:T1071.004",
        "CONTROL:C003", "CONTROL:C004", "RULE:92052", "RULE:92057",
        "MITRE:T1059.003", "METRIC:SACI",
    ]
    generic = [f"NODE:N{i:03d}" for i in range(99 - len(special))]
    node_ids = [p + x for x in special + generic]
    nodes = [{"id": n, "type": n.split(":", 2)[1] if ":" in n else "node"} for n in node_ids]

    # Six policy-exempt isolated nodes, matching the canonical paper narrative.
    isolated = {
        p + "CONTROL:C003", p + "CONTROL:C004", p + "RULE:92052",
        p + "RULE:92057", p + "MITRE:T1059.003", p + "METRIC:SACI",
    }
    active = [n for n in node_ids if n not in isolated]
    edges: list[dict[str, Any]] = []

    # Two semantically distinct ATT&CK relations for rule 110203.
    edges.append({
        "source": p + "RULE:110203", "relationship": DIRECT_MAPPING_REL,
        "target": p + "MITRE:T1071.001", "observed": 1,
        "evidence_id": f"{p}E000", "mapping_basis": "direct_rule_mapping",
    })
    edges.append({
        "source": p + "RULE:110203", "relationship": "contextualized_as",
        "target": p + "MITRE:T1071.004", "observed": 1,
        "evidence_id": f"{p}E001", "mapping_basis": "cti_context",
    })

    # 163 more unique triples = 165 unique triples total.
    relation_types = [
        "emits", "collected_by", "protected_by", "uses_log_source",
        "produces_rule", "alerted_in", "detects_technique", "contains_ioc",
        "queries", "matches_ioc", "converted_to_alert", "contextualized_as",
        "contributes_to", "expects", "observed_in", "generated_by",
        "validated_by", "derived_from",
    ]
    used = {(edges[0]["source"], edges[0]["relationship"], edges[0]["target"]),
            (edges[1]["source"], edges[1]["relationship"], edges[1]["target"])}
    idx = 2
    i = 0
    while len(used) < 165:
        src = active[i % len(active)]
        dst = active[(i * 7 + 11) % len(active)]
        rel = relation_types[i % len(relation_types)]
        triple = (src, rel, dst)
        i += 1
        if src == dst or triple in used:
            continue
        used.add(triple)
        edges.append({
            "source": src, "relationship": rel, "target": dst,
            "observed": 1, "evidence_id": f"{p}E{idx:03d}",
            "mapping_basis": "synthetic_benchmark",
        })
        idx += 1

    # Six parallel rows with distinct evidence IDs: 171 rows, 165 triples.
    for j in range(6):
        base = edges[2 + j]
        dup = dict(base)
        dup["evidence_id"] = f"{p}E{idx:03d}"
        dup["evidence_origin"] = f"parallel_instance_{j+1}"
        edges.append(dup)
        idx += 1

    rendered_edges = [dict(e) for e in edges]
    return nodes, edges, isolated, rendered_edges


def build_dataset(multiplier: int):
    all_nodes, all_edges, all_exempt, all_rendered = [], [], set(), []
    for r in range(multiplier):
        nodes, edges, exempt, rendered = canonical_replica(r)
        all_nodes.extend(nodes)
        all_edges.extend(edges)
        all_exempt |= exempt
        all_rendered.extend(rendered)
    return all_nodes, all_edges, all_exempt, all_rendered


def validate(nodes, edges, exempt_isolated, rendered_edges) -> tuple[str, list[Finding]]:
    findings: list[Finding] = []
    node_ids = [n.get("id") for n in nodes]
    node_set = set(node_ids)

    if len(node_ids) != len(node_set):
        findings.append(Finding("INVALID", "duplicate_node_id"))

    incident = set()
    direct_mappings: dict[str, set[str]] = {}
    triple_to_eids: dict[tuple[str, str, str], list[str]] = {}

    for e in edges:
        if not REQUIRED_EDGE_FIELDS.issubset(e):
            findings.append(Finding("INVALID", "missing_required_edge_field"))
            continue
        src, rel, dst = e["source"], e["relationship"], e["target"]
        if src not in node_set or dst not in node_set:
            findings.append(Finding("INVALID", "undeclared_endpoint"))
        incident.update((src, dst))
        triple_to_eids.setdefault((src, rel, dst), []).append(str(e.get("evidence_id", "")))
        if rel == DIRECT_MAPPING_REL and str(e.get("mapping_basis", "")).startswith("direct"):
            direct_mappings.setdefault(src, set()).add(dst)

    for targets in direct_mappings.values():
        if len(targets) > 1:
            findings.append(Finding("INVALID", "conflicting_direct_mapping"))

    for eids in triple_to_eids.values():
        if len(eids) > 1 and ("" in eids or len(eids) != len(set(eids))):
            findings.append(Finding("INVALID", "parallel_edge_identity"))

    isolated = node_set - incident
    undocumented = isolated - exempt_isolated
    if undocumented:
        findings.append(Finding("WARNING", "undocumented_isolated_node"))

    # Representation consistency is checked as a multiset of evidence IDs.
    csv_ids = sorted(str(e.get("evidence_id", "")) for e in edges)
    rendered_ids = sorted(str(e.get("evidence_id", "")) for e in rendered_edges)
    if csv_ids != rendered_ids:
        findings.append(Finding("INVALID", "csv_cyjs_mismatch"))

    if any(f.severity == "INVALID" for f in findings):
        return "INVALID", findings
    if any(f.severity == "WARNING" for f in findings):
        return "VALID_WITH_WARNINGS", findings
    return "VALID", findings


def inject_case(case: str):
    nodes, edges, exempt, rendered = canonical_replica(0)
    if case == "baseline":
        pass
    elif case == "undeclared_endpoint":
        edges[0]["target"] = "R0:MITRE:UNDECLARED"
        rendered[0]["target"] = "R0:MITRE:UNDECLARED"
    elif case == "duplicate_node_id":
        nodes.append(dict(nodes[0]))
    elif case == "conflicting_mapping":
        e = dict(edges[0])
        e["target"] = "R0:MITRE:T1071.004"
        e["evidence_id"] = "R0:E999"
        e["mapping_basis"] = "direct_rule_mapping"
        edges.append(e)
        rendered.append(dict(e))
    elif case == "representation_mismatch":
        rendered.pop()
    elif case == "missing_required_field":
        edges[0].pop("target")
        rendered[0].pop("target")
    elif case == "parallel_identity_collision":
        # Make one parallel row reuse its base evidence_id.
        edges[-1]["evidence_id"] = edges[7]["evidence_id"]
        rendered[-1]["evidence_id"] = rendered[7]["evidence_id"]
    elif case == "undocumented_isolated_node":
        exempt.remove("R0:METRIC:SACI")
    elif case == "documented_isolated_node":
        pass
    else:
        raise ValueError(case)
    return nodes, edges, exempt, rendered


def run_fault_matrix(out_dir: Path):
    expected = {
        "baseline": "VALID",
        "undeclared_endpoint": "INVALID",
        "duplicate_node_id": "INVALID",
        "conflicting_mapping": "INVALID",
        "representation_mismatch": "INVALID",
        "missing_required_field": "INVALID",
        "parallel_identity_collision": "INVALID",
        "undocumented_isolated_node": "VALID_WITH_WARNINGS",
        "documented_isolated_node": "VALID",
    }
    rows = []
    for case, exp in expected.items():
        status, findings = validate(*inject_case(case))
        rows.append({
            "case": case,
            "expected_status": exp,
            "observed_status": status,
            "pass": int(status == exp),
            "finding_codes": ";".join(sorted({f.code for f in findings})),
        })
    with (out_dir / "integrity_fault_matrix.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    return rows


def run_scalability(out_dir: Path, multipliers, repeats: int):
    rows = []
    for mult in multipliers:
        nodes, edges, exempt, rendered = build_dataset(mult)
        times, peaks = [], []
        final_status = None
        for _ in range(repeats):
            tracemalloc.start()
            t0 = time.perf_counter()
            status, findings = validate(nodes, edges, exempt, rendered)
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            if findings or status != "VALID":
                raise RuntimeError((mult, status, [asdict(x) for x in findings]))
            final_status = status
            times.append(elapsed_ms); peaks.append(peak / (1024 * 1024))
        rows.append({
            "multiplier": mult,
            "nodes": len(nodes),
            "edge_rows": len(edges),
            "unique_triples": 165 * mult,
            "status": final_status,
            "median_time_ms": round(statistics.median(times), 3),
            "min_time_ms": round(min(times), 3),
            "max_time_ms": round(max(times), 3),
            "median_peak_mib": round(statistics.median(peaks), 3),
            "repeats": repeats,
        })
    with (out_dir / "integrity_scalability.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="benchmark_results")
    ap.add_argument("--repeats", type=int, default=7)
    ap.add_argument("--multipliers", default="1,10,100,1000")
    args = ap.parse_args()
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    multipliers = [int(x) for x in args.multipliers.split(",") if x.strip()]
    fault = run_fault_matrix(out)
    scale = run_scalability(out, multipliers, args.repeats)
    summary = {"fault_matrix": fault, "scalability": scale,
               "scope_note": "Synthetic cardinality benchmark; not an operational SOC throughput test."}
    (out / "benchmark_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
