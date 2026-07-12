# SACI Laboratory Reproduction Scaffold

This directory provides a **reproduction scaffold**, not a byte-identical archive of the historical experiment.

## Profiles

- `evidence`: boots only `wsiem` and verifies the canonical publication artifacts.
- `portable`: boots every declared machine as Linux stubs to validate topology and provisioning flow without proprietary guest boxes.
- `native`: boots Linux, Windows and FreeBSD guests using provider-compatible boxes supplied through environment variables.

## Quick verification

```bash
SACI_LAB_PROFILE=evidence vagrant up --provider=virtualbox
```

## Full native topology

```bash
export SACI_DC01_BOX='your/windows-server-box'
export SACI_WS01_BOX='your/windows-client-box'
export SACI_FW01_PFSENSE_BOX='your/freebsd-or-pfsense-box'
SACI_LAB_PROFILE=native SACI_DEPLOY_SERVICES=0 vagrant up --provider=vmware_desktop
```

## ESXi

The repository never stores ESXi credentials. Supply them at runtime:

```bash
export GOAD_VAGRANT_ESXIHOST='192.0.2.10'
export GOAD_VAGRANT_ESXIUSER='root'
export GOAD_VAGRANT_ESXIPASSWORD='...'
export GOAD_VAGRANT_ESXIDATASTORE='datastore1'
export GOAD_VAGRANT_ESXINETWORK='SOC_VLAN'
SACI_LAB_PROFILE=native vagrant up --provider=vmware_esxi
```

## Scientific boundary

The canonical evidence snapshot is copied from `docs/data/final/` and validated inside the `wsiem` guest. Recreating live Wazuh/MISP/pfSense/GOAD telemetry requires provider-compatible images, secrets and an isolated authorized lab. The scaffold therefore supports topology reconstruction, artifact verification and controlled service deployment, but it must not be described as an exact digital twin of the original run.
