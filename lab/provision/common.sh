#!/usr/bin/env bash
set -euo pipefail
NAME="$1"; ASSET_ID="$2"; ROLE="$3"; PROFILE="$4"
sudo mkdir -p /etc/saci
printf 'name=%s\nasset_id=%s\nrole=%s\nprofile=%s\n' "$NAME" "$ASSET_ID" "$ROLE" "$PROFILE" | sudo tee /etc/saci/node.conf >/dev/null
echo "[SACI] Base provisioning complete for $NAME ($ASSET_ID)."
