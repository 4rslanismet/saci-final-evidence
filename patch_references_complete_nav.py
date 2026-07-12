#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re, shutil

ROOT=Path.cwd(); DOCS=ROOT/"docs"
if not DOCS.exists(): raise SystemExit("[!] docs/ bulunamadı.")
stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
backup=ROOT/"backups"/f"references_complete_{stamp}"
targets=sorted(DOCS.glob("*.html"))+sorted((DOCS/"en").glob("*.html"))
changed=[]

for path in targets:
    html=path.read_text(encoding="utf-8",errors="replace")
    if re.search(r'href=["\']references\.html["\']',html,re.I): continue
    m=re.compile(r'(<a\b[^>]*href=["\']data\.html["\'][^>]*>.*?</a>)',re.I|re.S)
    updated,count=m.subn(r'\1\n<a href="references.html">References</a>',html,count=1)
    if not count: continue
    rel=path.relative_to(ROOT); dst=backup/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(path,dst)
    path.write_text(updated,encoding="utf-8"); changed.append(str(rel))

print(f"References navigation updated in {len(changed)} page(s).")
if changed: print(f"Backups: {backup}")
