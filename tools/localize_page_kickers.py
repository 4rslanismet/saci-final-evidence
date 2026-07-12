#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import re
import shutil

ROOT = Path.cwd()
DOCS = ROOT / "docs"

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "backups" / f"page_kickers_{STAMP}"

LABELS = {
    "index.html": {
        "tr": "KANONİK YAYIN ANLIK GÖRÜNTÜSÜ",
        "en": "CANONICAL PUBLICATION SNAPSHOT",
    },
    "methodology.html": {
        "tr": "METODOLOJİ",
        "en": "METHODOLOGY",
    },
    "architecture.html": {
        "tr": "MİMARİ",
        "en": "ARCHITECTURE",
    },
    "evidence.html": {
        "tr": "FİNAL KANIT",
        "en": "FINAL EVIDENCE",
    },
    "artifacts.html": {
        "tr": "KANIT DOSYALARI",
        "en": "ARTIFACTS",
    },
    "graph.html": {
        "tr": "GRAF GEZGİNİ",
        "en": "GRAPH EXPLORER",
    },
    "explanation.html": {
        "tr": "AÇIKLAMA KATMANI",
        "en": "EXPLANATION LAYER",
    },
    "paper.html": {
        "tr": "MAKALE GÖRÜNÜMÜ",
        "en": "PAPER VIEW",
    },
    "data.html": {
        "tr": "VERİ VE KANIT KAYNAKLARI",
        "en": "DATA AND EVIDENCE SOURCES",
    },
    "validation.html": {
        "tr": "DOĞRULAMA",
        "en": "VALIDATION",
    },
}

KICKER_PATTERN = re.compile(
    r'''
    <
    (?P<tag>div|span|p)
    (?P<attrs>
        [^>]*
        class\s*=\s*
        ["']
        [^"']*
        (?:
            kicker
            |
            eyebrow
            |
            overline
            |
            page-label
            |
            page-kicker
            |
            page-eyebrow
            |
            hero-kicker
            |
            section-kicker
            |
            intro-kicker
        )
        [^"']*
        ["']
        [^>]*
    )
    >
    (?P<content>.*?)
    </(?P=tag)>
    ''',
    re.I | re.S | re.X,
)


def backup(path: Path) -> None:
    target = BACKUP / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def set_html_language(html: str, lang: str) -> str:
    if re.search(r"<html\b[^>]*\blang=", html, flags=re.I):
        return re.sub(
            r'(<html\b[^>]*\blang\s*=\s*)["\'][^"\']*["\']',
            rf'\1"{lang}"',
            html,
            count=1,
            flags=re.I,
        )

    return re.sub(
        r"<html\b",
        f'<html lang="{lang}"',
        html,
        count=1,
        flags=re.I,
    )


def replace_kicker(html: str, label: str) -> str:
    match = KICKER_PATTERN.search(html)

    if match:
        replacement = (
            f'<{match.group("tag")}{match.group("attrs")}>'
            f'{label}'
            f'</{match.group("tag")}>'
        )

        return (
            html[:match.start()]
            + replacement
            + html[match.end():]
        )

    # Kicker bulunamazsa ilk ana H1 başlığının önüne ekle.
    h1 = re.search(r"<h1\b[^>]*>", html, flags=re.I)

    if h1:
        kicker = f'<div class="kicker">{label}</div>\n'

        return (
            html[:h1.start()]
            + kicker
            + html[h1.start():]
        )

    return html


def process(path: Path, lang: str) -> None:
    if not path.exists():
        return

    label = LABELS.get(path.name, {}).get(lang)

    if not label:
        return

    backup(path)

    html = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    html = set_html_language(html, lang)
    html = replace_kicker(html, label)

    path.write_text(html, encoding="utf-8")

    print(f"[+] {lang.upper()}: {path.relative_to(ROOT)} → {label}")


for filename in LABELS:
    process(DOCS / filename, "tr")
    process(DOCS / "en" / filename, "en")

print()
print("=== PAGE KICKERS LOCALIZED ===")
print(f"Backup: {BACKUP}")
