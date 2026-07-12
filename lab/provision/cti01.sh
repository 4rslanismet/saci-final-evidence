#!/usr/bin/env bash
set -euo pipefail
PROFILE="$1"; MISP_REF="$2"; DEPLOY="$3"
if [[ "$DEPLOY" == "1" ]]; then
  echo "[SACI] MISP deployment requested (${MISP_REF})."
  echo "[SACI] Supply secrets through environment files excluded from version control."
fi
