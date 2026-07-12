from __future__ import annotations

import hashlib
import re
import zipfile
from pathlib import Path

import pypdfium2 as pdfium
from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


sources = {
    Path(r"E:\Downloads\IDAP26_SIEM_Graph_Attack_Surface_TR.docx"): "cf2bd7d46d3a536c354b060d330d64fdd43d535c45f3d313833ea5036663be86",
    Path(r"E:\Downloads\IDAP26_SIEM_Graph_Attack_Surface_Draft.docx"): "3e93767ff89e40dd93c738e0c4ef17d268d370f2ae55585cd0d625b11e40b02c",
}

outputs = [
    (
        "TR",
        ROOT / "deliverables" / "IDAP26_SACI_Graph_Attack_Surface_Final_TR.docx",
        ROOT / "doc_work_idap26" / "qa" / "tr-v7" / "final.pdf",
        "tr-TR",
        [
            "C. Matematiksel Tanımlar ve Ölçüm Dayanağı",
            "C. Araçların ve Teknolojilerin İşlevsel Rolleri",
            "VII. DENETİM PROTOKOLÜ VE OPERASYONEL YORUM",
            "IX. VERİ VE ARTEFAKT ERİŞİLEBİLİRLİĞİ",
        ],
    ),
    (
        "EN",
        ROOT / "deliverables" / "IDAP26_SACI_Graph_Attack_Surface_Final_EN.docx",
        ROOT / "doc_work_idap26" / "qa" / "en-v7" / "final.pdf",
        "en-US",
        [
            "C. Mathematical Definitions and Measurement Rationale",
            "C. Functional Roles of the Tools and Technologies",
            "VII. AUDIT PROTOCOL AND OPERATIONAL INTERPRETATION",
            "IX. DATA AND ARTIFACT AVAILABILITY",
        ],
    ),
]

for source, expected in sources.items():
    actual = digest(source)
    if actual != expected:
        raise SystemExit(f"Source changed: {source}\n{actual}")
    print(f"SOURCE_OK {source.name} sha256={actual}")

for tag, docx, pdf, language, required_headings in outputs:
    with zipfile.ZipFile(docx) as archive:
        bad_part = archive.testzip()
        if bad_part:
            raise SystemExit(f"{tag} corrupt part: {bad_part}")
        names = set(archive.namelist())
        root = etree.fromstring(archive.read("word/document.xml"))

    text = "\n".join("".join(p.itertext()) for p in root.findall(f".//{{{W}}}p"))
    forbidden = [
        "66.3",
        "66,3",
        "[University",
        "[Üniversite",
        "research draft",
        "araştırma taslağı",
        "Preliminary Results",
        "Ön Sonuçlar",
        "Because institutional and contact metadata",
        "Kurum ve iletişim bilgisi sağlanmadığından",
        "final-v2",
        "SACI v2",
        "w_as",
        "o_as",
        "T_scope",
        "{{",
    ]
    leftovers = [token for token in forbidden if token.casefold() in text.casefold()]
    if leftovers:
        raise SystemExit(f"{tag} forbidden text: {leftovers}")
    for required in ["25/25", "13/13", "8/8", "97", "171", "165", *required_headings]:
        if required not in text:
            raise SystemExit(f"{tag} missing required text: {required}")

    if root.findall(f".//{{{W}}}ins") or root.findall(f".//{{{W}}}del"):
        raise SystemExit(f"{tag} contains tracked changes")
    if any(name.startswith("word/comments") for name in names):
        raise SystemExit(f"{tag} contains comments")

    paragraph_texts = [
        "".join(paragraph.itertext()).strip()
        for paragraph in root.findall(f".//{{{W}}}p")
    ]
    reference_numbers = {
        int(match.group(1))
        for paragraph_text in paragraph_texts
        if (match := re.match(r"^\[(\d+)\]", paragraph_text))
    }
    if len(reference_numbers) < 20 or max(reference_numbers, default=0) < 32:
        raise SystemExit(
            f"{tag} insufficient references: {sorted(reference_numbers)}"
        )

    equation_count = len(root.findall(f".//{{{M}}}oMath"))
    if equation_count != 9:
        raise SystemExit(f"{tag} unexpected OMML equation count: {equation_count}")

    text_runs = root.findall(f".//{{{W}}}r[{{{W}}}t]")
    missing_language = 0
    for run in text_runs:
        lang = run.find(f"{{{W}}}rPr/{{{W}}}lang")
        if lang is None or lang.get(f"{{{W}}}val") != language:
            missing_language += 1
    if missing_language:
        raise SystemExit(f"{tag} text runs without {language}: {missing_language}")

    doc_prs = root.findall(f".//{{{WP}}}docPr")
    if not doc_prs or any(not node.get("descr") for node in doc_prs):
        raise SystemExit(f"{tag} image alt text missing")

    pdf_document = pdfium.PdfDocument(str(pdf))
    page_count = len(pdf_document)
    pdf_document.close()
    if page_count != 6:
        raise SystemExit(f"{tag} unexpected page count: {page_count}")

    print(
        f"FINAL_OK {tag} pages={page_count} size={docx.stat().st_size} "
        f"sha256={digest(docx)} text_runs={len(text_runs)} "
        f"equations={equation_count} references={len(reference_numbers)}"
    )
