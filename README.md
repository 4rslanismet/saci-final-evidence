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
