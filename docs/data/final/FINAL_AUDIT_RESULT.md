# SACI Final Audit Result

**Dataset:** Canonical publication snapshot  
**Audit result:** **PASS WITH STRUCTURAL REVIEW**  
**Package generated:** 2026-07-11

## 1. Final score

| Metric | Score | Weight | Applicable |
|---|---:|---:|---:|
| CWLC | 100.0 | 0.3 | 1 |
| CAC | 100.0 | 0.25 | 1 |
| MDC | 100.0 | 0.2 | 1 |
| CTIC | 100.0 | 0.15 | 1 |
| TF | 100 | 0.1 | 1 |
| SACI | 100.0 | 1.0 | 1 |

All active SACI components are scored at 100. The final SACI value is **100.0**.

## 2. Graph closure

| Check | Result |
|---|---:|
| Declared nodes | 97 |
| Edge rows | 171 |
| Observed edges | 171 |
| Missing edges | 0 |
| Rendered nodes after synthetic endpoint completion | 99 |

The canonical graph contains no missing visibility relation.

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

## 4. Structural integrity finding

Two edge endpoints are referenced without corresponding declarations in
`saci_nodes.csv`:

- `LOGSOURCE:Wazuh`
- `MITRE:T1071.001`

This is retained as a structural integrity finding. It does **not** create a
missing visibility relation and does not change the SACI score. A graph renderer
may synthesize these endpoints, producing 99 rendered nodes from 97 declared
nodes.

## 5. Interpretation boundary

The final score indicates that all visibility relations declared in the
evaluation scope were observed. It does not demonstrate absolute security,
complete attack prevention, or discovery of every unknown attack-surface
element.

## 6. Dataset separation

This canonical publication snapshot must not be merged numerically with the
historical S0–S18 controlled validation series. The historical series is used to
evaluate model behavior and sensitivity; the canonical snapshot is the
publication-level final evidence package.

<!-- SACI_INTEGRITY_GATE_START -->
## Independent evidence-integrity gate

| Check | Result |
|---|---:|
| Calculated SACI | 100.0 |
| Relation closure | 171/171 |
| Declared/rendered nodes | 99/99 |
| Integrity status | **VALID** |
| Publication gate | **OPEN** |

Finding F-01 was resolved by declaring the formerly implicit endpoints, separating direct ATT&CK mappings from CTI contextual associations, assigning unique evidence identifiers to parallel evidence edges and documenting intentionally retained out-of-scope nodes.
<!-- SACI_INTEGRITY_GATE_END -->
