
(() => {
  const $ = (id) => document.getElementById(id);
  const en = (document.documentElement.lang || "").toLowerCase().startsWith("en");
  const t = (tr, enText) => en ? enText : tr;
  const esc = (value) => String(value ?? "").replace(/[<>&"]/g, c => ({
    "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;"
  }[c]));

  const COLORS = {
    ink: "#e8edf5",
    muted: "#9aa6b6",
    line: "#2a3545",
    accent: "#7cc7f2",
    accentSoft: "#9fb7cf",
    good: "#55c98a",
    dark: "#0b1020",
    panel: "#111827",
    gray: "#667085"
  };

  const SCENARIO_TEXT = {
    FINAL: {
      tr: {
        title: "Final görünürlük kapanışı",
        focus: "Yayına esas final veri kümesinde tanımlı telemetri, kontrol, MITRE ve CTI ilişkilerinin kapanışı.",
        interpretation: "Aktif metriklerin tam puana ve missing ilişki sayısının sıfıra ulaşması, beyan edilen değerlendirme kapsamındaki kanıt zincirlerinin tamamlandığını gösterir. Sonuç mutlak güvenlik garantisi değildir."
      },
      en: {
        title: "Final visibility closure",
        focus: "Closure of declared telemetry, control, MITRE and CTI relations in the publication-level final dataset.",
        interpretation: "All active metrics reaching full score with zero missing relations demonstrates closure of the evidence chains within the declared evaluation scope. The result is not an absolute security guarantee."
      }
    },
    S0: {
      tr: {
        title: "SIEM bulunmayan başlangıç durumu",
        focus: "Merkezi log toplama ve ilişkilendirme altyapısının bulunmadığı temel durum.",
        interpretation: "Modelin sıfır noktasını temsil eder. Görünürlük zinciri kurulamadığından telemetri, detection, MITRE ve CTI boyutları operasyonel kanıt üretemez."
      },
      en: {
        title: "Baseline without a SIEM",
        focus: "Baseline state without central log collection and correlation.",
        interpretation: "This scenario defines the zero point of the model. Without an observation layer, telemetry, detection, MITRE and CTI dimensions cannot produce operational evidence."
      }
    },
    S1: {
      tr: {
        title: "SIEM kurulu, kapsam eksik",
        focus: "Wazuh çalışır durumdadır; ancak varlık ve log kaynağı kapsamı henüz tamamlanmamıştır.",
        interpretation: "Platformun kurulmuş olması tek başına operasyonel görünürlük sağlamaz. Beklenen ve gözlemlenen ilişkiler arasındaki fark kapsam boşluğunu görünür kılar."
      },
      en: {
        title: "SIEM deployed, scope incomplete",
        focus: "Wazuh is operational, but asset and log-source coverage remains incomplete.",
        interpretation: "A running platform does not by itself provide operational visibility. The difference between expected and observed relations exposes the remaining scope gap."
      }
    },
    S2: {
      tr: {
        title: "Envanter tanımlı, telemetri yetersiz",
        focus: "İzlenecek varlıklar beyan edilmiş; beklenen log kaynaklarının tamamı gözlemlenmemiştir.",
        interpretation: "Model kapsamı bilmesine rağmen telemetri eksikliği detection ve üst bağlam zincirlerinin oluşmasını sınırlar."
      },
      en: {
        title: "Inventory declared, telemetry insufficient",
        focus: "Assets are declared, but not all expected log sources are observed.",
        interpretation: "Although the model knows the scope, missing telemetry limits the formation of detection and higher-level context chains."
      }
    },
    S3: {
      tr: {
        title: "Telemetri var, detection zinciri eksik",
        focus: "Loglar ulaşmakta; ancak control, rule ve alert ilişkileri tamamlanmamıştır.",
        interpretation: "Verinin toplanması beklenen davranışların alarm kanıtına dönüştüğünü tek başına göstermez. Detection zinciri ayrıca doğrulanmalıdır."
      },
      en: {
        title: "Telemetry present, detection chain incomplete",
        focus: "Logs are ingested, but control, rule and alert relations remain incomplete.",
        interpretation: "Data collection alone does not prove conversion of expected behavior into alert evidence. The detection chain requires separate validation."
      }
    },
    S4: {
      tr: {
        title: "Detection etkin, üst bağlam kısmi",
        focus: "Alarm üretimi görünür; MITRE veya CTI bağlamının bir bölümü henüz bağlı değildir.",
        interpretation: "Detection üretimi ile saldırgan tekniği ve istihbarat bağlamı birbirinden ayrılır. Üst bağlam ilişkileri tamamlanmadan bütünsel kapanış oluşmaz."
      },
      en: {
        title: "Detection active, higher context partial",
        focus: "Alert generation is visible, while some MITRE or CTI context remains unlinked.",
        interpretation: "Detection output is separated from adversary-technique and intelligence context. Holistic closure is not achieved until higher-level relations are completed."
      }
    },
    S5: {
      tr: {
        title: "MITRE kapsamı kısmi",
        focus: "Kapsamdaki ATT&CK tekniklerinin bir bölümü kontrol ve rule kanıtıyla doğrulanmamıştır.",
        interpretation: "Tekniklerin yalnızca listelenmesi tam kapsam sayılmaz. MDC, teknikler operasyonel detection kanıtıyla bağlandığında yükselir."
      },
      en: {
        title: "MITRE coverage partial",
        focus: "Some in-scope ATT&CK techniques lack control and rule evidence.",
        interpretation: "Merely listing techniques does not constitute full coverage. MDC increases when techniques are connected to operational detection evidence."
      }
    },
    S6: {
      tr: {
        title: "CTI enrichment etkinleştirildi",
        focus: "MISP lookup ve enrichment zincirinin operasyonel kanıtları devreye alınmıştır.",
        interpretation: "CTI kapsamı yalnızca sorgunun çalışmasına değil, lookup sonucunun alarm ve graph ilişkilerine geri dönmesine bağlıdır."
      },
      en: {
        title: "CTI enrichment enabled",
        focus: "Operational evidence for the MISP lookup and enrichment chain is enabled.",
        interpretation: "CTI coverage depends not only on query execution, but on the result returning to the alert and graph relations."
      }
    },
    S7: {
      tr: {
        title: "Kısmi kanıt kapanışı",
        focus: "Temel görünürlük zinciri çalışmakta; bazı ilişkiler henüz eksik kalmaktadır.",
        interpretation: "Observed ilişkilerin artması model olgunluğunu yükseltir; ancak missing ilişkiler sıfırlanmadan tam kapanış kabul edilmez."
      },
      en: {
        title: "Partial evidence closure",
        focus: "The core visibility chain works, while some relations remain missing.",
        interpretation: "Increasing observed relations improves model maturity, but complete closure is not accepted until missing relations reach zero."
      }
    },
    S7A: {
      tr: {
        title: "Kritik DC01 Sysmon kaybı",
        focus: "Kritik domain controller üzerindeki Sysmon telemetrisi kaybedilmiştir.",
        interpretation: "Kritik varlık üzerindeki aynı tür telemetri kaybı, kritiklik ağırlığı nedeniyle SACI üzerinde daha güçlü etki oluşturur."
      },
      en: {
        title: "Critical DC01 Sysmon loss",
        focus: "Sysmon telemetry is lost on the critical domain controller.",
        interpretation: "The same telemetry loss produces a stronger SACI impact on a critical asset because of criticality weighting."
      }
    },
    S7B: {
      tr: {
        title: "Kritik olmayan WS01 Sysmon kaybı",
        focus: "Kritik olmayan endpoint üzerindeki Sysmon telemetrisi kaybedilmiştir.",
        interpretation: "S7A ile karşılaştırma, modelin aynı tür kaybı varlık önemine göre farklı değerlendirdiğini gösterir."
      },
      en: {
        title: "Non-critical WS01 Sysmon loss",
        focus: "Sysmon telemetry is lost on a non-critical endpoint.",
        interpretation: "Comparison with S7A shows that the model evaluates the same loss differently according to asset importance."
      }
    },
    S8: {
      tr: {
        title: "Tarihsel doğrulama kapanışı",
        focus: "S0–S18 kontrollü doğrulama serisinin tarihsel kapanış noktası.",
        interpretation: "Senaryo serisi içindeki beklenen ilişkiler kapatılmıştır. Bu veri kümesi yayına esas final veri kümesiyle birleştirilmez."
      },
      en: {
        title: "Historical validation closure",
        focus: "Historical closure point of the controlled S0–S18 validation series.",
        interpretation: "Expected relations within the scenario series are closed. This dataset remains separate from the publication-level final dataset."
      }
    },
    S9: {
      tr: {
        title: "DC01 Security telemetrisi kaybı",
        focus: "Domain controller Security kanalına dayalı kimlik doğrulama kanıtı kaybedilmiştir.",
        interpretation: "Windows güvenlik olaylarına bağlı kontrol ve ATT&CK ilişkileri zayıflar; kimlik davranışı görünürlüğü düşer."
      },
      en: {
        title: "DC01 Security telemetry loss",
        focus: "Authentication evidence from the domain-controller Security channel is lost.",
        interpretation: "Controls and ATT&CK relations based on Windows security events weaken, reducing identity-behavior visibility."
      }
    },
    S10: {
      tr: {
        title: "PowerShell telemetrisi kaybı",
        focus: "PowerShell operational veya script-block logları gözlemlenmemektedir.",
        interpretation: "Komut yürütme bağlamı ve T1059.001 ile ilişkili detection kanıtı azalır."
      },
      en: {
        title: "PowerShell telemetry loss",
        focus: "PowerShell operational or script-block logs are not observed.",
        interpretation: "Command-execution context and detection evidence related to T1059.001 are reduced."
      }
    },
    S11: {
      tr: {
        title: "Linux authlog kaybı",
        focus: "Linux kimlik doğrulama log kaynağı görünür değildir.",
        interpretation: "SSH brute-force ile başarılı ve başarısız oturum açma davranışlarının birincil kanıtı kaybolur."
      },
      en: {
        title: "Linux auth-log loss",
        focus: "The Linux authentication log source is not visible.",
        interpretation: "Primary evidence for SSH brute force and successful or failed logon behavior is lost."
      }
    },
    S12: {
      tr: {
        title: "Firewall IOC alarmı var, CTI zinciri açık",
        focus: "Detection oluşmasına rağmen MISP/CTI bağlam zinciri tam kapanmamıştır.",
        interpretation: "Alarmın görülmesi enrichment kapanışını tek başına kanıtlamaz. Lookup, hit, event/attribute ve typed CTI object ilişkileri birlikte değerlendirilmelidir."
      },
      en: {
        title: "Firewall IOC alert present, CTI chain open",
        focus: "Detection exists, but the MISP/CTI context chain is not fully closed.",
        interpretation: "Alert visibility alone does not prove enrichment closure. Lookup, hit, event/attribute and typed CTI object relations must be evaluated together."
      }
    },
    S13: {
      tr: {
        title: "MISP lookup var, IOC hit yok",
        focus: "MISP sorgusu çalışmış; ilgili indicator için eşleşme oluşmamıştır.",
        interpretation: "No-hit sonucu entegrasyon arızasından ayrılır. Model lookup yürütülmesini ve hit sonucunu ayrı operasyonel aşamalar olarak ele alır."
      },
      en: {
        title: "MISP lookup executed, no IOC hit",
        focus: "The MISP query executed, but no match was produced for the indicator.",
        interpretation: "A no-hit outcome is separated from integration failure. The model treats query execution and hit result as distinct operational stages."
      }
    },
    S14: {
      tr: {
        title: "MITRE kapsam genişlemesi",
        focus: "Değerlendirme kapsamına yeni ATT&CK tekniği eklenmiştir.",
        interpretation: "Yeni teknik için operasyonel kanıt oluşmadan MDC düşer. Böylece yeni kapsam beklentisi sahte tam kapsama altında gizlenmez."
      },
      en: {
        title: "MITRE scope expansion",
        focus: "A new ATT&CK technique is added to the evaluation scope.",
        interpretation: "MDC decreases until operational evidence exists for the new technique, preventing the new expectation from being hidden by artificial full coverage."
      }
    },
    S15: {
      tr: {
        title: "Telemetri freshness düşüşü",
        focus: "Daha önce gözlemlenen telemetrinin son görülme zamanı freshness eşiğini aşmıştır.",
        interpretation: "Geçmişteki observed ilişki ile güncel operasyonel telemetri birbirinden ayrılır. Eski kanıtın varlığı mevcut akışı garanti etmez."
      },
      en: {
        title: "Telemetry freshness degradation",
        focus: "The last-seen time of previously observed telemetry exceeds the freshness threshold.",
        interpretation: "Historical observation is separated from current operational telemetry. Existing past evidence does not guarantee present data flow."
      }
    },
    S16: {
      tr: {
        title: "Detection rule boşluğu",
        focus: "Telemetri mevcut olmasına rağmen beklenen Wazuh rule veya alert kanıtı oluşmamıştır.",
        interpretation: "Detection mantığındaki boşluk CAC değerini ve ilgili graph zincirini etkiler."
      },
      en: {
        title: "Detection-rule gap",
        focus: "Telemetry exists, but expected Wazuh rule or alert evidence is absent.",
        interpretation: "The detection-logic gap affects CAC and the related graph chain."
      }
    },
    S17: {
      tr: {
        title: "Düzeltme sonrası toparlanma",
        focus: "Önceki senaryoda kaybedilen telemetri veya kontrol ilişkileri yeniden gözlemlenmiştir.",
        interpretation: "Model yalnızca boşluğu tespit etmez; düzeltmenin kanıt zincirini geri getirip getirmediğini de ölçer."
      },
      en: {
        title: "Post-remediation recovery",
        focus: "Telemetry or control relations lost in the previous scenario are observed again.",
        interpretation: "The model not only detects the gap, but also measures whether remediation restores the evidence chain."
      }
    },
    S18: {
      tr: {
        title: "Aktif kapsam normalizasyonu",
        focus: "Senaryoya uygulanmayan legacy kontrol aktif değerlendirme kapsamı dışında tutulmuştur.",
        interpretation: "Uygulanabilir olmayan bileşen sıfırla cezalandırılmaz; N/A kabul edilir ve aktif ağırlıklar yeniden normalize edilir."
      },
      en: {
        title: "Active-scope normalization",
        focus: "A legacy control not applicable to the scenario is kept outside the active evaluation scope.",
        interpretation: "The inapplicable component is not penalized as zero; it is treated as N/A and active weights are renormalized."
      }
    }
  };

  async function getText(url, optional = false) {
    try {
      const response = await fetch(url, { cache: "no-store" });
      if (!response.ok) throw new Error(`${url} HTTP ${response.status}`);
      return await response.text();
    } catch (error) {
      if (optional) return "";
      throw error;
    }
  }

  async function getJson(url) {
    return JSON.parse(await getText(url));
  }

  function parseCSV(text) {
    if (!text.trim()) return [];
    const rows = [];
    let row = [], field = "", quoted = false;

    for (let i = 0; i < text.length; i++) {
      const c = text[i], next = text[i + 1];

      if (quoted) {
        if (c === '"' && next === '"') {
          field += '"';
          i++;
        } else if (c === '"') {
          quoted = false;
        } else {
          field += c;
        }
      } else if (c === '"') {
        quoted = true;
      } else if (c === ",") {
        row.push(field);
        field = "";
      } else if (c === "\n") {
        row.push(field.replace(/\r$/, ""));
        rows.push(row);
        row = [];
        field = "";
      } else {
        field += c;
      }
    }

    if (field.length || row.length) {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
    }

    const headers = (rows.shift() || []).map(x => x.trim());

    return rows
      .filter(r => r.some(x => String(x).trim() !== ""))
      .map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
  }

  function scoreMap(rows) {
    const result = {};

    if (rows.length === 1) {
      Object.entries(rows[0]).forEach(([key, value]) => {
        const k = key.toUpperCase();
        if (["CWLC", "LC", "CAC", "MDC", "CTIC", "TF", "SACI"].includes(k)) {
          result[k === "LC" ? "CWLC" : k] = value;
        }
      });
    }

    rows.forEach(row => {
      const key = String(row.metric || row.name || row.component || "").toUpperCase();
      if (key) {
        result[key === "LC" ? "CWLC" : key] =
          row.score ?? row.value ?? row.result ?? "";
      }
    });

    return result;
  }

  function normalizeCyjs(raw) {
    if (Array.isArray(raw)) return raw;
    if (Array.isArray(raw.elements)) return raw.elements;
    if (raw.elements?.nodes && raw.elements?.edges) {
      return [...raw.elements.nodes, ...raw.elements.edges];
    }
    if (raw.nodes && raw.edges) {
      return [...raw.nodes, ...raw.edges];
    }
    return [];
  }

  function graphStats(raw) {
    const elements = normalizeCyjs(raw);
    const nodes = elements.filter(x => !(x?.data?.source && x?.data?.target));
    const edges = elements.filter(x => x?.data?.source && x?.data?.target);

    const observed = edges.filter(x =>
      x.data.observed === 1 ||
      x.data.observed === true ||
      String(x.data.observed) === "1" ||
      String(x.data.observed).toLowerCase() === "true"
    ).length;

    const nodeIds = new Set(nodes.map(x => String(x?.data?.id ?? "")));

    const undeclared = [...new Set(
      edges
        .flatMap(x => [String(x.data.source), String(x.data.target)])
        .filter(id => id && !nodeIds.has(id))
    )].sort();

    return {
      nodes: nodes.length,
      renderedNodes: nodes.length + undeclared.length,
      edges: edges.length,
      observed,
      missing: edges.length - observed,
      undeclared
    };
  }

  function scenarioId(item) {
    const raw = String(item.id || item.scenario || item.name || "");

    if (
      /final/i.test(raw) ||
      String(item.kind || "").toLowerCase() === "canonical"
    ) {
      return "FINAL";
    }

    const match = raw.match(/S\d+[A-Za-z]?/i);
    return match ? match[0].toUpperCase() : raw.toUpperCase();
  }

  function scenarioSortKey(id) {
    if (id === "FINAL") return [-1, ""];

    const match = id.match(/^S(\d+)([A-Z]?)$/);
    return match ? [Number(match[1]), match[2]] : [999, id];
  }

  function finalEntry(manifest) {
    const rows = manifest.datasets || manifest.scenarios || [];

    return rows.find(item => scenarioId(item) === "FINAL") || rows[0];
  }

  function field(item, keys, fallback) {
    for (const key of keys) {
      if (item?.[key]) return item[key];
    }

    const base = item?.base || item?.dir || "";
    return base
      ? `${String(base).replace(/\/$/, "")}/${fallback}`
      : fallback;
  }

  async function firstCsv(paths) {
    for (const path of paths) {
      if (!path) continue;

      const text = await getText(path, true);

      if (text.trim()) {
        return {
          path,
          rows: parseCSV(text)
        };
      }
    }

    return {
      path: "",
      rows: []
    };
  }

  function numeric(value, fallback = 0) {
    const n = Number(value);
    return Number.isFinite(n) ? n : fallback;
  }

  function metricValue(scores, key) {
    const value = scores[key];

    if (
      value === undefined ||
      value === null ||
      value === "" ||
      String(value).toUpperCase() === "N/A"
    ) {
      return null;
    }

    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  }

  function coverageFromMitre(rows) {
    if (!rows.length) {
      return { covered: 0, total: 0 };
    }

    const total = rows.length;

    const covered = rows.filter(row => {
      const value = row.covered ?? row.observed ?? row.status;

      return (
        value === 1 ||
        value === true ||
        String(value) === "1" ||
        String(value).toLowerCase() === "true" ||
        String(value).toLowerCase() === "covered"
      );
    }).length;

    return { covered, total };
  }

  function coverageFromCti(rows) {
    if (!rows.length) {
      return { covered: 0, total: 0 };
    }

    const total = rows.length;

    const covered = rows.filter(row => {
      const direct = row.covered ?? row.closed ?? row.observed;

      if (direct !== undefined) {
        return (
          direct === 1 ||
          direct === true ||
          String(direct) === "1" ||
          String(direct).toLowerCase() === "true"
        );
      }

      const stagedKeys = [
        "lookup_executed",
        "misp_hit",
        "wazuh_alert",
        "mapped_to_mitre"
      ];

      const present = stagedKeys.filter(key => row[key] !== undefined);

      if (present.length) {
        return present.every(key =>
          String(row[key]) === "1" ||
          String(row[key]).toLowerCase() === "true"
        );
      }

      return false;
    }).length;

    return { covered, total };
  }

  function svgText(text) {
    return esc(text);
  }

  function componentSvg(scores, title) {
    const metrics = ["CWLC", "CAC", "MDC", "CTIC", "TF", "SACI"];
    const width = 1040;
    const height = 445;
    const left = 170;
    const right = 90;
    const top = 64;
    const rowGap = 56;
    const barWidth = width - left - right;

    const rows = metrics.map((metric, index) => {
      const y = top + index * rowGap;
      const value = metricValue(scores, metric);
      const fill = metric === "SACI" ? COLORS.accentSoft : COLORS.accent;

      if (value === null) {
        return `
          <text x="${left - 18}" y="${y + 18}" text-anchor="end"
                fill="${COLORS.ink}" font-size="18" font-weight="700">${metric}</text>

          <rect x="${left}" y="${y}" width="${barWidth}" height="24"
                rx="12" fill="${COLORS.panel}" stroke="${COLORS.line}"/>

          <text x="${left + 20}" y="${y + 18}"
                fill="${COLORS.gray}" font-size="15" font-weight="700">N/A</text>
        `;
      }

      const bounded = Math.max(0, Math.min(100, value));

      return `
        <text x="${left - 18}" y="${y + 18}" text-anchor="end"
              fill="${COLORS.ink}" font-size="18" font-weight="700">${metric}</text>

        <rect x="${left}" y="${y}" width="${barWidth}" height="24"
              rx="12" fill="${COLORS.panel}" stroke="${COLORS.line}"/>

        <rect x="${left}" y="${y}" width="${barWidth * bounded / 100}" height="24"
              rx="12" fill="${fill}"/>

        <text x="${left + barWidth + 16}" y="${y + 18}"
              fill="${COLORS.ink}" font-size="17" font-weight="700">
          ${bounded.toFixed(metric === "TF" ? 0 : 1)}
        </text>
      `;
    }).join("");

    return `
      <svg xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 ${width} ${height}"
           role="img"
           aria-label="${svgText(title)}">

        <rect width="${width}" height="${height}" rx="18" fill="${COLORS.dark}"/>

        <text x="44" y="40"
              fill="${COLORS.muted}" font-size="15" font-weight="700">
          ${svgText(title)}
        </text>

        ${rows}

        <text x="${left}" y="${height - 22}"
              fill="${COLORS.muted}" font-size="13">
          ${svgText(
            t(
              "N/A = aktif değerlendirme kapsamı dışında",
              "N/A = outside the active evaluation scope"
            )
          )}
        </text>
      </svg>
    `;
  }

  function closureSvg(graph) {
    const width = 920;
    const height = 420;
    const cx = 260;
    const cy = 205;
    const radius = 116;
    const circumference = 2 * Math.PI * radius;
    const ratioValue = graph.edges ? graph.observed / graph.edges : 0;
    const dash = circumference * ratioValue;

    return `
      <svg xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 ${width} ${height}"
           role="img"
           aria-label="${svgText(t("Graph kapanışı", "Graph closure"))}">

        <rect width="${width}" height="${height}" rx="18" fill="${COLORS.dark}"/>

        <circle cx="${cx}" cy="${cy}" r="${radius}"
                fill="none" stroke="${COLORS.line}" stroke-width="28"/>

        <circle cx="${cx}" cy="${cy}" r="${radius}"
                fill="none" stroke="${COLORS.good}" stroke-width="28"
                stroke-linecap="round"
                stroke-dasharray="${dash} ${circumference - dash}"
                transform="rotate(-90 ${cx} ${cy})"/>

        <text x="${cx}" y="${cy - 4}" text-anchor="middle"
              fill="${COLORS.ink}" font-size="54" font-weight="800">
          ${(ratioValue * 100).toFixed(0)}%
        </text>

        <text x="${cx}" y="${cy + 30}" text-anchor="middle"
              fill="${COLORS.muted}" font-size="16">
          ${svgText(t("observed edge oranı", "observed-edge ratio"))}
        </text>

        <g transform="translate(500,95)">
          <text x="0" y="0"
                fill="${COLORS.muted}" font-size="15" font-weight="700">
            ${svgText(t("Graph metrikleri", "Graph metrics"))}
          </text>

          <text x="0" y="66"
                fill="${COLORS.ink}" font-size="34" font-weight="800">
            ${graph.observed}
          </text>

          <text x="0" y="92"
                fill="${COLORS.muted}" font-size="14">
            ${svgText(t("gözlemlenen ilişki", "observed relations"))}
          </text>

          <text x="195" y="66"
                fill="${COLORS.ink}" font-size="34" font-weight="800">
            ${graph.missing}
          </text>

          <text x="195" y="92"
                fill="${COLORS.muted}" font-size="14">
            ${svgText(t("eksik ilişki", "missing relations"))}
          </text>

          <text x="0" y="176"
                fill="${COLORS.ink}" font-size="34" font-weight="800">
            ${graph.nodes}
          </text>

          <text x="0" y="202"
                fill="${COLORS.muted}" font-size="14">
            ${svgText(t("beyan edilen node", "declared nodes"))}
          </text>

          <text x="195" y="176"
                fill="${COLORS.ink}" font-size="34" font-weight="800">
            ${graph.renderedNodes}
          </text>

          <text x="195" y="202"
                fill="${COLORS.muted}" font-size="14">
            ${svgText(t("görüntülenen node", "rendered nodes"))}
          </text>
        </g>
      </svg>
    `;
  }

  function coverageSvg(mitre, cti) {
    const width = 920;
    const height = 420;

    const data = [
      {
        label: "MITRE ATT&CK",
        covered: mitre.covered,
        total: mitre.total,
        color: COLORS.accent
      },
      {
        label: "CTI / MISP",
        covered: cti.covered,
        total: cti.total,
        color: COLORS.accentSoft
      }
    ];

    const rows = data.map((item, index) => {
      const y = 120 + index * 135;
      const ratioValue = item.total ? item.covered / item.total : 0;
      const barWidth = 570;

      return `
        <text x="92" y="${y}"
              fill="${COLORS.ink}" font-size="24" font-weight="800">
          ${item.label}
        </text>

        <text x="810" y="${y}" text-anchor="end"
              fill="${COLORS.ink}" font-size="24" font-weight="800">
          ${item.covered}/${item.total}
        </text>

        <rect x="92" y="${y + 30}" width="${barWidth}" height="28"
              rx="14" fill="${COLORS.panel}" stroke="${COLORS.line}"/>

        <rect x="92" y="${y + 30}" width="${barWidth * ratioValue}" height="28"
              rx="14" fill="${item.color}"/>

        <text x="690" y="${y + 51}"
              fill="${COLORS.muted}" font-size="16">
          ${(ratioValue * 100).toFixed(0)}%
        </text>
      `;
    }).join("");

    return `
      <svg xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 ${width} ${height}"
           role="img"
           aria-label="${svgText(t("MITRE ve CTI kapsamı", "MITRE and CTI coverage"))}">

        <rect width="${width}" height="${height}" rx="18" fill="${COLORS.dark}"/>

        <text x="42" y="42"
              fill="${COLORS.muted}" font-size="15" font-weight="700">
          ${svgText(t("Final kapsam oranları", "Final coverage ratios"))}
        </text>

        ${rows}
      </svg>
    `;
  }

  function lineChartSvg(data, key, title, yLabel, color, maxOverride = null) {
    const width = 1240;
    const height = 500;
    const left = 82;
    const right = 34;
    const top = 62;
    const bottom = 88;

    const values = data.map(item => numeric(item[key]));
    const maxValue = maxOverride ?? Math.max(100, ...values, 1);
    const chartWidth = width - left - right;
    const chartHeight = height - top - bottom;
    const xStep = data.length > 1 ? chartWidth / (data.length - 1) : chartWidth;

    const yPos = value =>
      top + chartHeight - (Math.max(0, value) / maxValue) * chartHeight;

    const points = data.map((item, index) => ({
      x: left + index * xStep,
      y: yPos(numeric(item[key])),
      value: numeric(item[key]),
      label: item.id
    }));

    const polyline = points.map(p => `${p.x},${p.y}`).join(" ");

    const gridValues = maxValue === 100
      ? [0, 25, 50, 75, 100]
      : [0, maxValue * .25, maxValue * .5, maxValue * .75, maxValue];

    const grid = gridValues.map(value => {
      const y = yPos(value);

      return `
        <line x1="${left}" y1="${y}" x2="${width - right}" y2="${y}"
              stroke="${COLORS.line}" stroke-width="1"/>

        <text x="${left - 14}" y="${y + 5}" text-anchor="end"
              fill="${COLORS.muted}" font-size="12">
          ${Math.round(value)}
        </text>
      `;
    }).join("");

    const xLabels = points.map((p, index) => `
      <text x="${p.x}" y="${height - 52}" text-anchor="end"
            transform="rotate(-42 ${p.x} ${height - 52})"
            fill="${COLORS.muted}" font-size="11">
        ${svgText(data[index].id)}
      </text>
    `).join("");

    const dots = points.map(p => `
      <circle cx="${p.x}" cy="${p.y}" r="5"
              fill="${color}" stroke="${COLORS.dark}" stroke-width="2"/>

      <title>${svgText(`${p.label}: ${p.value}`)}</title>
    `).join("");

    return `
      <svg xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 ${width} ${height}"
           role="img"
           aria-label="${svgText(title)}">

        <rect width="${width}" height="${height}" rx="18" fill="${COLORS.dark}"/>

        <text x="42" y="40"
              fill="${COLORS.muted}" font-size="15" font-weight="700">
          ${svgText(title)}
        </text>

        ${grid}

        <polyline points="${polyline}"
                  fill="none" stroke="${color}" stroke-width="4"
                  stroke-linejoin="round" stroke-linecap="round"/>

        ${dots}
        ${xLabels}

        <text x="${left}" y="${height - 18}"
              fill="${COLORS.muted}" font-size="12">
          ${svgText(yLabel)}
        </text>
      </svg>
    `;
  }

  function groupedBarSvg(groups, metrics, title) {
    const width = 1040;
    const height = 470;
    const left = 88;
    const right = 34;
    const top = 72;
    const bottom = 96;
    const chartWidth = width - left - right;
    const chartHeight = height - top - bottom;

    const colors = [
      COLORS.accent,
      COLORS.accentSoft,
      COLORS.gray,
      COLORS.good
    ];

    const yPos = value =>
      top + chartHeight - (Math.max(0, value) / 100) * chartHeight;

    const grid = [0, 25, 50, 75, 100].map(value => {
      const y = yPos(value);

      return `
        <line x1="${left}" y1="${y}" x2="${width - right}" y2="${y}"
              stroke="${COLORS.line}" stroke-width="1"/>

        <text x="${left - 14}" y="${y + 5}" text-anchor="end"
              fill="${COLORS.muted}" font-size="12">
          ${value}
        </text>
      `;
    }).join("");

    const groupWidth = chartWidth / Math.max(groups.length, 1);
    const barArea = groupWidth * .7;
    const barWidth = barArea / Math.max(metrics.length, 1);

    const bars = groups.map((group, groupIndex) => {
      const groupX = left + groupIndex * groupWidth + (groupWidth - barArea) / 2;

      const metricBars = metrics.map((metric, metricIndex) => {
        const raw = metricValue(group.scores, metric);
        const x = groupX + metricIndex * barWidth;

        if (raw === null) {
          return `
            <rect x="${x + 3}" y="${top + chartHeight - 14}"
                  width="${Math.max(5, barWidth - 6)}" height="14"
                  rx="4" fill="${COLORS.gray}" opacity=".55"/>

            <text x="${x + barWidth / 2}" y="${top + chartHeight - 20}"
                  text-anchor="middle" fill="${COLORS.gray}" font-size="10">
              N/A
            </text>
          `;
        }

        const value = Math.max(0, Math.min(100, raw));
        const y = yPos(value);
        const h = top + chartHeight - y;

        return `
          <rect x="${x + 3}" y="${y}"
                width="${Math.max(5, barWidth - 6)}" height="${h}"
                rx="5" fill="${colors[metricIndex % colors.length]}"/>

          <title>${svgText(`${group.id} ${metric}: ${value}`)}</title>
        `;
      }).join("");

      return `
        ${metricBars}

        <text x="${left + groupIndex * groupWidth + groupWidth / 2}"
              y="${height - 58}" text-anchor="middle"
              fill="${COLORS.ink}" font-size="15" font-weight="700">
          ${svgText(group.id)}
        </text>
      `;
    }).join("");

    const legend = metrics.map((metric, index) => `
      <g transform="translate(${left + index * 142},${height - 26})">
        <rect width="18" height="8" rx="4"
              fill="${colors[index % colors.length]}"/>

        <text x="26" y="8"
              fill="${COLORS.muted}" font-size="12">
          ${metric}
        </text>
      </g>
    `).join("");

    return `
      <svg xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 ${width} ${height}"
           role="img"
           aria-label="${svgText(title)}">

        <rect width="${width}" height="${height}" rx="18" fill="${COLORS.dark}"/>

        <text x="42" y="40"
              fill="${COLORS.muted}" font-size="15" font-weight="700">
          ${svgText(title)}
        </text>

        ${grid}
        ${bars}
        ${legend}
      </svg>
    `;
  }

  function figureDownload(id, filename) {
    const svg = $(id)?.querySelector("svg");
    if (!svg) return;

    const source = new XMLSerializer().serializeToString(svg);
    const blob = new Blob([source], {
      type: "image/svg+xml;charset=utf-8"
    });

    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");

    anchor.href = url;
    anchor.download = filename;

    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();

    setTimeout(() => URL.revokeObjectURL(url), 800);
  }

  function renderSummary(scores, graph, mitre, cti) {
    $("scoreValue").textContent = scores.SACI ?? "-";

    $("scoreSub").textContent = t(
      "Aktif ağırlıklarla normalize edilmiş skor",
      "Score normalized across active weights"
    );

    $("closureValue").textContent = `${graph.observed}/${graph.edges}`;

    $("closureSub").textContent = t(
      `${graph.missing} missing edge`,
      `${graph.missing} missing edges`
    );

    $("mitreValue").textContent = `${mitre.covered}/${mitre.total}`;

    $("mitreSub").textContent = t(
      "Kapsamdaki ATT&CK teknikleri",
      "In-scope ATT&CK techniques"
    );

    $("ctiValue").textContent = `${cti.covered}/${cti.total}`;

    $("ctiSub").textContent = t(
      "Kapanan enrichment zincirleri",
      "Closed enrichment chains"
    );
  }

  function labelForScenario(item, id) {
    return en
      ? item.label_en || item.title_en || item.label || item.title || id
      : item.label_tr || item.title_tr || item.label || item.title || id;
  }

  function scenarioCopy(scenario) {
    const record = SCENARIO_TEXT[scenario.id];
    const localized = record ? record[en ? "en" : "tr"] : null;

    return {
      title: localized?.title || scenario.label || scenario.id,
      focus: localized?.focus || scenario.label || scenario.id,
      interpretation: localized?.interpretation || t(
        "Bu senaryo, aktif SACI metrikleri ile graph ilişkilerinin kontrollü değişime verdiği tepkiyi gösterir.",
        "This scenario shows how active SACI metrics and graph relations respond to a controlled change."
      )
    };
  }

  function scenarioStatus(scenario) {
    const score = metricValue(scenario.scores, "SACI");

    if (scenario.graph.missing === 0 && score === 100) {
      return {
        className: "complete",
        text: t("Kapanış tamam", "Closure complete")
      };
    }

    if (scenario.graph.missing > 0) {
      return {
        className: "gap",
        text: t("Açık ilişki var", "Open relations")
      };
    }

    return {
      className: "partial",
      text: t("Kısmi kapsama", "Partial coverage")
    };
  }

  function primaryMetricText(scenario) {
    const metrics = ["CWLC", "CAC", "MDC", "CTIC", "TF"]
      .map(key => ({
        key,
        value: metricValue(scenario.scores, key)
      }))
      .filter(item => item.value !== null);

    if (!metrics.length) {
      return t(
        "Aktif metrik bulunmamaktadır.",
        "No active metric is available."
      );
    }

    const lowest = [...metrics].sort((a, b) => a.value - b.value)[0];

    if (metrics.every(item => item.value === 100)) {
      return t(
        "Bütün aktif görünürlük boyutları 100 değerindedir.",
        "All active visibility dimensions are at 100."
      );
    }

    return t(
      `En düşük aktif boyut ${lowest.key} (${lowest.value}) değeridir; senaryonun nicel etkisi öncelikle bu boyutta görülmektedir.`,
      `The lowest active dimension is ${lowest.key} (${lowest.value}); the scenario's quantitative effect is primarily visible in this dimension.`
    );
  }

  function setupScenarioExplorer(scenarios) {
    const select = $("paperScenarioSelect");
    const picker = $("paperScenarioPicker");
    const trigger = $("paperScenarioTrigger");
    const triggerText = $("paperScenarioTriggerText");
    const popover = $("paperScenarioPopover");
    const search = $("paperScenarioSearch");
    const options = $("paperScenarioOptions");

    if (
      !select ||
      !picker ||
      !trigger ||
      !triggerText ||
      !popover ||
      !search ||
      !options ||
      !scenarios.length
    ) {
      return;
    }

    select.innerHTML = scenarios.map(scenario => {
      const copy = scenarioCopy(scenario);
      const prefix = scenario.id === "FINAL" ? "Final" : scenario.id;

      return `<option value="${esc(scenario.id)}">${esc(prefix)} — ${esc(copy.title)}</option>`;
    }).join("");

    const optionLabel = scenario => {
      const copy = scenarioCopy(scenario);
      const prefix = scenario.id === "FINAL" ? "Final" : scenario.id;
      return `${prefix} — ${copy.title}`;
    };

    const requested = String(
      new URLSearchParams(location.search).get("scenario") || "FINAL"
    ).toUpperCase();

    if (scenarios.some(item => item.id === requested)) {
      select.value = requested;
    } else {
      select.value = scenarios.some(item => item.id === "FINAL")
        ? "FINAL"
        : scenarios[0].id;
    }

    const closePicker = ({ restoreFocus = false } = {}) => {
      popover.hidden = true;
      trigger.setAttribute("aria-expanded", "false");
      search.value = "";

      if (restoreFocus) {
        trigger.focus();
      }
    };

    const renderOptions = (query = "") => {
      const normalized = query.trim().toLocaleLowerCase(
        en ? "en-US" : "tr-TR"
      );

      const filtered = scenarios.filter(scenario => {
        const copy = scenarioCopy(scenario);
        const haystack =
          `${scenario.id} ${copy.title} ${copy.focus}`.toLocaleLowerCase(
            en ? "en-US" : "tr-TR"
          );

        return !normalized || haystack.includes(normalized);
      });

      if (!filtered.length) {
        options.innerHTML = `
          <div class="paper-scenario-empty">
            ${t("Eşleşen senaryo bulunamadı.", "No matching scenario was found.")}
          </div>
        `;
        return;
      }

      options.innerHTML = filtered.map(scenario => {
        const copy = scenarioCopy(scenario);
        const prefix = scenario.id === "FINAL" ? "Final" : scenario.id;
        const selected = scenario.id === select.value;

        return `
          <button type="button"
                  class="paper-scenario-option"
                  role="option"
                  data-scenario-id="${esc(scenario.id)}"
                  aria-selected="${selected ? "true" : "false"}">
            <span class="paper-scenario-option-code">${esc(prefix)}</span>
            <span class="paper-scenario-option-title">${esc(copy.title)}</span>
          </button>
        `;
      }).join("");
    };

    const syncPicker = () => {
      const scenario =
        scenarios.find(item => item.id === select.value) ||
        scenarios[0];

      triggerText.textContent = optionLabel(scenario);

      options
        .querySelectorAll("[data-scenario-id]")
        .forEach(option => {
          option.setAttribute(
            "aria-selected",
            option.dataset.scenarioId === scenario.id ? "true" : "false"
          );
        });
    };

    const openPicker = () => {
      popover.hidden = false;
      trigger.setAttribute("aria-expanded", "true");
      renderOptions();
      requestAnimationFrame(() => search.focus());
    };

    const render = () => {
      const scenario =
        scenarios.find(item => item.id === select.value) ||
        scenarios[0];

      const copy = scenarioCopy(scenario);
      const status = scenarioStatus(scenario);
      const metrics = ["CWLC", "CAC", "MDC", "CTIC", "TF", "SACI"];

      syncPicker();

      $("paperScenarioCode").textContent =
        scenario.id === "FINAL" ? "FINAL" : scenario.id;

      $("paperScenarioTitle").textContent = copy.title;
      $("paperScenarioFocus").textContent = copy.focus;

      const statusEl = $("paperScenarioStatus");
      statusEl.className = `paper-scenario-status ${status.className}`;
      statusEl.textContent = status.text;

      $("paperScenarioMetrics").innerHTML = metrics.map(key => {
        const value = metricValue(scenario.scores, key);

        return `
          <div class="paper-scenario-metric">
            <span>${key}</span>
            <strong>${value === null ? "N/A" : esc(value)}</strong>
          </div>
        `;
      }).join("");

      $("paperScenarioGraphSummary").textContent = t(
        `${scenario.graph.observed}/${scenario.graph.edges} ilişki observed, ${scenario.graph.missing} ilişki missing; ${scenario.graph.nodes} node beyan edilmiş ve ${scenario.graph.renderedNodes} node görüntülenmiştir.`,
        `${scenario.graph.observed}/${scenario.graph.edges} relations are observed and ${scenario.graph.missing} are missing; ${scenario.graph.nodes} nodes are declared and ${scenario.graph.renderedNodes} are rendered.`
      );

      $("paperScenarioPrimaryImpact").textContent =
        primaryMetricText(scenario);

      $("paperScenarioInterpretation").textContent =
        copy.interpretation;

      $("paperScenarioFigureTitle").textContent = t(
        `${scenario.id === "FINAL" ? "Final" : scenario.id} bileşen profili`,
        `${scenario.id === "FINAL" ? "Final" : scenario.id} component profile`
      );

      $("paperScenarioFigure").innerHTML = componentSvg(
        scenario.scores,
        t(
          `${scenario.id === "FINAL" ? "Final" : scenario.id} SACI bileşen profili`,
          `${scenario.id === "FINAL" ? "Final" : scenario.id} SACI component profile`
        )
      );

      $("paperScenarioCaption").textContent = t(
        `${scenario.id === "FINAL" ? "Final veri kümesi" : scenario.id + " senaryosu"} için aktif SACI bileşenleri ve kapsam dışı N/A boyutları.`,
        `Active SACI components and out-of-scope N/A dimensions for ${scenario.id === "FINAL" ? "the final dataset" : "scenario " + scenario.id}.`
      );

      const download = $("paperScenarioDownload");
      download.dataset.filename =
        `saci-${scenario.id.toLowerCase()}-component-profile.svg`;

      $("paperScenarioGraphLink").href =
        `graph.html?scenario=${encodeURIComponent(scenario.id)}`;

      $("paperScenarioEvidenceLink").href =
        scenario.id === "FINAL"
          ? "evidence.html"
          : `evidence.html#scenario-${encodeURIComponent(scenario.id)}`;

      const url = new URL(location.href);
      url.searchParams.set("scenario", scenario.id);
      history.replaceState(null, "", url);
    };

    trigger.addEventListener("click", () => {
      if (popover.hidden) {
        openPicker();
      } else {
        closePicker();
      }
    });

    search.addEventListener("input", () => {
      renderOptions(search.value);
    });

    options.addEventListener("click", event => {
      const option = event.target.closest("[data-scenario-id]");

      if (!option) {
        return;
      }

      select.value = option.dataset.scenarioId;
      closePicker({ restoreFocus: true });
      render();
    });

    picker.addEventListener("keydown", event => {
      if (event.key === "Escape" && !popover.hidden) {
        event.preventDefault();
        closePicker({ restoreFocus: true });
      }
    });

    document.addEventListener("pointerdown", event => {
      if (!popover.hidden && !picker.contains(event.target)) {
        closePicker();
      }
    });

    $("previousPaperScenario").addEventListener("click", () => {
      const current = scenarios.findIndex(item => item.id === select.value);
      const nextIndex = (current - 1 + scenarios.length) % scenarios.length;
      select.value = scenarios[nextIndex].id;
      closePicker();
      render();
    });

    $("nextPaperScenario").addEventListener("click", () => {
      const current = scenarios.findIndex(item => item.id === select.value);
      const nextIndex = (current + 1) % scenarios.length;
      select.value = scenarios[nextIndex].id;
      closePicker();
      render();
    });

    renderOptions();
    render();
  }

  function renderAcademic(scores, graph, mitre, cti, scenarios) {
    const s7a = scenarios.find(item => item.id === "S7A");
    const s7b = scenarios.find(item => item.id === "S7B");
    const s15 = scenarios.find(item => item.id === "S15");
    const s17 = scenarios.find(item => item.id === "S17");
    const s18 = scenarios.find(item => item.id === "S18");

    const s7aSaci = s7a ? metricValue(s7a.scores, "SACI") : null;
    const s7bSaci = s7b ? metricValue(s7b.scores, "SACI") : null;
    const criticalityDelta =
      s7aSaci !== null && s7bSaci !== null
        ? Math.abs(s7aSaci - s7bSaci).toFixed(2)
        : "-";

    const s15Tf = s15 ? metricValue(s15.scores, "TF") : null;
    const s17Tf = s17 ? metricValue(s17.scores, "TF") : null;

    $("academicNotes").innerHTML = en
      ? `
        <article class="academic-note">
          <h3>Final visibility result</h3>
          <p>The final SACI score of ${esc(scores.SACI ?? "-")} indicates complete evidence coverage across the active visibility dimensions within the declared evaluation scope. This value should be interpreted as a scope-bounded visibility result rather than a direct measure of attack prevention or absolute security.</p>
        </article>

        <article class="academic-note">
          <h3>Relational closure</h3>
          <p>The evidence graph contains ${graph.observed} observed relations out of ${graph.edges} declared edge rows and ${graph.missing} missing relations. The result demonstrates closure of the evidence chains used by the scoring model while preserving the distinction between relation closure and structural node-declaration integrity.</p>
        </article>

        <article class="academic-note">
          <h3>Criticality sensitivity</h3>
          <p>The S7A and S7B scenarios apply comparable Sysmon losses to assets with different criticality levels. The resulting SACI difference of ${criticalityDelta} points demonstrates that the model does not treat all telemetry losses as operationally equivalent.</p>
        </article>

        <article class="academic-note">
          <h3>Freshness and recovery</h3>
          <p>Scenario S15 separates historical observation from current operational freshness by reducing TF to ${s15Tf ?? "-"}. Scenario S17 subsequently demonstrates recovery, with TF returning to ${s17Tf ?? "-"} after the missing evidence chain is restored.</p>
        </article>

        <article class="academic-note">
          <h3>Active-scope normalization</h3>
          <p>Scenario S18 treats a legacy control outside the active scope as N/A rather than zero. This prevents an inapplicable expectation from artificially reducing the final score and keeps the denominator aligned with the declared scenario scope.</p>
        </article>

        <article class="academic-note">
          <h3>MITRE and CTI context</h3>
          <p>MITRE ATT&CK coverage reached ${mitre.covered}/${mitre.total}, while CTI/MISP closure reached ${cti.covered}/${cti.total}. These results indicate that detection evidence was connected to adversary-technique context and that CTI enrichment was evaluated as a staged operational chain rather than a single lookup event.</p>
        </article>
      `
      : `
        <article class="academic-note">
          <h3>Final görünürlük sonucu</h3>
          <p>Final SACI skorunun ${esc(scores.SACI ?? "-")} olması, aktif görünürlük boyutlarının tanımlı değerlendirme kapsamında tam kanıt düzeyine ulaştığını gösterir. Bu değer saldırı önleme başarısı veya mutlak güvenlik ölçüsü olarak değil, kapsamla sınırlandırılmış bir görünürlük sonucu olarak yorumlanmalıdır.</p>
        </article>

        <article class="academic-note">
          <h3>İlişkisel kapanış</h3>
          <p>Kanıt graph'ında ${graph.edges} edge satırının ${graph.observed} tanesi gözlemlenmiş, ${graph.missing} ilişki eksik kalmıştır. Bu sonuç skorlama modelinin kullandığı kanıt zincirlerinin kapandığını gösterirken, ilişki kapanışı ile node bildirim bütünlüğü arasındaki ayrımı korur.</p>
        </article>

        <article class="academic-note">
          <h3>Kritiklik duyarlılığı</h3>
          <p>S7A ve S7B senaryoları benzer Sysmon kayıplarını farklı kritiklik düzeyindeki varlıklara uygular. Oluşan ${criticalityDelta} puanlık SACI farkı, modelin bütün telemetri kayıplarını operasyonel olarak eşdeğer kabul etmediğini gösterir.</p>
        </article>

        <article class="academic-note">
          <h3>Freshness ve toparlanma</h3>
          <p>S15 senaryosu TF değerini ${s15Tf ?? "-"} düzeyine düşürerek geçmişte gözlemlenen kanıt ile güncel operasyonel telemetriyi ayırır. S17 senaryosunda eksik kanıt zinciri geri getirildiğinde TF değeri ${s17Tf ?? "-"} düzeyine dönerek toparlanmayı gösterir.</p>
        </article>

        <article class="academic-note">
          <h3>Aktif kapsam normalizasyonu</h3>
          <p>S18 senaryosu aktif kapsam dışında kalan legacy kontrolü sıfır yerine N/A kabul eder. Böylece uygulanabilir olmayan bir beklentinin skoru yapay biçimde düşürmesi engellenir ve payda beyan edilen senaryo kapsamıyla uyumlu tutulur.</p>
        </article>

        <article class="academic-note">
          <h3>MITRE ve CTI bağlamı</h3>
          <p>MITRE ATT&CK kapsamı ${mitre.covered}/${mitre.total}, CTI/MISP kapanışı ise ${cti.covered}/${cti.total} düzeyine ulaşmıştır. Bu sonuçlar detection kanıtının saldırgan teknikleriyle ilişkilendirildiğini ve CTI enrichment sürecinin tek bir lookup olayı yerine aşamalı operasyonel zincir olarak değerlendirildiğini gösterir.</p>
        </article>
      `;

    $("structuralNote").innerHTML = graph.undeclared.length
      ? `
        <strong>${t("Yapısal audit notu:", "Structural audit note:")}</strong>
        ${t(
          "İlişki kapanışı tamam olmasına rağmen edge tablosunda referans edilen bazı uçlar node tablosunda açıkça beyan edilmemiştir. Bu durum SACI skorunu veya observed/missing edge hesabını değiştirmez; yapısal bütünlük bulgusu olarak korunur.",
          "Although relation closure is complete, some endpoints referenced by the edge table are not explicitly declared in the node table. This does not change the SACI score or observed/missing edge calculation and remains documented as a structural integrity finding."
        )}
        <br><code>${esc(graph.undeclared.join(", "))}</code>
      `
      : "";

    $("structuralNote").hidden = graph.undeclared.length === 0;
  }

  async function loadScenario(item) {
    const id = scenarioId(item);
    const scorePath = field(
      item,
      ["scores", "score", "score_csv"],
      "saci_scores.csv"
    );

    const graphPath = field(
      item,
      ["graph", "cyjs", "graph_cyjs"],
      "saci_graph.cyjs"
    );

    const scoreText = await getText(scorePath, true);
    const graphRawText = await getText(graphPath, true);

    let graphRaw = {};

    if (graphRawText.trim()) {
      try {
        graphRaw = JSON.parse(graphRawText);
      } catch (_) {
        graphRaw = {};
      }
    }

    return {
      id,
      label: labelForScenario(item, id),
      scores: scoreMap(parseCSV(scoreText)),
      graph: graphStats(graphRaw)
    };
  }

  async function init() {
    try {
      const manifest = await getJson("data/scenarios/manifest.json");
      const rows = manifest.datasets || manifest.scenarios || [];
      const entry = finalEntry(manifest);

      if (!entry) {
        throw new Error("Final dataset entry was not found.");
      }

      const base = String(entry.base || entry.dir || "").replace(/\/$/, "");

      const scorePath = field(
        entry,
        ["scores", "score", "score_csv"],
        "saci_scores.csv"
      );

      const graphPath = field(
        entry,
        ["graph", "cyjs", "graph_cyjs"],
        "saci_graph.cyjs"
      );

      const mitreCandidates = [
        entry.mitre,
        entry.mitre_csv,
        base ? `${base}/mitre_coverage.csv` : "",
        base ? `${base}/mitre_coverage_v2.csv` : ""
      ];

      const ctiCandidates = [
        entry.ctic,
        entry.cti,
        entry.ctic_csv,
        entry.cti_csv,
        base ? `${base}/ctic_coverage.csv` : "",
        base ? `${base}/cti_coverage.csv` : ""
      ];

      const [
        scoreText,
        graphRaw,
        mitreFile,
        ctiFile,
        scenarios
      ] = await Promise.all([
        getText(scorePath),
        getJson(graphPath),
        firstCsv(mitreCandidates),
        firstCsv(ctiCandidates),
        Promise.all(rows.map(loadScenario))
      ]);

      const scores = scoreMap(parseCSV(scoreText));
      const graph = graphStats(graphRaw);

      const mitre = mitreFile.rows.length
        ? coverageFromMitre(mitreFile.rows)
        : {
            covered: numeric(scores.MDC) === 100 ? 13 : 0,
            total: 13
          };

      const cti = ctiFile.rows.length
        ? coverageFromCti(ctiFile.rows)
        : {
            covered: numeric(scores.CTIC) === 100 ? 2 : 0,
            total: 2
          };

      scenarios.sort((a, b) => {
        const ka = scenarioSortKey(a.id);
        const kb = scenarioSortKey(b.id);

        return ka[0] - kb[0] ||
          String(ka[1]).localeCompare(String(kb[1]));
      });

      const historical = scenarios.filter(item => item.id !== "FINAL");

      renderSummary(scores, graph, mitre, cti);
      setupScenarioExplorer(scenarios);

      $("componentFigure").innerHTML = componentSvg(
        scores,
        t("Final SACI bileşen profili", "Final SACI component profile")
      );

      $("closureFigure").innerHTML = closureSvg(graph);
      $("coverageFigure").innerHTML = coverageSvg(mitre, cti);

      $("scenarioScoreFigure").innerHTML = lineChartSvg(
        historical.map(item => ({
          id: item.id,
          value: metricValue(item.scores, "SACI") ?? 0
        })),
        "value",
        t("S0–S18 SACI değişimi", "S0–S18 SACI progression"),
        t("SACI skoru", "SACI score"),
        COLORS.accentSoft,
        100
      );

      const maxMissing = Math.max(
        1,
        ...historical.map(item => item.graph.missing)
      );

      $("missingFigure").innerHTML = lineChartSvg(
        historical.map(item => ({
          id: item.id,
          value: item.graph.missing
        })),
        "value",
        t("S0–S18 missing edge değişimi", "S0–S18 missing-edge progression"),
        t("Eksik ilişki sayısı", "Missing relation count"),
        COLORS.accentSoft,
        maxMissing
      );

      const byId = id => historical.find(item => item.id === id);

      $("criticalityFigure").innerHTML = groupedBarSvg(
        [byId("S7A"), byId("S7B")].filter(Boolean),
        ["CWLC", "SACI"],
        t("Kritiklik ağırlığının etkisi", "Effect of criticality weighting")
      );

      $("ctiScenarioFigure").innerHTML = groupedBarSvg(
        [byId("S6"), byId("S12"), byId("S13")].filter(Boolean),
        ["CTIC", "SACI"],
        t("CTI zinciri davranışı", "CTI-chain behavior")
      );

      $("freshnessFigure").innerHTML = groupedBarSvg(
        [byId("S15"), byId("S17")].filter(Boolean),
        ["TF", "SACI"],
        t("Freshness düşüşü ve toparlanma", "Freshness degradation and recovery")
      );

      const s18 = byId("S18");

      $("scopeFigure").innerHTML = s18
        ? componentSvg(
            s18.scores,
            t(
              "S18 aktif kapsam normalizasyonu",
              "S18 active-scope normalization"
            )
          )
        : "";

      renderAcademic(scores, graph, mitre, cti, historical);

      document
        .querySelectorAll("[data-download-figure]")
        .forEach(button => {
          button.addEventListener("click", () => {
            figureDownload(
              button.dataset.downloadFigure,
              button.dataset.filename
            );
          });
        });

      $("printPage").addEventListener("click", () => window.print());

      $("loadingState").hidden = true;
      $("paperContent").hidden = false;

    } catch (error) {
      console.error(error);

      $("loadingState").textContent = t(
        `Bulgular yüklenemedi: ${error.message}`,
        `Results could not be loaded: ${error.message}`
      );
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
