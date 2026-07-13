#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import re
import shutil

ROOT = Path.cwd()

PAGES = [
    ROOT / "docs" / "graph.html",
    ROOT / "docs" / "en" / "graph.html",
]

CSS = r'''
<!-- SACI_STATUS_UI_START -->
<style id="saci-status-ui">
  body[data-page="graph"] .status-pill,
  body[data-page="graph"] .tech-status,
  body[data-page="graph"] .tech-state {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;

    min-height: 31px !important;
    padding: 0 11px !important;

    border-radius: 999px !important;
    border: 1px solid var(--border, var(--line)) !important;

    background: var(--surface, transparent) !important;
    background-image: none !important;

    color: var(--text) !important;

    font-size: 12px !important;
    font-weight: 700 !important;
    line-height: 1 !important;
    letter-spacing: 0.01em !important;
    text-transform: none !important;
    white-space: nowrap !important;

    text-shadow: none !important;
    box-shadow: none !important;
  }

  body[data-page="graph"] .status-pill::before,
  body[data-page="graph"] .tech-status::before,
  body[data-page="graph"] .tech-state::before {
    content: "" !important;

    width: 7px !important;
    height: 7px !important;
    flex: 0 0 7px !important;

    border-radius: 50% !important;
    background: currentColor !important;
    opacity: 0.9 !important;

    box-shadow:
      0 0 0 3px
      color-mix(in srgb, currentColor 12%, transparent) !important;
  }

  body[data-page="graph"] .status-pill.good,
  body[data-page="graph"] .tech-status.covered,
  body[data-page="graph"] .tech-state.covered {
    color: var(--green, #22c55e) !important;

    background:
      color-mix(
        in srgb,
        var(--green, #22c55e) 8%,
        var(--surface, transparent)
      ) !important;

    border-color:
      color-mix(
        in srgb,
        var(--green, #22c55e) 34%,
        var(--border, var(--line))
      ) !important;

    border-style: solid !important;
  }

  body[data-page="graph"] .status-pill.warn,
  body[data-page="graph"] .tech-status.missing,
  body[data-page="graph"] .tech-state.missing {
    color: var(--yellow, #eab308) !important;

    background:
      color-mix(
        in srgb,
        var(--yellow, #eab308) 8%,
        var(--surface, transparent)
      ) !important;

    background-image: none !important;

    border-color:
      color-mix(
        in srgb,
        var(--yellow, #eab308) 36%,
        var(--border, var(--line))
      ) !important;

    border-style: solid !important;
  }

  body[data-page="graph"] .status-pill.bad,
  body[data-page="graph"] .status-pill.danger {
    color: var(--red, #ef4444) !important;

    background:
      color-mix(
        in srgb,
        var(--red, #ef4444) 8%,
        var(--surface, transparent)
      ) !important;

    border-color:
      color-mix(
        in srgb,
        var(--red, #ef4444) 36%,
        var(--border, var(--line))
      ) !important;

    border-style: solid !important;
  }

  body[data-page="graph"] .status-pill:hover,
  body[data-page="graph"] .tech-status:hover,
  body[data-page="graph"] .tech-state:hover {
    filter: brightness(1.06);
  }

  html[data-theme="light"]
  body[data-page="graph"] .status-pill.good,
  html[data-theme="light"]
  body[data-page="graph"] .tech-status.covered,
  html[data-theme="light"]
  body[data-page="graph"] .tech-state.covered {
    background:
      color-mix(
        in srgb,
        var(--green, #15803d) 11%,
        var(--surface, #ffffff)
      ) !important;
  }

  html[data-theme="light"]
  body[data-page="graph"] .status-pill.warn,
  html[data-theme="light"]
  body[data-page="graph"] .tech-status.missing,
  html[data-theme="light"]
  body[data-page="graph"] .tech-state.missing {
    background:
      color-mix(
        in srgb,
        var(--yellow, #a16207) 12%,
        var(--surface, #ffffff)
      ) !important;
  }
</style>
<!-- SACI_STATUS_UI_END -->
'''

JS = r'''
<!-- SACI_STATUS_TEXT_START -->
<script id="saci-status-text">
(() => {
  const isEnglish = () =>
    (document.documentElement.lang || "")
      .toLowerCase()
      .startsWith("en");

  function changeText(selector, trText, enText) {
    const value = isEnglish() ? enText : trText;

    document.querySelectorAll(selector).forEach((node) => {
      if (node.textContent.trim() !== value) {
        node.textContent = value;
      }

      node.setAttribute("aria-label", value);
    });
  }

  function normalizeStatusLabels() {
    changeText(
      ".status-pill.good",
      "Kapanış tamam",
      "Closure complete"
    );

    changeText(
      ".status-pill.warn",
      "Kısmi kapsama",
      "Partial coverage"
    );

    changeText(
      ".status-pill.bad, .status-pill.danger",
      "Açık boşluk",
      "Open gap"
    );

    changeText(
      ".tech-status.covered, .tech-state.covered",
      "Kapsanıyor",
      "Covered"
    );

    changeText(
      ".tech-status.missing, .tech-state.missing",
      "Eksik",
      "Missing"
    );
  }

  let queued = false;

  function scheduleNormalize() {
    if (queued) return;

    queued = true;

    requestAnimationFrame(() => {
      queued = false;
      normalizeStatusLabels();
    });
  }

  function init() {
    normalizeStatusLabels();

    const observer = new MutationObserver(scheduleNormalize);

    observer.observe(document.body, {
      childList: true,
      subtree: true,
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
<!-- SACI_STATUS_TEXT_END -->
'''

def patch_html(html: str) -> str:
    html = re.sub(
        r"\s*<!-- SACI_STATUS_UI_START -->"
        r".*?"
        r"<!-- SACI_STATUS_UI_END -->\s*",
        "\n",
        html,
        flags=re.S,
    )

    html = re.sub(
        r"\s*<!-- SACI_STATUS_TEXT_START -->"
        r".*?"
        r"<!-- SACI_STATUS_TEXT_END -->\s*",
        "\n",
        html,
        flags=re.S,
    )

    if "</head>" not in html:
        raise RuntimeError("</head> etiketi bulunamadı.")

    if "</body>" not in html:
        raise RuntimeError("</body> etiketi bulunamadı.")

    html = html.replace(
        "</head>",
        CSS + "\n</head>",
        1,
    )

    html = html.replace(
        "</body>",
        JS + "\n</body>",
        1,
    )

    return html


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_root = ROOT / "backups" / f"graph_status_ui_{timestamp}"

updated = 0

for page in PAGES:
    if not page.exists():
        print(f"[!] Dosya bulunamadı: {page}")
        continue

    backup = backup_root / page.relative_to(ROOT)
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(page, backup)

    html = page.read_text(
        encoding="utf-8",
        errors="replace",
    )

    page.write_text(
        patch_html(html),
        encoding="utf-8",
    )

    updated += 1
    print(f"[+] Güncellendi: {page}")

print()
print(f"[+] Güncellenen sayfa sayısı: {updated}")
print(f"[+] Yedek klasörü: {backup_root}")
