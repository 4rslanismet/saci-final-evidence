from __future__ import annotations

import hashlib
import zipfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from lxml import etree

from article_content import (
    EN,
    EN_ADDITIONAL_REFERENCES,
    EN_AFTER_LAB_SECTION,
    EN_AFTER_METRICS,
    EN_BEFORE_CONCLUSION,
    TR,
    TR_ADDITIONAL_REFERENCES,
    TR_AFTER_LAB_SECTION,
    TR_AFTER_METRICS,
    TR_BEFORE_CONCLUSION,
)


ROOT = Path(__file__).resolve().parents[1]
WORK = Path(__file__).resolve().parent
DELIVERABLES = ROOT / "deliverables"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
XML = "http://www.w3.org/XML/1998/namespace"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W, "r": R, "wp": WP, "a": A, "pr": PR, "m": M}

MML2OMML = Path(r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL")
if not MML2OMML.exists():
    raise FileNotFoundError(f"Microsoft MathML converter not found: {MML2OMML}")
MATH_XSLT = etree.XSLT(etree.parse(str(MML2OMML)))

MATHML_BLOCKS: dict[int, list[str]] = {
    35: [
        """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>
        <mi mathvariant="normal">SACI</mi><mo>=</mo><mfrac>
        <mrow><munder><mo>∑</mo><mrow><mi>m</mi><mo>∈</mo><msup><mi>M</mi><mo>*</mo></msup></mrow></munder><msub><mi>w</mi><mi>m</mi></msub><msub><mi>S</mi><mi>m</mi></msub></mrow>
        <mrow><munder><mo>∑</mo><mrow><mi>m</mi><mo>∈</mo><msup><mi>M</mi><mo>*</mo></msup></mrow></munder><msub><mi>w</mi><mi>m</mi></msub></mrow>
        </mfrac></mrow></math>""",
    ],
    37: [
        """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>
        <msub><mi>L</mi><mi>a</mi></msub><mo>=</mo><mfrac>
        <mrow><munder><mo>∑</mo><mrow><mi>s</mi><mo>∈</mo><msub><mi>S</mi><mi>a</mi></msub></mrow></munder><msub><mi>w</mi><mrow><mi>a</mi><mi>s</mi></mrow></msub><msub><mi>o</mi><mrow><mi>a</mi><mi>s</mi></mrow></msub></mrow>
        <mrow><munder><mo>∑</mo><mrow><mi>s</mi><mo>∈</mo><msub><mi>S</mi><mi>a</mi></msub></mrow></munder><msub><mi>w</mi><mrow><mi>a</mi><mi>s</mi></mrow></msub></mrow>
        </mfrac></mrow></math>""",
        """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>
        <mi mathvariant="normal">CWLC</mi><mo>=</mo><mn>100</mn><mfrac>
        <mrow><munder><mo>∑</mo><mrow><mi>a</mi><mo>∈</mo><msup><mi>A</mi><mo>*</mo></msup></mrow></munder><msub><mi>c</mi><mi>a</mi></msub><msub><mi>L</mi><mi>a</mi></msub></mrow>
        <mrow><munder><mo>∑</mo><mrow><mi>a</mi><mo>∈</mo><msup><mi>A</mi><mo>*</mo></msup></mrow></munder><msub><mi>c</mi><mi>a</mi></msub></mrow>
        </mfrac></mrow></math>""",
    ],
    38: [
        """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>
        <mi mathvariant="normal">CAC</mi><mo>=</mo><mn>100</mn><mfrac>
        <mrow><munder><mo>∑</mo><mrow><mi>c</mi><mo>∈</mo><mi>C</mi></mrow></munder><msub><mi>w</mi><mi>c</mi></msub><msub><mi>e</mi><mi>c</mi></msub><msub><mi>s</mi><mi>c</mi></msub></mrow>
        <mrow><munder><mo>∑</mo><mrow><mi>c</mi><mo>∈</mo><mi>C</mi></mrow></munder><msub><mi>w</mi><mi>c</mi></msub><msub><mi>e</mi><mi>c</mi></msub></mrow>
        </mfrac></mrow></math>""",
    ],
    39: [
        """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>
        <mi mathvariant="normal">MDC</mi><mo>=</mo><mn>100</mn><mfrac>
        <mrow><munder><mo>∑</mo><mrow><mi>t</mi><mo>∈</mo><msub><mi>T</mi><mtext>scope</mtext></msub></mrow></munder><msub><mi>z</mi><mi>t</mi></msub></mrow>
        <mrow><mo>|</mo><msub><mi>T</mi><mtext>scope</mtext></msub><mo>|</mo></mrow>
        </mfrac></mrow></math>""",
    ],
    40: [
        """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>
        <mi mathvariant="normal">CTIC</mi><mo>=</mo><mfrac><mn>100</mn><mrow><mn>4</mn><mo>|</mo><mi>I</mi><mo>|</mo></mrow></mfrac>
        <munder><mo>∑</mo><mrow><mi>i</mi><mo>∈</mo><mi>I</mi></mrow></munder>
        <mo>(</mo><msub><mi>q</mi><mi>i</mi></msub><mo>+</mo><msub><mi>h</mi><mi>i</mi></msub><mo>+</mo><msub><mi>a</mi><mi>i</mi></msub><mo>+</mo><msub><mi>m</mi><mi>i</mi></msub><mo>)</mo>
        </mrow></math>""",
    ],
    41: [
        """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>
        <mi mathvariant="normal">TF</mi><mo>(</mo><mi>Δ</mi><mo>,</mo><mi>E</mi><mo>)</mo><mo>=</mo><mo stretchy="true">{</mo>
        <mtable columnalign="left left" rowspacing="0.2em">
          <mtr><mtd><mn>100</mn></mtd><mtd><mrow><mi>E</mi><mo>=</mo><mn>1</mn><mo>∧</mo><mi>Δ</mi><mo>≤</mo><mn>60</mn></mrow></mtd></mtr>
          <mtr><mtd><mn>80</mn></mtd><mtd><mrow><mi>E</mi><mo>=</mo><mn>1</mn><mo>∧</mo><mn>60</mn><mo>&lt;</mo><mi>Δ</mi><mo>≤</mo><mn>1440</mn></mrow></mtd></mtr>
          <mtr><mtd><mn>50</mn></mtd><mtd><mrow><mi>E</mi><mo>=</mo><mn>1</mn><mo>∧</mo><mi>Δ</mi><mo>&gt;</mo><mn>1440</mn></mrow></mtd></mtr>
          <mtr><mtd><mn>0</mn></mtd><mtd><mrow><mi>E</mi><mo>=</mo><mn>0</mn></mrow></mtd></mtr>
        </mtable></mrow></math>""",
    ],
    74: [
        """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>
        <mn>0.30</mn><mo>+</mo><mn>0.25</mn><mo>+</mo><mn>0.20</mn><mo>+</mo><mn>0.15</mn><mo>+</mo><mn>0.10</mn><mo>=</mo><mn>1.00</mn>
        </mrow></math>""",
        """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>
        <mi mathvariant="normal">SACI</mi><mo>=</mo><mfrac><mrow><mn>1.00</mn><mo>×</mo><mn>100</mn></mrow><mn>1.00</mn></mfrac><mo>=</mo><mn>100.0</mn>
        </mrow></math>""",
    ],
}

MATH_DESCRIPTIONS = {
    "tr-TR": {
        37: "Gözlem durumu ve kaynak ağırlığı log kaynağı düzeyinde tanımlanır; varlık görünürlüğü kritikliğiyle ağırlıklandırılır.",
        38: "Yalnızca etkin kontroller pay ve paydaya girer; disabled legacy kontroller CAC paydasından çıkarılır.",
        39: "MDC, beyan edilmiş kapsam içindeki tekniklerin sayısal kapanışıdır; yayımlanan priority alanı skor ağırlığı olarak kullanılmaz.",
        40: "Bayraklar sırasıyla lookup icrası, MISP eşleşmesi, Wazuh alarmı ve ATT&CK eşlemesidir. Lookup bayrağının beklenti alanından başlatılması bağımsız sorgu-icrası kanıtı değildir.",
        41: "E en az bir olayın varlığını, Δ ise skor zamanı ile tüm kaynaklar içindeki en yeni olay arasındaki dakika farkını gösterir. TF kaynak başına tazelik ölçmez.",
    },
    "en-US": {
        37: "Observation state and source weight are defined at log-source level; asset visibility is weighted by criticality.",
        38: "Only enabled controls enter the numerator and denominator; disabled legacy controls are excluded from CAC.",
        39: "MDC is the count-based closure of declared in-scope techniques; the published priority field is not used as a score weight.",
        40: "The flags represent lookup execution, MISP hit, Wazuh alert, and ATT&CK mapping. Initializing the lookup flag from an expectation field is not independent proof of query execution.",
        41: "E denotes the existence of at least one event, and Δ is the age in minutes of the newest event across all sources at scoring time. TF does not measure per-source freshness.",
    },
}


def qn(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def clone_first_run_properties(paragraph: etree._Element) -> etree._Element:
    first_run = paragraph.find(qn(W, "r"))
    if first_run is not None:
        rpr = first_run.find(qn(W, "rPr"))
        if rpr is not None:
            return deepcopy(rpr)
    return etree.Element(qn(W, "rPr"))


def set_toggle(rpr: etree._Element, tag: str, value: bool) -> None:
    node = rpr.find(qn(W, tag))
    if value:
        if node is None:
            node = etree.SubElement(rpr, qn(W, tag))
        node.set(qn(W, "val"), "1")
    elif node is not None:
        rpr.remove(node)


def set_language(rpr: etree._Element, language: str) -> None:
    lang = rpr.find(qn(W, "lang"))
    if lang is None:
        lang = etree.SubElement(rpr, qn(W, "lang"))
    lang.set(qn(W, "val"), language)
    lang.set(qn(W, "eastAsia"), language)


def append_text(run: etree._Element, text: str) -> None:
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if index:
            etree.SubElement(run, qn(W, "br"))
        text_node = etree.SubElement(run, qn(W, "t"))
        if line.startswith(" ") or line.endswith(" "):
            text_node.set(qn(XML, "space"), "preserve")
        text_node.text = line


def clear_paragraph_content(paragraph: etree._Element) -> None:
    for child in list(paragraph):
        if child.tag != qn(W, "pPr"):
            paragraph.remove(child)


def add_run(paragraph: etree._Element, text: str, rpr: etree._Element) -> etree._Element:
    run = etree.SubElement(paragraph, qn(W, "r"))
    run.append(rpr)
    append_text(run, text)
    return run


def replace_paragraph(paragraph: etree._Element, text: str, language: str) -> None:
    rpr = clone_first_run_properties(paragraph)
    set_language(rpr, language)
    clear_paragraph_content(paragraph)
    add_run(paragraph, text, rpr)


def replace_labeled_paragraph(
    paragraph: etree._Element,
    label: str,
    body: str,
    language: str,
) -> None:
    base_rpr = clone_first_run_properties(paragraph)
    clear_paragraph_content(paragraph)

    label_rpr = deepcopy(base_rpr)
    set_language(label_rpr, language)
    set_toggle(label_rpr, "b", True)
    add_run(paragraph, label, label_rpr)

    body_rpr = deepcopy(base_rpr)
    set_language(body_rpr, language)
    set_toggle(body_rpr, "b", False)
    add_run(paragraph, body, body_rpr)


def mathml_to_inline_omml(mathml: str, language: str) -> etree._Element:
    result = MATH_XSLT(etree.fromstring(mathml.encode("utf-8")))
    root = result.getroot()
    if root is None:
        raise ValueError("MathML conversion produced no root element")
    if root.tag == qn(M, "oMathPara"):
        root = root.find(qn(M, "oMath"))
    elif root.tag != qn(M, "oMath"):
        root = root.find(".//" + qn(M, "oMath"))
    if root is None or root.tag != qn(M, "oMath"):
        raise ValueError("MathML conversion did not produce inline OMML")
    node = deepcopy(root)

    for math_run in node.xpath(".//m:r", namespaces=NS):
        word_rpr = math_run.find(qn(W, "rPr"))
        if word_rpr is None:
            word_rpr = etree.Element(qn(W, "rPr"))
            math_text = math_run.find(qn(M, "t"))
            insert_at = math_run.index(math_text) if math_text is not None else len(math_run)
            math_run.insert(insert_at, word_rpr)
        for tag in ("sz", "szCs"):
            size = word_rpr.find(qn(W, tag))
            if size is None:
                size = etree.SubElement(word_rpr, qn(W, tag))
            size.set(qn(W, "val"), "20")
        set_language(word_rpr, language)
    return node


def add_line_break(paragraph: etree._Element, rpr: etree._Element) -> None:
    run = etree.SubElement(paragraph, qn(W, "r"))
    run.append(deepcopy(rpr))
    etree.SubElement(run, qn(W, "br"))


def replace_math_paragraph(
    paragraph: etree._Element,
    formulas: list[str],
    language: str,
    description: str | None = None,
) -> None:
    regular_rpr = clone_first_run_properties(paragraph)
    set_toggle(regular_rpr, "b", False)
    set_language(regular_rpr, language)
    clear_paragraph_content(paragraph)

    for index, formula in enumerate(formulas):
        if index:
            add_line_break(paragraph, regular_rpr)
        paragraph.append(mathml_to_inline_omml(formula, language))
    if description:
        add_line_break(paragraph, regular_rpr)
        add_run(paragraph, description, deepcopy(regular_rpr))


def insert_manual_page_break(paragraph: etree._Element) -> None:
    ppr = paragraph.find(qn(W, "pPr"))
    if ppr is not None:
        page_break_before = ppr.find(qn(W, "pageBreakBefore"))
        if page_break_before is not None:
            ppr.remove(page_break_before)
    run = etree.Element(qn(W, "r"))
    page_break = etree.SubElement(run, qn(W, "br"))
    page_break.set(qn(W, "type"), "page")
    paragraph.insert(1 if ppr is not None else 0, run)


def set_all_text_run_languages(document_root: etree._Element, language: str) -> None:
    for run in document_root.xpath(".//w:r[w:t]", namespaces=NS):
        rpr = run.find(qn(W, "rPr"))
        if rpr is None:
            rpr = etree.Element(qn(W, "rPr"))
            run.insert(0, rpr)
        set_language(rpr, language)


def patch_core_properties(payload: bytes, *, title: str, language: str, keywords: str) -> bytes:
    root = etree.fromstring(payload)
    namespaces = {
        "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
    }

    def set_value(prefix: str, name: str, value: str) -> None:
        namespace = namespaces[prefix]
        element = root.find(qn(namespace, name))
        if element is None:
            element = etree.SubElement(root, qn(namespace, name))
        element.text = value

    set_value("dc", "title", title)
    set_value("dc", "subject", "SACI graph-based SIEM visibility scoring")
    set_value("dc", "creator", "Ismet Arslan")
    set_value("cp", "lastModifiedBy", "Ismet Arslan")
    set_value("cp", "keywords", keywords)
    set_value("dc", "description", "Final IDAP'26 manuscript synchronized with the SACI evidence package.")
    set_value("dc", "language", language)
    modified = root.find(qn(namespaces["dcterms"], "modified"))
    if modified is not None:
        modified.text = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def relationship_target(rels_payload: bytes, relationship_id: str) -> str:
    root = etree.fromstring(rels_payload)
    for rel in root.findall(qn(PR, "Relationship")):
        if rel.get("Id") == relationship_id:
            target = rel.get("Target")
            if not target:
                break
            return str(Path("word") / target).replace("\\", "/")
    raise ValueError(f"Relationship not found: {relationship_id}")


def build_one(
    *,
    source: Path,
    expected_source_hash: str,
    output: Path,
    content: dict[int, str],
    extra_after_metrics: list[tuple[int, str]],
    extra_after_lab: list[tuple[int, str]],
    extra_before_conclusion: list[tuple[int, str]],
    additional_references: list[str],
    language: str,
    abstract_label: str,
    keyword_label: str,
    figure: Path,
    figure_alt: str,
) -> None:
    source_payload = source.read_bytes()
    if sha256(source_payload) != expected_source_hash:
        raise ValueError(f"Source hash mismatch: {source}")

    with zipfile.ZipFile(source) as archive:
        infos = archive.infolist()
        parts = {info.filename: archive.read(info.filename) for info in infos}

    document_root = etree.fromstring(parts["word/document.xml"])
    body = document_root.find(qn(W, "body"))
    if body is None:
        raise ValueError("word/document.xml has no body")
    paragraphs = body.findall(qn(W, "p"))
    if len(paragraphs) != 102:
        raise ValueError(f"Expected 102 top-level paragraphs, found {len(paragraphs)}")

    for index, text in sorted(content.items()):
        if index in {2, 23}:
            raise ValueError(f"Protected template slot requested for replacement: {index}")
        if index == 3:
            replace_labeled_paragraph(paragraphs[index], abstract_label, text, language)
        elif index == 4:
            replace_labeled_paragraph(paragraphs[index], keyword_label, text, language)
        else:
            replace_paragraph(paragraphs[index], text, language)

    for paragraph_index, formulas in MATHML_BLOCKS.items():
        replace_math_paragraph(
            paragraphs[paragraph_index],
            formulas,
            language,
            MATH_DESCRIPTIONS.get(language, {}).get(paragraph_index),
        )

    insertion_anchor = paragraphs[41]
    for template_index, text in extra_after_metrics:
        inserted = deepcopy(paragraphs[template_index])
        replace_paragraph(inserted, text, language)
        insertion_anchor.addnext(inserted)
        insertion_anchor = inserted

    insertion_anchor = paragraphs[66]
    for template_index, text in extra_after_lab:
        inserted = deepcopy(paragraphs[template_index])
        replace_paragraph(inserted, text, language)
        insertion_anchor.addnext(inserted)
        insertion_anchor = inserted

    insertion_anchor = paragraphs[83]
    for template_index, text in extra_before_conclusion:
        inserted = deepcopy(paragraphs[template_index])
        replace_paragraph(inserted, text, language)
        insertion_anchor.addnext(inserted)
        insertion_anchor = inserted

    # IDAP'26 requires at least four manuscript pages excluding references.
    # The English manuscript has room for a clean dedicated reference page.
    # In Turkish, a forced break strands the short availability section on an
    # otherwise blank page, so references continue in the normal column flow.
    if language == "en-US":
        insert_manual_page_break(paragraphs[89])

    reference_anchor = paragraphs[101]
    for reference in additional_references:
        appended_reference = deepcopy(paragraphs[101])
        reference_anchor.addnext(appended_reference)
        replace_paragraph(appended_reference, reference, language)
        reference_anchor = appended_reference

    figure_paragraph = paragraphs[23]
    blip = figure_paragraph.find(".//" + qn(A, "blip"))
    if blip is None:
        raise ValueError("Figure relationship not found in paragraph 23")
    image_rel_id = blip.get(qn(R, "embed"))
    if not image_rel_id:
        raise ValueError("Figure embed relationship is missing")
    figure_part = relationship_target(parts["word/_rels/document.xml.rels"], image_rel_id)

    doc_pr = figure_paragraph.find(".//" + qn(WP, "docPr"))
    if doc_pr is not None:
        doc_pr.set("title", "SACI evidence pipeline")
        doc_pr.set("descr", figure_alt)

    set_all_text_run_languages(document_root, language)
    parts["word/document.xml"] = etree.tostring(
        document_root, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    parts[figure_part] = figure.read_bytes()
    parts["docProps/core.xml"] = patch_core_properties(
        parts["docProps/core.xml"],
        title=content[0],
        language=language,
        keywords=content[4],
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        for info in infos:
            archive.writestr(info, parts[info.filename])

    with zipfile.ZipFile(output) as archive:
        bad_part = archive.testzip()
        if bad_part:
            raise ValueError(f"Corrupt output part: {bad_part}")
        output_parts = {name: archive.read(name) for name in archive.namelist()}

    allowed = {"word/document.xml", "docProps/core.xml", figure_part}
    changed = {
        name
        for name in parts
        if name in output_parts and sha256(parts[name]) != sha256(output_parts[name])
    }
    # `parts` already contains the planned mutations. Compare source payloads instead.
    with zipfile.ZipFile(source) as archive:
        source_parts = {name: archive.read(name) for name in archive.namelist()}
    changed = {
        name
        for name in source_parts
        if sha256(source_parts[name]) != sha256(output_parts[name])
    }
    unexpected = changed - allowed
    if unexpected:
        raise ValueError(f"Unexpected package-part changes: {sorted(unexpected)}")
    if changed != allowed:
        raise ValueError(f"Expected changed parts {sorted(allowed)}, got {sorted(changed)}")

    visible_text = "\n".join(
        "".join(node.itertext()) for node in body.findall(qn(W, "p"))
    )
    forbidden = (
        "66.3",
        "66,3",
        "[University",
        "[Üniversite",
        "research draft",
        "araştırma taslağı",
        "final-v2",
        "SACI v2",
        "w_as",
        "o_as",
        "T_scope",
    )
    leftovers = [token for token in forbidden if token.casefold() in visible_text.casefold()]
    if leftovers:
        raise ValueError(f"Obsolete or placeholder text remains: {leftovers}")

    print(f"Built {output.name}; changed parts: {', '.join(sorted(changed))}")


def main() -> None:
    build_one(
        source=Path(r"E:\Downloads\IDAP26_SIEM_Graph_Attack_Surface_TR.docx"),
        expected_source_hash="cf2bd7d46d3a536c354b060d330d64fdd43d535c45f3d313833ea5036663be86",
        output=DELIVERABLES / "IDAP26_SACI_Graph_Attack_Surface_Final_TR.docx",
        content=TR,
        extra_after_metrics=TR_AFTER_METRICS,
        extra_after_lab=TR_AFTER_LAB_SECTION,
        extra_before_conclusion=TR_BEFORE_CONCLUSION,
        additional_references=TR_ADDITIONAL_REFERENCES,
        language="tr-TR",
        abstract_label="Özet—",
        keyword_label="Anahtar Kelimeler—",
        figure=WORK / "pipeline_tr.png",
        figure_alt="SACI kapsam ve gözlenen kanıtının tiplenmiş grafa, beş bileşenli skora ve denetlenebilir araştırma çıktılarına akışını gösteren diyagram.",
    )
    build_one(
        source=Path(r"E:\Downloads\IDAP26_SIEM_Graph_Attack_Surface_Draft.docx"),
        expected_source_hash="3e93767ff89e40dd93c738e0c4ef17d268d370f2ae55585cd0d625b11e40b02c",
        output=DELIVERABLES / "IDAP26_SACI_Graph_Attack_Surface_Final_EN.docx",
        content=EN,
        extra_after_metrics=EN_AFTER_METRICS,
        extra_after_lab=EN_AFTER_LAB_SECTION,
        extra_before_conclusion=EN_BEFORE_CONCLUSION,
        additional_references=EN_ADDITIONAL_REFERENCES,
        language="en-US",
        abstract_label="Abstract—",
        keyword_label="Keywords—",
        figure=WORK / "pipeline_en.png",
        figure_alt="Diagram showing the flow of SACI scope and observed evidence into a typed graph, five-component score, and auditable research outputs.",
    )


if __name__ == "__main__":
    main()
