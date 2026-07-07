| Scenario | Description | Type | SACI | Missing edges | Observed / Total edges |
|---|---|---|---:|---:|---:|
| S0 | no_siem | controlled_evaluation_scenario | 0.0 | 167 | 6/173 |
| S1 | siem_deployed | controlled_evaluation_scenario | 10.56 | 163 | 10/173 |
| S2 | inventory_defined | controlled_evaluation_scenario | 11.56 | 163 | 10/173 |
| S3 | dc_visibility | controlled_evaluation_scenario | 42.96 | 109 | 64/173 |
| S4 | endpoint_visibility | controlled_evaluation_scenario | 69.0 | 42 | 131/173 |
| S5 | firewall_visibility | controlled_evaluation_scenario | 74.56 | 40 | 133/173 |
| S6 | cti_integration | controlled_evaluation_scenario | 94.0 | 30 | 143/173 |
| S7A | critical_dc01_sysmon_loss | controlled_visibility_regression | 78.53 | 57 | 116/173 |
| S7B | noncritical_ws01_sysmon_loss | controlled_visibility_regression | 92.52 | 32 | 141/173 |
| S8 | final_closure | final_lab_measurement | 100.0 | 0 | 173/173 |
| S9 | critical_dc01_security_loss | fault_injection | 96.47 | 7 | 166/173 |
| S10 | endpoint_powershell_loss | fault_injection | 95.05 | 12 | 161/173 |
| S11 | linux_authlog_loss | fault_injection | 95.91 | 7 | 166/173 |
| S12 | firewall_ioc_without_cti | cti_failure | 92.5 | 6 | 167/173 |
| S13 | misp_lookup_without_ioc_hit | cti_failure | 92.5 | 6 | 167/173 |
| S14 | mitre_scope_expansion_gap | coverage_gap | 97.54 | 5 | 173/178 |
| S15 | freshness_decay | sensitivity_test | 95.0 | 0 | 173/173 |
| S16 | detection_rule_gap | control_failure | 98.93 | 5 | 168/173 |
| S17 | recovery_after_fix | recovery | 100.0 | 0 | 173/173 |
| S18 | legacy_control_out_of_scope | scope_validation | 100.0 | 0 | 173/173 |
