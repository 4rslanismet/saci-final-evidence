# SACI Graph Summary

Nodes: 95
Edges: 173
Observed edges: 116
Missing edges: 57

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
- asset:A01 --emits--> logsource:Sysmon evidence=A01:Sysmon
- logsource:Sysmon --collected_by--> platform:Wazuh evidence=A01:Sysmon
- asset:A01 --protected_by--> control:C001 evidence=C001
- control:C001 --uses_log_source--> logsource:Sysmon evidence=C001
- control:C001 --produces_rule--> rule:110006 evidence=C001
- rule:110006 --alerted_in--> platform:Wazuh evidence=C001
- control:C001 --detects_technique--> mitre:T1071.004 evidence=C001
- asset:A01 --protected_by--> control:C002 evidence=C002
- control:C002 --uses_log_source--> logsource:Sysmon evidence=C002
- control:C002 --produces_rule--> rule:110005 evidence=C002
- rule:110005 --alerted_in--> platform:Wazuh evidence=C002
- control:C002 --detects_technique--> mitre:T1071.004 evidence=C002
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
- asset:A01 --protected_by--> control:C007 evidence=C007
- control:C007 --uses_log_source--> logsource:Sysmon evidence=C007
- control:C007 --produces_rule--> rule:110010 evidence=C007
- rule:110010 --alerted_in--> platform:Wazuh evidence=C007
- control:C007 --detects_technique--> mitre:T1087 evidence=C007
- asset:A01 --protected_by--> control:C008 evidence=C008
- control:C008 --uses_log_source--> logsource:Sysmon evidence=C008
- control:C008 --produces_rule--> rule:110011 evidence=C008
- rule:110011 --alerted_in--> platform:Wazuh evidence=C008
- control:C008 --detects_technique--> mitre:T1482 evidence=C008
- asset:A01 --protected_by--> control:C009 evidence=C009
- control:C009 --uses_log_source--> logsource:Sysmon evidence=C009
- control:C009 --produces_rule--> rule:110012 evidence=C009
- rule:110012 --alerted_in--> platform:Wazuh evidence=C009
- control:C009 --detects_technique--> mitre:T1016 evidence=C009
- asset:A01 --protected_by--> control:C010 evidence=C010
- control:C010 --uses_log_source--> logsource:Sysmon evidence=C010
- control:C010 --produces_rule--> rule:110013 evidence=C010
- rule:110013 --alerted_in--> platform:Wazuh evidence=C010
- control:C010 --detects_technique--> mitre:T1105 evidence=C010
- asset:A01 --protected_by--> control:C011 evidence=C011
- control:C011 --uses_log_source--> logsource:Sysmon evidence=C011
- control:C011 --produces_rule--> rule:110014 evidence=C011
- rule:110014 --alerted_in--> platform:Wazuh evidence=C011
- control:C011 --detects_technique--> mitre:T1135 evidence=C011
- asset:A01 --protected_by--> control:C012 evidence=C012
- control:C012 --uses_log_source--> logsource:Sysmon evidence=C012
- control:C012 --produces_rule--> rule:110011 evidence=C012
- rule:110011 --alerted_in--> platform:Wazuh evidence=C012
- control:C012 --detects_technique--> mitre:T1018 evidence=C012
- asset:A01 --protected_by--> control:C013 evidence=C013
- control:C013 --uses_log_source--> logsource:Sysmon evidence=C013
- control:C013 --produces_rule--> rule:110012 evidence=C013
- rule:110012 --alerted_in--> platform:Wazuh evidence=C013
- control:C013 --detects_technique--> mitre:T1049 evidence=C013