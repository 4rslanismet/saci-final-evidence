# Evaluation Design

The evaluation was designed to test whether SACI can represent SOC visibility changes in a controlled telemetry graph. Instead of relying on a single final score, the evaluation uses staged visibility progression and fault-injection scenarios.

The staged progression scenarios model the transition from no SIEM visibility to final expected visibility closure. In the early stages, the environment has limited or no telemetry coverage. As assets, log sources, detection controls, MITRE ATT&CK mappings, Wazuh rules, and CTI integration are added, the graph becomes more complete and the SACI score increases.

The fault-injection scenarios were designed to test whether SACI reacts meaningfully to different types of visibility degradation. These scenarios include critical domain controller log loss, non-critical endpoint telemetry loss, PowerShell telemetry loss, Linux authentication log loss, firewall IOC visibility without CTI closure, MISP lookup failure, MITRE scope expansion, telemetry freshness decay, detection rule gaps, and recovery after remediation.

The S7A and S7B scenarios were included to evaluate whether the model can differentiate between critical and non-critical telemetry loss. The S15 scenario was included to test whether stale telemetry can reduce the score even when the graph has no missing edges. The S17 scenario was included to verify recovery behavior, while S18 was included to validate legacy control handling.

This design was preferred because SACI is not a detection accuracy benchmark and does not claim to measure whether an organization is secure. Its purpose is to measure whether expected telemetry, detection, CTI, MITRE, and freshness relationships are observable in the SIEM graph.
