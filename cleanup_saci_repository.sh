#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

if [[ ! -d .git ]]; then
  echo "[HATA] Bu komut Git deposunun kökünde çalıştırılmalı."
  exit 1
fi

REMOTE_URL="$(git remote get-url origin 2>/dev/null || true)"
if [[ "$REMOTE_URL" != *"saci-final-evidence"* ]]; then
  echo "[HATA] Yanlış depo: $REMOTE_URL"
  exit 1
fi

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR=".cleanup-backup/$STAMP"
mkdir -p "$BACKUP_DIR"

backup_path() {
  local path="$1"
  if [[ -e "$path" ]]; then
    mkdir -p "$BACKUP_DIR/$(dirname "$path")"
    cp -a "$path" "$BACKUP_DIR/$path"
  fi
}

echo "[1/7] Mevcut README ve geçici kök dosyaları yedekleniyor..."
backup_path "README.md"

shopt -s nullglob
TEMP_FILES=(
  AGENTS.md
  README.txt
  README_APPLY.txt
  README_*.txt
  fix_*.py
  patch_*.py
  apply_*.py
  repair_*.py
  finalize_*.py
  saci-methodology-rhythm.css
)

for path in "${TEMP_FILES[@]}"; do
  [[ "$path" == "README.md" ]] && continue
  backup_path "$path"
done

if [[ -f arch.png ]]; then
  backup_path "arch.png"
fi

echo "[2/7] Profesyonel proje README dosyası yazılıyor..."
cat > README.md <<'EOF'
# SACI Final Evidence Package

**SACI (Security Analytics Coverage Index)** is a scope-bounded, graph-supported measurement protocol for auditing whether declared SIEM–CTI evidence relationships are observed, explainable, and structurally valid.

This repository publishes the canonical research artifact, validation tools, controlled-lab evidence, reproducibility scaffold, and bilingual GitHub Pages portal prepared for the SACI study.

> **Live research portal:** https://4rslanismet.github.io/saci-final-evidence/

## Canonical release status

| Item | Result |
|---|---:|
| SACI | **100.0** |
| Component vector | **CWLC 100 · CAC 100 · MDC 100 · CTIC 100 · TF 100** |
| Declared / rendered nodes | **99 / 99** |
| Observed relations | **171 / 171** |
| Missing relations | **0** |
| Active integrity findings | **0** |
| Integrity status | **VALID** |
| Publication gate | **OPEN** |

The reported score is bounded by the declared monitoring scope. It represents closure of the published SIEM–CTI evidence model; it is not an absolute security or risk score.

## Research contribution

SACI combines five deterministic coverage components:

- **CWLC — Criticality-Weighted Log Coverage:** checks whether expected log sources are observed, with asset and source importance weights.
- **CAC — Control and Alert Coverage:** checks whether enabled detection controls produced observable evidence.
- **MDC — MITRE Detection Coverage:** measures coverage of the in-scope ATT&CK techniques.
- **CTIC — CTI Integration Coverage:** evaluates closure of the configured MISP-to-Wazuh enrichment workflow.
- **TF — Telemetry Freshness:** reports the implemented recency indicator for the observation window.

The score is accompanied by a typed provenance graph, deterministic reason codes, an independent integrity validator, and a fail-closed publication gate.

## Integrity validation

The integrity layer is independent from score calculation. A dataset can achieve complete relation closure while still being structurally invalid.

The validator checks:

- undeclared graph endpoints,
- duplicate node identifiers,
- missing required fields,
- invalid observation values,
- CSV–CYJS representation mismatches,
- conflicting ATT&CK mappings,
- parallel relations without distinct `evidence_id` values,
- undocumented isolated nodes.

Only the `VALID` state opens the publication gate.

## Repository structure

```text
.
├── docs/                  # GitHub Pages research portal (TR/EN)
├── docs/data/final/       # Canonical machine-readable release
├── docs/data/scenarios/   # Historical and sensitivity scenarios
├── lab/                   # Reproduction topology and provisioning scaffold
├── tools/                 # Integrity and release validators
├── code/                  # Core scoring and graph-supporting code
├── data/                  # Research data workspace
├── deliverables/          # Paper and dissemination artifacts
└── archive/               # Preserved legacy material
```

## Validate the canonical release

```bash
python3 tools/validate_integrity.py \
  --data-dir docs/data/final \
  --check

python3 tools/validate_academic_site.py
python3 tools/validate_all.py
```

Expected final state:

```text
Integrity status : VALID
Publication gate : OPEN
Calculated SACI  : 100.0
Relation closure : 171/171
Findings         : 0 active findings
```

## Local portal preview

```bash
python3 -m http.server 8000 --directory docs
```

Open:

```text
http://127.0.0.1:8000/
```

## Reproduction scaffold

The Vagrant-based scaffold supports artifact verification and topology reconstruction profiles. It is a reproduction starting point, not an exact digital twin of the original laboratory.

```bash
ruby -c Vagrantfile
python3 -m json.tool lab/topology.json >/dev/null
```

See the portal's **Reproduce** section for profile-specific instructions.

## Canonical data package

The canonical release is stored under `docs/data/final/` and includes score tables, node and edge datasets, graph representations, coverage tables, integrity findings, manifest metadata, SHA-256 checksums, audit results, and the release ZIP.

## Historical result separation

Historical scenario outputs are kept separate from the canonical release. The historical S8 snapshot (`95` nodes, `173` relations) is not merged with the canonical final dataset (`99` nodes, `171` relations).

## Türkçe özet

SACI, tanımlı SIEM–CTI kanıt kapsamındaki beklenen ilişkilerin gözlenme durumunu ölçen; sonucu tiplenmiş bir köken grafı, açıklama kodları ve bağımsız bütünlük denetimiyle birlikte yayımlayan deterministik bir ölçüm protokolüdür. Güncel kanonik sürüm `99/99` düğüm, `171/171` gözlenen ilişki, `SACI 100`, `VALID` bütünlük durumu ve `OPEN` yayın kapısı üretmektedir.

## Author

**İsmet Arslan**  
M.Sc. Computer Engineering Researcher · Cyber Security Specialist  
GitHub: https://github.com/4rslanismet

## Citation

Until final paper metadata is available:

```text
İ. Arslan, “SACI Final Evidence Package,” GitHub repository, 2026.
https://github.com/4rslanismet/saci-final-evidence
```
EOF

echo "[3/7] CITATION.cff oluşturuluyor..."
cat > CITATION.cff <<'EOF'
cff-version: 1.2.0
message: "If you use this research artifact, please cite it using the metadata below."
title: "SACI Final Evidence Package"
type: software
authors:
  - family-names: "Arslan"
    given-names: "İsmet"
repository-code: "https://github.com/4rslanismet/saci-final-evidence"
url: "https://4rslanismet.github.io/saci-final-evidence/"
version: "v1.0.0-integrity-valid"
date-released: "2026-07-12"
abstract: >-
  A scope-bounded, graph-supported SIEM-CTI evidence coverage
  measurement and integrity-validation research artifact.
keywords:
  - cybersecurity
  - SIEM
  - Wazuh
  - MISP
  - MITRE ATT&CK
  - threat intelligence
  - provenance graph
  - research artifact
EOF

echo "[4/7] Kök dizindeki hotfix/patch kalıntıları kaldırılıyor..."
for path in "${TEMP_FILES[@]}"; do
  [[ "$path" == "README.md" ]] && continue
  if [[ -e "$path" ]]; then
    git rm -rf --ignore-unmatch -- "$path"
  fi
done

# Kullanışlı yayın betiğini kökten tools/ altına taşı.
if [[ -f publish_to_github.sh && ! -e tools/publish_to_github.sh ]]; then
  git mv publish_to_github.sh tools/publish_to_github.sh
fi

# arch.png hiçbir yerde kullanılmıyorsa kaldır; referans varsa koru.
if [[ -f arch.png ]]; then
  if git grep -n -F "arch.png" -- ':!arch.png' >/dev/null 2>&1; then
    echo "[BİLGİ] arch.png başka bir dosyada referanslı; korundu."
  else
    git rm -f --ignore-unmatch arch.png
  fi
fi

echo "[5/7] .gitignore temizliği ekleniyor..."
cat >> .gitignore <<'EOF'

# Local SACI maintenance artifacts
/.cleanup-backup/
/backups/
/*.zip
!/docs/data/final/saci_final_data_package.zip
/README_*.txt
/README.txt
/README_APPLY.txt
/AGENTS.md
/apply_*.py
/repair_*.py
/finalize_*.py
/fix_*.py
/patch_*.py
EOF

# Tekrarlanan satırları korumalı biçimde temizle.
python3 - <<'PY'
from pathlib import Path
p = Path(".gitignore")
lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
seen = set()
out = []
for line in lines:
    key = line.rstrip()
    if key and not key.startswith("#"):
        if key in seen:
            continue
        seen.add(key)
    out.append(line)
p.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
PY

echo "[6/7] Değişiklikler stage ediliyor ve doğrulamalar çalıştırılıyor..."
git add README.md CITATION.cff .gitignore
git add -u

python3 tools/validate_all.py

echo
echo "=== STAGED FILES ==="
git diff --cached --name-status

echo
echo "=== STAGED SUMMARY ==="
git diff --cached --stat

echo "[7/7] Hazır."
echo
echo "Yedek: $BACKUP_DIR"
echo
echo "Kontrol ettikten sonra:"
echo '  git commit -m "Clean repository root and publish canonical SACI overview"'
echo '  git push origin main'
