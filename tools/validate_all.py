#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
academic=root/"tools"/"validate_academic_site.py"
if academic.exists():
 rc=subprocess.run([sys.executable,str(academic)],cwd=root).returncode
 if rc: sys.exit(rc)
sync=root/"tools"/"validate_portal_paper_sync.py"
if sync.exists():
 rc=subprocess.run([sys.executable,str(sync)],cwd=root).returncode
 if rc: sys.exit(rc)
sys.exit(subprocess.run([sys.executable,str(root/"tools"/"validate_integrity.py"),"--data-dir","docs/data/final","--check"],cwd=root).returncode)
