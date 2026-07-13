# SACI Final Evidence Package

[![Validation](https://github.com/4rslanismet/saci-final-evidence/actions/workflows/validate.yml/badge.svg)](https://github.com/4rslanismet/saci-final-evidence/actions/workflows/validate.yml)
[![GitHub Pages](https://img.shields.io/badge/portal-live-2ea44f)](https://4rslanismet.github.io/saci-final-evidence/)

**SACI (Security Analytics Coverage Index)** is a scope-bounded, graph-supported measurement protocol for auditing whether declared SIEM–CTI evidence relationships are observed, explainable, and structurally valid.

This repository contains the canonical research artifact, controlled-laboratory evidence, reproducibility scaffold, validation tools, paper sources, and bilingual GitHub Pages companion for the SACI study.

> **Live research portal:** https://4rslanismet.github.io/saci-final-evidence/

## Abstract

Security monitoring programs often report isolated operational indicators—such as collected logs, enabled rules, ATT&CK mappings, or threat-intelligence integrations—without showing whether the expected evidence chain is complete and internally consistent. SACI addresses this gap through five deterministic coverage components: Criticality-Weighted Log Coverage (CWLC), Control/Alert Coverage (CAC), MITRE Detection Coverage (MDC), CTI Integration Coverage (CTIC), and Telemetry Freshness (TF). The components are combined through active-weight normalization and accompanied by a typed provenance graph, deterministic reason codes, and an independent integrity gate. In the corrected canonical laboratory release, SACI is 100.0, all 99 declared nodes match the 99 rendered nodes, all 171 expected relations are observed, no active integrity findings remain, and the publication gate is OPEN. The historical 97/99 mismatch is preserved only as the F-01 pre-release validation case.

## Canonical release

| Item | Result |
|---|---:|
| SACI | **100.0** |
| Component vector | **CWLC 100 · CAC 100 · MDC 100 · CTIC 100 · TF 100** |
| Declared / rendered nodes | **99 / 99** |
| Observed relations | **171 / 171** |
| Unique relation triples | **165** |
| Missing relations | **0** |
| Active integrity findings | **0** |
| Integrity status | **VALID** |
| Publication gate | **OPEN** |

The result is bounded by the declared evidence universe. It is not an absolute security or attack-risk score.

## Main contributions

- A deterministic five-component measurement model for scope-bounded SIEM–CTI evidence coverage.
- A typed provenance graph linking assets, log sources, controls, Wazuh rules, ATT&CK techniques, CTI objects, and score components.
- An integrity gate that is independent from score calculation and fails publication closed for structurally invalid datasets.
- A controlled nine-case fault-injection matrix for the integrity validator.
- A synthetic 1×–1000× cardinality experiment reaching 99,000 nodes and 171,000 edge rows.
- A bilingual research portal, machine-readable evidence package, SHA-256 ledger, and Vagrant-based reproduction scaffold.

## Repository structure

```text
.
├── archive/             # Clearly separated historical and maintenance material
├── code/                # Canonical scoring and graph-generation code
├── data/                # Pointer to the single canonical published data location
├── deliverables/        # Current paper artifacts and legacy drafts
├── doc_work_idap26/     # Current IEEEtran submission sources
├── docs/                # GitHub Pages portal and published evidence
├── lab/                 # Reproduction topology and provisioning scaffold
├── tools/               # Current validators and benchmark utilities
├── .github/workflows/   # Continuous validation
├── .gitignore
├── CITATION.cff
├── README.md
└── Vagrantfile
```

## Validate the release

```bash
python3 tools/validate_integrity.py   --data-dir docs/data/final   --check

python3 tools/validate_portal_paper_sync.py
python3 tools/validate_repository.py
python3 tools/validate_all.py
```

Expected final state:

```text
Integrity status : VALID
Publication gate : OPEN
Calculated SACI  : 100.0
Relation closure : 171/171
Active findings  : 0
```

## Local portal preview

```bash
python3 -m http.server 8000 --directory docs
```

Open `http://127.0.0.1:8000/`.

## Reproduction scaffold

```bash
ruby -c Vagrantfile
python3 -m json.tool lab/topology.json >/dev/null
```

The Vagrant scaffold supports artifact verification and topology reconstruction. It is a reproduction starting point, not an exact digital twin of the original live laboratory.

## Canonical data and historical separation

The only canonical publication dataset is `docs/data/final/`. Historical S0–S18 scenario outputs remain under `docs/data/scenarios/` and must not be merged numerically with the final snapshot. The historical S8 closure point contains 95 nodes and 173 relations; the canonical final contains 99 nodes and 171 relations.

## F-01 interpretation

F-01 is a pre-release regression case discovered in the artifact-generation process. It is not an active defect in the current release and is not presented as a theoretical discovery. The case showed that 171/171 relation closure could coexist with undeclared graph endpoints. The independent integrity gate blocked publication until the endpoints, mapping semantics, parallel evidence identities, and isolation policy were corrected.

## Türkçe özet

SACI, tanımlı SIEM–CTI kanıt kapsamındaki beklenen ilişkilerin gözlenme durumunu ölçen; sonucu tiplenmiş bir köken grafı, deterministik açıklama kodları ve bağımsız bütünlük denetimiyle birlikte yayımlayan bir ölçüm protokolüdür. Güncel kanonik sürüm `99/99` düğüm, `171/171` gözlenen ilişki, `SACI 100`, `VALID` bütünlük durumu ve `OPEN` yayın kapısı üretmektedir. Tarihsel `97/99` uyumsuzluğu yalnızca F-01 ön yayın doğrulama vakası olarak korunmaktadır.

## Citation

```text
İ. Arslan, “SACI Final Evidence Package,” GitHub repository, 2026.
https://github.com/4rslanismet/saci-final-evidence
```

## Author

**İsmet Arslan**<br>
M.Sc. Computer Engineering Researcher · Cyber Security Specialist<br>
https://github.com/4rslanismet
