#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path("/opt/saci-lab")
DATA = BASE / "data"
OUT = BASE / "outputs_v2"
GRAPH = BASE / "graph_v2"
GRAPH.mkdir(parents=True, exist_ok=True)

def read_csv(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def nid(prefix, value):
    return f"{prefix}:{str(value).replace(' ', '_').replace('/', '_').replace(':', '_')}"

nodes = {}
edges = []

def node(id, label, typ, **attrs):
    nodes[id] = {"id": id, "label": label, "type": typ, **attrs}

def edge(src, dst, rel, observed=1, weight=1.0, confidence="", last_seen=""):
    edges.append({
        "source": src,
        "target": dst,
        "relationship": rel,
        "observed": int(observed),
        "weight": weight,
        "confidence": confidence,
        "last_seen": last_seen,
    })

assets = read_csv(DATA / "assets.csv")
controls = read_csv(DATA / "detection_controls.csv")
mitre = read_csv(DATA / "mitre_scope.csv")
iocs = read_csv(DATA / "cti_iocs.csv")
cti_objects = read_csv(DATA / "cti_objects.csv")

log_status = read_csv(OUT / "log_source_status.csv")
control_cov = read_csv(OUT / "control_coverage_v2.csv")
mitre_cov = read_csv(OUT / "mitre_coverage_v2.csv")
ctic_cov = read_csv(OUT / "ctic_coverage_v2.csv")
scores = read_csv(OUT / "saci_scores_v2.csv")
reason_codes = read_csv(OUT / "reason_codes_v2.csv")

if not scores:
    raise SystemExit("No v2 score outputs found. Run /opt/saci-lab/saci_score_v2.py first.")

control_seen = {r["control_id"]: int(r.get("seen") or 0) for r in control_cov}
mitre_seen = {r["technique_id"]: int(r.get("covered") or 0) for r in mitre_cov}
ctic = {r["indicator"]: r for r in ctic_cov}

node("PLATFORM:Wazuh", "Wazuh SIEM", "platform")
node("PLATFORM:MISP", "MISP CTI", "platform")
node("INTEGRATION:custom-misp", "custom-misp", "integration")
node("SCORE:SACI", "SACI Score", "score", version="v2")

for s in scores:
    sid = nid("METRIC", s["metric"])
    node(
        sid,
        s["metric"],
        "metric",
        score=s.get("score", ""),
        weight=s.get("weight", ""),
        applicable=s.get("applicable", ""),
    )
    if s["metric"] != "SACI":
        edge(sid, "SCORE:SACI", "contributes_to", int(s.get("applicable") or 0), float(s.get("weight") or 1))

for a in assets:
    aid = nid("ASSET", a["asset_id"])
    node(
        aid,
        a.get("hostname", a["asset_id"]),
        "asset",
        ip=a.get("ip", ""),
        role=a.get("role", ""),
        criticality=a.get("criticality", ""),
    )

for row in log_status:
    aid = nid("ASSET", row["asset_id"])
    sid = nid("LOGSOURCE", row["log_source"])
    node(sid, row["log_source"], "log_source", source_weight=row.get("source_weight", ""))
    obs = int(row.get("observed") or 0)
    edge(aid, sid, "emits", obs, float(row.get("source_weight") or 1), "high" if obs else "missing", row.get("last_seen", ""))
    edge(sid, "PLATFORM:Wazuh", "collected_by", obs, 1.0, "high" if obs else "missing", row.get("last_seen", ""))

for m in mitre:
    mid = nid("MITRE", m["technique_id"])
    node(
        mid,
        m["technique_id"],
        "mitre_technique",
        technique_name=m.get("technique_name", ""),
        tactic=m.get("tactic", ""),
        covered=mitre_seen.get(m["technique_id"], 0),
    )

for c in controls:
    enabled = str(c.get("enabled", "1")) == "1"

    # Disabled / out-of-scope controls are not expected visibility edges.
    # They must not create missing graph relations in the final closure graph.
    if not enabled:
        cid = nid("CONTROL", c["control_id"])
        rid = nid("RULE", c["rule_id"])
        node(cid, c["control_id"], "control", description=c.get("description", ""), seen=0, enabled=0, scope="out_of_scope")
        node(rid, c["rule_id"], "wazuh_rule", description=c.get("description", ""), seen=0, enabled=0, scope="out_of_scope")
        continue

    cid = nid("CONTROL", c["control_id"])
    rid = nid("RULE", c["rule_id"])
    aid = nid("ASSET", c["asset_id"])
    sid = nid("LOGSOURCE", c["source"])
    seen = control_seen.get(c["control_id"], 0)

    node(cid, c["control_id"], "control", description=c.get("description", ""), seen=seen, enabled=1, scope="in_scope")
    node(rid, c["rule_id"], "wazuh_rule", description=c.get("description", ""), seen=seen, enabled=1, scope="in_scope")

    edge(aid, cid, "protected_by", seen, float(c.get("weight") or 1))
    edge(cid, sid, "uses_log_source", seen)
    edge(cid, rid, "produces_rule", seen)
    edge(rid, "PLATFORM:Wazuh", "alerted_in", seen)

    for tid in str(c.get("mitre_technique", "")).replace(",", ";").split(";"):
        tid = tid.strip()
        if tid:
            edge(cid, nid("MITRE", tid), "detects_technique", seen)

for i in iocs:
    indicator = i.get("indicator", "")
    iid = nid("CTI", indicator)
    row = ctic.get(indicator, {})
    lookup = int(row.get("lookup_executed") or 0)
    hit = int(row.get("misp_hit") or 0)
    alert = int(row.get("wazuh_alert") or 0)
    mapped = int(row.get("mapped_to_mitre") or 0)
    rule_id = row.get("expected_alert_rule") or i.get("expected_alert_rule", "")
    mitre_id = row.get("mitre_technique") or i.get("mitre_technique") or "T1071.004"

    node(
        iid,
        indicator,
        "cti_object",
        cti_type=i.get("type", "indicator"),
        source=i.get("source", ""),
        confidence=i.get("confidence", "medium"),
    )

    if lookup:
        edge("INTEGRATION:custom-misp", "PLATFORM:MISP", "queries", lookup, 1.0, "high")
    edge("PLATFORM:MISP", iid, "contains_ioc", hit, 1.0, "medium" if hit else "missing")
    edge("PLATFORM:Wazuh", "INTEGRATION:custom-misp", "triggers_integration", alert, 1.0)
    edge("INTEGRATION:custom-misp", iid, "matches_ioc", hit, 1.0)
    if rule_id:
        edge(iid, nid("RULE", rule_id), "converted_to_alert", alert, 1.0)
    if mitre_id:
        edge(iid, nid("MITRE", mitre_id), "mapped_to", mapped, 1.0)

for obj in cti_objects:
    oid = nid("CTI", obj.get("name") or obj.get("cti_object_id"))
    node(
        oid,
        obj.get("name") or obj.get("cti_object_id"),
        "cti_object",
        cti_type=obj.get("cti_type", ""),
        subtype=obj.get("subtype", ""),
        confidence=obj.get("confidence", ""),
    )

    target = obj.get("target", "")
    rel = obj.get("relation", "related_to")
    if target:
        if target.startswith("T"):
            target_id = nid("MITRE", target)
        else:
            target_id = nid("CTI", target)
        edge(oid, target_id, rel, 1, 1.0, obj.get("confidence", ""))

for idx, r in enumerate(reason_codes[:20], 1):
    rid = f"REASON:{idx:02d}"
    node(
        rid,
        r.get("reason_code", f"reason_{idx}"),
        "reason_code",
        metric=r.get("metric", ""),
        impact=r.get("impact", ""),
        fields_json=r.get("fields_json", ""),
    )
    metric = r.get("metric", "")
    if metric:
        edge(rid, nid("METRIC", metric), "explains_metric_gap", 1, float(r.get("impact") or 1))

node_rows = list(nodes.values())
node_fields = sorted(set(k for n in node_rows for k in n.keys()))
edge_fields = sorted(set(k for e in edges for k in e.keys()))

write_csv(GRAPH / "saci_nodes_v2.csv", node_rows, node_fields)
write_csv(GRAPH / "saci_edges_v2.csv", edges, edge_fields)

with open(GRAPH / "saci_graph_v2.cyjs", "w", encoding="utf-8") as f:
    json.dump({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "v2",
        "elements": {
            "nodes": [{"data": n} for n in node_rows],
            "edges": [{"data": {**e, "id": f"e{i}"}} for i, e in enumerate(edges)]
        }
    }, f, indent=2, ensure_ascii=False)

mmd = ["graph LR"]
for n in node_rows:
    safe = n["id"].replace(":", "_").replace(".", "_").replace("-", "_")
    label = str(n["label"]).replace('"', "'")
    mmd.append(f'  {safe}["{label}<br/>{n["type"]}"]')

for e in edges:
    src = e["source"].replace(":", "_").replace(".", "_").replace("-", "_")
    dst = e["target"].replace(":", "_").replace(".", "_").replace("-", "_")
    obs = "observed" if int(e["observed"]) else "missing"
    mmd.append(f'  {src} -- "{e["relationship"]} / {obs}" --> {dst}')

with open(GRAPH / "saci_graph_v2.mmd", "w", encoding="utf-8") as f:
    f.write("\n".join(mmd) + "\n")

observed_edges = sum(1 for e in edges if int(e["observed"]) == 1)
missing_edges = len(edges) - observed_edges

summary = f"""# SACI Graph Model Summary v2

## Graph Definition

G = (V, E)

V = Assets ∪ Log Sources ∪ Detection Controls ∪ Wazuh Rules ∪ MITRE Techniques ∪ Typed CTI Objects ∪ Platforms ∪ Score Metrics ∪ Reason Codes

E = emits ∪ collected_by ∪ protected_by ∪ uses_log_source ∪ produces_rule ∪ alerted_in ∪ detects_technique ∪ contains_ioc ∪ queries ∪ matches_ioc ∪ converted_to_alert ∪ mapped_to ∪ contributes_to ∪ explains_metric_gap

## Graph Size

- Nodes: {len(node_rows)}
- Edges: {len(edges)}
- Observed edges: {observed_edges}
- Missing edges: {missing_edges}

## Method Fixes

- N/A metrics are handled before weighted scoring.
- CWLC uses asset criticality and log-source weights.
- CTI is represented as typed CTI objects and staged closure relations.
- Reason codes are included as deterministic explanation evidence.
"""

with open(GRAPH / "saci_graph_summary_v2.md", "w", encoding="utf-8") as f:
    f.write(summary)

print("=== SACI GRAPH V2 GENERATED ===")
print(f"Nodes: {len(node_rows)}")
print(f"Edges: {len(edges)}")
print(f"Observed edges: {observed_edges}")
print(f"Missing edges: {missing_edges}")
print(f"Graph output: {GRAPH}")
