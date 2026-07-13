SACI COMPLETE REFERENCES / TECHNOLOGY STACK

Included technologies:
GOAD, Vagrant, VMware ESXi/vSphere, Active Directory Domain Services,
Ubuntu Server, pfSense, Wazuh, Wazuh Indexer, OpenSearch, Sysmon,
Windows Advanced Audit Policy, PowerShell logging, rsyslog,
systemd-journald, MISP, OpenCTI, MITRE ATT&CK, CISA mapping guidance,
Python, Requests, Cytoscape.js, Mermaid, GitHub Pages, NIST and academic sources.

Scope labels:
- Directly used in final chain
- Used in lab infrastructure
- Supporting; not in final score
- Methodological basis

Install:
cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_references_complete_stack.zip -d .
python3 patch_references_complete_nav.py

Test:
python3 -m http.server 8000 --directory docs
http://127.0.0.1:8000/references.html?stack=2
http://127.0.0.1:8000/en/references.html?stack=2
