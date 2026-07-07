#!/usr/bin/env bash
set -euo pipefail
REPO_URL="${1:-}"
if [ -z "$REPO_URL" ]; then
  echo "Usage: ./publish_to_github.sh https://github.com/<user>/<repo>.git"
  exit 1
fi
git init
git branch -M main
git add .
git commit -m "Publish SACI final evidence viewer"
git remote add origin "$REPO_URL"
git push -u origin main
