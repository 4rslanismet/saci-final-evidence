# SACI Graph Summary

Nodes: 95
Edges: 173
Observed edges: 167
Missing edges: 6

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
- control:C016 --produces_rule--> rule:110203 evidence=C016
- rule:110203 --alerted_in--> platform:Wazuh evidence=C016
- platform:MISP --contains_ioc--> ioc:203.0.113.66 evidence=203.0.113.66
- platform:Wazuh --queries--> platform:MISP evidence=203.0.113.66
- ioc:203.0.113.66 --converted_to_alert--> rule:110203 evidence=203.0.113.66
- rule:110203 --alerted_in--> platform:Wazuh evidence=203.0.113.66