# Finding F-01 / Bulgu F-01

## Status

**Resolved pre-release validation case — not an active canonical defect.**

## Observation

A pre-release snapshot reported 171/171 observed relations while the node table
declared 97 nodes and the renderer produced 99. The difference came from two
edge endpoints that were referenced but not declared:

- `LOGSOURCE:Wazuh`
- `MITRE:T1071.001`

The same audit also identified a direct-mapping/context distinction for rule
110203, parallel evidence rows without explicit instance identity, and isolated
nodes requiring policy documentation.

## Resolution

The canonical release now:

- declares both endpoints,
- uses `T1071.001` as the direct detection mapping and `T1071.004` as CTI context,
- assigns unique `evidence_id` values to parallel evidence instances, and
- documents intentional isolation exceptions.

## Canonical result

- 99 declared / 99 rendered nodes
- 171/171 observed relations
- 0 active integrity findings
- integrity status `VALID`
- publication gate `OPEN`

## Methodological interpretation

F-01 is a regression and validation case demonstrating that relation closure and
structural integrity are separate checks. It is not presented as a theoretical
discovery or as an active defect in the final dataset.
