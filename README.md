# SACI Final Evidence Package

A reproducible research artifact for **scope-bounded SIEM–CTI evidence coverage scoring, graph-supported explanation, and structural integrity validation**.

**Research portal:** https://4rslanismet.github.io/saci-final-evidence/

## Overview

SACI (**Security Analytics Coverage Index**) is a deterministic measurement protocol designed to evaluate whether the evidence relationships declared within a SIEM–CTI monitoring scope are observed, explainable, and structurally valid.

The study combines five coverage components:

- **CWLC** — Criticality-Weighted Log Coverage
- **CAC** — Control and Alert Coverage
- **MDC** — MITRE Detection Coverage
- **CTIC** — CTI Integration Coverage
- **TF** — Telemetry Freshness

The numerical score is published together with a typed provenance graph, machine-readable evidence tables, deterministic reason codes, an independent integrity validator, and a fail-closed publication gate.

## Canonical Release Status

| Metric | Result |
|---|---:|
| SACI | **100.0** |
| CWLC | **100.0** |
| CAC | **100.0** |
| MDC | **100.0** |
| CTIC | **100.0** |
| TF | **100.0** |
| Declared / rendered nodes | **99 / 99** |
| Observed relations | **171 / 171** |
| Missing relations | **0** |
| Active integrity findings | **0** |
| Integrity status | **VALID** |
| Publication gate | **OPEN** |

The reported score is bounded by the declared laboratory scope. It represents evidence closure within that scope; it is not an absolute security, prevention, or residual-risk score.

## Main Contributions

- Scope-bounded SIEM–CTI coverage measurement
- Typed provenance graph for evidence explanation
- Independent structural integrity validation
- Fail-closed canonical publication gate
- Controlled fault-injection evaluation
- Synthetic validator scalability evaluation
- Reproducible bilingual research portal
- Machine-readable canonical evidence package

## Repository Structure

```text
.
├── archive/                 # Historical and retired material
├── code/                    # Core scoring and graph-supporting code
├── data/                    # Data workspace and documentation
├── deliverables/            # Current paper and dissemination files
├── doc_work_idap26/         # Current IDAP submission source package
├── docs/                    # GitHub Pages research portal
│   ├── data/final/          # Canonical release
│   ├── data/scenarios/      # Historical and sensitivity scenarios
│   └── data/validation/     # Fault-injection and scalability results
├── lab/                     # Reproduction topology and lab scaffold
├── tools/                   # Validators and maintenance utilities
├── CITATION.cff             # Citation metadata
├── README.md
└── Vagrantfile
```

## Canonical Data Package

The authoritative release is located at:

```text
docs/data/final/
```

It contains:

- node and edge tables
- score outputs
- control, log-source, ATT&CK, and CTI coverage tables
- graph representations
- integrity findings
- manifest metadata
- SHA-256 checksums
- canonical release ZIP

Historical scenario outputs are kept separate from the canonical package.

## Validation

Run the complete validation chain from the repository root:

```bash
python3 tools/validate_all.py
```

Expected final state:

```text
SACI release validation PASSED
Final graph: 99 declared / 99 rendered nodes
Relation closure: 171/171
Integrity status: VALID
Publication gate: OPEN
Repository presentation validation: PASSED
```

The integrity validator can also be executed independently:

```bash
python3 tools/validate_integrity.py \
  --data-dir docs/data/final \
  --check
```

## Local Portal

Start a local server:

```bash
python3 -m http.server 8000 --directory docs
```

Open:

```text
http://127.0.0.1:8000/
```

The portal provides:

- methodology
- system architecture
- evidence tables
- interactive Cytoscape.js graph
- scenario analysis
- integrity case F-01
- fault-injection results
- scalability results
- downloadable artifacts
- Turkish and English views

## Reproduction Scaffold

The Vagrant-based laboratory scaffold supports artifact verification and topology reconstruction.

```bash
ruby -c Vagrantfile
python3 -m json.tool lab/topology.json >/dev/null
```

The scaffold is a reproducibility aid and not an exact digital twin of the original environment.

## Integrity Case F-01

The historical **97/99 node mismatch** is preserved as a pre-release regression case.

```text
Pre-release case:
97 declared / 99 rendered
171/171 relation closure
3 INVALID findings
12 WARNING findings
Publication gate: BLOCKED

Corrected canonical release:
99 declared / 99 rendered
171/171 observed relations
0 active findings
Integrity status: VALID
Publication gate: OPEN
```

F-01 demonstrates that complete numerical relation closure does not, by itself, establish graph integrity.

## Experimental Validation

The repository includes:

- a nine-case controlled fault-injection matrix
- synthetic validator scalability results from **1× to 1000×**
- the largest synthetic case with **99,000 nodes** and **171,000 edge rows**

These experiments evaluate integrity-validator behavior and data-structure growth. They do not represent SIEM ingestion throughput, OpenSearch performance, or production SOC capacity.

## Paper Artifacts

Current submission materials are available under:

```text
doc_work_idap26/current_submission/
```

Current dissemination files are available under:

```text
deliverables/
```

## Citation

Until final conference metadata is assigned, cite the repository as:

```text
İ. Arslan, “SACI Final Evidence Package,” GitHub repository, 2026.
https://github.com/4rslanismet/saci-final-evidence
```

Citation metadata is also available in `CITATION.cff`.

## Author

**İsmet Arslan**

M.Sc. Computer Engineering Researcher · Cyber Security Specialist
