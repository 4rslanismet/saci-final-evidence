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
- control:C006 --produces_rule--> rule:110100 evidence=C006
- rule:110100 --alerted_in--> platform:Wazuh evidence=C006
- platform:MISP --contains_ioc--> ioc:cti-test.example.com evidence=cti-test.example.com
- platform:Wazuh --queries--> platform:MISP evidence=cti-test.example.com
- ioc:cti-test.example.com --converted_to_alert--> rule:110100 evidence=cti-test.example.com
- rule:110100 --alerted_in--> platform:Wazuh evidence=cti-test.example.com