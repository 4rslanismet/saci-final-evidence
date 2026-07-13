#!/usr/bin/env bash
set -euo pipefail
pdflatex -interaction=nonstopmode -halt-on-error SACI_IDAP26_Turkce_Gonderime_Hazir.tex
bibtex SACI_IDAP26_Turkce_Gonderime_Hazir
pdflatex -interaction=nonstopmode -halt-on-error SACI_IDAP26_Turkce_Gonderime_Hazir.tex
pdflatex -interaction=nonstopmode -halt-on-error SACI_IDAP26_Turkce_Gonderime_Hazir.tex
