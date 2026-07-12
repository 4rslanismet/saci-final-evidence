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
- asset:A01 --emits--> logsource:Security evidence=A01:Security
- logsource:Security --collected_by--> platform:Wazuh evidence=A01:Security
- asset:A01 --protected_by--> control:C005 evidence=C005
- control:C005 --uses_log_source--> logsource:Security evidence=C005
- control:C005 --produces_rule--> rule:60106 evidence=C005
- rule:60106 --alerted_in--> platform:Wazuh evidence=C005
- control:C005 --detects_technique--> mitre:T1078 evidence=C005