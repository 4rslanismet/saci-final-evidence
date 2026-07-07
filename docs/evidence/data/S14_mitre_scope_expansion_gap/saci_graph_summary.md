# SACI Graph Summary

Nodes: 98
Edges: 178
Observed edges: 173
Missing edges: 5

## Node types
- asset: 6
- control: 28
- ioc: 2
- logsource: 11
- metric: 6
- mitre: 16
- platform: 2
- score: 1
- wazuh_rule: 26

## Missing edge examples
- asset:A04 --protected_by--> control:C900 evidence=C900
- control:C900 --uses_log_source--> logsource:Sysmon evidence=C900
- control:C900 --produces_rule--> rule:119900 evidence=C900
- rule:119900 --alerted_in--> platform:Wazuh evidence=C900
- control:C900 --detects_technique--> mitre:T1027 evidence=C900