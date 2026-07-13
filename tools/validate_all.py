#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
commands = [
    [sys.executable, str(root / "tools" / "validate_academic_site.py")],
    [sys.executable, str(root / "tools" / "validate_integrity.py"), "--data-dir", "docs/data/final", "--check"],
    [sys.executable, str(root / "tools" / "validate_portal_paper_sync.py")],
    [sys.executable, str(root / "tools" / "validate_repository.py")],
]

for command in commands:
    result = subprocess.run(command, cwd=root)
    if result.returncode:
        sys.exit(result.returncode)

print("SACI combined validation PASSED")
