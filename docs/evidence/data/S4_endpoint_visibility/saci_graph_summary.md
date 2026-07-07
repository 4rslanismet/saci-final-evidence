# SACI Graph Summary

Nodes: 95
Edges: 173
Observed edges: 131
Missing edges: 42

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
- asset:A03 --emits--> logsource:misp_api evidence=A03:misp_api
- logsource:misp_api --collected_by--> platform:Wazuh evidence=A03:misp_api
- asset:A07 --emits--> logsource:pfsense_syslog evidence=A07:pfsense_syslog
- logsource:pfsense_syslog --collected_by--> platform:Wazuh evidence=A07:pfsense_syslog
- asset:A01 --protected_by--> control:C003 evidence=C003
- control:C003 --uses_log_source--> logsource:Sysmon evidence=C003
- control:C003 --produces_rule--> rule:92057 evidence=C003
- rule:92057 --alerted_in--> platform:Wazuh evidence=C003
- control:C003 --detects_technique--> mitre:T1059.001 evidence=C003
- asset:A01 --protected_by--> control:C004 evidence=C004
- control:C004 --uses_log_source--> logsource:Sysmon evidence=C004
- control:C004 --produces_rule--> rule:92052 evidence=C004
- rule:92052 --alerted_in--> platform:Wazuh evidence=C004
- control:C004 --detects_technique--> mitre:T1059.003 evidence=C004
- asset:A02 --protected_by--> control:C006 evidence=C006
- control:C006 --uses_log_source--> logsource:Wazuh evidence=C006
- control:C006 --produces_rule--> rule:110100 evidence=C006
- rule:110100 --alerted_in--> platform:Wazuh evidence=C006
- control:C006 --detects_technique--> mitre:T1071.004 evidence=C006
- asset:A07 --protected_by--> control:C014 evidence=C014
- control:C014 --uses_log_source--> logsource:pfsense_syslog evidence=C014
- control:C014 --produces_rule--> rule:110200 evidence=C014
- rule:110200 --alerted_in--> platform:Wazuh evidence=C014
- control:C014 --detects_technique--> mitre:T1046 evidence=C014
- asset:A07 --protected_by--> control:C015 evidence=C015
- control:C015 --uses_log_source--> logsource:pfsense_syslog evidence=C015
- control:C015 --produces_rule--> rule:110201 evidence=C015
- rule:110201 --alerted_in--> platform:Wazuh evidence=C015
- control:C015 --detects_technique--> mitre:T1046 evidence=C015
- asset:A07 --protected_by--> control:C016 evidence=C016
- control:C016 --uses_log_source--> logsource:pfsense_syslog evidence=C016
- control:C016 --produces_rule--> rule:110203 evidence=C016
- rule:110203 --alerted_in--> platform:Wazuh evidence=C016
- control:C016 --detects_technique--> mitre:T1071.001 evidence=C016
- platform:MISP --contains_ioc--> ioc:cti-test.example.com evidence=cti-test.example.com
- platform:Wazuh --queries--> platform:MISP evidence=cti-test.example.com
- ioc:cti-test.example.com --converted_to_alert--> rule:110100 evidence=cti-test.example.com
- rule:110100 --alerted_in--> platform:Wazuh evidence=cti-test.example.com
- platform:MISP --contains_ioc--> ioc:203.0.113.66 evidence=203.0.113.66
- platform:Wazuh --queries--> platform:MISP evidence=203.0.113.66
- ioc:203.0.113.66 --converted_to_alert--> rule:110203 evidence=203.0.113.66
- rule:110203 --alerted_in--> platform:Wazuh evidence=203.0.113.66