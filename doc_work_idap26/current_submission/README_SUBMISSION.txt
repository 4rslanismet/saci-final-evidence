SACI IDAP'26 REVIEWER-HARDENED SUBMISSION PACKAGE
=================================================

Main PDF
--------
SACI_IDAP26_Arslan.pdf

Main LaTeX source
-----------------
SACI_IDAP26_Arslan.tex

Bibliography
------------
SACI_IDAP26_References.bib
saci_idap26.bib

Class file
----------
IEEEtran.cls (conference-provided IEEEtran v1.8b)

Figures
-------
figures/saci_pipeline.png
figures/saci_topology.png
figures/integrity_f01.png
figures/sensitivity_selected.png

Editable Graphviz sources for the first three figures are included.

New validation companion
------------------------
benchmark_integrity_scalability.py
benchmark_results/integrity_fault_matrix.csv
benchmark_results/integrity_scalability.csv
benchmark_results/benchmark_summary.json
benchmark_results/run.log
BENCHMARK_PROTOCOL.md

Build
-----
Run:

  ./compile.sh

or:

  pdflatex SACI_IDAP26_Arslan.tex
  bibtex SACI_IDAP26_Arslan
  pdflatex SACI_IDAP26_Arslan.tex
  pdflatex SACI_IDAP26_Arslan.tex

Preflight status
----------------
- IEEEtran conference mode
- A4 paper
- Two columns
- 12 pages including references
- 60 cited IEEE-style references (61 records in the BibTeX database)
- 4 figures
- 6 tables
- 7 numbered equations
- No unresolved citations or cross-references
- No overfull boxes
- All PDF fonts embedded and subsetted Type 1
- Last-page reference columns manually balanced at reference 53
- Template instructional/example text removed

Reviewer-hardening revisions
----------------------------
- The component equations are positioned as transparent operational measures
  aggregated by simple additive weighting, not as a new mathematical theorem.
- F-01 is framed as a pre-release validation case and regression target rather
  than a theoretical discovery.
- A nine-case controlled integrity fault-injection matrix was added.
- A synthetic cardinality benchmark was added for 99/171 through
  99,000/171,000 node/edge-row structures.
- Related work now connects the integrity gate to graph-constraint validation
  literature while clearly stating that the implementation is not SHACL.
- CTIC is described as configured workflow-field closure under the published
  schema; TF is described as a global recency indicator.
- Defensive boundary statements were concentrated in interpretation and
  threats-to-validity sections.

Controlled integrity results
----------------------------
All nine preregistered cases produced the expected state:
- Valid baseline: VALID
- Undeclared endpoint: INVALID
- Duplicate node identifier: INVALID
- Conflicting direct mapping: INVALID
- CSV-renderer mismatch: INVALID
- Missing required edge field: INVALID
- Parallel evidence-ID collision: INVALID
- Undocumented isolated node: VALID_WITH_WARNINGS
- Policy-documented isolated node: VALID

Synthetic integrity benchmark
-----------------------------
Single-process Python 3.13.5, Linux, 7 repeats per size:
- 99 nodes / 171 rows: median 0.778 ms, 0.035 MiB
- 990 nodes / 1,710 rows: median 5.763 ms, 0.308 MiB
- 9,900 nodes / 17,100 rows: median 67.691 ms, 4.270 MiB
- 99,000 nodes / 171,000 rows: median 883.438 ms, 41.170 MiB

This benchmark tests integrity-rule execution and data-structure growth only.
It is not a Wazuh ingestion, browser rendering, or enterprise SOC throughput
benchmark.

Canonical SACI result reported in the paper
-------------------------------------------
- SACI: 100
- Component vector: (100, 100, 100, 100, 100)
- 99 declared / 99 rendered nodes
- 171/171 observed relationship rows
- 165 unique relationship triples
- 18 relationship labels
- 0 active integrity findings
- Integrity status: VALID
- Publication gate: OPEN

Pre-release case F-01 is retained separately from the canonical release:
- 97 declared / 99 rendered nodes
- 171/171 relationship-row closure
- 3 INVALID and 12 WARNING findings
- Publication gate: BLOCKED

Author/contact note
-------------------
No email address or ORCID was invented. The author block uses the verified
institution, personal website, and GitHub profile.

Conference-header note
----------------------
The first-page conference banner was copied from the supplied IDAP'26 LaTeX
template, including its final word "Philippines". Confirm the organizer-issued
camera-ready banner before final submission.

Copyright note
--------------
No speculative IEEE copyright code was inserted. Add only the exact copyright
notice supplied by the conference for the camera-ready version.
