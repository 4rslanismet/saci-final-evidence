#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.cwd()
DOCS = ROOT / "docs"

if not DOCS.exists():
    raise SystemExit("[!] docs/ bulunamadı. Scripti repo kökünde çalıştır.")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_root = ROOT / "backups" / f"references_nav_{stamp}"
targets = sorted(DOCS.glob("*.html")) + sorted((DOCS / "en").glob("*.html"))
changed = []

for path in targets:
    html = path.read_text(encoding="utf-8", errors="replace")

    if re.search(r'href=["\']references\.html["\']', html, re.I):
        continue

    pattern = re.compile(
        r'(<a\b[^>]*href=["\']data\.html["\'][^>]*>.*?</a>)',
        re.I | re.S
    )

    updated, count = pattern.subn(
        r'\1\n      <a href="references.html">References</a>',
        html,
        count=1
    )

    if not count:
        continue

    rel = path.relative_to(ROOT)
    backup = backup_root / rel
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup)

    path.write_text(updated, encoding="utf-8")
    changed.append(str(rel))

print("References navigation installed.")
print(f"Updated pages: {len(changed)}")
if changed:
    print(f"Backups: {backup_root}")
    for item in changed:
        print(f"  - {item}")
