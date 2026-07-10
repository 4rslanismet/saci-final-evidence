#!/usr/bin/env bash
set +e

SACI_PAYLOAD_HOST="${SACI_PAYLOAD_HOST:-192.0.2.10}"
SACI_PAYLOAD_PORT="${SACI_PAYLOAD_PORT:-8000}"
SACI_DOMAIN="${SACI_DOMAIN:-sevenkingdoms.local}"
SACI_IOC_DOMAIN="${SACI_IOC_DOMAIN:-cti-test.example.com}"
SACI_TARGET="${SACI_TARGET:-dc01}"
SCENARIO_LOG="${SCENARIO_LOG:-/var/log/saci/saci-scenario-events.log}"

mkdir -p "$(dirname "$SCENARIO_LOG")"

cd /opt/windows-control || exit 1

emit_event() {
  SCENARIO_ID="$1"
  MITRE="$2"
  RULE_ID="$3"
  CMD="$4"
  RC="$5"

  python3 - "$SCENARIO_ID" "$MITRE" "$RULE_ID" "$CMD" "$RC" "$SCENARIO_LOG" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

scenario_id, mitre, rule_id, cmd, rc, log_path = sys.argv[1:]

ev = {
    "event_time": datetime.now(timezone.utc).isoformat(),
    "asset_id": "A01",
    "hostname": "DC01",
    "target": "dc01",
    "event_source": "windows",
    "log_source": "Sysmon",
    "scenario_id": scenario_id,
    "mitre_technique": mitre,
    "rule_id": rule_id,
    "command": cmd,
    "runner_rc": int(rc),
    "evidence_type": "normalized_lab_scenario"
}

p = Path(log_path)
p.parent.mkdir(parents=True, exist_ok=True)
with p.open("a", encoding="utf-8") as f:
    f.write(json.dumps(ev, ensure_ascii=False) + "\n")
PY
}

run_dc01() {
  NAME="$1"
  SCENARIO_ID="$2"
  MITRE="$3"
  RULE_ID="$4"
  CMD="$5"

  echo
  echo "[+] $NAME"
  echo "[SCENARIO] $SCENARIO_ID"
  echo "[MITRE] $MITRE"
  echo "[RULE] $RULE_ID"
  echo "[CMD] $CMD"

  ansible windows -i inventory.ini --limit "$SACI_TARGET" -m win_shell -a "$CMD"
  RC="$?"

  emit_event "$SCENARIO_ID" "$MITRE" "$RULE_ID" "$CMD" "$RC"

  echo "[+] Waiting 5 seconds..."
  sleep 5
}

echo "[+] Starting benign HTTP payload server on Wazuh host..."
pkill -f "python3 -m http.server ${SACI_PAYLOAD_PORT}" 2>/dev/null || true
nohup python3 -m http.server "${SACI_PAYLOAD_PORT}" --bind 0.0.0.0 --directory /opt/saci-lab/payloads >/tmp/saci_payload_http.log 2>&1 &
sleep 2

run_dc01 "T1087 - Account discovery" \
  "T1087_ACCOUNT_DISCOVERY" \
  "T1087" \
  "110010" \
  'cmd.exe /c whoami /groups'

run_dc01 "T1087 - Domain users discovery" \
  "T1087_ACCOUNT_DISCOVERY" \
  "T1087" \
  "110010" \
  'cmd.exe /c net user /domain'

run_dc01 "T1087 - Domain admins discovery" \
  "T1087_ACCOUNT_DISCOVERY" \
  "T1087" \
  "110010" \
  'cmd.exe /c net group "Domain Admins" /domain'

run_dc01 "T1482/T1018 - DC discovery" \
  "T1482_DOMAIN_TRUST_DISCOVERY" \
  "T1482;T1018" \
  "110011" \
  "cmd.exe /c nltest /dclist:${SACI_DOMAIN}"

run_dc01 "T1482 - Domain trust discovery" \
  "T1482_DOMAIN_TRUST_DISCOVERY" \
  "T1482" \
  "110011" \
  'cmd.exe /c nltest /domain_trusts'

run_dc01 "T1016 - Network config discovery" \
  "T1016_NETWORK_CONFIG_DISCOVERY" \
  "T1016" \
  "110012" \
  'cmd.exe /c ipconfig /all'

run_dc01 "T1016/T1049 - Route discovery" \
  "T1016_NETWORK_CONFIG_DISCOVERY" \
  "T1016;T1049" \
  "110012" \
  'cmd.exe /c route print'

run_dc01 "T1049 - Network connection discovery" \
  "T1016_NETWORK_CONFIG_DISCOVERY" \
  "T1049" \
  "110012" \
  'cmd.exe /c netstat -ano'

run_dc01 "T1135 - Network share discovery" \
  "T1135_NETWORK_SHARE_DISCOVERY" \
  "T1135" \
  "110014" \
  'cmd.exe /c net view'

run_dc01 "T1135 - DC share discovery" \
  "T1135_NETWORK_SHARE_DISCOVERY" \
  "T1135" \
  "110014" \
  'cmd.exe /c net view \\dc01'

run_dc01 "T1071.004 - DNS IOC query" \
  "DNS_QUERY_OBSERVED" \
  "T1071.004" \
  "110005" \
  "cmd.exe /c nslookup ${SACI_IOC_DOMAIN}"

run_dc01 "T1105 - Benign ingress transfer" \
  "T1105_INGRESS_TOOL_TRANSFER" \
  "T1105" \
  "110013" \
  "cmd.exe /c certutil.exe -urlcache -split -f http://${SACI_PAYLOAD_HOST}:${SACI_PAYLOAD_PORT}/benign_payload.txt %TEMP%\\benign_payload.txt"

echo
echo "[+] Done. Waiting 90 seconds for Wazuh ingestion..."
sleep 90

echo "[+] Recent lab alerts:"
grep -E '"id":"110005"|"id":"110010"|"id":"110011"|"id":"110012"|"id":"110013"|"id":"110014"|"id":"110100"' /var/ossec/logs/alerts/alerts.json | tail -n 30 | jq . 2>/dev/null || true

echo
echo "[+] Normalized scenario events:"
tail -n 20 "$SCENARIO_LOG" | jq . 2>/dev/null || tail -n 20 "$SCENARIO_LOG"
