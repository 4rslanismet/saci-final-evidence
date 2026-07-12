# SACI Graph Summary

Nodes: 95
Edges: 173
Observed edges: 161
Missing edges: 12

## Node types
- asset: 6
- control: 27
- ioc: 2
- logsource: 11
- metric: 6
- mitre: 15
- platform: 2
- score: 1
- wazuh_rule: 25

## Missing edge examples
- asset:A04 --emits--> logsource:PowerShell evidence=A04:PowerShell
- logsource:PowerShell --collected_by--> platform:Wazuh evidence=A04:PowerShell
- asset:A04 --protected_by--> control:C019 evidence=C019
- control:C019 --uses_log_source--> logsource:PowerShell evidence=C019
- control:C019 --produces_rule--> rule:110222 evidence=C019
- rule:110222 --alerted_in--> platform:Wazuh evidence=C019
- control:C019 --detects_technique--> mitre:T1059.001 evidence=C019
- asset:A04 --protected_by--> control:C026 evidence=C026
- control:C026 --uses_log_source--> logsource:PowerShell evidence=C026
- control:C026 --produces_rule--> rule:110243 evidence=C026
- rule:110243 --alerted_in--> platform:Wazuh evidence=C026
- control:C026 --detects_technique--> mitre:T1059.001 evidence=C026