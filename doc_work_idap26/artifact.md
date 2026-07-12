# IDAP'26 SACI article update contract

## References

- Turkish reference: `E:\Downloads\IDAP26_SIEM_Graph_Attack_Surface_TR.docx`
  - SHA-256: `cf2bd7d46d3a536c354b060d330d64fdd43d535c45f3d313833ea5036663be86`
  - Size: 127,269 bytes; 4 rendered pages; 2 sections.
  - Evidence: `evidence/tr_inventory.json`, `evidence/tr_style.json`, `tr_reference_render/`.
- English reference: `E:\Downloads\IDAP26_SIEM_Graph_Attack_Surface_Draft.docx`
  - SHA-256: `3e93767ff89e40dd93c738e0c4ef17d268d370f2ae55585cd0d625b11e40b02c`
  - Size: 88,132 bytes; 5 rendered pages; 2 sections.
  - Evidence: `evidence/draft_inventory.json`, `evidence/draft_style.json`, `draft_reference_render/`.
- The originals are retained read-only and must remain byte-identical.

## Page system

- A4 portrait, 8.2681 x 11.6931 in.
- Margins: left/right 0.6493 in, top 0.7479 in, bottom 1.0 in.
- Section 1: one column; Section 2: continuous break, two columns, 360 twip column spacing.
- No header/footer content, page-number fields, footnotes, endnotes, tables, or content controls.
- One inline pipeline figure in `word/document.xml`; source size is approximately 3.35 x 1.56 in (TR) and 3.05 x 1.45 in (EN).

## Typography and paragraph system

- Typeface throughout: Times New Roman.
- `paper title`: 24 pt, centered.
- `Author`: 10 pt, centered.
- `Body Text`: 10 pt, single spacing, 3 pt style space after; body paragraphs use source direct formatting and first-line indents.
- Abstract/keywords: 9 pt and 4 pt after; the source uses bold direct formatting.
- `Heading 1`: 10 pt bold, centered, 6 pt before/3 pt after, keep with next.
- `Heading 2`: 10 pt bold, left, 6 pt before/3 pt after, keep with next.
- Figure caption: 8 pt italic, centered.
- Display equations: 9 pt, centered.
- Result-list items: 9 pt bold, 0.12 in left indent, 2 pt after.
- References: 8 pt, 0.18 in hanging indent, 2 pt after.

## Content flow and slot map

- Paragraph 0: title; rewrite to include SACI.
- Paragraph 1: author block; retain `İsmet/Ismet Arslan`, remove bracketed affiliation/contact placeholders rather than inventing metadata.
- Paragraph 2: preserved blank separator and continuous two-column section boundary.
- Paragraphs 3-4: final abstract and keywords.
- Paragraphs 5-20: Introduction and Related Work; preserve hierarchy, update contribution and evidence language.
- Paragraphs 21-52: Proposed Model; rewrite metric definitions and equations to match `saci_score_v2.py` exactly. Preserve figure at paragraph 23 and caption role at paragraph 24.
- Paragraphs 53-66: controlled final-v2 laboratory design and data pipeline.
- Paragraphs 67-77: final results, interpretation boundary, graph-integrity disclosure, and historical scenario sensitivity.
- Paragraphs 78-80: limitations and threats to validity.
- Paragraphs 81-83: implementation and auditability boundary.
- Paragraphs 84-86: conclusion.
- Paragraphs 87-88: replace draft acknowledgment with Data and Artifact Availability.
- Paragraph 89: References heading.
- Paragraphs 90-101: preserve existing scholarly references.
- Append one source-derived paragraph after 101 for the SACI final-v2 research artifact and public evidence portal.

## Package preservation

- Full part-level size/SHA-256 inventories are recorded in `evidence/tr_inventory.json` and `evidence/draft_inventory.json`.
- Editable: text runs in `word/document.xml`, direct run formatting inside edited slots, core title/subject/keywords metadata, and one appended reference paragraph.
- Preserve-only: `[Content_Types].xml`, relationships except those already used by the document, `word/styles.xml`, `word/numbering.xml`, `word/settings.xml`, theme, font table, headers/footers, media files, section properties, drawing relationships, and all other opaque package parts.
- No source image replacement, section geometry change, new table, or alternate style system is permitted.

## Fidelity and publication gates

- Every final page must be rendered through Microsoft Word PDF export because LibreOffice is unavailable, then rasterized to PNG and inspected at 100%.
- Two-column geometry, title block, heading hierarchy, figure placement, reference hanging indents, and Times New Roman typography must remain source-derived.
- No clipping, overlap, orphaned heading, broken column flow, blank trailing page, bracketed placeholder, draft/preliminary claim, or stale `66.3/100` result may remain.
- Final-v2 and historical S8 are separate datasets: final-v2 is 97 declared nodes/171 edge rows; historical S8 is 95 nodes/173 edge rows.
- Claims must disclose two undeclared final-v2 edge endpoints, six isolated declared nodes, and rule 110203's cross-file technique inconsistency.
- The output/code bundle supports arithmetic and artifact auditability but does not independently replay unpublished upstream extraction or live Wazuh/MISP collection.
