#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / "docs"

GRAPH_PAGES = [
    DOCS / "graph.html",
    DOCS / "en" / "graph.html",
]

ALL_HTML = list(DOCS.glob("*.html")) + list((DOCS / "en").glob("*.html"))

MANIFESTS = [
    DOCS / "data" / "scenarios" / "manifest.json",
    DOCS / "en" / "data" / "scenarios" / "manifest.json",
]

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "backups" / f"final_scenario_explanation_{STAMP}"


REPORT_CSS = r'''
<!-- SACI_SCENARIO_REPORT_UI_START -->
<style id="saci-scenario-report-ui">
  body[data-page="graph"] .graph-analysis {
    align-items: start !important;
  }

  body[data-page="graph"] .analysis-panel {
    height: auto !important;
    min-height: 0 !important;
    align-self: start !important;
  }

  body[data-page="graph"] .saci-expanded-interpretation {
    display: grid;
    gap: 14px;
    margin-top: 14px;
  }

  body[data-page="graph"] .saci-explanation-block,
  body[data-page="graph"] .saci-scenario-report {
    padding: 16px;
    border: 1px solid
      color-mix(in srgb, var(--line) 62%, transparent);
    border-radius: 15px;
    background:
      color-mix(
        in srgb,
        var(--surface, var(--bg)) 82%,
        transparent
      );
  }

  body[data-page="graph"] .saci-explanation-block h4,
  body[data-page="graph"] .saci-scenario-report h4 {
    max-width: none !important;
    margin: 0 0 11px !important;
    color: var(--text);
    font-size: 17px !important;
    font-weight: 720 !important;
    line-height: 1.3 !important;
  }

  body[data-page="graph"] .saci-explanation-block p,
  body[data-page="graph"] .saci-scenario-report p {
    max-width: 82ch !important;
    margin: 0 0 12px;
    color: var(--muted);
    font-size: 14.5px !important;
    line-height: 1.74 !important;
  }

  body[data-page="graph"] .saci-explanation-block p:last-child,
  body[data-page="graph"] .saci-scenario-report p:last-child {
    margin-bottom: 0;
  }

  body[data-page="graph"] .saci-result-list {
    display: grid;
    grid-template-columns:
      repeat(auto-fit, minmax(145px, 1fr));
    gap: 8px;
    margin: 13px 0 0;
    padding: 0;
    list-style: none;
  }

  body[data-page="graph"] .saci-result-list li {
    min-width: 0;
    padding: 10px 11px;
    border: 1px solid
      color-mix(in srgb, var(--line) 54%, transparent);
    border-radius: 12px;
    background:
      color-mix(in srgb, var(--bg) 78%, transparent);
  }

  body[data-page="graph"] .saci-result-list span {
    display: block;
    margin-bottom: 5px;
    color: var(--muted);
    font-size: 11.5px;
    font-weight: 650;
    line-height: 1.35;
  }

  body[data-page="graph"] .saci-result-list strong {
    display: block;
    color: var(--text);
    font-size: 18px;
    font-weight: 720;
    line-height: 1.2;
  }

  body[data-page="graph"] .saci-report-kicker {
    display: block;
    margin-bottom: 7px;
    color: var(--accent);
    font-size: 11.5px;
    font-weight: 750;
    letter-spacing: .09em;
    text-transform: uppercase;
  }

  body[data-page="graph"] .saci-report-grid {
    display: grid;
    grid-template-columns:
      repeat(3, minmax(0, 1fr));
    gap: 10px;
    margin-top: 13px;
  }

  body[data-page="graph"] .saci-report-section {
    min-width: 0;
    padding: 13px;
    border: 1px solid
      color-mix(in srgb, var(--line) 54%, transparent);
    border-radius: 13px;
    background:
      color-mix(in srgb, var(--bg) 77%, transparent);
  }

  body[data-page="graph"] .saci-report-section > span {
    display: block;
    margin-bottom: 8px;
    color: var(--accent);
    font-size: 11.5px;
    font-weight: 750;
    letter-spacing: .04em;
    text-transform: uppercase;
  }

  body[data-page="graph"] .saci-report-section p {
    margin: 0 !important;
    color: var(--muted);
    font-size: 13.5px !important;
    line-height: 1.68 !important;
    overflow-wrap: anywhere;
  }

  body[data-page="graph"] .saci-report-note {
    margin-top: 13px;
    padding: 11px 13px;
    border-left: 2px solid var(--accent);
    border-radius: 0 10px 10px 0;
    background:
      color-mix(
        in srgb,
        var(--accent) 6%,
        transparent
      );
    color: var(--muted);
    font-size: 13px;
    line-height: 1.65;
  }

  body[data-page="graph"] .saci-report-note strong {
    color: var(--text);
  }

  @media (max-width: 1050px) {
    body[data-page="graph"] .saci-report-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 620px) {
    body[data-page="graph"] .saci-result-list {
      grid-template-columns: 1fr 1fr;
    }
  }
</style>
<!-- SACI_SCENARIO_REPORT_UI_END -->
'''


REPORT_JS = r'''
<!-- SACI_SCENARIO_REPORT_START -->
<script id="saci-scenario-report">
(() => {
  const isEnglish = () =>
    (document.documentElement.lang || "")
      .toLowerCase()
      .startsWith("en");

  const valueOf = (id) => {
    const node = document.getElementById(id);
    return node ? node.textContent.trim() : "-";
  };

  function metricValues() {
    const result = {};

    document.querySelectorAll(".score-chip").forEach((card) => {
      const key = card.querySelector("b")?.textContent.trim();
      const value = card.querySelector("strong")?.textContent.trim();

      if (key) {
        result[key.toUpperCase()] = value || "-";
      }
    });

    result.SACI = result.SACI || valueOf("saciScore");
    result.DECLARED = valueOf("declaredNodeCount");
    result.RENDERED = valueOf("nodeCount");
    result.EDGES = valueOf("edgeCount");
    result.OBSERVED = valueOf("observedCount");
    result.MISSING = valueOf("missingCount");

    return result;
  }

  function uniqueMitreCount() {
    const values = new Set();

    document.querySelectorAll(
      ".tech-id, [data-technique-id]"
    ).forEach((node) => {
      const value =
        node.dataset.techniqueId ||
        node.textContent.trim();

      if (value) {
        values.add(value);
      }
    });

    return values.size;
  }

  function currentScenario() {
    const select = document.getElementById("scenarioSelect");
    const option = select?.selectedOptions?.[0];

    return {
      id: String(select?.value || "final").toUpperCase(),
      label: String(option?.textContent || "Final").trim()
    };
  }

  function trReport(id, m) {
    const generic = {
      title: "Seçili senaryonun kanıt zinciri değerlendirildi",
      finding:
        `Seçili senaryoda ${m.EDGES} ilişki bulunmaktadır. ` +
        `${m.OBSERVED} ilişki gözlemlenmiş, ${m.MISSING} ilişki ise ` +
        `eksik kalmıştır. SACI skoru ${m.SACI} düzeyindedir.`,
      impact:
        "Eksik ilişkiler, görünürlük zincirinin asset, log source, " +
        "detection control, Wazuh rule, MITRE veya CTI katmanlarından " +
        "hangisinde kesildiğinin ayrıca incelenmesini gerektirir.",
      action:
        "Eksik edge kayıtlarının source, target, relationship ve reason " +
        "code alanları kontrol edilmeli; ilgili telemetri veya kontrol " +
        "yeniden doğrulandıktan sonra senaryo tekrar çalıştırılmalıdır."
    };

    const reports = {
      FINAL: {
        title: "Tanımlı kapsamda kanıt kapanışı sağlandı",
        finding:
          `Final veri kümesinde ${m.OBSERVED}/${m.EDGES} ilişki ` +
          `gözlemlenmiş ve eksik ilişki sayısı ${m.MISSING} olarak ` +
          `hesaplanmıştır. SACI skoru ${m.SACI} düzeyindedir.`,
        impact:
          "Beklenen telemetri, detection, MITRE ve CTI ilişkileri " +
          "tanımlı yayın kapsamı içinde izlenebilir durumdadır. Bu sonuç " +
          "mutlak güvenlik garantisi değil, beyan edilen kapsamın kanıtla " +
          "doğrulanmasıdır.",
        action:
          "Final veri kümesi yayın kanıtı olarak sabitlenmeli; inventory " +
          "drift, freshness düşüşü ve yeni kapsam eklemeleri ayrı senaryo " +
          "olarak izlenmelidir."
      },

      S0: {
        title: "SIEM katmanı bulunmadığı için kanıt zinciri kurulamıyor",
        finding:
          "Telemetriyi merkezi olarak toplayacak ve ilişkilendirecek SIEM " +
          "katmanı bulunmadığından asset-to-log-source ve log-source-to-" +
          "platform ilişkileri doğrulanamamaktadır.",
        impact:
          "Merkezi görünürlük, alarm korelasyonu, MITRE eşlemesi ve CTI " +
          "zenginleştirmesi üretilemez. Skor düşüşü bir detection " +
          "başarısızlığından önce temel gözlem altyapısının yokluğunu gösterir.",
        action:
          "Wazuh platformu kurulmalı, veri kabulü doğrulanmalı ve ilk " +
          "platform düğümleri graph üzerinde gözlemlenmelidir."
      },

      S1: {
        title: "SIEM kurulmuş ancak kanıt kapsamı henüz oluşmamış",
        finding:
          "Wazuh platformu görünür durumdadır; ancak varlık, log kaynağı " +
          "ve kontrol ilişkilerinin önemli bölümü henüz tanımlı veya " +
          "gözlemlenmiş değildir.",
        impact:
          "Platformun çalışması tek başına operasyonel görünürlük sağlamaz. " +
          "Agent bağlantıları ve beklenen telemetri kaynakları olmadan skor " +
          "kurulum durumunu gösterir, kapsama durumunu göstermez.",
        action:
          "Varlık envanteri tanımlanmalı, agent ve syslog kaynakları " +
          "bağlanmalı, beklenen log source ilişkileri oluşturulmalıdır."
      },

      S2: {
        title: "Envanter tanımlı ancak gözlenen telemetri yetersiz",
        finding:
          "Varlıklar ve beklenen izleme kapsamı beyan edilmiştir. Buna " +
          "karşılık beklenen log kaynaklarının tamamı graph üzerinde " +
          "observed ilişkiye dönüşmemiştir.",
        impact:
          "Model hangi varlığın izlenmesi gerektiğini bilir; ancak " +
          "telemetri gelmediği için görünürlük yalnızca beyan seviyesinde kalır.",
        action:
          "Her varlık için expected log source listesi ile Wazuh üzerinde " +
          "gözlenen kaynaklar karşılaştırılmalı ve eksik agent/channel " +
          "yapılandırmaları tamamlanmalıdır."
      },

      S3: {
        title: "Log kaynakları bağlı, detection zinciri henüz tamamlanmamış",
        finding:
          "Temel telemetri Wazuh tarafından alınmaktadır; ancak bu veriyi " +
          "detection control ve rule kanıtına dönüştüren ilişkiler eksiktir.",
        impact:
          "Veri geliyor olsa da beklenen davranışların alarm ve teknik " +
          "kapsamasına dönüştüğü kanıtlanamaz.",
        action:
          "Decoder, Wazuh rule ve control mapping kayıtları doğrulanmalı; " +
          "kontrollü test olaylarıyla rule-to-alert zinciri gözlemlenmelidir."
      },

      S4: {
        title: "Detection kontrolleri etkin ancak üst bağlam eksik",
        finding:
          `Kontrol ve alert kapsamı ${m.CAC || "-"} düzeyindedir. ` +
          "Bununla birlikte MITRE veya CTI ilişkilerinin bir bölümü henüz " +
          "kanıt zincirine bağlanmamıştır.",
        impact:
          "Alarm üretimi görünür olsa da saldırı davranışının teknik ve " +
          "istihbarat bağlamı eksik kalabilir.",
        action:
          "Her etkin kontrol için rule, MITRE technique ve gerektiğinde " +
          "CTI object ilişkileri tamamlanmalıdır."
      },

      S5: {
        title: "MITRE kapsamı tanımlı ancak tüm teknikler kanıtlanmamış",
        finding:
          `MDC metriği ${m.MDC || "-"} düzeyindedir. Tanımlı ATT&CK ` +
          "kapsamındaki bazı tekniklerin detection kanıtı eksik veya " +
          "gözlemlenmemiştir.",
        impact:
          "Kapsam listesinde bulunan bir teknik, yalnızca adı tanımlandığı " +
          "için kapsanmış sayılmaz; rule/control kanıtıyla bağlanması gerekir.",
        action:
          "Eksik teknikler için ilgili detection kontrolü ve Wazuh kuralı " +
          "belirlenmeli, senaryo testiyle covered ilişkisi doğrulanmalıdır."
      },

      S6: {
        title: "CTI enrichment etkinleştirilmiş ancak kapanış doğrulanıyor",
        finding:
          `CTIC metriği ${m.CTIC || "-"} düzeyindedir. Wazuh, entegrasyon, ` +
          "MISP ve typed CTI object ilişkilerinin tamamı aynı alarm zinciri " +
          "üzerinde doğrulanmalıdır.",
        impact:
          "Lookup işleminin çalışması tek başına CTI kapanışı değildir. " +
          "IOC sonucu alarm ve graph ilişkisine geri dönmelidir.",
        action:
          "Wazuh alert → custom-misp → MISP lookup → hit/no-hit event → " +
          "enrichment rule → CTI object zinciri uçtan uca kontrol edilmelidir."
      },

      S7: {
        title: "Kısmi kanıt kapanışı sağlandı",
        finding:
          `${m.MISSING} eksik ilişki kalmıştır. SACI skoru ${m.SACI}, ` +
          `MDC ${m.MDC || "-"} ve CTIC ${m.CTIC || "-"} düzeyindedir.`,
        impact:
          "Temel görünürlük zinciri çalışmaktadır; ancak eksik edge " +
          "kayıtları belirli varlıkların veya kontrol bağlamlarının tam " +
          "izlenmesini engellemektedir.",
        action:
          "Reason code sıralaması kullanılarak en yüksek etkili eksik " +
          "ilişkiler önce kapatılmalıdır."
      },

      S7A: {
        title: "Kritik DC01 Sysmon telemetrisi kaybedildi",
        finding:
          "Kritik domain controller üzerinde beklenen Sysmon kanalı " +
          "gözlemlenmediği için process, DNS ve davranışsal detection " +
          "zincirleri etkilenmektedir.",
        impact:
          "Kritikliği yüksek bir varlıktaki kayıp, aynı kaybın sıradan bir " +
          "endpointte oluşmasına göre CWLC ve ilişkili kontroller üzerinde " +
          "daha yüksek etki üretmelidir.",
        action:
          "DC01 Sysmon servisi, agent localfile/channel ayarları, event " +
          "forwarding ve son görülme zamanı doğrulanmalıdır."
      },

      S7B: {
        title: "Kritik olmayan WS01 Sysmon telemetrisi kaybedildi",
        finding:
          "WS01 üzerinde beklenen Sysmon kaynağı gözlemlenmemektedir. " +
          "Eksiklik endpoint davranış görünürlüğünü azaltmaktadır.",
        impact:
          "Kayıp gerçek bir görünürlük boşluğudur; ancak varlık kritiklik " +
          "ağırlığı nedeniyle DC01 üzerindeki benzer kayıptan daha düşük " +
          "skor etkisi üretmesi beklenir.",
        action:
          "WS01 agent durumu, Sysmon configuration ve Wazuh kanal toplama " +
          "ayarları kontrol edilmelidir."
      },

      S8: {
        title: "Tarihsel doğrulama serisinde final kapanış sağlandı",
        finding:
          `${m.OBSERVED}/${m.EDGES} ilişki gözlemlenmiş ve eksik ilişki ` +
          `sayısı ${m.MISSING} olmuştur. SACI skoru ${m.SACI} düzeyindedir.`,
        impact:
          "Tarihsel senaryo serisi içinde tanımlanan boşlukların kapatıldığı " +
          "gösterilir. Bu veri kümesi yayın finalinden ayrı bir doğrulama " +
          "anıdır.",
        action:
          "Bu sonuç tarihsel kapanış kanıtı olarak korunmalı; kanonik final " +
          "yayın veri kümesiyle sayısal olarak birleştirilmemelidir."
      },

      S9: {
        title: "Kritik DC01 Security telemetrisi kaybedildi",
        finding:
          "Domain controller Security kanalı gözlemlenmediği için kimlik " +
          "doğrulama, hesap kullanımı ve Windows güvenlik olaylarına dayalı " +
          "kontroller etkilenmektedir.",
        impact:
          "Kimlik ve erişim davranışlarının görünürlüğü azalır; Valid " +
          "Accounts ve benzeri tekniklerin kanıt zinciri eksik kalabilir.",
        action:
          "Windows Security auditing, agent eventchannel ayarı ve kanalın " +
          "son görülme zamanı doğrulanmalıdır."
      },

      S10: {
        title: "Endpoint PowerShell telemetrisi kaybedildi",
        finding:
          "Beklenen PowerShell operational veya script-block telemetrisi " +
          "gözlemlenmediği için T1059.001 kapsamındaki detection kanıtları " +
          "zayıflamaktadır.",
        impact:
          "PowerShell tabanlı komut yürütme davranışları yalnızca process " +
          "creation verisine bağlı kalabilir ve içerik bağlamı kaybolabilir.",
        action:
          "PowerShell logging policy, Script Block Logging, Module Logging " +
          "ve Wazuh kanal toplama ayarları doğrulanmalıdır."
      },

      S11: {
        title: "Linux authlog telemetrisi kaybedildi",
        finding:
          `Linux kimlik doğrulama kaynağı gözlemlenmediği için ${m.MISSING} ` +
          "ilişki eksik kalmıştır. CAC ${m.CAC || "-"} ve SACI " +
          `${m.SACI} düzeyindedir.`,
        impact:
          "SSH brute-force, başarılı veya başarısız oturum açma ve kimlik " +
          "doğrulama davranışlarının kanıt zinciri zayıflar.",
        action:
          "auth.log veya secure dosya yolu, rsyslog üretimi, Wazuh localfile " +
          "tanımı ve log freshness kontrol edilmelidir."
      },

      S12: {
        title: "Firewall IOC alarmı var, CTI bağlam zinciri kapanmamış",
        finding:
          `Firewall IOC olayı detection tarafında görünmesine rağmen CTIC ` +
          `${m.CTIC || "-"} düzeyinde kalmış ve ${m.MISSING} ilişki eksik ` +
          "olarak gözlemlenmiştir. IOC alarmı ile MISP/CTI bağlamı arasındaki " +
          "beklenen zincir tam kurulamamıştır.",
        impact:
          "SOC analisti alarmı görebilir; ancak indicator reputation, MISP " +
          "event/attribute, confidence, kaynak ve enrichment sonucu alarm " +
          "üzerinde doğrulanabilir olmayabilir. Bu nedenle triage bağlamı " +
          "eksik kalır.",
        action:
          "pfSense IOC alert → Wazuh rule → custom-misp query → MISP hit/no-hit " +
          "event → enrichment rule → typed CTI object ilişkileri tek tek " +
          "doğrulanmalıdır."
      },

      S13: {
        title: "MISP lookup çalıştı ancak IOC eşleşmesi oluşmadı",
        finding:
          `CTIC metriği ${m.CTIC || "-"} düzeyindedir. Lookup işlemi ` +
          "gerçekleşmiş ancak ilgili indicator için MISP hit kanıtı " +
          "üretilmemiştir.",
        impact:
          "Bu durum entegrasyonun bozuk olduğunu değil, sorgulanan IOC'nin " +
          "MISP veri kümesinde bulunmadığını gösterebilir. Hit ve no-hit " +
          "sonuçları ayrı reason code ile yorumlanmalıdır.",
        action:
          "MISP sorgu değeri, indicator tipi, to_ids filtresi, event/attribute " +
          "durumu ve no-hit Wazuh kuralı kontrol edilmelidir."
      },

      S14: {
        title: "MITRE kapsamı genişledi, yeni teknik için detection boşluğu oluştu",
        finding:
          `MDC metriği ${m.MDC || "-"} düzeyine düşmüştür. Yeni eklenen ` +
          "ATT&CK tekniği için beklenen control/rule kanıtı henüz graph " +
          "üzerinde gözlemlenmemiştir.",
        impact:
          "Kapsam genişletildiğinde skorun düşmesi modelin yeni beklentiyi " +
          "cezalandırdığını ve sahte tam kapsama üretmediğini gösterir.",
        action:
          "Yeni teknik için detection kontrolü, veri kaynağı, Wazuh kuralı " +
          "ve kontrollü doğrulama senaryosu tanımlanmalıdır."
      },

      S15: {
        title: "Telemetri güncelliği düşmüş",
        finding:
          `TF metriği ${m.TF || "-"} düzeyindedir. İlişkiler geçmişte ` +
          "gözlemlenmiş olsa da son görülme zamanları tanımlı freshness " +
          "eşiğini aşmıştır.",
        impact:
          "Eski kanıt, mevcut operasyonel görünürlüğün sürdüğünü garanti " +
          "etmez. Kapsama var görünürken telemetri fiilen durmuş olabilir.",
        action:
          "Her log source için last_seen değeri, freshness eşikleri, agent " +
          "heartbeat ve ingestion gecikmesi kontrol edilmelidir."
      },

      S16: {
        title: "Detection rule boşluğu oluştu",
        finding:
          `CAC metriği ${m.CAC || "-"} düzeyindedir. Beklenen kontrol etkin ` +
          "olmasına rağmen ilişkili Wazuh rule veya alert kanıtı " +
          "gözlemlenmemiştir.",
        impact:
          "Telemetri mevcut olsa bile detection mantığı olayı alarm " +
          "kanıtına dönüştürmediği için teknik kapsamı operasyonel değildir.",
        action:
          "Rule ID, decoder eşleşmesi, rule level, field condition, enabled " +
          "kontrol durumu ve test olayının alerts.json çıktısı doğrulanmalıdır."
      },

      S17: {
        title: "Düzeltme sonrasında görünürlük geri kazanıldı",
        finding:
          "Önceki senaryoda eksik olan telemetri veya kontrol ilişkileri " +
          "yeniden gözlemlenmiş ve SACI skoru toparlanmıştır.",
        impact:
          "Model yalnızca boşluğu tespit etmekle kalmamış, düzeltme sonrası " +
          "kanıt zincirinin yeniden kurulduğunu da göstermiştir.",
        action:
          "Önceki ve sonraki reason code kayıtları karşılaştırılmalı; " +
          "düzeltmenin kalıcı olduğu freshness izlemesiyle doğrulanmalıdır."
      },

      S18: {
        title: "Legacy kontrol değerlendirme kapsamı dışında bırakıldı",
        finding:
          "İlgili kontrol aktif değerlendirme kapsamından çıkarılmış ve " +
          "N/A olarak ele alınmıştır. Aktif metrik ağırlıkları yeniden " +
          "normalize edilmiştir.",
        impact:
          "Kapsam dışı kontrolün sıfır puanla cezalandırılmaması, senaryoya " +
          "uygulanabilir olmayan beklentilerin skoru yapay biçimde " +
          "düşürmesini engeller.",
        action:
          "Kontrolün neden kapsam dışı olduğu, kapsam kararı ve aktif ağırlık " +
          "normalizasyonu audit çıktısında açıkça gösterilmelidir."
      }
    };

    return reports[id] || generic;
  }

  function enReport(id, m) {
    const generic = {
      title: "The evidence chain of the selected scenario was evaluated",
      finding:
        `The selected scenario contains ${m.EDGES} relations. ` +
        `${m.OBSERVED} are observed and ${m.MISSING} are missing. ` +
        `The SACI score is ${m.SACI}.`,
      impact:
        "Missing relations require inspection of the asset, log-source, " +
        "detection-control, Wazuh-rule, MITRE or CTI layer where the " +
        "visibility chain is interrupted.",
      action:
        "Review the source, target, relationship and reason-code fields of " +
        "the missing edges, validate the relevant telemetry or control, " +
        "and rerun the scenario."
    };

    const reports = {
      FINAL: {
        title: "Evidence closure was achieved within the declared scope",
        finding:
          `The final dataset contains ${m.OBSERVED}/${m.EDGES} observed ` +
          `relations and ${m.MISSING} missing relations. The SACI score ` +
          `is ${m.SACI}.`,
        impact:
          "The expected telemetry, detection, MITRE and CTI relations are " +
          "traceable within the declared publication scope. This is not an " +
          "absolute security guarantee.",
        action:
          "Freeze this dataset as publication evidence and monitor inventory " +
          "drift, freshness decay and future scope changes separately."
      },

      S0: {
        title: "The evidence chain cannot be established without a SIEM layer",
        finding:
          "There is no central platform to collect and correlate telemetry; " +
          "asset-to-log-source and log-source-to-platform relations cannot " +
          "be validated.",
        impact:
          "Central visibility, alert correlation, MITRE mapping and CTI " +
          "enrichment cannot be produced.",
        action:
          "Deploy Wazuh, validate data ingestion and observe the initial " +
          "platform relations on the graph."
      },

      S1: {
        title: "The SIEM is deployed but the evidence scope is incomplete",
        finding:
          "Wazuh is visible, but a substantial part of the asset, log-source " +
          "and control relations has not yet been declared or observed.",
        impact:
          "A running platform does not by itself establish operational " +
          "visibility.",
        action:
          "Define the asset inventory, connect agents and syslog sources, " +
          "and establish expected log-source relations."
      },

      S2: {
        title: "The inventory is declared but observed telemetry is insufficient",
        finding:
          "Assets and monitoring expectations are declared, but not all " +
          "expected log sources have become observed graph relations.",
        impact:
          "The model knows what should be monitored, but visibility remains " +
          "at declaration level while telemetry is absent.",
        action:
          "Compare expected sources with Wazuh observations and complete the " +
          "missing agent or channel configurations."
      },

      S3: {
        title: "Log sources are connected but the detection chain is incomplete",
        finding:
          "Telemetry reaches Wazuh, but relations that convert data into " +
          "detection-control and rule evidence are missing.",
        impact:
          "Incoming data does not prove that expected behaviors are converted " +
          "into alerts and technique coverage.",
        action:
          "Validate decoders, Wazuh rules and control mappings with controlled " +
          "test events."
      },

      S4: {
        title: "Detection controls are active but higher-level context is incomplete",
        finding:
          `Control and alert coverage is ${m.CAC || "-"}. Some MITRE or CTI ` +
          "relations remain unverified.",
        impact:
          "Alerts may exist without complete adversary-technique or " +
          "intelligence context.",
        action:
          "Complete the rule, MITRE-technique and CTI-object relations for " +
          "each enabled control."
      },

      S5: {
        title: "The MITRE scope is declared but not fully evidenced",
        finding:
          `MDC is ${m.MDC || "-"}. Some in-scope ATT&CK techniques lack ` +
          "observed detection evidence.",
        impact:
          "A technique is not covered merely because it is listed in scope; " +
          "it must be connected to rule and control evidence.",
        action:
          "Define the corresponding control and Wazuh rule, then validate it " +
          "with a controlled scenario."
      },

      S6: {
        title: "CTI enrichment is enabled and closure is being validated",
        finding:
          `CTIC is ${m.CTIC || "-"}. Wazuh, integration, MISP and typed CTI ` +
          "relations must be validated on the same alert chain.",
        impact:
          "A successful lookup alone is not CTI closure; the result must " +
          "return to the alert and graph.",
        action:
          "Validate the alert → custom-misp → MISP → hit/no-hit event → " +
          "enrichment rule → CTI-object chain."
      },

      S7: {
        title: "Partial evidence closure was achieved",
        finding:
          `${m.MISSING} relations remain missing. SACI is ${m.SACI}, MDC is ` +
          `${m.MDC || "-"} and CTIC is ${m.CTIC || "-"}.`,
        impact:
          "The core visibility chain works, but unresolved relations still " +
          "limit complete evidence traceability.",
        action:
          "Prioritize the missing relations by reason-code impact."
      },

      S7A: {
        title: "Critical DC01 Sysmon telemetry was lost",
        finding:
          "The expected Sysmon channel on the domain controller is not " +
          "observed, affecting process, DNS and behavioral detection chains.",
        impact:
          "A loss on a critical asset should have a greater CWLC impact than " +
          "the same loss on a non-critical endpoint.",
        action:
          "Validate the DC01 Sysmon service, agent event-channel collection " +
          "and last-seen timestamp."
      },

      S7B: {
        title: "Non-critical WS01 Sysmon telemetry was lost",
        finding:
          "The expected Sysmon source on WS01 is not observed, reducing " +
          "endpoint behavioral visibility.",
        impact:
          "The gap is real but should have less score impact than the same " +
          "loss on DC01 because of asset criticality.",
        action:
          "Validate the WS01 agent, Sysmon configuration and Wazuh channel " +
          "collection."
      },

      S8: {
        title: "Final closure was achieved in the historical validation series",
        finding:
          `${m.OBSERVED}/${m.EDGES} relations are observed and ${m.MISSING} ` +
          `are missing. SACI is ${m.SACI}.`,
        impact:
          "The historical series shows that the declared gaps were closed. " +
          "This remains separate from the canonical publication dataset.",
        action:
          "Preserve it as historical closure evidence and do not merge its " +
          "counts with the publication snapshot."
      },

      S9: {
        title: "Critical DC01 Security telemetry was lost",
        finding:
          "The domain-controller Security channel is not observed, affecting " +
          "authentication, account-use and Windows security controls.",
        impact:
          "Identity and access behavior loses evidence, potentially affecting " +
          "Valid Accounts and related techniques.",
        action:
          "Validate Windows auditing, the Wazuh event-channel definition and " +
          "the channel last-seen time."
      },

      S10: {
        title: "Endpoint PowerShell telemetry was lost",
        finding:
          "Expected PowerShell operational or script-block telemetry is " +
          "missing, weakening T1059.001 evidence.",
        impact:
          "PowerShell execution may remain visible only as process creation, " +
          "without command-content context.",
        action:
          "Validate Script Block Logging, Module Logging and Wazuh PowerShell " +
          "channel collection."
      },

      S11: {
        title: "Linux auth-log telemetry was lost",
        finding:
          `${m.MISSING} relations are missing. CAC is ${m.CAC || "-"} and ` +
          `SACI is ${m.SACI}.`,
        impact:
          "SSH brute-force and authentication behavior lose their primary " +
          "evidence source.",
        action:
          "Validate auth.log or secure paths, rsyslog production, Wazuh " +
          "localfile settings and freshness."
      },

      S12: {
        title: "The firewall IOC alert exists, but the CTI context chain is open",
        finding:
          `The firewall IOC is visible at the detection layer, but CTIC is ` +
          `${m.CTIC || "-"} and ${m.MISSING} relations are missing. The ` +
          "expected chain between the IOC alert and MISP/CTI context is not " +
          "fully established.",
        impact:
          "The analyst can see the alert, but indicator reputation, MISP " +
          "event/attribute, confidence, source and enrichment context may " +
          "not be verifiable during triage.",
        action:
          "Validate the pfSense IOC alert → Wazuh rule → custom-misp query → " +
          "MISP hit/no-hit event → enrichment rule → typed CTI-object chain."
      },

      S13: {
        title: "The MISP lookup ran without an IOC match",
        finding:
          `CTIC is ${m.CTIC || "-"}. The lookup executed, but no MISP-hit ` +
          "evidence was produced for the indicator.",
        impact:
          "This may indicate that the IOC is absent from MISP rather than an " +
          "integration failure. Hit and no-hit outcomes must be distinguished.",
        action:
          "Validate the queried value, indicator type, to_ids filter, MISP " +
          "attribute state and the no-hit Wazuh rule."
      },

      S14: {
        title: "MITRE scope expansion introduced a detection gap",
        finding:
          `MDC is ${m.MDC || "-"}. A newly introduced ATT&CK technique lacks ` +
          "observed control or rule evidence.",
        impact:
          "The score decrease correctly reflects the new expectation instead " +
          "of preserving artificial full coverage.",
        action:
          "Define the data source, detection control, Wazuh rule and validation " +
          "scenario for the new technique."
      },

      S15: {
        title: "Telemetry freshness has decayed",
        finding:
          `TF is ${m.TF || "-"}. Relations were observed previously, but their ` +
          "last-seen timestamps exceed the freshness threshold.",
        impact:
          "Historical evidence does not prove that current operational " +
          "visibility is still active.",
        action:
          "Validate last-seen timestamps, freshness thresholds, agent " +
          "heartbeats and ingestion latency."
      },

      S16: {
        title: "A detection-rule gap was introduced",
        finding:
          `CAC is ${m.CAC || "-"}. The expected control is enabled, but its ` +
          "Wazuh-rule or alert evidence is not observed.",
        impact:
          "Telemetry can exist while detection logic fails to convert it into " +
          "operational evidence.",
        action:
          "Validate the rule ID, decoder match, field conditions, enabled state " +
          "and alerts.json output."
      },

      S17: {
        title: "Visibility recovered after remediation",
        finding:
          "Previously missing telemetry or control relations are observed again " +
          "and the SACI score has recovered.",
        impact:
          "The model demonstrates both gap detection and post-fix evidence " +
          "recovery.",
        action:
          "Compare before-and-after reason codes and confirm persistence through " +
          "freshness monitoring."
      },

      S18: {
        title: "The legacy control was excluded from the active scope",
        finding:
          "The control is treated as N/A and active metric weights are " +
          "renormalized.",
        impact:
          "An inapplicable control is not incorrectly treated as a zero-score " +
          "failure.",
        action:
          "Document the scope decision and active-weight normalization in the " +
          "audit output."
      }
    };

    return reports[id] || generic;
  }

  function render() {
    const host = document.getElementById("interpretation");

    if (!host) return;

    const m = metricValues();

    if (
      [m.DECLARED, m.RENDERED, m.EDGES]
        .every((value) => value === "-" || value === "")
    ) {
      return;
    }

    const scenario = currentScenario();
    const en = isEnglish();
    const report = en
      ? enReport(scenario.id, m)
      : trReport(scenario.id, m);

    host
      .querySelectorAll(".saci-expanded-interpretation")
      .forEach((node) => node.remove());

    const mitreCount = uniqueMitreCount();

    const wrapper = document.createElement("div");
    wrapper.className = "saci-expanded-interpretation";

    wrapper.innerHTML = en
      ? `
        <section class="saci-explanation-block">
          <h4>Evidence-chain interpretation</h4>

          <p>
            The selected dataset contains
            <strong>${m.DECLARED}</strong> declared nodes,
            <strong>${m.RENDERED}</strong> rendered nodes and
            <strong>${m.EDGES}</strong> relations.
            Of these relations, <strong>${m.OBSERVED}</strong> are
            observed and <strong>${m.MISSING}</strong> are missing.
          </p>

          <p>
            The graph evaluates assets, log sources, detection controls,
            Wazuh rules, MITRE ATT&amp;CK techniques, CTI objects,
            platforms, metrics and reason codes as a connected evidence
            chain. A complete result refers only to the declared evaluation
            scope and is not an absolute security guarantee.
          </p>

          <ul class="saci-result-list">
            <li><span>Declared nodes</span><strong>${m.DECLARED}</strong></li>
            <li><span>Rendered nodes</span><strong>${m.RENDERED}</strong></li>
            <li><span>Total relations</span><strong>${m.EDGES}</strong></li>
            <li><span>Observed relations</span><strong>${m.OBSERVED}</strong></li>
            <li><span>Missing relations</span><strong>${m.MISSING}</strong></li>
            <li><span>MITRE techniques</span><strong>${mitreCount || "-"}</strong></li>
            <li><span>SACI</span><strong>${m.SACI}</strong></li>
          </ul>
        </section>

        <section class="saci-scenario-report">
          <span class="saci-report-kicker">
            Scenario-level explanation output
          </span>

          <h4>${report.title}</h4>

          <div class="saci-report-grid">
            <article class="saci-report-section">
              <span>Finding</span>
              <p>${report.finding}</p>
            </article>

            <article class="saci-report-section">
              <span>Operational meaning</span>
              <p>${report.impact}</p>
            </article>

            <article class="saci-report-section">
              <span>Recommended validation</span>
              <p>${report.action}</p>
            </article>
          </div>

          <div class="saci-report-note">
            <strong>Explanation-layer boundary:</strong>
            this report is generated from deterministic SACI metrics,
            graph relations and scenario reason codes. An LLM may rephrase
            this structured report, but it does not calculate or modify
            the score.
          </div>
        </section>
      `
      : `
        <section class="saci-explanation-block">
          <h4>Kanıt zinciri yorumu</h4>

          <p>
            Seçili veri kümesinde
            <strong>${m.DECLARED}</strong> beyan edilmiş node,
            <strong>${m.RENDERED}</strong> gösterilen node ve
            <strong>${m.EDGES}</strong> ilişki bulunmaktadır.
            Bu ilişkilerin <strong>${m.OBSERVED}</strong> tanesi
            gözlemlenmiş, <strong>${m.MISSING}</strong> tanesi eksik
            durumdadır.
          </p>

          <p>
            Graph; varlıkları, log kaynaklarını, detection kontrollerini,
            Wazuh kurallarını, MITRE ATT&amp;CK tekniklerini, CTI
            nesnelerini, platformları, metrikleri ve reason code
            kayıtlarını bağlantılı bir kanıt zinciri olarak değerlendirir.
            Tam sonuç yalnızca beyan edilen değerlendirme kapsamını ifade
            eder; mutlak güvenlik garantisi değildir.
          </p>

          <ul class="saci-result-list">
            <li><span>Beyan edilen node</span><strong>${m.DECLARED}</strong></li>
            <li><span>Gösterilen node</span><strong>${m.RENDERED}</strong></li>
            <li><span>Toplam ilişki</span><strong>${m.EDGES}</strong></li>
            <li><span>Gözlemlenen ilişki</span><strong>${m.OBSERVED}</strong></li>
            <li><span>Eksik ilişki</span><strong>${m.MISSING}</strong></li>
            <li><span>MITRE tekniği</span><strong>${mitreCount || "-"}</strong></li>
            <li><span>SACI</span><strong>${m.SACI}</strong></li>
          </ul>
        </section>

        <section class="saci-scenario-report">
          <span class="saci-report-kicker">
            Senaryo bazlı açıklama çıktısı
          </span>

          <h4>${report.title}</h4>

          <div class="saci-report-grid">
            <article class="saci-report-section">
              <span>Bulgu</span>
              <p>${report.finding}</p>
            </article>

            <article class="saci-report-section">
              <span>Operasyonel anlam</span>
              <p>${report.impact}</p>
            </article>

            <article class="saci-report-section">
              <span>Önerilen doğrulama</span>
              <p>${report.action}</p>
            </article>
          </div>

          <div class="saci-report-note">
            <strong>Açıklama katmanı sınırı:</strong>
            Bu rapor deterministik SACI metriklerinden, graph
            ilişkilerinden ve senaryo reason code kayıtlarından üretilir.
            Bir LLM bu yapılandırılmış raporu doğal dilde yeniden ifade
            edebilir; ancak skoru hesaplamaz veya değiştirmez.
          </div>
        </section>
      `;

    host.appendChild(wrapper);
  }

  let queued = false;

  function schedule() {
    if (queued) return;

    queued = true;

    requestAnimationFrame(() => {
      queued = false;
      render();
    });
  }

  function init() {
    const select = document.getElementById("scenarioSelect");

    if (select) {
      select.addEventListener("change", () => {
        setTimeout(schedule, 120);
      });
    }

    const observer = new MutationObserver(schedule);

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });

    schedule();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>
<!-- SACI_SCENARIO_REPORT_END -->
'''


def backup(path: Path) -> None:
    if not path.exists():
        return

    target = BACKUP / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def remove_old_blocks(html: str) -> str:
    patterns = [
        (
            "SACI_GRAPH_EXPLANATION_START",
            "SACI_GRAPH_EXPLANATION_END",
        ),
        (
            "SACI_SCENARIO_REPORT_UI_START",
            "SACI_SCENARIO_REPORT_UI_END",
        ),
        (
            "SACI_SCENARIO_REPORT_START",
            "SACI_SCENARIO_REPORT_END",
        ),
    ]

    for start, end in patterns:
        html = re.sub(
            rf"\s*<!-- {start} -->.*?<!-- {end} -->\s*",
            "\n",
            html,
            flags=re.S,
        )

    return html


def patch_graph_page(path: Path) -> None:
    if not path.exists():
        print(f"[!] Bulunamadı: {path}")
        return

    html = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    html = remove_old_blocks(html)

    replacements = {
        "final-v2 — Kanonik yayın anlık görüntüsü":
            "Final — Kanonik yayın anlık görüntüsü",

        "final-v2 — Canonical publication snapshot":
            "Final — Canonical publication snapshot",

        "final-v2 canonical publication snapshot":
            "Canonical publication snapshot",

        "Kanonik final-v2 görünümünde":
            "Kanonik final görünümünde",

        "kanonik final-v2 görünümünde":
            "kanonik final görünümünde",

        "canonical final-v2 view":
            "canonical final view",

        "Final-v2":
            "Final",

        "final-v2":
            "final",
    }

    for old, new in replacements.items():
        html = html.replace(old, new)

    if "</head>" not in html:
        raise RuntimeError(f"</head> bulunamadı: {path}")

    if "</body>" not in html:
        raise RuntimeError(f"</body> bulunamadı: {path}")

    html = html.replace(
        "</head>",
        REPORT_CSS + "\n</head>",
        1,
    )

    html = html.replace(
        "</body>",
        REPORT_JS + "\n</body>",
        1,
    )

    path.write_text(html, encoding="utf-8")
    print(f"[+] Graph açıklaması güncellendi: {path}")


def patch_all_visible_html() -> None:
    replacements = {
        "final-v2 — Kanonik yayın anlık görüntüsü":
            "Final — Kanonik yayın anlık görüntüsü",

        "final-v2 — Canonical publication snapshot":
            "Final — Canonical publication snapshot",

        "final-v2 canonical publication snapshot":
            "Canonical publication snapshot",

        "Kanonik final-v2":
            "Kanonik final",

        "kanonik final-v2":
            "kanonik final",

        "canonical final-v2":
            "canonical final",

        "Final-v2":
            "Final",

        "final-v2":
            "final",
    }

    for path in ALL_HTML:
        if not path.exists():
            continue

        html = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        for old, new in replacements.items():
            html = html.replace(old, new)

        path.write_text(html, encoding="utf-8")


def patch_manifest(path: Path) -> None:
    if not path.exists():
        print(f"[!] Manifest bulunamadı: {path}")
        return

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    if str(data.get("default", "")).lower() in {
        "final_v2",
        "final-v2",
    }:
        data["default"] = "final"

    if str(data.get("default_scenario", "")).lower() in {
        "final_v2",
        "final-v2",
    }:
        data["default_scenario"] = "final"

    records = (
        data.get("datasets")
        or data.get("scenarios")
        or []
    )

    for item in records:
        item_id = str(item.get("id", "")).lower()
        kind = str(item.get("kind", "")).lower()

        if (
            item_id in {
                "final",
                "final_v2",
                "final-v2",
            }
            or kind == "canonical"
        ):
            item["id"] = "final"

            item["label_tr"] = (
                "Final — Kanonik yayın anlık görüntüsü"
            )

            item["label_en"] = (
                "Final — Canonical publication snapshot"
            )

            item["label"] = (
                "Final — Kanonik yayın anlık görüntüsü"
                if "/en/" not in path.as_posix()
                else "Final — Canonical publication snapshot"
            )

            item["title"] = item["label"]
            item["name"] = item["label"]

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"[+] Manifest final adı düzeltildi: {path}")


for path in set(ALL_HTML + MANIFESTS):
    backup(path)

patch_all_visible_html()

for page in GRAPH_PAGES:
    patch_graph_page(page)

for manifest in MANIFESTS:
    patch_manifest(manifest)

print()
print("=== FINAL NAME AND SCENARIO EXPLANATION FIX COMPLETE ===")
print(f"Backup: {BACKUP}")
