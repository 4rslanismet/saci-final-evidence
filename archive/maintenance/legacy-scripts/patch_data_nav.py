#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re
import shutil

root = Path.cwd()
docs = root / "docs"

if not docs.exists():
    raise SystemExit("Run this script from the repository root containing docs/.")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_root = root / "backups" / f"data_page_nav_{stamp}"

targets = list(docs.glob("*.html")) + list((docs / "en").glob("*.html"))
changed = []

pattern = re.compile(
    r'(<a\b[^>]*href=["\']artifacts\.html["\'][^>]*>.*?</a>)',
    re.I | re.S
)

for path in targets:
    text = path.read_text(encoding="utf-8", errors="replace")

    # Do not create duplicates.
    if re.search(r'href=["\']data\.html["\']', text, re.I):
        continue

    updated, count = pattern.subn(
        r'\1\n      <a href="data.html">Data</a>',
        text,
        count=1
    )

    if count:
        rel = path.relative_to(root)
        backup_path = backup_root / rel
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)
        path.write_text(updated, encoding="utf-8")
        changed.append(str(rel))

print("Data page installed.")
print(f"Navigation updated in {len(changed)} page(s).")
if changed:
    print(f"Backups: {backup_root}")
    for item in changed:
        print(f"  - {item}")
