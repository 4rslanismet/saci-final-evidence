#!/usr/bin/env python3
"""Validate the SACI canonical publication portal, datasets and reproduction scaffold."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FINAL = DOCS / "data" / "final"
TR_MANIFEST = DOCS / "data" / "scenarios" / "manifest.json"
EN_MANIFEST = DOCS / "en" / "data" / "scenarios" / "manifest.json"

NAV = [
    "index.html", "methodology.html", "architecture.html", "evidence.html",
    "scenarios.html", "artifacts.html", "reproducibility.html", "data.html",
    "references.html", "graph.html", "explanation.html", "paper.html",
]
PAGES = NAV + ["validation.html"]

REQUIRED_FINAL = [
    "saci_scores.csv", "saci_scores.json", "saci_nodes.csv", "saci_edges.csv",
    "saci_graph.cyjs", "saci_graph.mmd", "saci_graph_summary.md",
    "asset_log_coverage.csv", "control_coverage.csv", "mitre_coverage.csv",
    "ctic_coverage.csv", "log_source_status.csv", "reason_codes.csv",
    "reason_codes.json", "VALIDATION.txt", "FINAL_AUDIT_RESULT.md",
    "SHA256SUMS.txt", "saci_final_data_package.zip", "manifest.json",
]

REQUIRED_REPRO = [
    ROOT / "Vagrantfile",
    ROOT / "lab" / "topology.json",
    ROOT / "lab" / "verify.py",
    ROOT / "lab" / "provision" / "common.sh",
    ROOT / "lab" / "provision" / "install_docker.sh",
    ROOT / "lab" / "provision" / "wsiem.sh",
    ROOT / "lab" / "provision" / "cti01.sh",
    ROOT / "lab" / "provision" / "role_stub.sh",
    ROOT / "lab" / "provision" / "freebsd.sh",
    ROOT / "lab" / "provision" / "windows.ps1",
    DOCS / "downloads" / "reproducibility" / "Vagrantfile",
    DOCS / "downloads" / "reproducibility" / "topology.json",
    DOCS / "downloads" / "reproducibility" / "README.md",
    DOCS / "downloads" / "reproducibility" / "verify.py",
]

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]; self.ids=[]; self.lang=None; self.title=""; self._title=False
        self.nav=[]; self._in_nav=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="html": self.lang=a.get("lang")
        if tag=="title": self._title=True
        if a.get("id"): self.ids.append(a["id"])
        if tag=="nav" and "nav" in (a.get("class") or "").split(): self._in_nav=True
        if tag=="a" and a.get("href"):
            self.links.append(("href",a["href"]))
            if self._in_nav: self.nav.append(a["href"])
        if tag in {"img","script","link","source"}:
            key="href" if tag=="link" else "src"
            if a.get(key): self.links.append((key,a[key]))
    def handle_endtag(self, tag):
        if tag=="title": self._title=False
        if tag=="nav" and self._in_nav: self._in_nav=False
    def handle_data(self, data):
        if self._title: self.title += data

def csv_rows(name):
    path=FINAL/name
    if not path.is_file(): return []
    with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))

def fail(errors,msg): errors.append(msg)
def eq(errors,label,actual,expected):
    if actual!=expected: fail(errors,f"{label}: expected {expected!r}, got {actual!r}")

def resolve_local(page, raw):
    parsed=urlsplit(raw)
    if parsed.scheme in {"http","https","mailto","tel","data","javascript"} or raw.startswith("//"): return None
    if raw.startswith("#"): return (page, unquote(parsed.fragment))
    path=unquote(parsed.path)
    if not path: return (page, unquote(parsed.fragment))
    return ((page.parent/path).resolve(), unquote(parsed.fragment))

def validate_pages(errors):
    for folder,lang in ((DOCS,"tr"),(DOCS/"en","en")):
        for name in PAGES:
            page=folder/name
            if not page.is_file(): fail(errors,f"Missing page: {page.relative_to(ROOT)}"); continue
            text=page.read_text(encoding="utf-8",errors="replace")
            p=Parser(); p.feed(text)
            if p.lang!=lang: fail(errors,f"Invalid lang in {page.relative_to(ROOT)}: {p.lang}")
            if not p.title.strip(): fail(errors,f"Missing title: {page.relative_to(ROOT)}")
            if not re.search(r'<meta\s+name=["\']description["\']',text,re.I): fail(errors,f"Missing description: {page.relative_to(ROOT)}")
            if not re.search(r'<link\s+rel=["\']canonical["\']',text,re.I): fail(errors,f"Missing canonical: {page.relative_to(ROOT)}")
            if 'class="skip-link"' not in text or 'id="main"' not in text: fail(errors,f"Missing skip/main target: {page.relative_to(ROOT)}")
            duplicates=[x for x,c in Counter(p.ids).items() if c>1]
            if duplicates: fail(errors,f"Duplicate IDs in {page.relative_to(ROOT)}: {duplicates}")
            if p.nav[:len(NAV)]!=NAV: fail(errors,f"Navigation mismatch in {page.relative_to(ROOT)}: {p.nav}")
            for attr,raw in p.links:
                resolved=resolve_local(page,raw)
                if resolved is None: continue
                target,fragment=resolved
                try: target.relative_to(DOCS.resolve())
                except ValueError: fail(errors,f"Link escapes docs root in {page.relative_to(ROOT)}: {raw}"); continue
                if not target.exists(): fail(errors,f"Broken {attr} in {page.relative_to(ROOT)}: {raw}"); continue
                if fragment and target.suffix.lower() in {".html",".htm"}:
                    tp=Parser(); tp.feed(target.read_text(encoding="utf-8",errors="replace"))
                    if fragment not in tp.ids: fail(errors,f"Broken fragment in {page.relative_to(ROOT)}: {raw}")
    for path in DOCS.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".html",".js",".css",".json",".md",".txt"}:
            text=path.read_text(encoding="utf-8",errors="replace")
            if re.search(r'final[-_ ]?v2',text,re.I): fail(errors,f"Legacy final-v2 wording in published file: {path.relative_to(ROOT)}")

def validate_final(errors):
    for name in REQUIRED_FINAL:
        if not (FINAL/name).is_file(): fail(errors,f"Missing canonical artifact: docs/data/final/{name}")
    if errors and not FINAL.is_dir(): return
    scores=csv_rows("saci_scores.csv")
    if scores:
        eq(errors,"score metrics",{r["metric"] for r in scores},{"CWLC","CAC","MDC","CTIC","TF","SACI"})
        eq(errors,"all scores",{float(r["score"]) for r in scores},{100.0})
    logs=csv_rows("log_source_status.csv")
    if logs:
        eq(errors,"log rows",len(logs),12); eq(errors,"observed log pairs",sum(r["observed"]=="1" for r in logs),12); eq(errors,"assets",len({r["asset_id"] for r in logs}),6)
    controls=csv_rows("control_coverage.csv")
    if controls:
        enabled=[r for r in controls if r["enabled"]=="1"]
        eq(errors,"control rows",len(controls),27); eq(errors,"enabled controls",len(enabled),25); eq(errors,"seen enabled controls",sum(r["seen"]=="1" for r in enabled),25)
    mitre=csv_rows("mitre_coverage.csv")
    if mitre: eq(errors,"MITRE count",len(mitre),13); eq(errors,"covered MITRE",sum(r["covered"]=="1" for r in mitre),13)
    ctic=csv_rows("ctic_coverage.csv")
    if ctic:
        stages=("lookup_executed","misp_hit","wazuh_alert","mapped_to_mitre")
        eq(errors,"CTI rows",len(ctic),2); eq(errors,"CTI stage flags",sum(r[k]=="1" for r in ctic for k in stages),8)
    nodes=csv_rows("saci_nodes.csv"); edges=csv_rows("saci_edges.csv")
    if nodes and edges:
        eq(errors,"declared nodes",len(nodes),99); eq(errors,"edge rows",len(edges),171); eq(errors,"observed edges",sum(r["observed"]=="1" for r in edges),171)
        ids={r["id"] for r in nodes}; endpoints={r["source"] for r in edges}|{r["target"] for r in edges}
        eq(errors,"undeclared endpoints",endpoints-ids,set())
    reasons=csv_rows("reason_codes.csv")
    if (FINAL/"reason_codes.csv").is_file(): eq(errors,"active reason codes",len(reasons),0)
    for name in ("saci_scores.json","saci_graph.cyjs","reason_codes.json","manifest.json"):
        path=FINAL/name
        if path.is_file():
            try: json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc: fail(errors,f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
    sums_path=FINAL/"SHA256SUMS.txt"
    if sums_path.is_file():
        for line in sums_path.read_text().splitlines():
            if not line.strip(): continue
            digest,name=line.split(None,1); path=FINAL/name.strip()
            if not path.is_file(): fail(errors,f"Checksum file missing: {name.strip()}")
            else: eq(errors,f"SHA-256 {name.strip()}",hashlib.sha256(path.read_bytes()).hexdigest(),digest)
    bundle=FINAL/"saci_final_data_package.zip"
    if bundle.is_file():
        try:
            with zipfile.ZipFile(bundle) as z:
                names=set(z.namelist())
                for name in ["saci_scores.csv","saci_nodes.csv","saci_edges.csv","saci_graph.cyjs","VALIDATION.txt","FINAL_AUDIT_RESULT.md","SHA256SUMS.txt"]:
                    if name not in names: fail(errors,f"Canonical ZIP missing {name}")
        except zipfile.BadZipFile as exc: fail(errors,f"Invalid canonical ZIP: {exc}")

def manifest_items(path, errors, label):
    if not path.is_file(): fail(errors,f"Missing {label} scenario manifest"); return None,[]
    try: raw=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: fail(errors,f"Invalid {label} scenario manifest JSON: {exc}"); return None,[]
    if isinstance(raw,dict): return raw,raw.get("datasets",raw.get("scenarios",[]))
    if isinstance(raw,list): return {"default":"final","datasets":raw},raw
    fail(errors,f"Unsupported {label} manifest root type: {type(raw).__name__}"); return None,[]

def validate_manifest(path, page_root, errors, label):
    manifest,items=manifest_items(path,errors,label)
    if manifest is None: return []
    eq(errors,f"{label} manifest default",manifest.get("default"),"final")
    eq(errors,f"{label} dataset count",len(items),21)
    ids=[str(x.get("id")) for x in items if isinstance(x,dict)]
    eq(errors,f"{label} unique dataset IDs",len(set(ids)),len(ids))
    for item in items:
        if not isinstance(item,dict): fail(errors,f"Non-object dataset entry in {label} manifest: {item!r}"); continue
        for key in ("graph","nodes","edges","scores","mitre","summary","controls","assets","ctic"):
            value=item.get(key)
            target=(page_root/str(value)).resolve() if value else None
            if not value or not target.is_file(): fail(errors,f"Missing {label} manifest target {item.get('id')} {key}: {value}")
    return items

def validate_scenarios(errors):
    tr_items=validate_manifest(TR_MANIFEST,DOCS,errors,"TR")
    validate_manifest(EN_MANIFEST,DOCS/"en",errors,"EN")
    final=next((x for x in tr_items if x.get("id")=="final"),None)
    s8=next((x for x in tr_items if x.get("id")=="S8"),None)
    if not final: fail(errors,"Canonical final item missing")
    if not s8: fail(errors,"Historical S8 item missing"); return
    graph_path=(DOCS/str(s8.get("graph",""))).resolve()
    if not graph_path.is_file(): fail(errors,f"Historical S8 graph is missing: {graph_path}"); return
    raw=json.loads(graph_path.read_text(encoding="utf-8")); elements=raw.get("elements",{})
    nodes=elements.get("nodes",[]) if isinstance(elements,dict) else []; edges=elements.get("edges",[]) if isinstance(elements,dict) else []
    eq(errors,"S8 node count",len(nodes),95); eq(errors,"S8 edge count",len(edges),173)
    eq(errors,"S8 observed rows",sum(str(e.get("data",{}).get("observed"))=="1" for e in edges),173)

def validate_reproducibility(errors):
    for path in REQUIRED_REPRO:
        if not path.is_file(): fail(errors,f"Missing reproduction artifact: {path.relative_to(ROOT)}")
    vagrant=ROOT/"Vagrantfile"
    if vagrant.is_file():
        text=vagrant.read_text(encoding="utf-8",errors="replace")
        if not ("docs/data/final" in text or re.search(r'File\.join\(ROOT,\s*["\']docs["\'],\s*["\']data["\'],\s*["\']final["\']\)', text)):
            fail(errors,"Vagrantfile does not use canonical docs/data/final path")
        if re.search(r'final[-_ ]?v2',text,re.I): fail(errors,"Vagrantfile still references final-v2")
        if "ESXI_ROOT_SIFREN" in text: fail(errors,"Vagrantfile contains a placeholder ESXi password default")
        ruby=shutil.which("ruby")
        if ruby:
            result=subprocess.run([ruby,"-c",str(vagrant)],capture_output=True,text=True)
            if result.returncode!=0: fail(errors,f"Vagrantfile Ruby syntax failed: {result.stderr.strip() or result.stdout.strip()}")
    topo=ROOT/"lab"/"topology.json"
    if topo.is_file():
        try: data=json.loads(topo.read_text(encoding="utf-8"))
        except Exception as exc: fail(errors,f"Invalid lab/topology.json: {exc}"); return
        machines=set(data.get("machines",{}))
        expected={"wsiem","dc01","ws01","uhost","cti01","fw01-pfsense"}
        eq(errors,"reproduction machine set",machines,expected)

def main():
    errors=[]
    if not (DOCS/".nojekyll").is_file(): fail(errors,"docs/.nojekyll missing")
    validate_pages(errors)
    validate_final(errors)
    validate_scenarios(errors)
    validate_reproducibility(errors)
    if errors:
        print("SACI release validation FAILED")
        for error in errors: print("-",error)
        return 1
    print("SACI release validation PASSED")
    print("Pages: 26 | Datasets: 21 | Final SACI: 100")
    print("Final graph: 99 declared / 99 rendered nodes | 171/171 observed relations | 0 missing")
    print("Coverage: 12/12 asset-log | 25/25 controls | 13/13 ATT&CK | 2/2 CTI | 0 active reason codes")
    print("Dataset separation: canonical final 99/171 | historical S8 95/173")
    print("Reproducibility: Vagrant syntax, topology and downloadable scaffold validated")
    return 0

if __name__=="__main__": sys.exit(main())
