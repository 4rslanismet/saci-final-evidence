SACI IDAP'26 CURRENT SUBMISSION PACKAGE
======================================

Status
------
This directory contains the current official Turkish submission package.

Paper title
-----------
SACI: SIEM-CTI Görünürlük Kanıtlarının Graf Destekli Ölçümü

Language and format
-------------------
- Main language: Turkish
- English abstract and keywords included
- IEEEtran conference format
- A4, two columns
- 6 pages including references

Main files
----------
- SACI_IDAP26_Turkce_Gonderime_Hazir.pdf
- SACI_IDAP26_Turkce_Gonderime_Hazir.tex
- SACI_IDAP26_Turkce_Gonderime_Hazir.bbl
- SACI_IDAP26_References.bib
- IEEEtran.cls
- figures/

Canonical result reported
-------------------------
- SACI: 100.0
- Components: CWLC=100, CAC=100, MDC=100, CTIC=100, TF=100
- Asset-log pairs: 12/12
- Enabled controls: 25/25
- In-scope ATT&CK techniques: 13/13
- CTI workflow flags: 8/8 for two IOCs
- Graph: 99 declared / 99 rendered nodes
- Relations: 171/171 observed
- Active integrity findings: 0
- Integrity status: VALID
- Publication gate: OPEN

F-01
----
The historical 97/99 mismatch is retained only as a resolved pre-release
regression case. It is not an active defect in the canonical release.

Repository alignment
--------------------
The extended English reviewer-hardened manuscript is retained separately
under ../supplementary_extended_en/.

The optional LLM explanation layer and the synthetic validator scalability
benchmark are supplementary portal features. They do not compute or modify
the deterministic score or integrity result reported in the current paper.

Build
-----
  pdflatex SACI_IDAP26_Turkce_Gonderime_Hazir.tex
  bibtex SACI_IDAP26_Turkce_Gonderime_Hazir
  pdflatex SACI_IDAP26_Turkce_Gonderime_Hazir.tex
  pdflatex SACI_IDAP26_Turkce_Gonderime_Hazir.tex
