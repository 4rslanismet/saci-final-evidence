# SACI Graph Summary

Nodes: 95
Edges: 173
Observed edges: 141
Missing edges: 32

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
- asset:A04 --emits--> logsource:Sysmon evidence=A04:Sysmon
- logsource:Sysmon --collected_by--> platform:Wazuh evidence=A04:Sysmon
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
- asset:A04 --protected_by--> control:C018 evidence=C018
- control:C018 --uses_log_source--> logsource:Sysmon evidence=C018
- control:C018 --produces_rule--> rule:110220 evidence=C018
- rule:110220 --alerted_in--> platform:Wazuh evidence=C018
- control:C018 --detects_technique--> mitre:T1087 evidence=C018
- asset:A04 --protected_by--> control:C024 evidence=C024
- control:C024 --uses_log_source--> logsource:Sysmon evidence=C024
- control:C024 --produces_rule--> rule:110241 evidence=C024
- rule:110241 --alerted_in--> platform:Wazuh evidence=C024
- control:C024 --detects_technique--> mitre:T1087 evidence=C024
- asset:A04 --protected_by--> control:C025 evidence=C025
- control:C025 --uses_log_source--> logsource:Sysmon evidence=C025
- control:C025 --produces_rule--> rule:110242 evidence=C025
- rule:110242 --alerted_in--> platform:Wazuh evidence=C025
- control:C025 --detects_technique--> mitre:T1016 evidence=C025
- asset:A04 --protected_by--> control:C027 evidence=C027
- control:C027 --uses_log_source--> logsource:Sysmon evidence=C027
- control:C027 --produces_rule--> rule:110244 evidence=C027
- rule:110244 --alerted_in--> platform:Wazuh evidence=C027
- control:C027 --detects_technique--> mitre:T1071.004 evidence=C027