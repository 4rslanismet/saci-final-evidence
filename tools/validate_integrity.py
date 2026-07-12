#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        return list(csv.DictReader(f))

def pick(row, *names, default=""):
    low = {str(k).lower(): v for k, v in row.items()}
    for name in names:
        value = low.get(name.lower())
        if value not in (None, ""):
            return str(value).strip()
    return default

def split_techniques(value):
    return {
        item.upper()
        for item in re.split(r"[;,|\s]+", value or "")
        if re.fullmatch(r"T\d{4}(?:\.\d{3})?", item.upper())
    }

def make_finding(code, category, severity, title_tr, title_en, detail_tr, detail_en,
                 object_type="", object_id="", remediation_tr="", remediation_en=""):
    return {
        "finding_id": code,
        "category": category,
        "severity": severity,
        "title_tr": title_tr,
        "title_en": title_en,
        "detail_tr": detail_tr,
        "detail_en": detail_en,
        "object_type": object_type,
        "object_id": object_id,
        "remediation_tr": remediation_tr,
        "remediation_en": remediation_en,
    }

def summary(status, saci, declared, rendered, edges, observed, findings, unique=0):
    counts = Counter(item["severity"] for item in findings)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy_version": "1.0",
        "integrity_status": status,
        "publication_allowed": status == "VALID",
        "publication_gate": "OPEN" if status == "VALID" else "BLOCKED",
        "calculated_saci": saci,
        "declared_nodes": declared,
        "rendered_nodes": rendered,
        "edges": edges,
        "unique_edge_triples": unique,
        "observed_edges": observed,
        "missing_edges": max(edges - observed, 0),
        "relation_closure_percent": round(100 * observed / edges, 2) if edges else None,
        "finding_counts": {k: counts.get(k, 0) for k in ("INCOMPLETE", "INVALID", "WARNING", "INFO")},
        "finding_f01": {
            "id": "F-01",
            "title_tr": "İlişki kapanışı ile graph bütünlüğü ayrı doğrulama boyutlarıdır",
            "title_en": "Relation closure and graph integrity are distinct validation dimensions",
        },
    }

def validate(data_dir: Path):
    findings = []
    policy_path = data_dir / "integrity_policy.json"
    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8")) if policy_path.exists() else {}
    except Exception:
        policy = {}

    required = ["saci_nodes.csv", "saci_edges.csv", "saci_graph.cyjs", "saci_scores.csv"]
    missing = [name for name in required if not (data_dir / name).exists()]
    if missing:
        for name in missing:
            findings.append(make_finding(
                "S001-" + name, "schema", "INCOMPLETE",
                "Zorunlu dosya eksik", "Required file is missing",
                f"{name} bulunamadı.", f"{name} was not found.",
                "file", name, "Dosyayı yeniden üretin.", "Regenerate the file."
            ))
        return summary("INCOMPLETE", None, 0, 0, 0, 0, findings), findings

    nodes = read_csv(data_dir / "saci_nodes.csv")
    edges = read_csv(data_dir / "saci_edges.csv")
    scores = read_csv(data_dir / "saci_scores.csv")

    node_ids, node_rows = [], {}
    for row_no, row in enumerate(nodes, start=2):
        node_id = pick(row, "id", "node_id")
        node_type = pick(row, "type", "node_type")
        if not node_id:
            findings.append(make_finding(
                f"S-NODE-ID-{row_no}", "schema", "INVALID",
                "Node kimliği eksik", "Node identifier is missing",
                f"Satır {row_no} id boş.", f"Row {row_no} id is empty.",
                "node_row", str(row_no), "Node kimliğini tanımlayın.", "Declare the node id."
            ))
            continue
        if not node_type:
            findings.append(make_finding(
                f"S-NODE-TYPE-{row_no}", "schema", "INVALID",
                "Node tipi eksik", "Node type is missing",
                f"{node_id} tipi boş.", f"{node_id} type is empty.",
                "node", node_id, "Node tipini tanımlayın.", "Declare the node type."
            ))
        node_ids.append(node_id)
        node_rows[node_id] = row

    for node_id, count in Counter(node_ids).items():
        if count > 1:
            findings.append(make_finding(
                "G-NODE-DUP-" + node_id, "graph_integrity", "INVALID",
                "Yinelenen node kimliği", "Duplicate node identifier",
                f"{node_id} {count} kez tanımlı.", f"{node_id} is declared {count} times.",
                "node", node_id, "Tek kayıt bırakın.", "Keep one record."
            ))

    node_set = set(node_ids)
    degree, triples = Counter(), []
    observed = 0

    for row_no, row in enumerate(edges, start=2):
        source = pick(row, "source", "src")
        target = pick(row, "target", "dst")
        relation = pick(row, "relationship", "relation", "rel")
        observed_raw = pick(row, "observed")

        for field_name, value in (
            ("source", source), ("target", target),
            ("relationship", relation), ("observed", observed_raw)
        ):
            if value == "":
                findings.append(make_finding(
                    f"S-EDGE-{field_name}-{row_no}", "schema", "INVALID",
                    "Edge alanı eksik", "Edge field is missing",
                    f"Satır {row_no} {field_name} boş.", f"Row {row_no} {field_name} is empty.",
                    "edge_row", str(row_no), "Alanı doldurun.", "Populate the field."
                ))

        if source:
            degree[source] += 1
        if target:
            degree[target] += 1

        if source and source not in node_set:
            findings.append(make_finding(
                f"G-ENDPOINT-SRC-{row_no}", "graph_integrity", "INVALID",
                "Beyan edilmemiş source endpoint", "Undeclared source endpoint",
                f"{source} node envanterinde yok.", f"{source} is absent from the node inventory.",
                "endpoint", source, "Node'u ekleyin veya edge'i düzeltin.",
                "Declare the node or correct the edge."
            ))

        if target and target not in node_set:
            findings.append(make_finding(
                f"G-ENDPOINT-DST-{row_no}", "graph_integrity", "INVALID",
                "Beyan edilmemiş target endpoint", "Undeclared target endpoint",
                f"{target} node envanterinde yok.", f"{target} is absent from the node inventory.",
                "endpoint", target, "Node'u ekleyin veya edge'i düzeltin.",
                "Declare the node or correct the edge."
            ))

        if observed_raw not in ("0", "1", "0.0", "1.0"):
            findings.append(make_finding(
                f"S-EDGE-OBS-{row_no}", "schema", "INVALID",
                "Geçersiz observed değeri", "Invalid observed value",
                f"observed={observed_raw!r}", f"observed={observed_raw!r}",
                "edge_row", str(row_no), "0/1 kullanın.", "Use 0/1."
            ))

        try:
            observed += 1 if int(float(observed_raw)) == 1 else 0
        except Exception:
            pass

        if source and target and relation:
            triples.append((source, relation, target))

    triple_counts = Counter(triples)
    triple_evidence = defaultdict(list)
    for row in edges:
        triple = (
            pick(row, "source", "src"),
            pick(row, "relationship", "relation", "rel"),
            pick(row, "target", "dst"),
        )
        if all(triple):
            triple_evidence[triple].append(pick(row, "evidence_id"))

    for triple, count in triple_counts.items():
        if count <= 1:
            continue
        evidence_ids = triple_evidence.get(triple, [])
        distinct_evidence = (
            len(evidence_ids) == count
            and all(evidence_ids)
            and len(set(evidence_ids)) == count
        )
        if distinct_evidence:
            continue
        src, rel, dst = triple
        findings.append(make_finding(
            "G-EDGE-DUP-" + str(abs(hash("|".join(triple)))),
            "graph_integrity", "WARNING",
            "Yinelenen edge üçlüsü", "Duplicate edge triple",
            f"{src} --{rel}--> {dst} {count} kez var ve benzersiz evidence_id ile ayrılmamış.",
            f"{src} --{rel}--> {dst} appears {count} times without distinct evidence_id values.",
            "edge_triple", "|".join(triple),
            "Gerçek tekrarları kaldırın veya her kanıt örneğine benzersiz evidence_id ekleyin.",
            "Remove true duplicates or assign a unique evidence_id to each evidence instance."
        ))

    exempt_types = {str(x).lower() for x in policy.get("exempt_isolated_node_types", ["legend", "annotation", "note"])}
    exempt_ids = set(policy.get("exempt_isolated_node_ids", []))
    for node_id in sorted(node_set):
        if degree[node_id] or node_id in exempt_ids:
            continue
        node_type = pick(node_rows[node_id], "type", "node_type").lower()
        if node_type in exempt_types:
            continue
        findings.append(make_finding(
            "G-ISOLATED-" + node_id, "graph_integrity", "WARNING",
            "İzole node", "Isolated node",
            f"{node_id} için ilişki yok.", f"{node_id} has no relation.",
            "node", node_id,
            "Node'u ilişkilendirin, kaldırın veya gerekçelendirin.",
            "Connect, remove, or justify the node."
        ))

    baseline, extra = defaultdict(set), defaultdict(set)
    for row in read_csv(data_dir / "control_coverage.csv"):
        rule_id = pick(row, "rule_id", "wazuh_rule")
        baseline[rule_id].update(split_techniques(pick(row, "mitre_technique", "technique_id", "mitre")))
    for row in read_csv(data_dir / "ctic_coverage.csv"):
        rule_id = pick(row, "expected_alert_rule", "rule_id", "wazuh_rule")
        extra[rule_id].update(split_techniques(pick(row, "mitre_technique", "mapped_to", "technique_id", "mitre")))

    control_rules, control_techniques = defaultdict(set), defaultdict(set)
    for src, rel, dst in triples:
        rel_lower = rel.lower()
        if src.startswith("CONTROL:") and dst.startswith("RULE:") and rel_lower == "produces_rule":
            control_rules[src].add(dst.split(":", 1)[1])
        if src.startswith("CONTROL:") and dst.startswith("MITRE:") and rel_lower in ("detects_technique", "mapped_to"):
            control_techniques[src].add(dst.split(":", 1)[1])
        if src.startswith("RULE:") and dst.startswith("MITRE:") and rel_lower in ("mapped_to", "detects_technique"):
            extra[src.split(":", 1)[1]].add(dst.split(":", 1)[1])

    for control_id, rules in control_rules.items():
        for rule_id in rules:
            extra[rule_id].update(control_techniques.get(control_id, set()))

    allowed = {
        str(rule): {str(x).upper() for x in values}
        for rule, values in policy.get("allowed_multi_rule_mappings", {}).items()
    }
    for rule_id in sorted(set(baseline) | set(extra)):
        if not baseline[rule_id] or not extra[rule_id]:
            continue
        outside = extra[rule_id] - allowed.get(rule_id, baseline[rule_id])
        if outside:
            findings.append(make_finding(
                "M-ATTACK-" + rule_id, "mapping_consistency", "INVALID",
                "Çelişkili ATT&CK eşlemesi", "Conflicting ATT&CK mapping",
                f"Rule {rule_id}: baseline={sorted(baseline[rule_id])}, ek={sorted(extra[rule_id])}.",
                f"Rule {rule_id}: baseline={sorted(baseline[rule_id])}, extra={sorted(extra[rule_id])}.",
                "wazuh_rule", rule_id,
                "Eşlemeyi düzeltin veya izinli çoklu eşlemeyi politika dosyasına yazın.",
                "Correct the mapping or document an allowed multi-mapping."
            ))

    rendered = len(node_set)
    try:
        graph = json.loads((data_dir / "saci_graph.cyjs").read_text(encoding="utf-8"))
        elements = graph.get("elements", {})
        graph_node_ids = {
            str(item.get("data", {}).get("id", "")).strip()
            for item in elements.get("nodes", [])
            if str(item.get("data", {}).get("id", "")).strip()
        }
        rendered = len(graph_node_ids)
        graph_triples = Counter()
        for item in elements.get("edges", []):
            data = item.get("data", {})
            source = str(data.get("source", "")).strip()
            target = str(data.get("target", "")).strip()
            relation = str(data.get("relationship", data.get("relation", ""))).strip()
            if source and target and relation:
                graph_triples[(source, relation, target)] += 1
        if graph_node_ids != node_set or graph_triples != Counter(triples):
            findings.append(make_finding(
                "G-CYJS-MISMATCH", "graph_integrity", "INVALID",
                "CSV ve CYJS uyuşmuyor", "CSV and CYJS do not match",
                f"CSV node={len(node_set)}, CYJS node={len(graph_node_ids)}, CSV edge={len(triples)}, CYJS edge={sum(graph_triples.values())}.",
                f"CSV nodes={len(node_set)}, CYJS nodes={len(graph_node_ids)}, CSV edges={len(triples)}, CYJS edges={sum(graph_triples.values())}.",
                "graph", "saci_graph.cyjs",
                "CYJS dosyasını CSV kaynaklarından yeniden üretin.",
                "Regenerate CYJS from CSV sources."
            ))
    except Exception as exc:
        findings.append(make_finding(
            "G-CYJS-READ", "graph_integrity", "INCOMPLETE",
            "CYJS okunamadı", "CYJS could not be read",
            str(exc), str(exc), "graph", "saci_graph.cyjs",
            "Geçerli CYJS üretin.", "Generate valid CYJS."
        ))

    saci = None
    for row in scores:
        if pick(row, "metric").upper() == "SACI":
            try:
                saci = float(pick(row, "score"))
            except Exception:
                pass

    severity = Counter(item["severity"] for item in findings)
    status = (
        "INCOMPLETE" if severity["INCOMPLETE"]
        else "INVALID" if severity["INVALID"]
        else "VALID_WITH_WARNINGS" if severity["WARNING"]
        else "VALID"
    )
    return summary(status, saci, len(node_set), rendered, len(edges), observed, findings, len(triple_counts)), findings

def write_outputs(data_dir: Path, result, findings):
    (data_dir / "integrity_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (data_dir / "integrity_findings.json").write_text(json.dumps(findings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["finding_id", "category", "severity", "title_tr", "title_en", "detail_tr", "detail_en", "object_type", "object_id", "remediation_tr", "remediation_en"]
    with (data_dir / "integrity_findings.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(findings)
    lines = [
        "# SACI Evidence Integrity Result", "",
        f"**Integrity status:** `{result['integrity_status']}`  ",
        f"**Publication gate:** `{result['publication_gate']}`  ",
        f"**Calculated SACI:** `{result.get('calculated_saci')}`  ",
        f"**Relation closure:** `{result.get('observed_edges')}/{result.get('edges')}`  ",
        "", "## Finding F-01", "",
        "Relation closure and graph integrity are distinct validation dimensions.", "",
    ]
    for item in findings:
        lines.extend([
            f"### {item['finding_id']} — {item['severity']}", "",
            item["title_en"], "",
            f"- Object: `{item['object_type']}:{item['object_id']}`",
            f"- Detail: {item['detail_en']}",
            f"- Remediation: {item['remediation_en']}", "",
        ])
    (data_dir / "INTEGRITY_RESULT.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    (data_dir / "FINDING_F01.md").write_text(
        "# Finding F-01 / Bulgu F-01\n\n"
        "Relation closure and graph integrity are distinct validation dimensions.\n\n"
        "İlişki kapanışı ile graph bütünlüğü ayrı doğrulama boyutlarıdır.\n",
        encoding="utf-8"
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="docs/data/final")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    result, findings = validate(data_dir)
    if args.write:
        write_outputs(data_dir, result, findings)
    print("=== SACI EVIDENCE INTEGRITY ===")
    print("Integrity status :", result["integrity_status"])
    print("Publication gate :", result["publication_gate"])
    print("Calculated SACI  :", result.get("calculated_saci"))
    print("Relation closure :", f"{result.get('observed_edges')}/{result.get('edges')}")
    print("Findings         :", result["finding_counts"])
    if args.write and not args.check:
        return 0
    return {"VALID": 0, "VALID_WITH_WARNINGS": 1, "INVALID": 2, "INCOMPLETE": 3}.get(result["integrity_status"], 3)

if __name__ == "__main__":
    sys.exit(main())
