# SACI Graph Summary

Nodes: 95
Edges: 173
Observed edges: 166
Missing edges: 7

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
- asset:A05 --emits--> logsource:authlog evidence=A05:authlog
- logsource:authlog --collected_by--> platform:Wazuh evidence=A05:authlog
- asset:A05 --protected_by--> control:C020 evidence=C020
- control:C020 --uses_log_source--> logsource:authlog evidence=C020
- control:C020 --produces_rule--> rule:110230 evidence=C020
- rule:110230 --alerted_in--> platform:Wazuh evidence=C020
- control:C020 --detects_technique--> mitre:T1110 evidence=C020