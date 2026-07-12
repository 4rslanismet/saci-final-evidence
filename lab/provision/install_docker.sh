#!/usr/bin/env bash
set -euo pipefail
if command -v docker >/dev/null 2>&1; then exit 0; fi
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "${SUDO_USER:-$USER}" || true
