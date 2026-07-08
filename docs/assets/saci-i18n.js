
(function(){
  const KEY = "saci_site_lang";
  let applying = false;

  const pairs = [
    ["Readable paper diagrams, scenario-level interactive output, and full graph links.", "Okunabilir makale diyagramları, senaryo bazlı interaktif çıktı ve tam graph bağlantıları."],
    ["SACI Paper Clean View", "SACI Makale Temiz Görünüm"],
    ["Final SACI Evidence Package", "Final SACI Kanıt Paketi"],
    ["Controlled Lab Architecture", "Kontrollü Lab Mimarisi"],
    ["Interactive evidence graph", "Etkileşimli kanıt grafı"],
    ["Interactive Evidence Graph", "Etkileşimli Kanıt Grafı"],
    ["Explanation report", "Açıklama raporu"],
    ["Explanation Report", "Açıklama Raporu"],
    ["Paper Clean View", "Makale Temiz Görünümü"],

    ["Total scenarios", "Toplam senaryo"],
    ["Total scenario", "Toplam senaryo"],
    ["S8 missing edges", "S8 eksik ilişki"],
    ["S8 missing edge", "S8 eksik ilişki"],
    ["Explanation layer", "Açıklama katmanı"],
    ["Policy-guided", "Politika yönlendirmeli"],
    ["Policy-guided explanation", "Politika yönlendirmeli açıklama"],

    ["Model", "Model"],
    ["S8 closure", "S8 kapanış"],
    ["Criticality", "Kritiklik"],
    ["S7A missing", "S7A eksik"],
    ["Taxonomy", "Taksonomi"],
    ["Fault matrix", "Hata matrisi"],
    ["Scenario detail", "Senaryo detayı"],
    ["Scenario Detail", "Senaryo Detayı"],
    ["Full table", "Tam tablo"],
    ["Full evaluation table", "Tam değerlendirme tablosu"],
    ["Full Evaluation Table", "Tam Değerlendirme Tablosu"],

    ["Comparison", "Karşılaştırma"],
    ["Delta", "Fark"],
    ["Active scenario", "Aktif senaryo"],
    ["Graph closure", "Graf kapanışı"],
    ["observed/expected", "gözlenen/beklenen"],
    ["critical vs non-critical", "kritik / kritik olmayan"],
    ["critical asset impact", "kritik varlık etkisi"],
    ["explains, does not calculate the score", "skoru hesaplamaz, açıklar"],

    ["Fault scenarios", "Hata senaryoları"],
    ["controlled tests", "kontrollü testler"],
    ["Lowest SACI", "En düşük SACI"],
    ["Recovery", "İyileşme"],
    ["after fix", "düzeltme sonrası"],
    ["Scope validation", "Kapsam doğrulama"],
    ["out-of-scope", "kapsam dışı"],

    ["SACI Conceptual Model", "SACI Kavramsal Modeli"],
    ["Visibility Inputs", "Görünürlük Girdileri"],
    ["SOC Evidence Layer", "SOC Kanıt Katmanı"],
    ["Graph Scoring Core", "Graf Skorlama Çekirdeği"],
    ["Explanation Output", "Açıklama Çıktısı"],
    ["Log Sources", "Log Kaynakları"],
    ["Observed Alerts", "Gözlenen Alarmlar"],
    ["Detection Controls", "Tespit Kontrolleri"],
    ["SACI Metrics", "SACI Metrikleri"],
    ["SACI Score", "SACI Skoru"],

    ["S8 Final Visibility Closure", "S8 Final Görünürlük Kapanışı"],
    ["Final closure reference state.", "Final kapanış referans durumu."],
    ["All expected visibility relationships are observed within the defined evaluation scope.", "Tanımlı değerlendirme kapsamındaki tüm beklenen görünürlük ilişkileri gözlenmiştir."],

    ["Critical vs Non-critical Telemetry Loss", "Kritik ve Kritik Olmayan Telemetri Kaybı"],
    ["S7A Critical DC01 Sysmon Loss", "S7A Kritik DC01 Sysmon Kaybı"],
    ["S7B Non-critical WS01 Sysmon Loss", "S7B Kritik Olmayan WS01 Sysmon Kaybı"],
    ["Critical DC01 Sysmon telemetry loss causes a strong visibility regression and increases missing graph relations.", "Kritik DC01 Sysmon telemetri kaybı güçlü bir görünürlük gerilemesine neden olur ve eksik graf ilişkilerini artırır."],
    ["Non-critical endpoint telemetry loss has lower impact than critical DC01 telemetry loss.", "Kritik olmayan uç sistem telemetri kaybının etkisi, kritik DC01 telemetri kaybına göre daha düşüktür."],
    ["This comparison demonstrates that SACI is sensitive not only to missing telemetry, but also to the criticality of the affected asset and its expected visibility relationships.", "Bu karşılaştırma, SACI’nin yalnızca eksik telemetriye değil, etkilenen varlığın kritiklik düzeyine ve beklenen görünürlük ilişkilerine de duyarlı olduğunu gösterir."],

    ["Scenario Taxonomy", "Senaryo Taksonomisi"],
    ["Reviewer-oriented Fault-injection Matrix", "Hakem Odaklı Hata Enjeksiyon Matrisi"],
    ["Full Scenario Table", "Tam Senaryo Tablosu"],

    ["SACI", "SACI"],
    ["Stage", "Aşama"],
    ["Name", "Ad"],
    ["Type", "Tür"],
    ["Observed", "Gözlenen"],
    ["Missing", "Eksik"],
    ["Graph", "Graf"],
    ["Description", "Açıklama"],
    ["Components", "Bileşenler"],
    ["Missing edges", "Eksik ilişkiler"],
    ["Observed edges", "Gözlenen ilişkiler"],
    ["Total edges", "Toplam ilişkiler"],
    ["Raw scenario JSON", "Ham senaryo JSON"],

    ["Full interactive graph", "Tam etkileşimli graf"],
    ["Evidence package index", "Kanıt paketi indeksi"],
    ["Load graph", "Grafı yükle"],
    ["Graph summary", "Graf özeti"],

    ["Telemetry flow", "Telemetri akışı"],
    ["Telemetry", "Telemetri"],
    ["telemetry", "telemetri"],
    ["Visibility", "Görünürlük"],
    ["visibility", "görünürlük"],
    ["Evidence", "Kanıt"],
    ["evidence", "kanıt"],
    ["Score", "Skor"],
    ["score", "skor"],
    ["Scenario", "Senaryo"],
    ["scenario", "senaryo"]
  ];

  function ensureToggle(){
    if(document.querySelector(".saci-global-lang-toggle")) return;

    const box = document.createElement("div");
    box.className = "saci-global-lang-toggle";
    box.innerHTML = `
      <button type="button" data-saci-lang="tr">TR</button>
      <button type="button" data-saci-lang="en">EN</button>
    `;

    document.body.appendChild(box);

    box.addEventListener("click", function(e){
      const btn = e.target.closest("button[data-saci-lang]");
      if(!btn) return;
      setLang(btn.dataset.saciLang);
    });
  }

  function normalizeToEnglish(text){
    let out = text;
    for(const [en, tr] of pairs){
      out = out.split(tr).join(en);
    }
    return out;
  }

  function toTurkish(text){
    let out = normalizeToEnglish(text);
    for(const [en, tr] of pairs){
      out = out.split(en).join(tr);
    }
    return out;
  }

  function convertText(text, lang){
    return lang === "tr" ? toTurkish(text) : normalizeToEnglish(text);
  }

  function shouldSkip(node){
    const p = node.parentElement;
    if(!p) return true;

    const skipTags = new Set(["SCRIPT","STYLE","PRE","CODE","TEXTAREA"]);
    if(skipTags.has(p.tagName)) return true;

    if(p.closest(".saci-global-lang-toggle")) return true;
    if(p.closest("pre, code, script, style, textarea")) return true;

    return false;
  }

  function applyLang(lang){
    if(applying) return;
    applying = true;

    try{
      document.documentElement.setAttribute("lang", lang);

      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        {
          acceptNode(node){
            if(shouldSkip(node)) return NodeFilter.FILTER_REJECT;
            if(!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
            return NodeFilter.FILTER_ACCEPT;
          }
        }
      );

      const nodes = [];
      while(walker.nextNode()) nodes.push(walker.currentNode);

      nodes.forEach(node => {
        node.nodeValue = convertText(node.nodeValue, lang);
      });

      document.querySelectorAll("[title]").forEach(el => {
        el.setAttribute("title", convertText(el.getAttribute("title"), lang));
      });

      document.querySelectorAll("[placeholder]").forEach(el => {
        el.setAttribute("placeholder", convertText(el.getAttribute("placeholder"), lang));
      });

      document.querySelectorAll(".saci-global-lang-toggle button").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.saciLang === lang);
      });

    } finally {
      applying = false;
    }
  }

  function setLang(lang){
    localStorage.setItem(KEY, lang);
    applyLang(lang);
  }

  function currentLang(){
    return localStorage.getItem(KEY) || "en";
  }

  function boot(){
    ensureToggle();
    applyLang(currentLang());
  }

  document.addEventListener("DOMContentLoaded", boot);

  const observer = new MutationObserver(() => {
    if(applying) return;
    clearTimeout(window.__saciLangTimer);
    window.__saciLangTimer = setTimeout(() => applyLang(currentLang()), 80);
  });

  document.addEventListener("DOMContentLoaded", () => {
    observer.observe(document.body, {
      childList:true,
      subtree:true,
      characterData:true
    });
  });

  setTimeout(boot, 250);
  setTimeout(() => applyLang(currentLang()), 800);
})();
