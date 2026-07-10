# SACI Final Evidence Package

**SACI (Security Attack Surface Coverage Index)** is an explainable, graph-based SIEM visibility scoring model designed to evaluate whether expected security visibility relationships are observed and closed within a declared SOC evaluation scope.

This repository publishes the final supporting evidence package for the SACI v2 laboratory evaluation.

## Public Evidence Portal

https://4rslanismet.github.io/saci-final-evidence/

## Türkçe Özet

SACI, bir kurumun tamamen güvenli olup olmadığını ölçen bir güvenlik garantisi modeli değildir. SACI, tanımlı değerlendirme kapsamı içinde beklenen görünürlük ilişkilerinin SIEM, CTI, MITRE ATT&CK ve kanıt grafı üzerinden gözlemlenip gözlemlenmediğini ölçen açıklanabilir bir görünürlük skorlama modelidir.

Bu repository, SACI v2 final kanıt paketini yayınlar.

## Final v2 Evidence Summary

| Metric | Meaning | Final Value |
|---|---|---:|
| CWLC | Criticality-weighted log coverage | 100 |
| CAC | Control / alert coverage | 100 |
| MDC | MITRE ATT&CK detection coverage | 100 |
| CTIC | CTI / MISP enrichment coverage | 100 |
| TF | Telemetry freshness | 100 |
| SACI | Overall SACI visibility score | 100 |

## Final Graph Closure

| Item | Value |
|---|---:|
| Nodes | 97 |
| Edges | 171 |
| Observed edges | 171 |
| Missing edges | 0 |

## Core Components

SACI v2 evaluates visibility through the following layers:

- Asset and expected log source coverage
- Criticality-weighted log coverage
- Wazuh detection control coverage
- MITRE ATT&CK technique coverage
- CTI / MISP enrichment closure
- Evidence graph closure
- Deterministic reason codes
- Policy-guided explanation reporting

## Repository Structure

- docs/index.html: Main GitHub Pages portal
- docs/lab_topology.html: SACI lab architecture
- docs/graph.html: Interactive evidence graph
- docs/evidence/lab/index.html: Final lab evidence report
- docs/evidence/paper_clean/index.html: Paper-oriented visual summary
- docs/evidence/explanation_report.html: Policy-guided explanation report
- docs/data/VALIDATION.txt: Final validation note
- docs/data/FINAL_AUDIT_RESULT.md: Final audit result
- docs/data/v2/: Final SACI v2 CSV, JSON and graph data
- archive/saci_lab_old_version/: Legacy PoC files retained for traceability only

## Important Interpretation Note

**SACI=100 does not mean that the environment is fully secure.**

It means that all expected visibility relationships defined within the declared evaluation scope were observed and closed.

Türkçe olarak:

**SACI=100, ortamın tamamen güvenli olduğu anlamına gelmez.**

Bu sonuç yalnızca tanımlı değerlendirme kapsamındaki beklenen görünürlük ilişkilerinin gözlemlendiğini ve kanıt grafı üzerinde kapandığını ifade eder.

## Evidence Pages

- Main portal: https://4rslanismet.github.io/saci-final-evidence/
- Lab architecture: https://4rslanismet.github.io/saci-final-evidence/lab_topology.html
- Final lab evidence: https://4rslanismet.github.io/saci-final-evidence/evidence/lab/
- Interactive graph: https://4rslanismet.github.io/saci-final-evidence/graph.html
- Paper clean view: https://4rslanismet.github.io/saci-final-evidence/evidence/paper_clean/
- Explanation report: https://4rslanismet.github.io/saci-final-evidence/evidence/explanation_report.html

## Citation

Suggested repository citation:

Arslan, I. (2026). SACI Final Evidence Package: Supporting Evidence for an Explainable Graph-Based SIEM Visibility Scoring Model. GitHub. https://github.com/4rslanismet/saci-final-evidence

## License

This evidence package is released under the Creative Commons Attribution 4.0 International License, unless otherwise stated.
