#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path.cwd()
DOCS = ROOT / "docs"
EN = DOCS / "en"

TR_MANIFEST = DOCS / "data" / "scenarios" / "manifest.json"
EN_MANIFEST = EN / "data" / "scenarios" / "manifest.json"

def first_existing(base, names):
    for name in names:
        p = base / name
        if p.exists():
            return name
    return None

def rel_from_docs(path):
    return path.relative_to(DOCS).as_posix()

def entry_from_dir(base, sid, label):
    nodes = first_existing(base, [
        "saci_nodes_v2.csv",
        "saci_nodes.csv",
        "nodes.csv"
    ])

    edges = first_existing(base, [
        "saci_edges_v2.csv",
        "saci_edges.csv",
        "edges.csv"
    ])

    graph = first_existing(base, [
        "saci_graph_v2.cyjs",
        "saci_graph.cyjs",
        "graph.cyjs"
    ])

    scores = first_existing(base, [
        "saci_scores_v2.csv",
        "saci_scores.csv",
        "saci_scores.json",
        "scores.csv",
        "scores.json"
    ])

    summary = first_existing(base, [
        "saci_graph_summary_v2.md",
        "saci_graph_summary.md",
        "graph_summary.md",
        "summary.md"
    ])

    if not graph:
        return None

    base_rel = rel_from_docs(base)

    def p(name):
        return f"{base_rel}/{name}" if name else ""

    return {
        "id": sid,
        "name": label,
        "label": label,
        "title": label,
        "dir": base_rel,
        "base": base_rel,

        "nodes": p(nodes),
        "node_csv": p(nodes),
        "nodes_csv": p(nodes),

        "edges": p(edges),
        "edge_csv": p(edges),
        "edges_csv": p(edges),

        "graph": p(graph),
        "cyjs": p(graph),
        "graph_cyjs": p(graph),

        "scores": p(scores),
        "score": p(scores),
        "summary": p(summary),
        "graph_summary": p(summary)
    }

def discover():
    found = []
    seen = set()

    preferred = [
        (DOCS / "evidence" / "lab" / "final_v2", "final_v2", "final-v2 canonical publication snapshot"),
        (DOCS / "evidence" / "lab" / "final", "final", "final lab closure snapshot"),
    ]

    for base, sid, label in preferred:
        if base.exists():
            e = entry_from_dir(base, sid, label)
            if e:
                found.append(e)
                seen.add(e["dir"])

    # Evidence altındaki bütün cyjs dosyalarını tara.
    for cyjs in sorted((DOCS / "evidence").glob("**/*.cyjs")):
        base = cyjs.parent
        base_rel = rel_from_docs(base)
        if base_rel in seen:
            continue

        name = base.name
        sid = name.split("_", 1)[0] if name.startswith("S") else name
        label = name.replace("_", " ")

        e = entry_from_dir(base, sid, label)
        if e:
            found.append(e)
            seen.add(base_rel)

    return found

def make_en_manifest(tr_manifest):
    en_manifest = {
        "default": tr_manifest.get("default"),
        "default_scenario": tr_manifest.get("default_scenario"),
        "scenarios": []
    }

    for item in tr_manifest["scenarios"]:
        x = dict(item)
        for k, v in list(x.items()):
            if isinstance(v, str) and (
                v.startswith("evidence/") or
                v.startswith("data/") or
                v.startswith("assets/")
            ):
                x[k] = "../" + v
        en_manifest["scenarios"].append(x)

    return en_manifest

def main():
    scenarios = discover()

    if not scenarios:
        print("[!] Hiç graph dataset bulunamadı.")
        print("[!] Şu komutla dosyaları kontrol et:")
        print("    find docs/evidence -iname '*.cyjs' -o -iname 'saci_nodes*.csv' -o -iname 'saci_edges*.csv'")
        raise SystemExit(1)

    default_id = scenarios[0]["id"]

    tr_manifest = {
        "default": default_id,
        "default_scenario": default_id,
        "scenarios": scenarios
    }

    TR_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    EN_MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    TR_MANIFEST.write_text(json.dumps(tr_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    EN_MANIFEST.write_text(json.dumps(make_en_manifest(tr_manifest), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[+] TR manifest: {TR_MANIFEST}")
    print(f"[+] EN manifest: {EN_MANIFEST}")
    print(f"[+] scenario count: {len(scenarios)}")
    for s in scenarios[:10]:
        print(f"    - {s['id']} -> {s['graph']}")

if __name__ == "__main__":
    main()
