(function () {
  const FONT_KEY = "saci-font-level";
  const THEME_KEY = "saci-graph-theme";
  const LANG_KEY = "saci-language";
  const ARCH_ZOOM_KEY = "saci-arch-zoom";

  const I18N = {
    tr: {
      navHome: "Home",
      navMethodology: "Methodology",
      navArchitecture: "Architecture",
      navEvidence: "Evidence",
      navArtifacts: "Artifacts",
      navGraph: "Graph",
      navExplanation: "Explanation",
      navPaper: "Paper View",

      langLabel: "Language",
      fontLabel: "Font",
      themeLabel: "Theme",

      architectureKicker: "MİMARİ / ARCHITECTURE",
      architectureTitle: "Lab mimarisi ve veri akışı",
      architectureLead:
        "Bu sayfa, SACI değerlendirmesinde kullanılan kontrollü laboratuvar mimarisini ve verinin uçtan uca nasıl aktığını açıklar. Amaç, telemetri kaynaklarından başlayarak Wazuh toplama ve detection katmanına, MITRE/CTI bağlamına, SACI skorlamasına ve evidence graph çıktısına kadar olan ilişkiyi sade biçimde göstermektir.",

      dataFlowTitle: "Veri akış diyagramı",
      dataFlowText:
        "Diyagram; Windows, Linux, pfSense ve MISP kaynaklarından gelen verinin Wazuh üzerinde işlenmesini, detection ve enrichment ilişkilerinin kurulmasını, ardından SACI skor ve graph çıktısına dönüşmesini gösterir.",
      openImage: "Görseli aç",
      missingImage:
        "Görsel bulunamadı. Türkçe görseli docs/assets/arch-tr.png, İngilizce görseli docs/assets/arch-en.png konumuna koy.",
      figureCaption:
        "Şekil: SACI lab mimarisi. Diyagram, final skorun kendisini değil; final skorun beslendiği telemetri, detection, CTI/MITRE, SACI ve graph ilişkilerinin mimari akışını gösterir.",

      whatArchitectureRepresents: "Mimari neyi temsil eder?",
      whatArchitectureRepresentsP1:
        "SACI mimarisi, güvenlik görünürlüğünü tek bir ürün veya tek bir log kaynağı üzerinden açıklamaz. Bunun yerine, telemetri üreten varlıkları, bu telemetrinin Wazuh tarafından toplanmasını, detection rule ve alert üretimini, MITRE ATT&CK bağlamını, CTI/MISP enrichment zincirini ve bunların SACI graph modeline nasıl taşındığını birlikte ele alır.",
      whatArchitectureRepresentsP2:
        "Bu yaklaşımın nedeni şudur: Bir logun var olması tek başına yeterli değildir. Logun doğru kaynaktan gelmesi, Wazuh pipeline içinde işlenmesi, beklenen detection kontrolüne bağlanması, ilgili MITRE tekniğiyle ilişkilendirilmesi ve gerektiğinde CTI enrichment zinciriyle desteklenmesi gerekir. SACI, bu uçtan uca ilişkileri evidence graph üzerinde ölçülebilir hale getirir.",

      labComponents: "Lab bileşenleri",
      windowsSources: "Windows kaynakları",
      windowsSourcesDesc:
        "DC01 ve WS01 üzerinden Security, Sysmon ve PowerShell telemetrisi üretilir. Bu kaynaklar, kimlik doğrulama, komut çalıştırma, discovery ve endpoint görünürlüğü gibi senaryoların temel kanıtlarını sağlar.",
      linuxSources: "Linux kaynakları",
      linuxSourcesDesc:
        "uhost üzerinden authlog, syslog ve process kayıtları alınır. Bu katman Linux tarafındaki kimlik doğrulama, sistem bilgisi ve süreç görünürlüğünü SACI kapsamına dahil eder.",
      pfsenseSources: "pfSense / firewall kaynakları",
      pfsenseSourcesDesc:
        "FW01 üzerinden firewall ve pfsense_syslog olayları toplanır. Ağ geçişleri, kural gözlemleri ve firewall görünürlüğü bu katmandan değerlendirmeye girer.",
      mispSources: "MISP / CTI kaynakları",
      mispSourcesDesc:
        "CTI01 üzerinde IOC, MISP event, misp_api ve misp_enrichment çıktıları kullanılır. Amaç, tehdit istihbaratı bilgisinin yalnızca tutulması değil, alert ve MITRE bağlamına dönüşüp dönüşmediğini göstermektir.",
      wazuhLayer: "Wazuh toplama ve detection katmanı",
      wazuhLayerDesc:
        "Wazuh; log ve event ingestion, decoder/rule eşleşmeleri, alert üretimi ve MITRE mapping adımlarını yürütür. SACI için bu katman, telemetrinin operasyonel detection kanıtına dönüşüp dönüşmediğini gösterir.",

      endToEndFlow: "Uçtan uca veri akışı",
      telemetry: "Telemetry",
      telemetryDesc: "Windows, Linux, pfSense ve MISP kaynaklarından ham log, event ve IOC bilgisi üretilir.",
      wazuh: "Wazuh",
      wazuhDesc: "Gelen loglar Wazuh tarafından alınır, decoder ve rule katmanlarından geçirilir.",
      detection: "Detection",
      detectionDesc: "Kurallar alert üretir; alertlerin detection control ve MITRE technique ilişkileri kurulur.",
      mitreCti: "MITRE / CTI",
      mitreCtiDesc: "MITRE ATT&CK teknikleri ve MISP enrichment çıktıları alert bağlamını güçlendirir.",
      saci: "SACI",
      saciDesc: "CWLC, CAC, MDC, CTIC ve TF metrikleri declared scope ve observed/missing ilişkiler üzerinden hesaplanır.",
      graph: "Graph",
      graphDesc: "Asset, log source, control, Wazuh rule, MITRE technique, CTI object, metric ve reason code ilişkileri evidence graph içinde birleşir.",

      chainTitle: "Telemetry → Wazuh → Detection → MITRE/CTI → SACI → Graph ilişkisi",
      chainP1:
        "Bu zincirdeki her aşama, SACI skorunun başka bir yönünü besler. Telemetry katmanı log görünürlüğünü, Wazuh ve detection katmanı control/alert coverage değerini, MITRE/CTI katmanı teknik ve istihbarat bağlamını, SACI katmanı metrik hesaplamasını, graph katmanı ise bu ilişkilerin observed veya missing olarak açıklanmasını sağlar.",
      chainP2:
        "Bu nedenle mimari yalnızca “hangi sunucu nerede?” sorusuna cevap vermez. Asıl amaç, verinin hangi adımlardan geçerek final kanıt paketine dönüştüğünü göstermektir. Architecture sayfası, Methodology ve Graph sayfaları arasındaki köprü olarak okunmalıdır.",
      interpretationNote:
        "Yorumlama notu: Diyagram final ortamın tamamen güvenli olduğunu göstermez. Yalnızca SACI kapsamındaki beklenen telemetri, detection, MITRE/CTI ve graph ilişkilerinin hangi mimari akış üzerinden değerlendirildiğini gösterir."
    },

    en: {
      navHome: "Home",
      navMethodology: "Methodology",
      navArchitecture: "Architecture",
      navEvidence: "Evidence",
      navArtifacts: "Artifacts",
      navGraph: "Graph",
      navExplanation: "Explanation",
      navPaper: "Paper View",

      langLabel: "Language",
      fontLabel: "Font",
      themeLabel: "Theme",

      architectureKicker: "ARCHITECTURE",
      architectureTitle: "Lab architecture and data flow",
      architectureLead:
        "This page explains the controlled laboratory architecture used in the SACI evaluation and how data flows end to end. The goal is to show the relationship from telemetry sources to Wazuh collection and detection, MITRE/CTI context, SACI scoring, and the final evidence graph output.",

      dataFlowTitle: "Data flow diagram",
      dataFlowText:
        "The diagram shows how data from Windows, Linux, pfSense and MISP sources is processed in Wazuh, how detection and enrichment relations are established, and how the result is transformed into SACI scoring and graph output.",
      openImage: "Open image",
      missingImage:
        "Image not found. Put the Turkish image at docs/assets/arch-tr.png and the English image at docs/assets/arch-en.png.",
      figureCaption:
        "Figure: SACI lab architecture. The diagram does not represent the final score itself; it shows the architectural flow that feeds telemetry, detection, CTI/MITRE, SACI and graph relations.",

      whatArchitectureRepresents: "What does the architecture represent?",
      whatArchitectureRepresentsP1:
        "The SACI architecture does not explain security visibility through a single product or a single log source. Instead, it combines telemetry-producing assets, Wazuh collection, detection rule and alert generation, MITRE ATT&CK context, CTI/MISP enrichment, and how all of these are transferred into the SACI graph model.",
      whatArchitectureRepresentsP2:
        "The reason for this approach is simple: the existence of a log alone is not sufficient. The log must come from the expected source, be processed by the Wazuh pipeline, be linked to the expected detection control, be mapped to the relevant MITRE technique, and when needed, be supported by the CTI enrichment chain. SACI makes these end-to-end relations measurable on the evidence graph.",

      labComponents: "Lab components",
      windowsSources: "Windows sources",
      windowsSourcesDesc:
        "Security, Sysmon and PowerShell telemetry is produced from DC01 and WS01. These sources provide the core evidence for authentication, command execution, discovery and endpoint visibility scenarios.",
      linuxSources: "Linux sources",
      linuxSourcesDesc:
        "authlog, syslog and process records are collected from uhost. This layer adds Linux-side authentication, system information and process visibility to the SACI scope.",
      pfsenseSources: "pfSense / firewall sources",
      pfsenseSourcesDesc:
        "Firewall and pfsense_syslog events are collected from FW01. Network transitions, rule observations and firewall visibility are evaluated through this layer.",
      mispSources: "MISP / CTI sources",
      mispSourcesDesc:
        "IOC, MISP event, misp_api and misp_enrichment outputs are used on CTI01. The purpose is not only to store threat intelligence, but to verify whether it is converted into alert and MITRE context.",
      wazuhLayer: "Wazuh collection and detection layer",
      wazuhLayerDesc:
        "Wazuh performs log and event ingestion, decoder/rule matching, alert generation and MITRE mapping. For SACI, this layer shows whether telemetry becomes operational detection evidence.",

      endToEndFlow: "End-to-end data flow",
      telemetry: "Telemetry",
      telemetryDesc: "Raw logs, events and IOC information are produced by Windows, Linux, pfSense and MISP sources.",
      wazuh: "Wazuh",
      wazuhDesc: "Incoming logs are collected by Wazuh and processed through decoder and rule layers.",
      detection: "Detection",
      detectionDesc: "Rules generate alerts; alert relations are linked to detection controls and MITRE techniques.",
      mitreCti: "MITRE / CTI",
      mitreCtiDesc: "MITRE ATT&CK techniques and MISP enrichment outputs strengthen the alert context.",
      saci: "SACI",
      saciDesc: "CWLC, CAC, MDC, CTIC and TF metrics are calculated from declared scope and observed/missing relations.",
      graph: "Graph",
      graphDesc: "Asset, log source, control, Wazuh rule, MITRE technique, CTI object, metric and reason code relations are merged into the evidence graph.",

      chainTitle: "Telemetry → Wazuh → Detection → MITRE/CTI → SACI → Graph relation",
      chainP1:
        "Each stage in this chain feeds a different aspect of the SACI score. The telemetry layer feeds log visibility, Wazuh and detection feed control/alert coverage, MITRE/CTI feeds technical and intelligence context, SACI calculates the metrics, and the graph layer explains these relations as observed or missing.",
      chainP2:
        "Therefore, the architecture does not only answer the question of which server is located where. Its main purpose is to show the steps through which data becomes a final evidence package. The Architecture page should be read as a bridge between the Methodology and Graph pages.",
      interpretationNote:
        "Interpretation note: The diagram does not mean that the final environment is completely secure. It only shows the architectural flow through which expected telemetry, detection, MITRE/CTI and graph relations are evaluated within the SACI scope."
    }
  };

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function t(key) {
    const lang = localStorage.getItem(LANG_KEY) || "tr";
    return (I18N[lang] && I18N[lang][key]) || I18N.tr[key] || "";
  }

  function applyI18n() {
    const lang = localStorage.getItem(LANG_KEY) || "tr";
    document.documentElement.setAttribute("lang", lang);
    document.documentElement.setAttribute("data-lang", lang);

    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      if (t(key)) el.textContent = t(key);
    });

    document.querySelectorAll("[data-i18n-html]").forEach(el => {
      const key = el.getAttribute("data-i18n-html");
      if (t(key)) el.innerHTML = t(key);
    });

    const tr = document.getElementById("langTR");
    const en = document.getElementById("langEN");
    if (tr) tr.classList.toggle("active", lang === "tr");
    if (en) en.classList.toggle("active", lang === "en");

    document.dispatchEvent(new CustomEvent("saci:languagechange", { detail: { lang } }));
  }

  function initLanguageControls() {
    const tr = document.getElementById("langTR");
    const en = document.getElementById("langEN");

    if (!localStorage.getItem(LANG_KEY)) {
      localStorage.setItem(LANG_KEY, "tr");
    }

    if (tr) tr.onclick = () => {
      localStorage.setItem(LANG_KEY, "tr");
      applyI18n();
    };

    if (en) en.onclick = () => {
      localStorage.setItem(LANG_KEY, "en");
      applyI18n();
    };

    applyI18n();
  }

  function initFontControls() {
    let level = Number(localStorage.getItem(FONT_KEY) || "0");
    if (!Number.isFinite(level)) level = 0;

    function apply() {
      level = clamp(level, -2, 2);
      document.documentElement.setAttribute("data-font-level", String(level));
      localStorage.setItem(FONT_KEY, String(level));
    }

    const down = document.getElementById("fontDown");
    const reset = document.getElementById("fontReset");
    const up = document.getElementById("fontUp");

    if (down) down.onclick = () => { level -= 1; apply(); };
    if (reset) reset.onclick = () => { level = 0; apply(); };
    if (up) up.onclick = () => { level += 1; apply(); };

    apply();
  }

  function initThemeControls() {
    const saved = localStorage.getItem(THEME_KEY) || "dim";
    document.documentElement.setAttribute("data-theme", saved);

    document.querySelectorAll("[data-theme-btn]").forEach(btn => {
      const theme = btn.getAttribute("data-theme-btn");
      btn.classList.toggle("active", theme === saved);

      btn.onclick = () => {
        localStorage.setItem(THEME_KEY, theme);
        document.documentElement.setAttribute("data-theme", theme);

        document.querySelectorAll("[data-theme-btn]").forEach(b => {
          b.classList.toggle("active", b.getAttribute("data-theme-btn") === theme);
        });
      };
    });
  }

  function initArchitectureImage() {
    const img = document.getElementById("archImage");
    const openLink = document.getElementById("archOpenLink");
    const missing = document.getElementById("missingImage");
    if (!img) return;

    function setImage(lang) {
      const src = lang === "en"
        ? (img.getAttribute("data-src-en") || "assets/arch-en.png")
        : (img.getAttribute("data-src-tr") || "assets/arch-tr.png");

      img.style.display = "block";
      if (missing) missing.style.display = "none";
      img.src = src;
      if (openLink) openLink.href = src;
    }

    img.addEventListener("error", () => {
      img.style.display = "none";
      if (missing) missing.style.display = "block";
    });

    img.addEventListener("load", () => {
      img.style.display = "block";
      if (missing) missing.style.display = "none";
      applyArchZoom(localStorage.getItem(ARCH_ZOOM_KEY) || "fit");
    });

    document.addEventListener("saci:languagechange", e => setImage(e.detail.lang));
    setImage(localStorage.getItem(LANG_KEY) || "tr");
  }

  function applyArchZoom(mode) {
    const img = document.getElementById("archImage");
    if (!img) return;

    const safe = ["fit", "125", "150"].includes(mode) ? mode : "fit";

    if (safe === "fit") {
      img.style.width = "100%";
      img.style.maxWidth = "100%";
    } else {
      img.style.width = safe + "%";
      img.style.maxWidth = "none";
    }

    localStorage.setItem(ARCH_ZOOM_KEY, safe);

    document.querySelectorAll("[data-zoom]").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-zoom") === safe);
    });
  }

  function initArchZoom() {
    document.querySelectorAll("[data-zoom]").forEach(btn => {
      btn.onclick = () => applyArchZoom(btn.getAttribute("data-zoom"));
    });
    applyArchZoom(localStorage.getItem(ARCH_ZOOM_KEY) || "fit");
  }

  function init() {
    initFontControls();
    initThemeControls();
    initLanguageControls();
    initArchitectureImage();
    initArchZoom();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
