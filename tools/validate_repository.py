#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, json, sys

root = Path(__file__).resolve().parents[1]
errors = []

allowed_root_dirs = {
    ".github", "archive", "code", "data", "deliverables",
    "doc_work_idap26", "docs", "lab", "tools",
}
allowed_root_files = {
    ".gitignore", "CITATION.cff", "README.md", "Vagrantfile", "LICENSE", "DATA_LICENSE.md",
}
ignored_runtime = {".git", "__pycache__"}

for item in root.iterdir():
    if item.name in ignored_runtime:
        continue
    if item.is_dir() and item.name not in allowed_root_dirs:
        errors.append(f"unexpected root directory: {item.name}")
    if item.is_file() and item.name not in allowed_root_files:
        errors.append(f"unexpected root file: {item.name}")

readme = root / "README.md"
if not readme.exists() or not readme.read_text(encoding="utf-8").startswith("# SACI Final Evidence Package"):
    errors.append("README.md is missing the academic project overview")
if readme.exists() and "responsive header hotfix" in readme.read_text(encoding="utf-8").lower():
    errors.append("README.md still contains hotfix documentation")

for pattern in ("README*.txt", "fix_*.py", "patch_*.py", "apply_*.py", "repair_*.py", "finalize_*.py"):
    for path in root.glob(pattern):
        errors.append(f"maintenance artifact remains at repository root: {path.name}")

for rel in [
    "docs/architecture.backup.20260711_120224.html",
    "docs/assets/saci-ui.backup.20260711_120224.js",
    "docs/assets/graph-v2.js",
    "docs/home_concepts.html",
    "docs/home_10_concepts.html",
]:
    if (root / rel).exists():
        errors.append(f"unreferenced site backup remains active: {rel}")

if (root / "AGENTS.md").exists() or (root / "tools/chat_memory.py").exists():
    errors.append("private assistant-memory guidance remains in public tree")

# One canonical data location: root data must be a pointer only.
data_files = [p for p in (root / "data").rglob("*") if p.is_file()]
if [p.relative_to(root / "data").as_posix() for p in data_files] != ["README.md"]:
    errors.append("root data/ contains a second data copy; expected README pointer only")

# Source code and portal downloads must match exactly.
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for name in ("saci_attack_runner.sh", "saci_graph.py", "saci_score.py"):
    source = root / "code" / name
    mirror = root / "docs" / "code" / name
    if not source.exists() or not mirror.exists():
        errors.append(f"missing code source/mirror: {name}")
    elif digest(source) != digest(mirror):
        errors.append(f"code mirror mismatch: {name}")

# Current paper files must exist.
for rel in [
    "deliverables/SACI_IDAP26_Reviewer_Hardened_EN.pdf",
    "deliverables/SACI_IDAP26_Turkce_Hakem_Guclendirilmis.docx",
    "doc_work_idap26/current_submission/SACI_IDAP26_Arslan.tex",
    "doc_work_idap26/current_submission/SACI_IDAP26_References.bib",
]:
    if not (root / rel).exists():
        errors.append(f"missing current paper artifact: {rel}")

# Working directory should not contain old QA render farms.
if (root / "doc_work_idap26" / "qa").exists():
    errors.append("old QA render farm remains in current paper workspace")

# Canonical counts from actual files.
final = root / "docs" / "data" / "final"
with (final / "saci_nodes.csv").open(encoding="utf-8-sig", newline="") as f:
    nodes = list(csv.DictReader(f))
with (final / "saci_edges.csv").open(encoding="utf-8-sig", newline="") as f:
    edges = list(csv.DictReader(f))
if len(nodes) != 99:
    errors.append(f"actual canonical node count is {len(nodes)}, expected 99")
if len(edges) != 171:
    errors.append(f"actual canonical edge count is {len(edges)}, expected 171")

summary = json.loads((final / "integrity_summary.json").read_text(encoding="utf-8"))
if summary.get("integrity_status") != "VALID" or summary.get("publication_gate") != "OPEN":
    errors.append("canonical integrity state is not VALID/OPEN")

if errors:
    print("SACI repository presentation validation FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("SACI repository presentation validation PASSED")
print("Root layout: clean")
print("Canonical data location: docs/data/final")
print("Current paper artifacts: present")
print("Private/temporary maintenance files: absent from active tree")
