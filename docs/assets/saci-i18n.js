
(function(){
  const KEY = "saci_site_lang";
  let applying = false;

  const pairs = [
    ["SACI Paper Clean View","SACI Makale Temiz Görünüm"],
    ["Readable paper diagrams, scenario-level interactive output, and full graph links.","Okunabilir makale diyagramları, senaryo bazlı interaktif çıktı ve tam graph bağlantıları."],
    ["Evidence package index","Kanıt paketi indeksi"],
    ["Full interactive graph","Tam etkileşimli graf"],
    ["Policy-guided explanation","Politika yönlendirmeli açıklama"],
    ["Total scenarios","Toplam senaryo"],
    ["S8 missing edges","S8 eksik ilişki"],
    ["Explanation layer","Açıklama katmanı"],
    ["explains, does not calculate the score","skoru hesaplamaz, açıklar"],
    ["Overview","Genel bakış"],
    ["Model","Model"],
    ["S8 closure","S8 kapanış"],
    ["Criticality","Kritiklik"],
    ["S7A missing","S7A eksik"],
    ["Taxonomy","Taksonomi"],
    ["Fault matrix","Hata matrisi"],
    ["Scenario detail","Senaryo detayı"],
    ["Full table","Tam tablo"],
    ["SACI Conceptual Model","SACI Kavramsal Modeli"],
    ["Visibility Inputs","Görünürlük Girdileri"],
    ["SOC Evidence Layer","SOC Kanıt Katmanı"],
    ["Graph Scoring Core","Graf Skorlama Çekirdeği"],
    ["Explanation Output","Açıklama Çıktısı"],
    ["S8 Final Visibility Closure","S8 Final Görünürlük Kapanışı"],
    ["Critical vs Non-critical Telemetry Loss","Kritik ve Kritik Olmayan Telemetri Kaybı"],
    ["S7A Critical DC01 Sysmon Loss","S7A Kritik DC01 Sysmon Kaybı"],
    ["S7B Non-critical WS01 Sysmon Loss","S7B Kritik Olmayan WS01 Sysmon Kaybı"],
    ["SACI Evaluation Scenario Taxonomy","SACI Değerlendirme Senaryo Taksonomisi"],
    ["Reviewer-oriented Fault-injection Matrix","Hakem Odaklı Hata Enjeksiyon Matrisi"],
    ["Full evaluation table","Tam değerlendirme tablosu"],
    ["Active scenario","Aktif senaryo"],
    ["Comparison","Karşılaştırma"],
    ["Delta","Fark"],
    ["Critical asset impact","Kritik varlık etkisi"],
    ["critical vs non-critical","kritik / kritik olmayan"],
    ["controlled tests","kontrollü testler"],
    ["Lowest SACI","En düşük SACI"],
    ["Recovery","İyileşme"],
    ["Scope validation","Kapsam doğrulama"],
    ["Missing edges","Eksik ilişkiler"],
    ["Observed edges","Gözlenen ilişkiler"],
    ["Total edges","Toplam ilişkiler"],
    ["Observed","Gözlenen"],
    ["Missing","Eksik"],
    ["Graph","Graf"],
    ["Description","Açıklama"],
    ["Components","Bileşenler"],
    ["Type","Tür"],
    ["Stage","Aşama"],
    ["Name","Ad"],
    ["Raw scenario JSON","Ham senaryo JSON"],
    ["Telemetry Loss","Telemetri Kaybı"],
    ["telemetry","telemetri"],
    ["Telemetry","Telemetri"],
    ["visibility","görünürlük"],
    ["Visibility","Görünürlük"],
    ["evidence","kanıt"],
    ["Evidence","Kanıt"]
  ];

  function ensureToggle(){
    document.querySelectorAll(".saci-lang-toggle").forEach(el => el.remove());
    const existing = document.querySelectorAll(".saci-global-lang-toggle");
    existing.forEach((el, idx) => { if(idx > 0) el.remove(); });
    if(document.querySelector(".saci-global-lang-toggle")) return;

    const box = document.createElement("div");
    box.className = "saci-global-lang-toggle";
    box.innerHTML = '<button type="button" data-saci-lang="tr">TR</button><button type="button" data-saci-lang="en">EN</button>';
    document.body.appendChild(box);
    box.addEventListener("click", e => {
      const btn = e.target.closest("button[data-saci-lang]");
      if(!btn) return;
      setLang(btn.dataset.saciLang);
    });
  }

  function normalizeToEnglish(text){
    let out = text;
    for(const [en,tr] of pairs) out = out.split(tr).join(en);
    return out;
  }

  function toTurkish(text){
    let out = normalizeToEnglish(text);
    for(const [en,tr] of pairs) out = out.split(en).join(tr);
    return out;
  }

  function shouldSkip(node){
    const p = node.parentElement;
    if(!p) return true;
    if(p.closest(".saci-global-lang-toggle")) return true;
    if(p.closest("pre, code, script, style, textarea")) return true;
    return false;
  }

  function applyLang(lang){
    if(applying) return;
    applying = true;
    try{
      document.documentElement.setAttribute("lang", lang);
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
        acceptNode(node){
          if(shouldSkip(node)) return NodeFilter.FILTER_REJECT;
          if(!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      });
      const nodes = [];
      while(walker.nextNode()) nodes.push(walker.currentNode);
      nodes.forEach(n => n.nodeValue = lang === "tr" ? toTurkish(n.nodeValue) : normalizeToEnglish(n.nodeValue));
      
      document.querySelectorAll("[data-tr][data-en]").forEach(el => {
        if (el.children && el.children.length) return;
        const value = el.getAttribute("data-" + lang);
        if (value) el.textContent = value;
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

  window.SACI_I18N = { apply: () => applyLang(currentLang()), setLang, currentLang };

  document.addEventListener("DOMContentLoaded", boot);
  const observer = new MutationObserver(() => {
    if(applying) return;
    clearTimeout(window.__saciLangTimer);
    window.__saciLangTimer = setTimeout(() => applyLang(currentLang()), 80);
  });
  document.addEventListener("DOMContentLoaded", () => {
    observer.observe(document.body, {childList:true, subtree:true, characterData:true});
  });
  setTimeout(boot, 250);
  setTimeout(() => applyLang(currentLang()), 900);
})();
