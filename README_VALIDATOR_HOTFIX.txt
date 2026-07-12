SACI VALIDATOR + MANIFEST HOTFIX

Fixes:
- old list-only scenario-manifest parser
- canonical {default,datasets} manifest support
- English manifest paths
- reproducibility page metadata, skip link and main target
- English reproduction download paths
- validator coverage for Reproduce/Vagrant/topology

Install from repository root:
unzip -o saci_validator_manifest_hotfix.zip -d .
python3 tools/validate_academic_site.py
