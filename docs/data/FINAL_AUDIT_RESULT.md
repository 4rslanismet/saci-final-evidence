# SACI Final Audit Result

## Validation Status

- Scenario count: 20
- Formula consistency: OK
- Edge arithmetic consistency: OK
- S8 final closure: OK
- Policy-guided explanation report: OK
- Old/invalid LLM terms: Not found
- Final web artifacts: Available

## Key Results

- S8 final_closure: SACI=100.0, missing=0, observed=173/173
- S7A critical_dc01_sysmon_loss: SACI=78.53, missing=57
- S7B noncritical_ws01_sysmon_loss: SACI=92.52, missing=32
- S14 mitre_scope_expansion_gap: SACI=97.54, missing=5, observed=173, edges=178
- S15 freshness_decay: SACI=95.0, missing=0, TF=50.0
- S17 recovery_after_fix: SACI=100.0, missing=0
- S18 legacy_control_out_of_scope: SACI=100.0, missing=0

## Interpretation

The final SACI outputs are internally consistent. SACI scores match the defined formula, graph edge counts are arithmetically valid, and the final closure scenario has no missing visibility edges.

SACI=100 must be interpreted as expected visibility closure within the defined evaluation scope, not as a general security guarantee.

## Primary Artifacts

- web/llm_report.html
- web/llm_report.md
- web/paper_clean_v2/index.html
- web/graph.html
- VALIDATION.txt
