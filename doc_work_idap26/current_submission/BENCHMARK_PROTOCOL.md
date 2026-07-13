# SACI integrity-gate benchmark protocol

## Purpose

This companion evaluates two claims that are narrower than operational SIEM
performance:

1. The integrity gate assigns the expected status to controlled structural and
   policy faults.
2. Its single-process validation time and traced Python memory remain practical
   as a valid graph is replicated to larger cardinalities.

## Synthetic baseline

Each replica contains:

- 99 declared nodes,
- 171 relationship rows,
- 165 unique source-relation-target triples,
- 6 parallel evidence rows with distinct `evidence_id` values,
- a direct `110203 -> T1071.001` mapping,
- a contextual `T1071.004` relation,
- 6 policy-exempt isolated nodes.

The structure mirrors the published canonical cardinalities. It does not replay
Wazuh alerts, MISP transactions, endpoint events, or browser rendering.

## Controlled cases

- valid baseline,
- undeclared endpoint,
- duplicate node identifier,
- conflicting direct ATT&CK mapping,
- CSV-renderer representation mismatch,
- missing required edge field,
- parallel evidence-ID collision,
- undocumented isolated node,
- policy-documented isolated node.

Expected states are encoded before validation in the benchmark script.

## Cardinality series

Replication factors: 1, 10, 100, 1000.

Resulting largest case: 99,000 nodes, 171,000 relationship rows, and 165,000
unique triples.

Each case is validated seven times. The report retains median, minimum and
maximum wall-clock time and median peak memory reported by Python `tracemalloc`.

## Environment used for the included results

- Python 3.13.5
- Linux 4.4.0 x86_64
- single Python process
- 4 GiB memory available to the execution environment

CPU model information was not exposed by the execution environment; therefore
no cross-machine performance comparison is claimed.

## Reproduction

```bash
python3 benchmark_integrity_scalability.py \
  --out-dir benchmark_results \
  --repeats 7 \
  --multipliers 1,10,100,1000
```

## Interpretation boundary

The output is evidence about the implemented validation rules and synthetic
data-structure growth. It is not evidence about SIEM ingestion throughput,
OpenSearch query latency, concurrent SOC workloads, alert detection efficacy,
or Cytoscape.js rendering performance.
