#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path("/opt/saci-lab")
DATA = BASE / "data"
OUT = BASE / "outputs_v2"

ALERTS_JSON = Path("/var/ossec/logs/alerts/alerts.json")
MISP_LOG = Path("/var/log/wazuh-misp/misp-enrichment.log")
SCENARIO_LOG = Path("/var/log/saci/saci-scenario-events.log")
PFSENSE_EVENTS_LOG = Path("/var/log/saci/pfsense-events.log")

SCENARIO_RULE_MAP = {
    "DNS_QUERY_OBSERVED": "110005",
    "DOMAIN_IOC_PROCESS_OBSERVED": "110006",
    "T1087_ACCOUNT_DISCOVERY": "110010",
    "T1482_DOMAIN_TRUST_DISCOVERY": "110011",
    "T1016_NETWORK_CONFIG_DISCOVERY": "110012",
    "T1105_INGRESS_TOOL_TRANSFER": "110013",
    "T1135_NETWORK_SHARE_DISCOVERY": "110014",
    "PFSENSE_FIREWALL_EVENT": "110200",
    "PFSENSE_BLOCK_EVENT": "110201",
    "PFSENSE_IOC_TRAFFIC": "110203",
}

PFSENSE_RULES = {"110200", "110201", "110203"}

WEIGHTS = {
    "CWLC": 0.30,
    "CAC": 0.25,
    "MDC": 0.20,
    "CTIC": 0.15,
    "TF": 0.10,
}

DEFAULT_SOURCE_WEIGHTS = {
    "Security": 5,
    "Sysmon": 4,
    "PowerShell": 3,
    "authlog": 4,
    "syslog": 2,
    "process": 3,
    "pfsense_syslog": 5,
    "ossec": 2,
    "misp_enrichment": 4,
    "misp_api": 4,
}

def read_csv(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def deep_get(obj, dotted, default=""):
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur

def iter_json_lines(path, tail_lines=None):
    if not path.exists():
        return
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return
    if tail_lines:
        lines = lines[-tail_lines:]
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except Exception:
            continue

def parse_time(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None

def iso_or_empty(dt):
    if not dt:
        return ""
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()

def safe_ratio(numerator, denominator):
    if denominator == 0:
        return None
    return numerator / denominator

def weighted_score(metrics, weights):
    active = {k: v for k, v in metrics.items() if v is not None}
    if not active:
        return None
    total_weight = sum(weights[k] for k in active)
    if total_weight == 0:
        return None
    return sum(weights[k] * active[k] for k in active) / total_weight

def as_float(value, default=1.0):
    try:
        return float(value)
    except Exception:
        return default

def asset_by_hostname(assets):
    out = {}
    for a in assets:
        aid = a.get("asset_id", "")
        hn = (a.get("hostname") or "").upper()
        if hn:
            out[hn] = aid
    return out

def get_source_weight(weights_rows, asset_id, source):
    for r in weights_rows:
        if r.get("asset_id") == asset_id and r.get("log_source") == source:
            return as_float(r.get("source_weight"), DEFAULT_SOURCE_WEIGHTS.get(source, 1))
    return DEFAULT_SOURCE_WEIGHTS.get(source, 1)

def add_live_source(live_sources, source_latest, asset_id, source, ts=None):
    if not asset_id or not source:
        return
    live_sources.setdefault(asset_id, set()).add(source)
    if ts:
        old = source_latest.get((asset_id, source))
        if old is None or ts > old:
            source_latest[(asset_id, source)] = ts

def infer_alert_asset_source(alert, assets_host_map):
    rid = str(deep_get(alert, "rule.id", ""))
    desc = str(deep_get(alert, "rule.description", ""))
    location = str(alert.get("location", ""))
    agent_name = str(deep_get(alert, "agent.name", "")).upper()
    agent_id = str(deep_get(alert, "agent.id", ""))

    provider = str(deep_get(alert, "data.win.system.providerName", ""))
    channel = str(deep_get(alert, "data.win.system.channel", ""))
    eventdata_channel = str(deep_get(alert, "data.win.system.Channel", ""))

    full = json.dumps(alert, ensure_ascii=False)

    asset_id = assets_host_map.get(agent_name, "")

    if agent_name == "DC01":
        asset_id = asset_id or "A01"
    elif agent_name in ("WS01", "WIN11", "ENDPOINT01"):
        asset_id = asset_id or "A04"
    elif agent_name in ("WSIEM", "WAZUH", "WAZUH-MANAGER") or agent_id == "000":
        asset_id = asset_id or "A02"

    source = ""

    if "misp-enrichment.log" in location:
        return "A02", "misp_enrichment"

    if "pfsense" in location.lower() or rid in PFSENSE_RULES:
        return "A07", "pfsense_syslog"

    if provider == "Microsoft-Windows-Sysmon" or "Microsoft-Windows-Sysmon" in full or "Sysmon" in desc:
        source = "Sysmon"
    elif "PowerShell" in provider or "PowerShell" in channel or "PowerShell" in eventdata_channel or "PowerShell" in desc:
        source = "PowerShell"
    elif channel == "Security" or eventdata_channel == "Security" or "Security" in location or "Security" in desc:
        source = "Security"
    elif "auth.log" in location or "authlog" in location:
        source = "authlog"
    elif "syslog" in location:
        source = "syslog"
    elif agent_id == "000":
        source = "ossec"

    return asset_id, source

def build_reason(reason_code, metric, impact, **fields):
    return {
        "reason_code": reason_code,
        "metric": metric,
        "impact": round(float(impact), 4),
        "fields": fields,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tail-lines", type=int, default=500000)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)

    assets = read_csv(DATA / "assets.csv")
    controls = read_csv(DATA / "detection_controls.csv")
    mitre_scope = read_csv(DATA / "mitre_scope.csv")
    cti_iocs = read_csv(DATA / "cti_iocs.csv")
    source_weights = read_csv(DATA / "log_source_weights.csv")

    host_map = asset_by_hostname(assets)

    live_sources = {a["asset_id"]: set() for a in assets if a.get("asset_id")}
    source_latest = {}
    seen_rules = set()
    seen_mitre = set()
    seen_iocs = set()
    latest_times = []
    misp_log_text = ""

    # 1) Wazuh alerts.json
    for alert in iter_json_lines(ALERTS_JSON, args.tail_lines):
        rid = str(deep_get(alert, "rule.id", ""))
        if rid:
            seen_rules.add(rid)

        ts = parse_time(str(alert.get("timestamp", "")))
        if ts:
            latest_times.append(ts)

        mitre_ids = deep_get(alert, "rule.mitre.id", [])
        if isinstance(mitre_ids, str):
            mitre_ids = [mitre_ids]
        if isinstance(mitre_ids, list):
            for mid in mitre_ids:
                if mid:
                    seen_mitre.add(str(mid))

        asset_id, source = infer_alert_asset_source(alert, host_map)
        add_live_source(live_sources, source_latest, asset_id, source, ts)

        full = json.dumps(alert, ensure_ascii=False)
        for ioc in cti_iocs:
            ind = (ioc.get("indicator") or "").strip()
            if ind and ind in full:
                seen_iocs.add(ind)

    # 2) Normalized scenario/evidence logs
    # Kritik düzeltme:
    # Eski kodda T* senaryosu görülünce otomatik A01/Sysmon ekleniyordu.
    # Burada sadece event içinde asset_id ve log_source varsa live source sayılır.
    for ev_path in [SCENARIO_LOG, PFSENSE_EVENTS_LOG]:
        for ev in iter_json_lines(ev_path, None):
            scenario_id = str(ev.get("scenario_id", ""))
            rid = str(ev.get("rule_id") or SCENARIO_RULE_MAP.get(scenario_id, ""))
            if rid:
                seen_rules.add(rid)

            ts = parse_time(str(ev.get("event_time") or ev.get("timestamp") or ""))
            if ts:
                latest_times.append(ts)

            asset_id = str(ev.get("asset_id", ""))
            log_source = str(ev.get("log_source", ""))
            event_source = str(ev.get("event_source", "")).lower()

            if scenario_id.startswith("PFSENSE_") or event_source == "pfsense":
                asset_id = asset_id or "A07"
                log_source = log_source or "pfsense_syslog"

            add_live_source(live_sources, source_latest, asset_id, log_source, ts)

            mt = str(ev.get("mitre_technique", ""))
            if mt:
                for part in mt.replace(",", ";").split(";"):
                    part = part.strip()
                    if part:
                        seen_mitre.add(part)

            ind = str(ev.get("indicator", ""))
            if ind:
                seen_iocs.add(ind)

            raw = json.dumps(ev, ensure_ascii=False)
            for ioc in cti_iocs:
                indicator = (ioc.get("indicator") or "").strip()
                if indicator and indicator in raw:
                    seen_iocs.add(indicator)

    # 3) MISP enrichment log
    if MISP_LOG.exists():
        misp_log_text = MISP_LOG.read_text(encoding="utf-8", errors="ignore")
        if misp_log_text.strip():
            add_live_source(live_sources, source_latest, "A02", "misp_enrichment")
            add_live_source(live_sources, source_latest, "A03", "misp_api")

        for obj in iter_json_lines(MISP_LOG, None):
            ts = parse_time(obj.get("timestamp", ""))
            if ts:
                latest_times.append(ts)
            ind = str(obj.get("indicator", ""))
            if ind:
                seen_iocs.add(ind)

        for ioc in cti_iocs:
            ind = (ioc.get("indicator") or "").strip()
            if ind and ind in misp_log_text:
                seen_iocs.add(ind)

    # 4) CWLC: asset criticality + source weight
    log_status_rows = []
    asset_rows = []
    asset_weighted_sum = 0.0
    asset_weight_total = 0.0
    reasons = []

    for asset in assets:
        aid = asset.get("asset_id", "")
        hostname = asset.get("hostname", "")
        crit = as_float(asset.get("criticality"), 1)
        expected = [x.strip() for x in (asset.get("expected_log_sources") or "").split(";") if x.strip()]
        received = sorted(live_sources.get(aid, set()))

        source_observed_weight = 0.0
        source_total_weight = 0.0

        for source in expected:
            sw = get_source_weight(source_weights, aid, source)
            observed = source in received
            source_total_weight += sw
            if observed:
                source_observed_weight += sw

            last_seen = source_latest.get((aid, source))

            log_status_rows.append({
                "asset_id": aid,
                "hostname": hostname,
                "log_source": source,
                "expected": 1,
                "observed": 1 if observed else 0,
                "asset_criticality": crit,
                "source_weight": sw,
                "last_seen": iso_or_empty(last_seen),
            })

            if not observed:
                reasons.append(build_reason(
                    "expected_log_source_not_observed",
                    "CWLC",
                    WEIGHTS["CWLC"] * crit * sw,
                    asset_id=aid,
                    hostname=hostname,
                    log_source=source,
                    asset_criticality=crit,
                    source_weight=sw,
                ))

        coverage = safe_ratio(source_observed_weight, source_total_weight)
        coverage_percent = None if coverage is None else round(coverage * 100, 2)

        if coverage is not None:
            asset_weighted_sum += crit * coverage
            asset_weight_total += crit

        asset_rows.append({
            "asset_id": aid,
            "hostname": hostname,
            "expected_sources": ";".join(expected),
            "received_sources": ";".join(received),
            "coverage_percent": "" if coverage_percent is None else coverage_percent,
            "criticality": crit,
            "coverage_applicable": 1 if coverage is not None else 0,
        })

    cwlc_ratio = safe_ratio(asset_weighted_sum, asset_weight_total)
    cwlc_score = None if cwlc_ratio is None else round(cwlc_ratio * 100, 2)

    # 5) CAC: enabled detection controls observed as Wazuh rules
    control_rows = []
    control_weight_seen = 0.0
    control_weight_total = 0.0

    for c in controls:
        enabled = str(c.get("enabled", "1")) == "1"
        weight = as_float(c.get("weight"), 1)
        rid = str(c.get("rule_id", ""))
        seen = 1 if enabled and rid in seen_rules else 0

        if enabled:
            control_weight_total += weight
            if seen:
                control_weight_seen += weight
            else:
                reasons.append(build_reason(
                    "enabled_control_not_seen",
                    "CAC",
                    WEIGHTS["CAC"] * weight,
                    control_id=c.get("control_id", ""),
                    rule_id=rid,
                    asset_id=c.get("asset_id", ""),
                    source=c.get("source", ""),
                    control_weight=weight,
                ))

        control_rows.append({
            "control_id": c.get("control_id", ""),
            "asset_id": c.get("asset_id", ""),
            "source": c.get("source", ""),
            "rule_id": rid,
            "mitre_technique": c.get("mitre_technique", ""),
            "enabled": 1 if enabled else 0,
            "seen": seen,
            "weight": weight,
            "description": c.get("description", ""),
        })

        if seen and c.get("mitre_technique"):
            for part in str(c["mitre_technique"]).replace(",", ";").split(";"):
                part = part.strip()
                if part:
                    seen_mitre.add(part)

    cac_ratio = safe_ratio(control_weight_seen, control_weight_total)
    cac_score = None if cac_ratio is None else round(cac_ratio * 100, 2)

    # 6) MDC
    mitre_rows = []
    mitre_total = 0
    mitre_seen = 0

    for m in mitre_scope:
        if str(m.get("in_scope", "1")) != "1":
            continue

        tid = m.get("technique_id", "")
        priority = as_float(m.get("priority") or m.get("weight"), 1)
        covered = 1 if tid in seen_mitre else 0

        mitre_total += 1
        mitre_seen += covered

        if not covered:
            reasons.append(build_reason(
                "mitre_technique_not_covered",
                "MDC",
                WEIGHTS["MDC"] * priority,
                technique_id=tid,
                technique_name=m.get("technique_name", ""),
                tactic=m.get("tactic", ""),
                technique_priority=priority,
            ))

        mitre_rows.append({
            "technique_id": tid,
            "technique_name": m.get("technique_name", ""),
            "tactic": m.get("tactic", ""),
            "covered": covered,
            "priority": priority,
        })

    mdc_ratio = safe_ratio(mitre_seen, mitre_total)
    mdc_score = None if mdc_ratio is None else round(mdc_ratio * 100, 2)

    # 7) CTIC staged closure
    ctic_rows = []
    cti_partial_scores = []

    for ioc in cti_iocs:
        indicator = (ioc.get("indicator") or "").strip()
        expected_rule = str(ioc.get("expected_alert_rule", "")).strip()
        expected_lookup = str(ioc.get("expected_lookup", "1")) != "0"

        lookup_executed = 1 if expected_lookup else 0
        if indicator and indicator in misp_log_text:
            lookup_executed = 1

        misp_hit = 1 if indicator and indicator in seen_iocs else 0
        wazuh_alert = 1 if expected_rule and expected_rule in seen_rules else 0

        mapped_to_mitre = 0
        mitre_expected = str(ioc.get("mitre_technique", "") or "T1071.004").strip()
        if mitre_expected and mitre_expected in seen_mitre and wazuh_alert:
            mapped_to_mitre = 1

        if expected_lookup:
            partial = 0.0
            partial += 0.25 if lookup_executed else 0.0
            partial += 0.25 if misp_hit else 0.0
            partial += 0.25 if wazuh_alert else 0.0
            partial += 0.25 if mapped_to_mitre else 0.0
            cti_partial_scores.append(partial)

            if lookup_executed and not misp_hit:
                reasons.append(build_reason(
                    "cti_lookup_without_hit",
                    "CTIC",
                    WEIGHTS["CTIC"] * 1.0,
                    indicator=indicator,
                    lookup_executed=lookup_executed,
                    misp_hit=misp_hit,
                ))

            if misp_hit and not wazuh_alert:
                reasons.append(build_reason(
                    "ioc_not_converted_to_alert",
                    "CTIC",
                    WEIGHTS["CTIC"] * 1.5,
                    indicator=indicator,
                    misp_hit=misp_hit,
                    expected_alert_rule=expected_rule,
                    wazuh_alert=wazuh_alert,
                ))

        ctic_rows.append({
            "indicator": indicator,
            "type": ioc.get("type", ""),
            "lookup_executed": lookup_executed,
            "misp_hit": misp_hit,
            "wazuh_alert": wazuh_alert,
            "mapped_to_mitre": mapped_to_mitre,
            "expected_alert_rule": expected_rule,
            "mitre_technique": mitre_expected,
            "expected_lookup": 1 if expected_lookup else 0,
        })

    if cti_iocs:
        ctic_score = round((sum(cti_partial_scores) / len(cti_partial_scores)) * 100, 2) if cti_partial_scores else None
    else:
        ctic_score = None

    # 8) TF
    now = datetime.now(timezone.utc)
    if latest_times:
        latest = max([t if t.tzinfo else t.replace(tzinfo=timezone.utc) for t in latest_times])
        age_min = (now - latest).total_seconds() / 60
        if age_min <= 60:
            tf_score = 100
        elif age_min <= 1440:
            tf_score = 80
        else:
            tf_score = 50

        if tf_score < 100:
            reasons.append(build_reason(
                "telemetry_freshness_decay",
                "TF",
                WEIGHTS["TF"] * (100 - tf_score),
                latest_event_time=latest.isoformat(),
                age_minutes=round(age_min, 2),
                tf_score=tf_score,
            ))
    else:
        tf_score = 0
        reasons.append(build_reason(
            "telemetry_freshness_absent",
            "TF",
            WEIGHTS["TF"] * 100,
            latest_event_time="",
            age_minutes="",
            tf_score=tf_score,
        ))

    # 9) Overall SACI v2 with active-weight normalization
    metrics_0_1 = {
        "CWLC": None if cwlc_score is None else cwlc_score / 100,
        "CAC": None if cac_score is None else cac_score / 100,
        "MDC": None if mdc_score is None else mdc_score / 100,
        "CTIC": None if ctic_score is None else ctic_score / 100,
        "TF": None if tf_score is None else tf_score / 100,
    }

    saci_ratio = weighted_score(metrics_0_1, WEIGHTS)
    saci_score = None if saci_ratio is None else round(saci_ratio * 100, 2)

    score_rows = [
        {"metric": "CWLC", "name": "Criticality-Weighted Log Coverage", "weight": WEIGHTS["CWLC"], "score": "" if cwlc_score is None else cwlc_score, "applicable": 0 if cwlc_score is None else 1},
        {"metric": "CAC", "name": "Control / Alert Coverage", "weight": WEIGHTS["CAC"], "score": "" if cac_score is None else cac_score, "applicable": 0 if cac_score is None else 1},
        {"metric": "MDC", "name": "MITRE Detection Coverage", "weight": WEIGHTS["MDC"], "score": "" if mdc_score is None else mdc_score, "applicable": 0 if mdc_score is None else 1},
        {"metric": "CTIC", "name": "CTI Integration Coverage", "weight": WEIGHTS["CTIC"], "score": "" if ctic_score is None else ctic_score, "applicable": 0 if ctic_score is None else 1},
        {"metric": "TF", "name": "Timeliness / Freshness", "weight": WEIGHTS["TF"], "score": "" if tf_score is None else tf_score, "applicable": 0 if tf_score is None else 1},
        {"metric": "SACI", "name": "Overall SACI Visibility Score", "weight": 1.0, "score": "" if saci_score is None else saci_score, "applicable": 0 if saci_score is None else 1},
    ]

    reasons_ranked = sorted(reasons, key=lambda r: r.get("impact", 0), reverse=True)

    write_csv(OUT / "saci_scores_v2.csv", score_rows, ["metric", "name", "weight", "score", "applicable"])
    write_csv(OUT / "log_source_status.csv", log_status_rows, ["asset_id", "hostname", "log_source", "expected", "observed", "asset_criticality", "source_weight", "last_seen"])
    write_csv(OUT / "asset_log_coverage_v2.csv", asset_rows, ["asset_id", "hostname", "expected_sources", "received_sources", "coverage_percent", "criticality", "coverage_applicable"])
    write_csv(OUT / "control_coverage_v2.csv", control_rows, ["control_id", "asset_id", "source", "rule_id", "mitre_technique", "enabled", "seen", "weight", "description"])
    write_csv(OUT / "mitre_coverage_v2.csv", mitre_rows, ["technique_id", "technique_name", "tactic", "covered", "priority"])
    write_csv(OUT / "ctic_coverage_v2.csv", ctic_rows, ["indicator", "type", "lookup_executed", "misp_hit", "wazuh_alert", "mapped_to_mitre", "expected_alert_rule", "mitre_technique", "expected_lookup"])
    write_json(OUT / "saci_scores_v2.json", score_rows)
    write_json(OUT / "reason_codes_v2.json", reasons_ranked)

    reason_csv_rows = []
    for r in reasons_ranked:
        flat = {
            "reason_code": r["reason_code"],
            "metric": r["metric"],
            "impact": r["impact"],
            "fields_json": json.dumps(r.get("fields", {}), ensure_ascii=False),
        }
        reason_csv_rows.append(flat)

    write_csv(OUT / "reason_codes_v2.csv", reason_csv_rows, ["reason_code", "metric", "impact", "fields_json"])

    print("=== SACI SCORE V2 ===")
    for r in score_rows:
        score = r["score"] if r["score"] != "" else "N/A"
        print(f"{r['metric']:<5} {str(score):>7}  {r['name']}  applicable={r['applicable']}")

    print()
    print("Top reasons:")
    for r in reasons_ranked[:10]:
        print(f"- {r['metric']} {r['reason_code']} impact={r['impact']} fields={r['fields']}")

    print()
    print(f"Outputs written to: {OUT}")

if __name__ == "__main__":
    main()
