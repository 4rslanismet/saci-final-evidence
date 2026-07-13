# Source coverage map

The manuscript cites 60 IEEE-style references from a 61-record BibTeX database.
Citations are attached to the claims they support rather than collected only in
the related-work section.

## Measurement and aggregation

- NIST SP 800-55 Volumes 1 and 2: measure definition, scope, calculation,
  interpretation, and program design.
- ISO/IEC 27004: monitoring, measurement, analysis, and evaluation.
- NIST SP 800-137 and SP 800-92: continuous monitoring and log management.
- Triantaphyllou: simple additive weighting and multi-criteria decision-making
  context. The paper explicitly states that SACI does not introduce a new
  aggregation operator.

## ATT&CK and detection engineering

- MITRE Enterprise Matrix, ATT&CK Data Sources, design philosophy, and data
  tools.
- CISA best practices for precise ATT&CK mapping.
- DeTT&CT and MITRE D3FEND.
- Academic ATT&CK assessment and survey studies.

## Cyber threat intelligence

- OASIS STIX 2.1 and TAXII 2.1.
- MISP implementation and taxonomy/scoring literature.
- CTI taxonomy and ontology studies.

## Graph provenance and validation

- W3C PROV-O for provenance concepts.
- W3C SHACL for explicit graph-constraint validation.
- Trav-SHACL for scalable graph-shape validation research.
- Cybersecurity knowledge-graph literature.
- Cytoscape.js and Mermaid for interactive and textual representations.

The manuscript states that SACI uses a purpose-built CSV/property-graph
validator and is not an RDF/SHACL implementation.

## Reproducibility and integrity

- NIST FIPS 180-4 for SHA-256.
- ACM artifact review guidance.
- National Academies reproducibility and replicability report.
- Vagrant and provider documentation for the reconstruction scaffold.

## Laboratory and data pipeline

- Wazuh architecture, agents, collection, rules, ATT&CK metadata, and external
  integration.
- Microsoft Sysmon, PowerShell logging, and advanced audit policy.
- systemd-journald, rsyslog, and pfSense remote logging.
- Ansible WinRM.
- JSON and CSV RFCs.

## Explainability boundary

- Retrieval-augmented generation literature.
- NIST AI RMF and Generative AI Profile.

These sources support the design in which language models may summarize
validated evidence but do not calculate SACI or determine the publication gate.
