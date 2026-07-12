#!/usr/bin/env bash
set -euo pipefail
PROFILE="$1"; WAZUH_VERSION="$2"; WAZUH_REF="$3"; DEPLOY="$4"
sudo mkdir -p /opt/saci-final
sudo cp -a /tmp/saci-final/. /opt/saci-final/
python3 /tmp/saci-verify.py /opt/saci-final
if [[ "$DEPLOY" == "1" ]]; then
  echo "[SACI] Service deployment requested for Wazuh ${WAZUH_VERSION} (${WAZUH_REF})."
  echo "[SACI] Pin and review the official Wazuh Docker deployment before production use."
fi
