#!/usr/bin/env bash
set -euo pipefail
BIBTEX_CMD="${BIBTEX_CMD:-bibtex}"
if ! command -v "$BIBTEX_CMD" >/dev/null 2>&1; then
  if command -v bibtex.original >/dev/null 2>&1; then
    BIBTEX_CMD="bibtex.original"
  elif [ -x /usr/bin/bibtex.original ]; then
    BIBTEX_CMD="/usr/bin/bibtex.original"
  else
    echo "BibTeX bulunamadı. TeX Live/MiKTeX BibTeX paketini kurun." >&2
    exit 127
  fi
fi
pdflatex -interaction=nonstopmode -halt-on-error SACI_IDAP26_Arslan.tex
"$BIBTEX_CMD" SACI_IDAP26_Arslan
pdflatex -interaction=nonstopmode -halt-on-error SACI_IDAP26_Arslan.tex
pdflatex -interaction=nonstopmode -halt-on-error SACI_IDAP26_Arslan.tex
