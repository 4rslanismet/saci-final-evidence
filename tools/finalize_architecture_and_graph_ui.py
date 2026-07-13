#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / "docs"

FILES = [
    DOCS / "architecture.html",
    DOCS / "en" / "architecture.html",
    DOCS / "graph.html",
    DOCS / "en" / "graph.html",
    DOCS / "data" / "scenarios" / "manifest.json",
    DOCS / "en" / "data" / "scenarios" / "manifest.json",
]

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "backups" / f"final_ui_cleanup_{STAMP}"

UI_CSS = r'''
<!-- SACI_FINAL_UI_START -->
<style id="saci-final-ui">
  /*
   * Final publication UI cleanup
   * Uses the site's global theme variables.
   */

  body[data-page="graph"] .graph-hero .lead,
  body[data-page="architecture"] .lead,
  body[data-page="architecture"] .hero-copy,
  body[data-page="architecture"] .architecture-intro,
  body[data-page="architecture"] main > section > p {
    max-width: 76ch !important;
    line-height: 1.78 !important;
  }

  body[data-page="architecture"] .architecture-scope-note,
  body[data-page="graph"] .graph-scope-note {
    max-width: 76ch;
    margin-top: 20px;
    padding-left: 15px;
    border-left: 2px solid
      color-mix(in srgb, var(--accent) 54%, transparent);
    color: var(--muted);
    font-size: 14.5px;
    line-height: 1.72;
  }

  body[data-page="architecture"] h1 {
    max-width: 18ch !important;
  }

  body[data-page="architecture"] h2 {
    margin-top: clamp(44px, 6vw, 76px) !important;
  }

  body[data-page="architecture"] .figure-shell,
  body[data-page="architecture"] .architecture-figure {
    margin-top: 18px !important;
  }

  /*
   * Graph analysis cards should size according to their own content.
   * Previously the shorter card inherited the height of the MITRE panel.
   */
  body[data-page="graph"] .graph-analysis {
    align-items: start !important;
  }

  body[data-page="graph"] .analysis-panel {
    align-self: start !important;
    min-height: 0 !important;
    height: auto !important;
  }

  body[data-page="graph"] #interpretation {
    display: block !important;
  }

  body[data-page="graph"] .interpretation-text {
    max-width: none !important;
    font-size: 15.5px !important;
    line-height: 1.74 !important;
  }

  body[data-page="graph"] .saci-expanded-interpretation {
    margin-top: 14px;
    display: grid;
    gap: 12px;
  }

  body[data-page="graph"] .saci-explanation-block {
    padding: 14px 15px;
    border: 1px solid
      color-mix(in srgb, var(--line) 58%, transparent);
    border-radius: 14px;
    background:
      color-mix(
        in srgb,
        var(--surface, var(--bg)) 82%,
        transparent
      );
  }

  body[data-page="graph"] .saci-explanation-block h4 {
    margin: 0 0 9px;
    color: var(--text);
    font-size: 15px;
    font-weight: 700;
  }

  body[data-page="graph"] .saci-explanation-block p {
    max-width: 78ch !important;
    margin: 0 0 10px;
    color: var(--muted);
    font-size: 14.5px !important;
    line-height: 1.7 !important;
  }

  body[data-page="graph"] .saci-explanation-block p:last-child {
    margin-bottom: 0;
  }

  body[data-page="graph"] .saci-result-list {
    display: grid;
    grid-template-columns:
      repeat(auto-fit, minmax(170px, 1fr));
    gap: 8px;
    margin: 11px 0 0;
    padding: 0;
    list-style: none;
  }

  body[data-page="graph"] .saci-result-list li {
    padding: 10px 11px;
    border: 1px solid
      color-mix(in srgb, var(--line) 52%, transparent);
    border-radius: 12px;
    background:
      color-mix(
        in srgb,
        var(--bg) 78%,
        transparent
      );
  }

  body[data-page="graph"] .saci-result-list span {
    display: block;
    margin-bottom: 4px;
    color: var(--muted);
    font-size: 11.5px;
    font-weight: 650;
  }

  body[data-page="graph"] .saci-result-list strong {
    display: block;
    color: var(--text);
    font-size: 18px;
    font-weight: 700;
  }

  body[data-page="graph"] .saci-policy-explanation {
    margin-top: 14px;
    border: 1px solid
      color-mix(in srgb, var(--line) 62%, transparent);
    border-radius: 14px;
    overflow: hidden;
    background:
      color-mix(
        in srgb,
        var(--surface, var(--bg)) 76%,
        transparent
      );
  }

  body[data-page="graph"] .saci-policy-explanation summary {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 13px 15px;
    color: var(--text);
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    list-style: none;
  }

  body[data-page="graph"]
  .saci-policy-explanation summary::-webkit-details-marker {
    display: none;
  }

  body[data-page="graph"] .saci-policy-explanation summary::before {
    content: "›";
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border: 1px solid
      color-mix(in srgb, var(--accent) 42%, var(--line));
    border-radius: 50%;
    color: var(--accent);
    transition: transform .16s ease;
  }

  body[data-page="graph"]
  .saci-policy-explanation[open] summary::before {
    transform: rotate(90deg);
  }

  body[data-page="graph"] .saci-policy-body {
    padding: 0 15px 15px;
  }

  body[data-page="graph"] .saci-policy-body p {
    max-width: 78ch !important;
    margin: 0 0 10px;
    color: var(--muted);
    font-size: 14.5px !important;
    line-height: 1.7 !important;
  }

  body[data-page="graph"] .saci-policy-note {
    padding: 10px 12px;
    border-left: 2px solid var(--accent);
    background:
      color-mix(
        in srgb,
        var(--accent) 6%,
        transparent
      );
    color: var(--muted);
    font-size: 13px;
    line-height: 1.62;
  }

  @media (max-width: 760px) {
    body[data-page="graph"] .saci-result-list {
      grid-template-columns: 1fr 1fr;
    }
  }

  @media (max-width: 480px) {
    body[data-page="graph"] .saci-result-list {
      grid-template-columns: 1fr;
    }
  }
</style>
<!-- SACI_FINAL_UI_END -->
'''

GRAPH_ENHANCER_JS = r'''
<!-- SACI_GRAPH_EXPLANATION_START -->
<script id="saci-graph-explanation">
(() => {
  const isEnglish = () =>
    (document.documentElement.lang || "")
      .toLowerCase()
      .startsWith("en");

  function text(id) {
    const node = document.getElementById(id);
    return node ? node.textContent.trim() : "-";
  }

  function cleanVisibleFinalNames(root = document) {
    const walker = document.createTreeWalker(
      root,
      NodeFilter.SHOW_TEXT
    );

    const nodes = [];

    while (walker.nextNode()) {
      nodes.push(walker.currentNode);
    }

    nodes.forEach((node) => {
      const parent = node.parentElement;

      if (!parent) return;

      if (
        ["SCRIPT", "STYLE", "CODE", "PRE"].includes(parent.tagName)
      ) {
        return;
      }

      let value = node.nodeValue;

      value = value
        .replace(
          /final-v2\s*[—-]\s*Kanonik yayın anlık görüntüsü/gi,
          "Final — Kanonik yayın anlık görüntüsü"
        )
        .replace(
          /final-v2\s*[—-]\s*Canonical publication snapshot/gi,
          "Final — Canonical publication snapshot"
        )
        .replace(
          /final-v2 canonical publication snapshot/gi,
          "Canonical publication snapshot"
        )
        .replace(
          /kanonik final-v2 görünümünde/gi,
          "Kanonik final görünümünde"
        )
        .replace(
          /canonical final-v2 view/gi,
          "canonical final view"
        );

      if (value !== node.nodeValue) {
        node.nodeValue = value;
      }
    });
  }

  function buildExpandedInterpretation() {
    const host = document.getElementById("interpretation");

    if (!host) return;

    if (host.querySelector(".saci-expanded-interpretation")) {
      return;
    }

    const en = isEnglish();

    const declared = text("declaredNodeCount");
    const rendered = text("nodeCount");
    const edges = text("edgeCount");
    const observed = text("observedCount");
    const missing = text("missingCount");
    const saci = text("saciScore");

    if (
      [declared, rendered, edges, observed, missing]
        .every((value) => value === "-" || value === "")
    ) {
      return;
    }

    const mitreItems = document.querySelectorAll(
      ".tech-item, .mitre-technique, [data-technique-id]"
    ).length;

    const expanded = document.createElement("div");
    expanded.className = "saci-expanded-interpretation";

    expanded.innerHTML = en
      ? `
        <section class="saci-explanation-block">
          <h4>Evidence-chain interpretation</h4>

          <p>
            This graph represents the publication-level SACI evidence
            structure. Assets, log sources, detection controls, Wazuh
            rules, MITRE ATT&amp;CK techniques, CTI objects, platforms,
            metrics and reason codes are evaluated as connected evidence
            rather than as isolated counters.
          </p>

          <p>
            The selected final dataset contains
            <strong>${declared}</strong> declared nodes,
            <strong>${rendered}</strong> rendered nodes and
            <strong>${edges}</strong> relations.
            Of these relations, <strong>${observed}</strong> are observed
            and <strong>${missing}</strong> are missing.
          </p>

          <p>
            A complete result means that the visibility relations declared
            for the evaluation scope can be traced through the graph. It
            does not mean that the monitored environment is absolutely
            secure or that every unknown attack-surface element has been
            discovered.
          </p>

          <ul class="saci-result-list">
            <li>
              <span>Declared nodes</span>
              <strong>${declared}</strong>
            </li>
            <li>
              <span>Rendered nodes</span>
              <strong>${rendered}</strong>
            </li>
            <li>
              <span>Total relations</span>
              <strong>${edges}</strong>
            </li>
            <li>
              <span>Observed relations</span>
              <strong>${observed}</strong>
            </li>
            <li>
              <span>Missing relations</span>
              <strong>${missing}</strong>
            </li>
            <li>
              <span>SACI</span>
              <strong>${saci}</strong>
            </li>
          </ul>
        </section>

        <details class="saci-policy-explanation">
          <summary>Policy-guided explanation layer</summary>

          <div class="saci-policy-body">
            <p>
              The explanation layer translates deterministic SACI outputs
              into a readable operational summary. It interprets score
              components, graph completeness, missing visibility
              relations, MITRE coverage, CTI closure and telemetry
              freshness.
            </p>

            <p>
              In this final view, the evidence chain indicates that the
              declared telemetry, detection, ATT&amp;CK and CTI relations
              required by the evaluation scope are available for
              inspection. Where the missing-relation count is zero, the
              result is interpreted as evidence closure within that scope.
            </p>

            <div class="saci-policy-note">
              This layer does not calculate, modify or override the SACI
              score. It only converts deterministic results into natural
              language. Any future LLM implementation must receive
              structured SACI outputs and reason codes rather than infer
              the score independently.
            </div>
          </div>
        </details>
      `
      : `
        <section class="saci-explanation-block">
          <h4>Kanıt zinciri yorumu</h4>

          <p>
            Bu graph, SACI modelinin yayına esas kanıt yapısını temsil
            eder. Varlıklar, log kaynakları, detection kontrolleri, Wazuh
            kuralları, MITRE ATT&amp;CK teknikleri, CTI nesneleri,
            platformlar, metrikler ve reason code düğümleri birbirinden
            bağımsız sayaçlar olarak değil, bağlantılı kanıtlar olarak
            değerlendirilir.
          </p>

          <p>
            Seçili final veri kümesinde
            <strong>${declared}</strong> beyan edilmiş node,
            <strong>${rendered}</strong> gösterilen node ve
            <strong>${edges}</strong> ilişki bulunmaktadır.
            Bu ilişkilerin <strong>${observed}</strong> tanesi gözlemlenmiş,
            <strong>${missing}</strong> tanesi eksik durumdadır.
          </p>

          <p>
            Tam kapanış sonucu, değerlendirme kapsamında beyan edilen
            görünürlük ilişkilerinin graph üzerinden izlenebildiğini
            gösterir. Bu sonuç, izlenen ortamın mutlak olarak güvenli
            olduğu veya bilinmeyen bütün saldırı yüzeyi unsurlarının
            keşfedildiği anlamına gelmez.
          </p>

          <ul class="saci-result-list">
            <li>
              <span>Beyan edilen node</span>
              <strong>${declared}</strong>
            </li>
            <li>
              <span>Gösterilen node</span>
              <strong>${rendered}</strong>
            </li>
            <li>
              <span>Toplam ilişki</span>
              <strong>${edges}</strong>
            </li>
            <li>
              <span>Gözlemlenen ilişki</span>
              <strong>${observed}</strong>
            </li>
            <li>
              <span>Eksik ilişki</span>
              <strong>${missing}</strong>
            </li>
            <li>
              <span>SACI</span>
              <strong>${saci}</strong>
            </li>
          </ul>
        </section>

        <details class="saci-policy-explanation">
          <summary>Politika yönlendirmeli açıklama katmanı</summary>

          <div class="saci-policy-body">
            <p>
              Açıklama katmanı, deterministik SACI çıktılarını okunabilir
              bir operasyonel özete dönüştürür. Skor bileşenlerini, graph
              completeness değerini, eksik görünürlük ilişkilerini, MITRE
              kapsamını, CTI kapanışını ve telemetri güncelliğini yorumlar.
            </p>

            <p>
              Bu final görünümde kanıt zinciri, değerlendirme kapsamında
              gerekli görülen telemetri, detection, ATT&amp;CK ve CTI
              ilişkilerinin incelenebilir olduğunu göstermektedir. Eksik
              ilişki sayısının sıfır olduğu durumda sonuç, tanımlı kapsam
              içinde kanıt kapanışı olarak yorumlanır.
            </p>

            <div class="saci-policy-note">
              Bu katman SACI skorunu hesaplamaz, değiştirmez veya geçersiz
              kılmaz. Yalnızca deterministik çıktıları doğal dile
              dönüştürür. Gelecekte kullanılacak LLM, skoru kendisi
              tahmin etmek yerine yapılandırılmış SACI çıktılarını ve
              reason code kayıtlarını girdi olarak almalıdır.
            </div>
          </div>
        </details>
      `;

    host.appendChild(expanded);
  }

  let queued = false;

  function refresh() {
    if (queued) return;

    queued = true;

    requestAnimationFrame(() => {
      queued = false;

      cleanVisibleFinalNames();
      buildExpandedInterpretation();
    });
  }

  function init() {
    refresh();

    const observer = new MutationObserver(refresh);

    observer.observe(document.body, {
      subtree: true,
      childList: true,
      characterData: true
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>
<!-- SACI_GRAPH_EXPLANATION_END -->
'''

ARCH_TR_INTRO = '''
<div class="architecture-final-intro">
  <p>
    Bu sayfa, SACI değerlendirmesinde kullanılan kontrollü laboratuvar
    mimarisini ve verinin uçtan uca nasıl aktığını açıklar. Amaç,
    telemetri kaynaklarından başlayarak Wazuh toplama ve detection
    katmanına, oradan MITRE / CTI bağlamına, SACI skorlamasına ve son
    olarak evidence graph çıktısına uzanan ilişkiyi sade ve izlenebilir
    biçimde göstermektir.
  </p>

  <p>
    Gösterilen mimari; Windows, Linux, pfSense ve MISP kaynaklarından
    üretilen verinin nasıl toplandığını, normalize edildiğini, detection
    mantığıyla işlendiğini ve graph tabanlı görünürlük modeline nasıl
    dönüştürüldüğünü açıklar. Böylece yalnızca hangi araçların kullanıldığı
    değil, hangi verinin hangi kanıt ilişkisini beslediği de görülebilir.
  </p>

  <p class="architecture-scope-note">
    Kapsam notu: Portalda final yayın görünümü ile S0–S18 tarihsel senaryo
    serisi ayrı tutulur. Final görünüm yayına esas değerlendirme sonucunu;
    tarihsel senaryolar ise metodolojik doğrulama ve değişim analizini
    temsil eder.
  </p>
</div>
'''

ARCH_EN_INTRO = '''
<div class="architecture-final-intro">
  <p>
    This page explains the controlled laboratory architecture used in
    SACI and how data flows end to end through the model. The objective
    is to show, in a clear and traceable form, how telemetry sources feed
    the Wazuh collection and detection layer, how MITRE / CTI context is
    attached, and how the result is transformed into SACI scoring and
    evidence-graph output.
  </p>

  <p>
    The architecture illustrates how data produced by Windows, Linux,
    pfSense and MISP is collected, normalized, processed through
    detection logic and converted into a graph-based visibility model.
    This makes it possible to understand not only which tools are used,
    but also which evidence relation is supported by each data source.
  </p>

  <p class="architecture-scope-note">
    Scope note: the portal keeps the final publication view separate from
    the S0–S18 historical scenario series. The final view represents the
    publication-level evaluation result, while the historical scenarios
    support methodological validation and change analysis.
  </p>
</div>
'''


def backup(path: Path) -> None:
    if not path.exists():
        return

    target = BACKUP / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def remove_injected_blocks(html: str) -> str:
    html = re.sub(
        r"\s*<!-- SACI_FINAL_UI_START -->.*?"
        r"<!-- SACI_FINAL_UI_END -->\s*",
        "\n",
        html,
        flags=re.S,
    )

    html = re.sub(
        r"\s*<!-- SACI_GRAPH_EXPLANATION_START -->.*?"
        r"<!-- SACI_GRAPH_EXPLANATION_END -->\s*",
        "\n",
        html,
        flags=re.S,
    )

    return html


def add_css(html: str) -> str:
    html = remove_injected_blocks(html)

    if "</head>" not in html:
        raise RuntimeError("</head> bulunamadı.")

    return html.replace(
        "</head>",
        UI_CSS + "\n</head>",
        1,
    )


def patch_graph(path: Path) -> None:
    if not path.exists():
        print(f"[!] Bulunamadı: {path}")
        return

    html = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    html = add_css(html)

    if "</body>" not in html:
        raise RuntimeError(f"</body> bulunamadı: {path}")

    html = html.replace(
        "</body>",
        GRAPH_ENHANCER_JS + "\n</body>",
        1,
    )

    html = html.replace(
        "final-v2 — Kanonik yayın anlık görüntüsü",
        "Final — Kanonik yayın anlık görüntüsü",
    )

    html = html.replace(
        "final-v2 — Canonical publication snapshot",
        "Final — Canonical publication snapshot",
    )

    html = html.replace(
        "final-v2 canonical publication snapshot",
        "Canonical publication snapshot",
    )

    path.write_text(html, encoding="utf-8")
    print(f"[+] Graph güncellendi: {path}")


def replace_arch_intro(
    html: str,
    english: bool,
) -> str:
    html = re.sub(
        r'\s*<div class="architecture-final-intro">.*?</div>\s*',
        "\n",
        html,
        flags=re.S,
    )

    block = ARCH_EN_INTRO if english else ARCH_TR_INTRO

    h1_pattern = (
        r'(<h1[^>]*>\s*'
        + (
            r'Lab architecture and data flow'
            if english
            else r'Lab mimarisi ve veri akışı'
        )
        + r'\s*</h1>)'
    )

    match = re.search(
        h1_pattern,
        html,
        flags=re.I | re.S,
    )

    if not match:
        return html

    start = match.end()

    next_heading = re.search(
        r'<h2[^>]*>',
        html[start:],
        flags=re.I,
    )

    if not next_heading:
        return html[:start] + "\n" + block + html[start:]

    section_end = start + next_heading.start()

    segment = html[start:section_end]

    segment = re.sub(
        r'<p[^>]*>.*?</p>',
        '',
        segment,
        flags=re.S | re.I,
    )

    segment = re.sub(
        r'<div[^>]+class="[^"]*(?:lead|hero-copy)[^"]*"[^>]*>'
        r'.*?</div>',
        '',
        segment,
        flags=re.S | re.I,
    )

    return (
        html[:start]
        + "\n"
        + block
        + "\n"
        + segment
        + html[section_end:]
    )


def patch_architecture(
    path: Path,
    english: bool,
) -> None:
    if not path.exists():
        print(f"[!] Bulunamadı: {path}")
        return

    html = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    html = add_css(html)
    html = replace_arch_intro(html, english)

    html = html.replace(
        "final-v2",
        "final",
    )

    html = html.replace(
        "Final-v2",
        "Final",
    )

    path.write_text(html, encoding="utf-8")
    print(f"[+] Mimari güncellendi: {path}")


def patch_manifest(
    path: Path,
    english: bool,
) -> None:
    if not path.exists():
        print(f"[!] Manifest bulunamadı: {path}")
        return

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    records = (
        data.get("datasets")
        or data.get("scenarios")
        or []
    )

    for item in records:
        item_id = str(item.get("id", "")).lower()

        if item_id in {
            "final",
            "final_v2",
            "final-v2",
        }:
            if english:
                item["label_en"] = (
                    "Final — Canonical publication snapshot"
                )
                item["label"] = (
                    "Final — Canonical publication snapshot"
                )
                item["title"] = (
                    "Final — Canonical publication snapshot"
                )
            else:
                item["label_tr"] = (
                    "Final — Kanonik yayın anlık görüntüsü"
                )
                item["label"] = (
                    "Final — Kanonik yayın anlık görüntüsü"
                )
                item["title"] = (
                    "Final — Kanonik yayın anlık görüntüsü"
                )

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"[+] Manifest güncellendi: {path}")


for item in FILES:
    backup(item)

patch_architecture(
    DOCS / "architecture.html",
    english=False,
)

patch_architecture(
    DOCS / "en" / "architecture.html",
    english=True,
)

patch_graph(
    DOCS / "graph.html",
)

patch_graph(
    DOCS / "en" / "graph.html",
)

patch_manifest(
    DOCS / "data" / "scenarios" / "manifest.json",
    english=False,
)

patch_manifest(
    DOCS / "en" / "data" / "scenarios" / "manifest.json",
    english=True,
)

print()
print("=== FINAL UI CLEANUP COMPLETE ===")
print(f"Backup: {BACKUP}")
print()
print("Kullanıcı arayüzünde final-v2 yerine Final gösterilir.")
print("İç veri yolları ve teknik klasör adları değiştirilmedi.")
