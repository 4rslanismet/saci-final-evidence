# SACI Graph Model Summary

## Graph Definition

G = (V, E)

V = Assets ∪ Log Sources ∪ Detection Controls ∪ Wazuh Rules ∪ MITRE Techniques ∪ Typed CTI Objects ∪ Platforms ∪ Score Metrics ∪ Reason Codes

E = emits ∪ collected_by ∪ protected_by ∪ uses_log_source ∪ produces_rule ∪ alerted_in ∪ detects_technique ∪ contains_ioc ∪ queries ∪ matches_ioc ∪ converted_to_alert ∪ mapped_to ∪ contributes_to ∪ explains_metric_gap

## Graph Size

- Nodes: 97
- Edges: 171
- Observed edges: 171
- Missing edges: 0

## Method Fixes

- N/A metrics are handled before weighted scoring.
- CWLC uses asset criticality and log-source weights.
- CTI is represented as typed CTI objects and staged closure relations.
- Reason codes are included as deterministic explanation evidence.
