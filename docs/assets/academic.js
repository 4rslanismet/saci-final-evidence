(function () {
  "use strict";

  document.documentElement.classList.add("js");
  const LANG_KEY = "saci-academic-language";

  function preferredLanguage() {
    return localStorage.getItem(LANG_KEY) || "tr";
  }

  function setLanguage(lang) {
    const next = lang === "en" ? "en" : "tr";
    localStorage.setItem(LANG_KEY, next);
    document.documentElement.lang = next;
    document.querySelectorAll("[data-tr][data-en]").forEach((element) => {
      element.textContent = element.getAttribute(`data-${next}`) || "";
    });
    document.querySelectorAll("[data-tr-aria][data-en-aria]").forEach((element) => {
      element.setAttribute("aria-label", element.getAttribute(`data-${next}-aria`) || "");
    });
    document.querySelectorAll("[data-lang]").forEach((button) => {
      const active = button.dataset.lang === next;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    const body = document.body;
    if (body) {
      const title = body.getAttribute(`data-title-${next}`);
      if (title) document.title = title;
    }
    window.dispatchEvent(new CustomEvent("saci:language", { detail: { lang: next } }));
  }

  function initLanguage() {
    document.querySelectorAll("[data-lang]").forEach((button) => {
      button.addEventListener("click", () => setLanguage(button.dataset.lang));
    });
    setLanguage(preferredLanguage());
  }

  function initNavigation() {
    const toggle = document.querySelector(".nav-toggle");
    if (toggle) {
      toggle.addEventListener("click", () => {
        const open = document.body.classList.toggle("nav-open");
        toggle.setAttribute("aria-expanded", String(open));
      });
      document.querySelectorAll(".nav-panel a").forEach((link) => {
        link.addEventListener("click", () => {
          document.body.classList.remove("nav-open");
          toggle.setAttribute("aria-expanded", "false");
        });
      });
    }

    const anchors = [...document.querySelectorAll('.nav-links a[href^="#"]')];
    const sections = anchors
      .map((anchor) => document.querySelector(anchor.getAttribute("href")))
      .filter(Boolean);
    if (sections.length && "IntersectionObserver" in window) {
      const observer = new IntersectionObserver((entries) => {
        const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (!visible) return;
        anchors.forEach((anchor) => anchor.classList.toggle("active", anchor.getAttribute("href") === `#${visible.target.id}`));
      }, { rootMargin: "-28% 0px -60%", threshold: [0, .2, .5] });
      sections.forEach((section) => observer.observe(section));
    }
  }

  function initMotion() {
    const items = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) {
      items.forEach((item) => item.classList.add("is-visible"));
      return;
    }
    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        entry.target.querySelectorAll(".metric-row").forEach((row, index) => {
          window.setTimeout(() => row.classList.add("is-visible"), index * 90);
        });
        currentObserver.unobserve(entry.target);
      });
    }, { threshold: .12 });
    items.forEach((item) => observer.observe(item));

    const progress = document.querySelector(".reading-progress span");
    if (progress) {
      const update = () => {
        const total = document.documentElement.scrollHeight - innerHeight;
        const ratio = total > 0 ? Math.min(1, scrollY / total) : 0;
        progress.style.transform = `scaleX(${ratio})`;
      };
      addEventListener("scroll", update, { passive: true });
      update();
    }
  }

  function initCopyButtons() {
    document.querySelectorAll("[data-copy-target]").forEach((button) => {
      const original = { tr: button.dataset.tr || button.textContent, en: button.dataset.en || button.textContent };
      button.addEventListener("click", async () => {
        const target = document.getElementById(button.dataset.copyTarget);
        if (!target) return;
        const text = target.innerText.trim();
        try {
          await navigator.clipboard.writeText(text);
          const lang = preferredLanguage();
          button.textContent = lang === "en" ? "Copied" : "Kopyalandı";
          window.setTimeout(() => { button.textContent = original[lang] || original.tr; }, 1400);
        } catch (_) {
          window.getSelection()?.selectAllChildren(target);
        }
      });
    });
  }

  function parseCSV(text) {
    const rows = [];
    let row = [];
    let field = "";
    let quoted = false;
    for (let index = 0; index < text.length; index += 1) {
      const character = text[index];
      if (quoted) {
        if (character === '"' && text[index + 1] === '"') {
          field += '"';
          index += 1;
        } else if (character === '"') {
          quoted = false;
        } else {
          field += character;
        }
      } else if (character === '"') {
        quoted = true;
      } else if (character === ",") {
        row.push(field);
        field = "";
      } else if (character === "\n") {
        row.push(field.replace(/\r$/, ""));
        if (row.some((value) => value !== "")) rows.push(row);
        row = [];
        field = "";
      } else {
        field += character;
      }
    }
    row.push(field.replace(/\r$/, ""));
    if (row.some((value) => value !== "")) rows.push(row);
    if (!rows.length) return [];
    const headers = rows.shift();
    return rows.map((values) => Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ""])));
  }

  async function fetchCSV(path) {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`${response.status} ${path}`);
    return parseCSV(await response.text());
  }

  function cell(value, className) {
    const element = document.createElement("td");
    element.textContent = value ?? "";
    if (className) element.className = className;
    return element;
  }

  function statusCell(active, labels) {
    const element = document.createElement("td");
    const badge = document.createElement("span");
    badge.className = `pill ${active ? "success" : "muted"}`;
    badge.dataset.tr = active ? labels.trTrue : labels.trFalse;
    badge.dataset.en = active ? labels.enTrue : labels.enFalse;
    badge.textContent = badge.getAttribute(`data-${preferredLanguage()}`);
    element.appendChild(badge);
    return element;
  }

  function appendRow(body, values) {
    const row = document.createElement("tr");
    values.forEach((value) => row.appendChild(value instanceof Node ? value : cell(value)));
    body.appendChild(row);
    return row;
  }

  function renderScores(rows) {
    document.querySelectorAll("[data-metric-score]").forEach((element) => {
      const metric = rows.find((row) => row.metric === element.dataset.metricScore);
      if (metric) element.textContent = Number(metric.score).toFixed(1);
    });
    const body = document.querySelector('[data-table="scores"]');
    if (!body) return;
    body.replaceChildren();
    rows.forEach((row) => appendRow(body, [
      row.metric,
      row.name,
      Number(row.weight).toFixed(2),
      Number(row.score).toFixed(1),
      statusCell(row.applicable === "1", { trTrue: "Uygulanabilir", trFalse: "N/A", enTrue: "Applicable", enFalse: "N/A" })
    ]));
  }

  function renderLogs(rows) {
    const body = document.querySelector('[data-table="logs"]');
    if (!body) return;
    body.replaceChildren();
    rows.forEach((row) => appendRow(body, [
      row.asset_id,
      row.hostname,
      row.log_source,
      row.asset_criticality,
      row.source_weight,
      statusCell(row.observed === "1", { trTrue: "Gözlendi", trFalse: "Eksik", enTrue: "Observed", enFalse: "Missing" }),
      row.last_seen ? new Date(row.last_seen).toISOString().replace(".000", "") : "—"
    ]));
  }

  function renderControls(rows) {
    const body = document.querySelector('[data-table="controls"]');
    if (!body) return;
    body.replaceChildren();
    rows.forEach((item) => {
      const row = appendRow(body, [
        item.control_id,
        item.asset_id,
        item.source,
        item.rule_id,
        item.mitre_technique || "—",
        statusCell(item.enabled === "1", { trTrue: "Etkin", trFalse: "Legacy / dış kapsam", enTrue: "Enabled", enFalse: "Legacy / out of scope" }),
        statusCell(item.seen === "1", { trTrue: "Gözlendi", trFalse: "Sayılmadı", enTrue: "Observed", enFalse: "Not counted" }),
        item.weight
      ]);
      row.dataset.source = item.source.toLowerCase();
      row.dataset.state = item.enabled === "1" ? "enabled" : "disabled";
      row.dataset.search = Object.values(item).join(" ").toLowerCase();
    });
    initTableFilter("controls", rows.length);
  }

  function renderMitre(rows) {
    const body = document.querySelector('[data-table="mitre"]');
    if (!body) return;
    body.replaceChildren();
    rows.forEach((item) => {
      const row = appendRow(body, [
        item.technique_id,
        item.technique_name,
        item.tactic,
        statusCell(item.covered === "1", { trTrue: "Kapsandı", trFalse: "Eksik", enTrue: "Covered", enFalse: "Missing" })
      ]);
      row.dataset.tactic = item.tactic.toLowerCase();
      row.dataset.search = Object.values(item).join(" ").toLowerCase();
    });
    initTableFilter("mitre", rows.length);
  }

  function renderCTI(rows) {
    const body = document.querySelector('[data-table="ctic"]');
    if (!body) return;
    body.replaceChildren();
    rows.forEach((item) => appendRow(body, [
      item.indicator,
      item.type,
      statusCell(item.lookup_executed === "1", { trTrue: "Kayıtlı", trFalse: "Yok", enTrue: "Recorded", enFalse: "Absent" }),
      statusCell(item.misp_hit === "1", { trTrue: "Kayıtlı", trFalse: "Yok", enTrue: "Recorded", enFalse: "Absent" }),
      statusCell(item.wazuh_alert === "1", { trTrue: "Kayıtlı", trFalse: "Yok", enTrue: "Recorded", enFalse: "Absent" }),
      statusCell(item.mapped_to_mitre === "1", { trTrue: "Kayıtlı", trFalse: "Yok", enTrue: "Recorded", enFalse: "Absent" }),
      item.expected_alert_rule,
      item.mitre_technique
    ]));
  }

  function initTableFilter(name, total) {
    const body = document.querySelector(`[data-table="${name}"]`);
    const search = document.querySelector(`[data-filter-search="${name}"]`);
    const select = document.querySelector(`[data-filter-select="${name}"]`);
    const count = document.querySelector(`[data-table-count="${name}"]`);
    if (!body || (!search && !select)) return;
    const update = () => {
      const query = (search?.value || "").trim().toLowerCase();
      const selection = (select?.value || "all").toLowerCase();
      let visible = 0;
      body.querySelectorAll("tr").forEach((row) => {
        const matchesText = !query || (row.dataset.search || row.textContent.toLowerCase()).includes(query);
        const state = row.dataset.state || row.dataset.tactic || row.dataset.source || "";
        const matchesSelect = selection === "all" || state.includes(selection);
        const show = matchesText && matchesSelect;
        row.hidden = !show;
        if (show) visible += 1;
      });
      if (count) count.textContent = `${visible} / ${total}`;
    };
    search?.addEventListener("input", update);
    select?.addEventListener("change", update);
    update();
  }

  async function initEvidenceData() {
    const root = document.body.dataset.dataRoot;
    if (!root) return;
    const status = document.querySelector("[data-load-status]");
    try {
      const [scores, logs, controls, mitre, ctic] = await Promise.all([
        fetchCSV(`${root}saci_scores_v2.csv`),
        fetchCSV(`${root}log_source_status.csv`),
        fetchCSV(`${root}control_coverage_v2.csv`),
        fetchCSV(`${root}mitre_coverage_v2.csv`),
        fetchCSV(`${root}ctic_coverage_v2.csv`)
      ]);
      renderScores(scores);
      renderLogs(logs);
      renderControls(controls);
      renderMitre(mitre);
      renderCTI(ctic);
      setLanguage(preferredLanguage());
      if (status) {
        status.dataset.tr = "Kaynak dosyalardan yüklendi";
        status.dataset.en = "Loaded from source artifacts";
        status.textContent = status.getAttribute(`data-${preferredLanguage()}`);
        status.classList.add("loaded");
      }
    } catch (error) {
      console.error("SACI evidence data could not be loaded", error);
      if (status) {
        status.dataset.tr = "Veri yüklenemedi; doğrudan indirme bağlantılarını kullanın.";
        status.dataset.en = "Data could not be loaded; use the direct download links.";
        status.textContent = status.getAttribute(`data-${preferredLanguage()}`);
      }
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    initLanguage();
    initNavigation();
    initMotion();
    initCopyButtons();
    initEvidenceData();
    document.querySelectorAll("[data-current-year]").forEach((element) => { element.textContent = new Date().getFullYear(); });
  });
})();
