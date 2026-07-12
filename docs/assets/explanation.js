
(() => {
  const REPORTS = {"FINAL": {"tr": {"title": "Final kanıt kapanışı", "situation": "Final veri kümesi, yayına esas SACI kanıt yapısını temsil eder. Beklenen telemetri, detection, MITRE ATT&CK ve CTI/MISP ilişkileri tanımlı değerlendirme kapsamı içinde graph üzerinde gözlemlenmiştir.", "evidence": "Aktif skor bileşenlerinin 100 olması, missing edge sayısının sıfır olması ve observed edge sayısının toplam edge sayısına eşit olması, kapsam içindeki kanıt zincirinin kapandığını gösterir.", "impact": "Bu sonuç, güvenlik operasyonunda beklenen görünürlük zincirlerinin izlenebilir ve denetlenebilir olduğunu gösterir. Ancak bilinmeyen tüm saldırı yüzeylerinin keşfedildiği veya ortamın mutlak güvenli olduğu anlamına gelmez.", "action": "Final veri kümesi yayın kanıtı olarak sabitlenmeli; inventory drift, yeni kapsam eklemeleri, telemetri kayıpları ve freshness düşüşleri ayrı değerlendirme senaryolarında izlenmelidir."}, "en": {"title": "Final evidence closure", "situation": "The final dataset represents the publication-level SACI evidence structure. Expected telemetry, detection, MITRE ATT&CK and CTI/MISP relations are observed on the graph within the declared evaluation scope.", "evidence": "Active score components being 100, the missing-edge count being zero and the observed-edge count matching the total edge count indicate closure of the in-scope evidence chain.", "impact": "The result shows that expected visibility chains are traceable and auditable. It does not mean that every unknown attack-surface element has been discovered or that the environment is absolutely secure.", "action": "Freeze the final dataset as publication evidence and evaluate inventory drift, scope additions, telemetry losses and freshness decay through separate scenarios."}}, "S0": {"tr": {"title": "SIEM bulunmayan başlangıç durumu", "situation": "Merkezi log toplama ve ilişkilendirme platformu bulunmadığından SACI kanıt zinciri temel seviyede kurulamamaktadır.", "evidence": "Asset, log source, control, MITRE ve CTI ilişkilerinin büyük bölümü gözlemlenemez; bileşen metrikleri bu nedenle sıfıra yakın veya sıfırdır.", "impact": "Alarm korelasyonu, davranış eşleme ve CTI zenginleştirme üretilemez. Sorun detection kalitesinden önce gözlem altyapısının yokluğudur.", "action": "Wazuh kurulmalı, veri kabulü doğrulanmalı ve ilk asset-to-log-source ilişkileri graph üzerinde gözlemlenmelidir."}, "en": {"title": "Baseline without a SIEM", "situation": "The SACI evidence chain cannot be established because no central log collection and correlation platform exists.", "evidence": "Most asset, log-source, control, MITRE and CTI relations are not observable, leaving component metrics at or near zero.", "impact": "Alert correlation, behavior mapping and CTI enrichment cannot be produced. The problem originates in the absence of the observation layer.", "action": "Deploy Wazuh, validate ingestion and observe the first asset-to-log-source relations on the graph."}}, "S1": {"tr": {"title": "SIEM kurulu, kapsam henüz eksik", "situation": "Wazuh görünür durumdadır; ancak varlık, log kaynağı ve kontrol ilişkilerinin tamamı henüz beyan edilmemiş veya gözlemlenmemiştir.", "evidence": "Platform düğümü bulunmasına rağmen expected ve observed ilişkiler arasında belirgin fark vardır.", "impact": "Kurulumun çalışması operasyonel görünürlüğün tamamlandığı anlamına gelmez.", "action": "Envanter, agent bağlantıları, syslog kaynakları ve expected log-source ilişkileri tamamlanmalıdır."}, "en": {"title": "SIEM deployed, scope incomplete", "situation": "Wazuh is visible, but not all asset, log-source and control relations are declared or observed.", "evidence": "The platform node exists while a clear gap remains between expected and observed relations.", "impact": "A running installation does not mean that operational visibility is complete.", "action": "Complete the inventory, agent connections, syslog sources and expected log-source relations."}}, "S2": {"tr": {"title": "Envanter tanımlı, telemetri yetersiz", "situation": "İzlenmesi beklenen varlıklar beyan edilmiştir; beklenen log kaynaklarının tamamı observed ilişkiye dönüşmemiştir.", "evidence": "Model kapsamı bilir fakat telemetri yokluğu nedeniyle ilişki zincirleri eksik kalır.", "impact": "Görünürlük beyan seviyesinde kalır ve detection katmanı yeterli veriyle beslenemez.", "action": "Expected kaynak listesi Wazuh gözlemleriyle karşılaştırılmalı, eksik agent ve event-channel ayarları tamamlanmalıdır."}, "en": {"title": "Inventory declared, telemetry insufficient", "situation": "Assets expected to be monitored are declared, but not all expected log sources become observed relations.", "evidence": "The model knows the scope, yet missing telemetry leaves relation chains incomplete.", "impact": "Visibility remains at declaration level and the detection layer lacks sufficient input.", "action": "Compare expected sources with Wazuh observations and complete missing agent and event-channel settings."}}, "S3": {"tr": {"title": "Telemetri var, detection zinciri eksik", "situation": "Log kaynakları Wazuh'a ulaşmaktadır; veriyi control, rule ve alert kanıtına dönüştüren ilişkiler tamamlanmamıştır.", "evidence": "Observed telemetri bulunmasına rağmen control-to-rule veya rule-to-alert edge kayıtları eksik kalır.", "impact": "Verinin geliyor olması, beklenen saldırı davranışlarının alarm üretimine dönüştüğünü kanıtlamaz.", "action": "Decoder, rule ve control mapping kayıtları kontrollü test olaylarıyla doğrulanmalıdır."}, "en": {"title": "Telemetry present, detection chain incomplete", "situation": "Log sources reach Wazuh, but relations that convert data into control, rule and alert evidence are incomplete.", "evidence": "Observed telemetry exists while control-to-rule or rule-to-alert edges remain missing.", "impact": "Incoming data does not prove that expected attack behavior is converted into alerts.", "action": "Validate decoders, rules and control mappings with controlled test events."}}, "S4": {"tr": {"title": "Detection etkin, üst bağlam kısmi", "situation": "Detection kontrolleri ve alert üretimi görünürdür; MITRE veya CTI bağlamının bir bölümü henüz bağlanmamıştır.", "evidence": "CAC yükselirken MDC veya CTIC aynı hızda kapanmayabilir.", "impact": "Alarm üretimi vardır; saldırı tekniği ve istihbarat bağlamı eksik kalabilir.", "action": "Her kontrol için rule, ATT&CK technique ve gerekli CTI object ilişkileri tamamlanmalıdır."}, "en": {"title": "Detection active, higher-level context partial", "situation": "Detection controls and alert generation are visible, but some MITRE or CTI context remains unlinked.", "evidence": "CAC can increase while MDC or CTIC does not close at the same rate.", "impact": "Alerts exist, but adversary-technique and intelligence context may remain incomplete.", "action": "Complete rule, ATT&CK-technique and required CTI-object relations for every control."}}, "S5": {"tr": {"title": "MITRE kapsamı kısmi", "situation": "Kapsamdaki ATT&CK tekniklerinin bir bölümü detection kanıtıyla doğrulanmamıştır.", "evidence": "MDC, bir teknik yalnızca listelendiği için değil, control ve rule kanıtıyla bağlandığında yükselir.", "impact": "Sahte tam kapsama önlenir; kapsamda olup kanıtlanmayan teknikler görünür kalır.", "action": "Eksik teknikler için veri kaynağı, kontrol, Wazuh kuralı ve kontrollü test tanımlanmalıdır."}, "en": {"title": "MITRE coverage is partial", "situation": "Some in-scope ATT&CK techniques are not validated by detection evidence.", "evidence": "MDC increases only when a technique is linked to control and rule evidence, not merely listed.", "impact": "Artificial full coverage is prevented and unverified in-scope techniques remain visible.", "action": "Define the data source, control, Wazuh rule and controlled test for missing techniques."}}, "S6": {"tr": {"title": "CTI enrichment etkinleştirildi", "situation": "MISP/CTI entegrasyonu devreye alınmış; lookup, hit/no-hit ve alarm geri dönüş ilişkileri doğrulanmaktadır.", "evidence": "CTIC yalnızca lookup çağrısına değil, enrichment sonucunun alarm ve graph zincirine dönmesine bağlıdır.", "impact": "Entegrasyonun kurulması ile operasyonel CTI kapanışı birbirinden ayrılır.", "action": "Alert → custom-misp → MISP → enrichment rule → typed CTI object zinciri uçtan uca test edilmelidir."}, "en": {"title": "CTI enrichment enabled", "situation": "MISP/CTI integration is enabled and lookup, hit/no-hit and alert-return relations are being validated.", "evidence": "CTIC depends not only on a lookup call, but on the enrichment result returning to the alert and graph chain.", "impact": "Integration deployment is separated from operational CTI closure.", "action": "Test the alert → custom-misp → MISP → enrichment-rule → typed-CTI-object chain end to end."}}, "S7": {"tr": {"title": "Kısmi kanıt kapanışı", "situation": "Temel görünürlük zinciri çalışmaktadır; bazı edge ilişkileri eksik olduğu için tam kapanış sağlanmamıştır.", "evidence": "Observed edge sayısı artmış, missing edge sayısı azalmış olsa da sıfıra inmemiştir.", "impact": "SOC belirli davranışları izleyebilir; eksik zincirler açıklanabilir boşluk olarak korunur.", "action": "Reason code sıralamasıyla en yüksek etkili eksik ilişkiler önce kapatılmalıdır."}, "en": {"title": "Partial evidence closure", "situation": "The core visibility chain works, but some edges remain missing.", "evidence": "Observed edges increase and missing edges decrease, but missing relations do not reach zero.", "impact": "The SOC can monitor selected behavior while unresolved chains remain explicit gaps.", "action": "Prioritize the highest-impact missing relations using reason-code ordering."}}, "S7A": {"tr": {"title": "Kritik DC01 Sysmon kaybı", "situation": "Kritik domain controller üzerindeki Sysmon telemetrisi kaybedilmiştir.", "evidence": "Process, DNS ve davranışsal detection ilişkileri etkilenir; CWLC kritiklik ağırlığı nedeniyle belirgin düşer.", "impact": "Aynı telemetri kaybının kritik varlıkta oluşması, kritik olmayan endpoint kaybından daha yüksek operasyonel risk taşır.", "action": "DC01 Sysmon servisi, event-channel toplama ayarı, agent bağlantısı ve last_seen değeri doğrulanmalıdır."}, "en": {"title": "Critical DC01 Sysmon loss", "situation": "Sysmon telemetry is lost on the critical domain controller.", "evidence": "Process, DNS and behavioral detection relations are affected, while CWLC drops more because of criticality weighting.", "impact": "The same telemetry loss on a critical asset carries greater operational risk than a loss on a non-critical endpoint.", "action": "Validate the DC01 Sysmon service, event-channel collection, agent connection and last-seen value."}}, "S7B": {"tr": {"title": "Kritik olmayan WS01 Sysmon kaybı", "situation": "WS01 üzerinde beklenen Sysmon telemetrisi kaybedilmiştir.", "evidence": "Endpoint davranış görünürlüğü azalır; varlık kritiklik ağırlığı nedeniyle etkisi DC01 kaybından daha düşüktür.", "impact": "Model aynı tür kaybı varlık önemine göre farklı puanlayarak kritiklik duyarlılığını gösterir.", "action": "WS01 agent, Sysmon configuration ve Wazuh event-channel toplama ayarı kontrol edilmelidir."}, "en": {"title": "Non-critical WS01 Sysmon loss", "situation": "Expected Sysmon telemetry is lost on WS01.", "evidence": "Endpoint behavioral visibility decreases, but score impact is lower than the DC01 loss because of asset criticality.", "impact": "The model demonstrates criticality sensitivity by scoring the same loss differently according to asset importance.", "action": "Check the WS01 agent, Sysmon configuration and Wazuh event-channel collection."}}, "S8": {"tr": {"title": "Tarihsel doğrulama serisinde kapanış", "situation": "S0–S18 doğrulama serisinin tarihsel kapanış noktasıdır.", "evidence": "Seri içindeki beklenen ilişkiler gözlemlenmiş ve missing edge sayısı sıfıra indirilmiştir.", "impact": "Modelin boşlukları adım adım kapatabildiği gösterilir; bu veri kümesi yayın finalinden ayrı tutulur.", "action": "S8 tarihsel doğrulama kanıtı olarak korunmalı, final yayın veri kümesinin sayılarıyla birleştirilmemelidir."}, "en": {"title": "Closure in the historical validation series", "situation": "This is the historical closure point of the S0–S18 validation series.", "evidence": "Expected relations in the series are observed and the missing-edge count reaches zero.", "impact": "The model demonstrates stepwise closure of visibility gaps; this dataset remains separate from the publication final.", "action": "Preserve S8 as historical validation evidence and do not merge its counts with the publication final."}}, "S9": {"tr": {"title": "DC01 Security telemetrisi kaybı", "situation": "Domain controller Security kanalı gözlemlenmemektedir.", "evidence": "Kimlik doğrulama, hesap kullanımı ve Windows güvenlik olaylarına dayalı control ilişkileri etkilenir.", "impact": "Valid Accounts ve ilişkili tekniklerin kanıt zinciri zayıflar.", "action": "Windows auditing, Wazuh event-channel tanımı ve kanal freshness değeri doğrulanmalıdır."}, "en": {"title": "DC01 Security telemetry loss", "situation": "The domain-controller Security channel is not observed.", "evidence": "Authentication, account-use and Windows-security control relations are affected.", "impact": "Evidence for Valid Accounts and related techniques is weakened.", "action": "Validate Windows auditing, the Wazuh event-channel definition and channel freshness."}}, "S10": {"tr": {"title": "PowerShell telemetrisi kaybı", "situation": "PowerShell operational veya script-block telemetrisi kaybedilmiştir.", "evidence": "T1059.001 ve komut içeriğine dayalı detection ilişkileri zayıflar.", "impact": "Süreç oluşturma görülebilse bile komut bağlamı ve ayrıntılı yürütme kanıtı kaybolabilir.", "action": "Script Block Logging, Module Logging ve Wazuh PowerShell kanal toplaması doğrulanmalıdır."}, "en": {"title": "PowerShell telemetry loss", "situation": "PowerShell operational or script-block telemetry is lost.", "evidence": "T1059.001 and command-content detection relations are weakened.", "impact": "Process creation may remain visible while command context and detailed execution evidence are lost.", "action": "Validate Script Block Logging, Module Logging and Wazuh PowerShell-channel collection."}}, "S11": {"tr": {"title": "Linux authlog kaybı", "situation": "Linux kimlik doğrulama log kaynağı gözlemlenmemektedir.", "evidence": "SSH brute-force, başarılı ve başarısız oturum açma ilişkileri eksik kalır.", "impact": "Linux kimlik doğrulama davranışları için birincil kanıt kaynağı kaybolur.", "action": "auth.log/secure yolu, rsyslog üretimi, Wazuh localfile tanımı ve freshness kontrol edilmelidir."}, "en": {"title": "Linux auth-log loss", "situation": "The Linux authentication log source is not observed.", "evidence": "SSH brute-force and successful or failed logon relations remain missing.", "impact": "The primary evidence source for Linux authentication behavior is lost.", "action": "Validate the auth.log/secure path, rsyslog production, Wazuh localfile definition and freshness."}}, "S12": {"tr": {"title": "Firewall IOC alarmı var, CTI zinciri açık", "situation": "Firewall IOC olayı detection katmanında görünür; MISP/CTI enrichment ilişkileri tam kapanmamıştır.", "evidence": "Alert görülmesine rağmen lookup, hit, event/attribute ve typed CTI object ilişkilerinin bir bölümü eksiktir.", "impact": "SOC analisti alarmı görür; reputation, confidence, source ve enrichment bağlamı triage sırasında doğrulanamayabilir.", "action": "pfSense IOC alert → Wazuh rule → custom-misp → MISP → enrichment rule → CTI object zinciri doğrulanmalıdır."}, "en": {"title": "Firewall IOC alert present, CTI chain open", "situation": "The firewall IOC event is visible at the detection layer while MISP/CTI enrichment relations remain incomplete.", "evidence": "The alert exists, but some lookup, hit, event/attribute and typed-CTI-object relations are missing.", "impact": "The SOC analyst can see the alert, but reputation, confidence, source and enrichment context may not be verifiable during triage.", "action": "Validate the pfSense IOC alert → Wazuh rule → custom-misp → MISP → enrichment rule → CTI-object chain."}}, "S13": {"tr": {"title": "MISP lookup var, IOC hit yok", "situation": "MISP sorgusu çalışmıştır; ilgili indicator için hit oluşmamıştır.", "evidence": "lookup_executed ilişkisi gözlemlenirken misp_hit ilişkisi oluşmaz.", "impact": "Bu durum entegrasyon arızası değil, IOC'nin veri kümesinde bulunmaması olabilir. Hit ve no-hit ayrı yorumlanmalıdır.", "action": "Sorgu değeri, indicator tipi, to_ids filtresi ve no-hit Wazuh kuralı doğrulanmalıdır."}, "en": {"title": "MISP lookup executed, no IOC hit", "situation": "The MISP query executed, but no hit was produced for the indicator.", "evidence": "The lookup-executed relation is observed while the MISP-hit relation is absent.", "impact": "This may be a legitimate no-hit result rather than an integration failure. Hit and no-hit outcomes must be interpreted separately.", "action": "Validate the query value, indicator type, to_ids filter and no-hit Wazuh rule."}}, "S14": {"tr": {"title": "MITRE kapsamı genişledi", "situation": "Değerlendirme kapsamına yeni ATT&CK tekniği eklenmiştir.", "evidence": "Yeni teknik için control veya rule kanıtı henüz gözlemlenmediğinden MDC düşer.", "impact": "Model yeni beklentiyi görünür kılar ve sahte tam kapsama üretmez.", "action": "Yeni teknik için veri kaynağı, detection control, Wazuh kuralı ve kontrollü test tanımlanmalıdır."}, "en": {"title": "MITRE scope expanded", "situation": "A new ATT&CK technique is added to the evaluation scope.", "evidence": "MDC decreases because control or rule evidence for the new technique is not yet observed.", "impact": "The model makes the new expectation visible instead of preserving artificial full coverage.", "action": "Define the data source, detection control, Wazuh rule and controlled test for the new technique."}}, "S15": {"tr": {"title": "Telemetri freshness düşüşü", "situation": "Daha önce gözlemlenen telemetrinin son görülme zamanı freshness eşiğini aşmıştır.", "evidence": "İlişki geçmişte observed olsa bile TF metriği mevcut operasyonel güncelliği ayrı değerlendirir.", "impact": "Eski kanıtın varlığı, telemetrinin hâlâ aktığını garanti etmez.", "action": "last_seen değerleri, heartbeat, ingestion gecikmesi ve freshness eşikleri kontrol edilmelidir."}, "en": {"title": "Telemetry freshness degradation", "situation": "The last-seen time of previously observed telemetry exceeds the freshness threshold.", "evidence": "Even when a relation was observed historically, TF evaluates current operational recency separately.", "impact": "Historical evidence does not guarantee that telemetry is still flowing.", "action": "Check last-seen values, heartbeats, ingestion latency and freshness thresholds."}}, "S16": {"tr": {"title": "Detection rule boşluğu", "situation": "Beklenen kontrol etkin olmasına rağmen ilişkili Wazuh rule veya alert kanıtı gözlemlenmemektedir.", "evidence": "CAC düşer ve control-to-rule veya rule-to-alert ilişkileri missing kalır.", "impact": "Telemetri mevcut olsa bile detection mantığı olayı operasyonel alarm kanıtına dönüştürmez.", "action": "Rule ID, decoder eşleşmesi, koşullar, level ve alerts.json çıktısı doğrulanmalıdır."}, "en": {"title": "Detection-rule gap", "situation": "The expected control is enabled, but related Wazuh-rule or alert evidence is not observed.", "evidence": "CAC decreases and control-to-rule or rule-to-alert relations remain missing.", "impact": "Telemetry can exist while detection logic fails to convert it into operational alert evidence.", "action": "Validate the rule ID, decoder match, conditions, level and alerts.json output."}}, "S17": {"tr": {"title": "Düzeltme sonrası toparlanma", "situation": "Önceki senaryoda eksik olan telemetri veya kontrol ilişkileri yeniden gözlemlenmiştir.", "evidence": "Missing edge sayısı azalır, ilgili metrikler ve SACI skoru yükselir.", "impact": "Model boşluğu yalnızca tespit etmez; düzeltmenin kanıt zincirini geri getirip getirmediğini de gösterir.", "action": "Önceki ve sonraki reason code kayıtları karşılaştırılmalı, toparlanmanın kalıcılığı freshness ile doğrulanmalıdır."}, "en": {"title": "Post-remediation recovery", "situation": "Telemetry or control relations missing in the previous scenario are observed again.", "evidence": "The missing-edge count decreases and related metrics and SACI increase.", "impact": "The model not only detects the gap, but also shows whether remediation restores the evidence chain.", "action": "Compare before-and-after reason codes and validate persistence through freshness monitoring."}}, "S18": {"tr": {"title": "Legacy kontrol aktif kapsam dışında", "situation": "Senaryoya uygulanmayan legacy kontrol aktif değerlendirme kapsamından çıkarılmıştır.", "evidence": "Kontrol sıfır olarak cezalandırılmaz; N/A kabul edilir ve aktif ağırlıklar yeniden normalize edilir.", "impact": "Uygulanabilir olmayan beklentilerin skoru yapay biçimde düşürmesi engellenir.", "action": "Kapsam dışı bırakma gerekçesi ve aktif ağırlık normalizasyonu audit çıktısında açıkça gösterilmelidir."}, "en": {"title": "Legacy control outside the active scope", "situation": "A legacy control that is not applicable to the scenario is removed from the active evaluation scope.", "evidence": "The control is not penalized as zero; it is treated as N/A and active weights are renormalized.", "impact": "Inapplicable expectations do not artificially reduce the score.", "action": "Document the exclusion rationale and active-weight normalization in the audit output."}}};
  const $ = (id) => document.getElementById(id);
  const en = (document.documentElement.lang || "").toLowerCase().startsWith("en");
  const t = (tr, enText) => en ? enText : tr;
  const esc = (value) => String(value ?? "").replace(/[<>&"]/g, c => ({
    "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;"
  }[c]));

  async function getText(url) {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`${url} HTTP ${response.status}`);
    return response.text();
  }

  async function getJson(url) { return JSON.parse(await getText(url)); }

  function parseCSV(text) {
    if (!text.trim()) return [];
    const rows = [];
    let row = [], field = "", quoted = false;

    for (let i = 0; i < text.length; i++) {
      const c = text[i], next = text[i + 1];
      if (quoted) {
        if (c === '"' && next === '"') { field += '"'; i++; }
        else if (c === '"') quoted = false;
        else field += c;
      } else if (c === '"') quoted = true;
      else if (c === ",") { row.push(field); field = ""; }
      else if (c === "\n") { row.push(field.replace(/\r$/, "")); rows.push(row); row = []; field = ""; }
      else field += c;
    }

    if (field.length || row.length) { row.push(field.replace(/\r$/, "")); rows.push(row); }

    const headers = (rows.shift() || []).map(x => x.trim());
    return rows
      .filter(r => r.some(x => String(x).trim() !== ""))
      .map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
  }

  function scenarioId(item) {
    const raw = String(item.id || item.scenario || item.name || "");
    if (/final/i.test(raw) || String(item.kind || "").toLowerCase() === "canonical") return "FINAL";
    const match = raw.match(/S\d+[A-Za-z]?/i);
    return match ? match[0].toUpperCase() : raw.toUpperCase();
  }

  function scenarioSortKey(id) {
    if (id === "FINAL") return [-1, ""];
    const match = id.match(/^S(\d+)([A-Z]?)$/);
    return match ? [Number(match[1]), match[2]] : [999, id];
  }

  function field(item, keys, fallback) {
    for (const key of keys) if (item[key]) return item[key];
    const base = item.base || item.dir || "";
    return base ? `${String(base).replace(/\/$/, "")}/${fallback}` : "";
  }

  function labelFor(item, id) {
    return en
      ? item.label_en || item.title_en || item.label || item.title || id
      : item.label_tr || item.title_tr || item.label || item.title || id;
  }

  function scoreMap(rows) {
    const result = {};
    if (rows.length === 1) {
      Object.entries(rows[0]).forEach(([key, value]) => {
        const k = key.toUpperCase();
        if (["CWLC", "LC", "CAC", "MDC", "CTIC", "TF", "SACI"].includes(k)) result[k === "LC" ? "CWLC" : k] = value;
      });
    }
    rows.forEach(row => {
      const k = String(row.metric || row.name || row.component || "").toUpperCase();
      if (k) result[k === "LC" ? "CWLC" : k] = row.score ?? row.value ?? row.result ?? "";
    });
    return result;
  }

  function normalizeCyjs(raw) {
    if (Array.isArray(raw)) return raw;
    if (Array.isArray(raw.elements)) return raw.elements;
    if (raw.elements?.nodes && raw.elements?.edges) return [...raw.elements.nodes, ...raw.elements.edges];
    if (raw.nodes && raw.edges) return [...raw.nodes, ...raw.edges];
    return [];
  }

  function graphInfo(raw) {
    const elements = normalizeCyjs(raw);
    const nodes = elements.filter(x => !(x?.data?.source && x?.data?.target));
    const edges = elements.filter(x => x?.data?.source && x?.data?.target);
    const observed = edges.filter(x =>
      x.data.observed === 1 || x.data.observed === true ||
      String(x.data.observed) === "1" || String(x.data.observed).toLowerCase() === "true"
    ).length;

    const ids = new Set(nodes.map(x => String(x?.data?.id ?? "")));
    const undeclared = [...new Set(
      edges.flatMap(x => [String(x.data.source), String(x.data.target)]).filter(id => id && !ids.has(id))
    )];

    const mitre = nodes
      .filter(x => {
        const d = x.data || {};
        const type = d.type || d.node_type || d.group || "";
        return type === "mitre_technique" || /^MITRE:T\d{4}/.test(String(d.id || ""));
      })
      .map(x => {
        const d = x.data || {};
        return {
          id: String(d.technique_id || d.id || "").replace(/^MITRE:/, ""),
          name: d.technique_name || d.label || d.name || d.id || ""
        };
      });

    return { nodes: nodes.length, edges: edges.length, observed, missing: edges.length - observed, undeclared, mitre };
  }

  function techniqueUrl(id) {
    const clean = String(id).replace(/^MITRE:/i, "");
    const [base, sub] = clean.split(".");
    return `https://attack.mitre.org/techniques/${base}/${sub ? sub + "/" : ""}`;
  }

  function metric(data, key) {
    const value = data.scores[key];
    return value === undefined || value === "" ? "-" : value;
  }

  function metricGrid(data) {
    return `<div class="metric-grid">${
      ["CWLC", "CAC", "MDC", "CTIC", "TF", "SACI"].map(key => `
        <div class="metric-card"><span>${key}</span><strong>${esc(metric(data, key))}</strong></div>
      `).join("")
    }</div>`;
  }

  function reportText(data) {
    const record = REPORTS[data.id] || REPORTS.FINAL;
    return record[en ? "en" : "tr"];
  }

  function longReport(data) {
    const r = reportText(data);
    return `
      <div class="long-report">
        <section class="report-block"><h4>${t("Durum", "Situation")}</h4><p>${esc(r.situation)}</p></section>
        <section class="report-block"><h4>${t("Kanıt yorumu", "Evidence interpretation")}</h4><p>${esc(r.evidence)}</p></section>
        <section class="report-block"><h4>${t("Operasyonel anlam", "Operational meaning")}</h4><p>${esc(r.impact)}</p></section>
        <section class="report-block"><h4>${t("Önerilen doğrulama", "Recommended validation")}</h4><p>${esc(r.action)}</p></section>
      </div>
    `;
  }

  function mitreHtml(data) {
    if (!data.graph.mitre.length) return "";
    return `
      <div class="mitre-context">
        <h4>${t("MITRE ATT&CK bağlamı", "MITRE ATT&CK context")}</h4>
        <div class="mitre-links">
          ${data.graph.mitre.map(item => `
            <a href="${techniqueUrl(item.id)}" target="_blank" rel="noopener">
              <strong>${esc(item.id)}</strong><span>${esc(item.name)}</span>
            </a>
          `).join("")}
        </div>
      </div>
    `;
  }

  function renderFinal(data) {
    const structural = data.graph.undeclared.length
      ? `<div class="structural-note">
          <strong>${t("Yapısal bütünlük notu:", "Structural integrity note:")}</strong>
          ${t(
            "İlişki kapanışı tamamdır; ancak edge tablosunda referans edilen bazı uçlar node tablosunda açıkça beyan edilmemiştir. Bu durum skoru değiştirmez ve audit bulgusu olarak korunur.",
            "Relation closure is complete; however, some endpoints referenced by the edge table are not explicitly declared in the node table. This does not change the score and remains documented as an audit finding."
          )}
          <br><code>${esc(data.graph.undeclared.join(", "))}</code>
        </div>`
      : "";

    $("finalReport").innerHTML = `
      <div class="final-report-top">
        <div><h3>${t("Final closure yorumu", "Final closure interpretation")}</h3><p>${esc(data.label)}</p></div>
        <span class="status-chip">${t("Kapanış tamam", "Closure complete")}</span>
      </div>
      ${metricGrid(data)}
      <div class="scenario-report-grid">
        <section class="report-block">
          <h4>${t("Graph kapanışı", "Graph closure")}</h4>
          <p>${t(
            `Toplam ${data.graph.edges} ilişkinin ${data.graph.observed} tanesi gözlemlenmiş, ${data.graph.missing} tanesi eksik kalmıştır.`,
            `${data.graph.observed} of ${data.graph.edges} relations are observed and ${data.graph.missing} are missing.`
          )}</p>
        </section>
        <section class="report-block">
          <h4>${t("Yorumlama sınırı", "Interpretation boundary")}</h4>
          <p>${t(
            "SACI=100 yalnızca beyan edilen değerlendirme kapsamındaki görünürlük ilişkilerinin doğrulandığını gösterir; mutlak güvenlik garantisi değildir.",
            "SACI=100 only indicates that visibility relations within the declared evaluation scope are validated; it is not an absolute security guarantee."
          )}</p>
        </section>
      </div>
      ${longReport(data)}
      ${structural}
    `;
  }

  function renderScenario(data) {
    const r = reportText(data);
    $("scenarioReport").innerHTML = `
      <h3>${esc(r.title)}</h3>
      <p class="scenario-subtitle">${esc(data.label)}</p>
      ${metricGrid(data)}
      <div class="scenario-report-grid">
        <section class="report-block">
          <h4>${t("Graph durumu", "Graph state")}</h4>
          <p>${t(
            `${data.graph.observed} observed, ${data.graph.missing} missing edge bulunmaktadır.`,
            `The graph contains ${data.graph.observed} observed and ${data.graph.missing} missing edges.`
          )}</p>
        </section>
        <section class="report-block">
          <h4>${t("Policy-guided sonuç", "Policy-guided outcome")}</h4>
          <p>${data.graph.missing === 0
            ? t("Eksik ilişki bulunmadığı için veri kümesi tanımlı kapsamda kapanış olarak yorumlanır.",
                "Because no relation is missing, the dataset is interpreted as closure within the declared scope.")
            : t("Eksik ilişkiler bulunduğu için sonuç kısmi kapsama olarak yorumlanır; ilgili reason code ve edge kayıtları incelenmelidir.",
                "Because missing relations exist, the result is interpreted as partial coverage and relevant reason-code and edge records should be reviewed.")
          }</p>
        </section>
      </div>
      ${longReport(data)}
      ${mitreHtml(data)}
      <div class="explanation-boundary">
        <strong>${t("Sınır:", "Boundary:")}</strong>
        ${t(
          "Bu açıklama yapılandırılmış SACI metrikleri, graph ilişkileri ve senaryo politikasından üretilir. LLM yalnızca yapılandırılmış raporu yeniden ifade edebilir; skoru hesaplamaz, değiştirmez veya geçersiz kılmaz.",
          "This explanation is produced from structured SACI metrics, graph relations and scenario policy. An LLM may only rephrase the structured report; it does not calculate, modify or override the score."
        )}
      </div>
    `;

    $("openGraph").href = `graph.html?scenario=${encodeURIComponent(data.id)}`;
    $("openEvidence").href = `evidence.html#scenario-${encodeURIComponent(data.id)}`;
  }

  async function loadItem(item) {
    const id = scenarioId(item);
    const scorePath = field(item, ["scores", "score", "score_csv"], "saci_scores.csv");
    const graphPath = field(item, ["graph", "cyjs", "graph_cyjs"], "saci_graph.cyjs");
    let scores = [], graph = {};
    try { scores = parseCSV(await getText(scorePath)); } catch (_) {}
    try { graph = await getJson(graphPath); } catch (_) {}
    return { id, label: labelFor(item, id), scores: scoreMap(scores), graph: graphInfo(graph) };
  }

  async function init() {
    try {
      const manifest = await getJson("data/scenarios/manifest.json");
      const items = manifest.datasets || manifest.scenarios || [];
      if (!items.length) throw new Error("Scenario manifest is empty.");

      const datasets = await Promise.all(items.map(loadItem));
      datasets.sort((a, b) => {
        const ka = scenarioSortKey(a.id), kb = scenarioSortKey(b.id);
        return ka[0] - kb[0] || String(ka[1]).localeCompare(String(kb[1]));
      });

      const finalData = datasets.find(x => x.id === "FINAL") || datasets[0];
      renderFinal(finalData);

      const select = $("scenarioSelect");
      select.innerHTML = datasets.map(data =>
        `<option value="${esc(data.id)}">${esc(data.id === "FINAL" ? "Final" : data.id)} — ${esc(data.label)}</option>`
      ).join("");

      const requested = String(new URLSearchParams(location.search).get("scenario") || "").toUpperCase();
      if (requested && datasets.some(x => x.id === requested)) select.value = requested;

      const choose = () => {
        const data = datasets.find(x => x.id === select.value) || finalData;
        renderScenario(data);
        const url = new URL(location.href);
        url.searchParams.set("scenario", data.id);
        history.replaceState(null, "", url);
      };

      select.addEventListener("change", choose);
      choose();

      $("loadingState").hidden = true;
      $("reportContent").hidden = false;
    } catch (error) {
      console.error(error);
      $("loadingState").textContent = t(
        `Açıklama verileri yüklenemedi: ${error.message}`,
        `Explanation data could not be loaded: ${error.message}`
      );
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
