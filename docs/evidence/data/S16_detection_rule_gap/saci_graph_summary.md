# SACI Graph Summary

Nodes: 95
Edges: 173
Observed edges: 168
Missing edges: 5

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
- asset:A04 --protected_by--> control:C024 evidence=C024
- control:C024 --uses_log_source--> logsource:Sysmon evidence=C024
- control:C024 --produces_rule--> rule:110241 evidence=C024
- rule:110241 --alerted_in--> platform:Wazuh evidence=C024
- control:C024 --detects_technique--> mitre:T1087 evidence=C024