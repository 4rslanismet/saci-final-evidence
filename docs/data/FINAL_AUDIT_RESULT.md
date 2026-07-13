# SACI Final Audit Result

**Dataset:** Canonical publication snapshot
**Audit result:** **PASS — INTEGRITY VALID**
**Publication gate:** **OPEN**

## 1. Final score

| Metric | Score | Weight | Applicable |
|---|---:|---:|---:|
| CWLC | 100.0 | 0.30 | 1 |
| CAC | 100.0 | 0.25 | 1 |
| MDC | 100.0 | 0.20 | 1 |
| CTIC | 100.0 | 0.15 | 1 |
| TF | 100.0 | 0.10 | 1 |
| SACI | 100.0 | 1.00 | 1 |

All active SACI components are scored at 100.0.

## 2. Canonical graph

| Check | Result |
|---|---:|
| Declared nodes | 99 |
| Rendered nodes | 99 |
| Edge rows | 171 |
| Unique source–relationship–target triples | 165 |
| Observed edges | 171 |
| Missing edges | 0 |
| Active integrity findings | 0 |

The node inventory and rendered graph agree at 99/99. Every published edge references a declared endpoint.

## 3. Coverage audit

| Evidence domain | Result |
|---|---:|
| Assets | 6 |
| Expected asset-log pairs | 12 |
| Observed asset-log pairs | 12 |
| Enabled controls | 25 |
| Seen enabled controls | 25 |
| MITRE ATT&CK techniques | 13/13 |
| CTI/MISP enrichment chains | 2/2 |
| Active reason codes | 0 |

## 4. Integrity gate

| Check | Result |
|---|---:|
| Integrity status | **VALID** |
| Publication gate | **OPEN** |
| INVALID findings | 0 |
| WARNING findings | 0 |
| INCOMPLETE findings | 0 |

The validator checks endpoint declarations, duplicate node identifiers, required fields, observed values, CSV–CYJS consistency, direct ATT&CK mapping consistency, parallel-edge evidence identity, and isolated-node policy.

## 5. F-01 pre-release case

The earlier 97-declared/99-rendered mismatch is retained only as a historical pre-release regression case. It is not an active defect in this canonical release.

The correction:

- declared `LOGSOURCE:Wazuh` and `MITRE:T1071.001`,
- separated the direct `110203 → T1071.001` mapping from `T1071.004` CTI context,
- assigned unique `evidence_id` values to parallel evidence rows, and
- documented intentionally retained isolated nodes in policy.

## 6. Interpretation boundary

SACI=100 means that all evidence relationships declared in the evaluated scope are observed under the published rules. It does not represent absolute security, complete attack prevention, or discovery of every unknown attack-surface element.

## 7. Dataset separation

The canonical final snapshot (99 nodes, 171 edge rows) is separate from the historical S0–S18 controlled sensitivity series. Historical S8 contains 95 nodes and 173 edge rows and must not be merged numerically with the canonical release.
