| Scenario | Purpose | SACI | Missing edges | Main interpretation |
|---|---|---:|---:|---|
| S8 | Final visibility closure | 100.0 | 0 | All expected visibility relationships were observed within the defined evaluation scope. |
| S7A | Critical DC01 Sysmon loss | 78.53 | 57 | Loss of critical asset telemetry causes a strong visibility regression. |
| S7B | Non-critical WS01 Sysmon loss | 92.52 | 32 | Non-critical endpoint telemetry loss has a smaller impact than critical DC telemetry loss. |
| S14 | MITRE scope expansion gap | 97.54 | 5 | Expanding the ATT&CK scope introduces new expected relationships and reveals coverage gaps. |
| S15 | Freshness decay | 95.0 | 0 | SACI can decrease due to stale telemetry even when no graph edges are missing. |
| S17 | Recovery after fix | 100.0 | 0 | Restoring the missing control relationships returns the graph to closure. |
| S18 | Legacy control out of scope | 100.0 | 0 | Legacy controls can be retained for traceability without lowering the active evaluation score. |
