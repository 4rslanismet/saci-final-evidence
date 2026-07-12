#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / "docs"
EN = DOCS / "en"
ASSETS = DOCS / "assets"
VERSION = "scenario-analysis-2"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "backups" / f"scenario_analysis_{STAMP}"

SCENARIO_CSS = r"""
body[data-page="scenarios"]{overflow-x:hidden}
.scenario-page{width:min(calc(100% - clamp(36px,8vw,128px)),1440px)!important;max-width:none!important;margin-inline:auto!important;padding-top:clamp(34px,4vw,58px)!important;padding-bottom:clamp(64px,7vw,104px)!important}
.scenario-hero{max-width:94rem;margin-bottom:clamp(28px,4vw,52px)}
.scenario-hero h1{max-width:18ch!important;margin:0 0 20px!important;color:var(--text)!important;font-size:clamp(46px,5.6vw,78px)!important;font-weight:720!important;line-height:1.01!important;letter-spacing:-.05em!important;text-wrap:balance}
.scenario-hero .lead{max-width:79ch!important;margin:0 0 15px!important;color:var(--muted)!important;font-size:clamp(17px,.5vw + 15px,21px)!important;line-height:1.72!important}
.scenario-note{max-width:82ch;margin-top:20px;padding:13px 15px;border-left:2px solid var(--accent);border-radius:0 12px 12px 0;background:color-mix(in srgb,var(--accent) 6%,transparent);color:var(--muted);font-size:14px;line-height:1.7}
.scenario-summary{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-bottom:18px}
.scenario-summary-card,.scenario-card,.comparison-card{min-width:0;padding:15px;border:1px solid color-mix(in srgb,var(--line) 62%,transparent);border-radius:16px;background:color-mix(in srgb,var(--surface,var(--bg)) 80%,transparent)}
.scenario-summary-card span{display:block;margin-bottom:7px;color:var(--muted);font-size:11.5px;font-weight:650}.scenario-summary-card strong{display:block;color:var(--text);font-size:clamp(22px,2vw,30px)}
.scenario-section{margin-top:clamp(46px,6vw,82px)}.scenario-section-head{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-bottom:18px}.scenario-section-head h2{margin:0!important;max-width:28ch!important;color:var(--text)!important;font-size:clamp(29px,3vw,42px)!important;line-height:1.1!important;letter-spacing:-.035em!important}.scenario-section-head p{max-width:72ch;margin:0;color:var(--muted);font-size:14.5px;line-height:1.68}
.scenario-toolbar{position:sticky;top:82px;z-index:25;display:grid;grid-template-columns:minmax(240px,1fr) minmax(210px,.45fr) auto;gap:10px;align-items:end;margin-bottom:14px;padding:11px;border:1px solid color-mix(in srgb,var(--line) 68%,transparent);border-radius:17px;background:color-mix(in srgb,var(--bg) 90%,transparent);backdrop-filter:blur(14px)}
.scenario-toolbar label{display:block;margin-bottom:6px;color:var(--muted);font-size:11.5px;font-weight:680}.scenario-toolbar input,.scenario-toolbar select,.scenario-toolbar button{height:42px;border:1px solid color-mix(in srgb,var(--line) 74%,transparent);border-radius:12px;background:color-mix(in srgb,var(--surface,var(--bg)) 82%,transparent);color:var(--text);font:inherit;font-size:13px}.scenario-toolbar input,.scenario-toolbar select{width:100%;padding-inline:12px}.scenario-toolbar button{padding-inline:16px;cursor:pointer;font-weight:680}
.scenario-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.scenario-card{padding:18px}.scenario-card-head{display:flex;align-items:start;justify-content:space-between;gap:14px;margin-bottom:12px}.scenario-card h3{margin:3px 0 6px;color:var(--text);font-size:20px;line-height:1.25}.scenario-id{color:var(--accent);font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12px;font-weight:720}.scenario-card p{max-width:none!important;margin:0 0 12px;color:var(--muted);font-size:14px!important;line-height:1.7!important}
.status-chip{display:inline-flex;align-items:center;gap:7px;min-height:30px;padding:0 10px;border:1px solid color-mix(in srgb,var(--line) 66%,transparent);border-radius:999px;background:color-mix(in srgb,var(--surface,var(--bg)) 78%,transparent);color:var(--text);font-size:11.5px;font-weight:720;white-space:nowrap}.status-chip:before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}.status-chip.complete{color:var(--green,#22c55e);border-color:color-mix(in srgb,var(--green,#22c55e) 34%,var(--line));background:color-mix(in srgb,var(--green,#22c55e) 8%,var(--surface,var(--bg)))}.status-chip.partial{color:var(--yellow,#eab308);border-color:color-mix(in srgb,var(--yellow,#eab308) 34%,var(--line));background:color-mix(in srgb,var(--yellow,#eab308) 8%,var(--surface,var(--bg)))}.status-chip.baseline{color:var(--accent);border-color:color-mix(in srgb,var(--accent) 34%,var(--line));background:color-mix(in srgb,var(--accent) 7%,var(--surface,var(--bg)))}
.metric-strip{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:7px;margin:12px 0}.metric-box,.scenario-fact{min-width:0;padding:9px;border:1px solid color-mix(in srgb,var(--line) 52%,transparent);border-radius:11px;background:color-mix(in srgb,var(--bg) 78%,transparent)}.metric-box span,.scenario-fact span{display:block;margin-bottom:4px;color:var(--muted);font-size:10.5px;font-weight:670}.metric-box strong{display:block;color:var(--text);font-size:17px}.scenario-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin:12px 0}.scenario-fact strong{color:var(--text);font-size:15px}
.scenario-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:13px}.scenario-actions a{display:inline-flex;align-items:center;justify-content:center;min-height:34px;padding:0 11px;border:1px solid color-mix(in srgb,var(--line) 62%,transparent);border-radius:999px;background:transparent;color:var(--text);text-decoration:none;font-size:12px;font-weight:670}.scenario-actions a:hover{border-color:color-mix(in srgb,var(--accent) 48%,var(--line));color:var(--accent)}
.comparison-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.comparison-card h3{margin:0 0 9px;color:var(--text);font-size:17px}.comparison-card p{margin:0;color:var(--muted);font-size:13.5px;line-height:1.68}
.table-shell{overflow-x:auto;border:1px solid color-mix(in srgb,var(--line) 64%,transparent);border-radius:17px;background:color-mix(in srgb,var(--surface,var(--bg)) 78%,transparent)}.scenario-table{width:100%;min-width:1120px;border-collapse:collapse}.scenario-table th,.scenario-table td{padding:12px 11px;border-bottom:1px solid color-mix(in srgb,var(--line) 46%,transparent);text-align:left;vertical-align:top}.scenario-table th{position:sticky;top:0;z-index:2;background:var(--bg);color:var(--muted);font-size:11px;font-weight:720;letter-spacing:.03em;text-transform:uppercase}.scenario-table td{color:var(--muted);font-size:12.5px;line-height:1.55}.scenario-table td strong{color:var(--text);font-weight:680}.scenario-table tr:hover td{background:color-mix(in srgb,var(--accent) 4%,transparent)}.score-value{display:block;color:var(--text);font-size:17px;font-weight:720}.score-bar{display:block;width:100%;height:4px;margin-top:6px;border-radius:999px;background:color-mix(in srgb,var(--line) 54%,transparent);overflow:hidden}.score-bar span{display:block;height:100%;background:var(--accent)}.table-link{color:var(--accent);text-decoration:none;font-weight:660}
.mitre-panel{margin-top:12px;padding:13px;border:1px solid color-mix(in srgb,var(--line) 52%,transparent);border-radius:13px;background:color-mix(in srgb,var(--bg) 76%,transparent)}.mitre-panel h4{margin:0 0 10px;color:var(--text);font-size:14px}.mitre-group{margin-top:10px}.mitre-group-title{display:inline-flex;margin-bottom:6px;color:var(--accent);font-size:12px;font-weight:720;text-decoration:none}.mitre-techniques{display:flex;flex-wrap:wrap;gap:6px}.mitre-technique{display:inline-flex;align-items:center;gap:6px;min-height:29px;padding:0 9px;border:1px solid color-mix(in srgb,var(--line) 52%,transparent);border-radius:999px;color:var(--text);text-decoration:none;font-size:11.5px}
.empty-state{padding:18px;border:1px dashed color-mix(in srgb,var(--line) 70%,transparent);border-radius:14px;color:var(--muted);font-size:14px;line-height:1.68}
@media(max-width:1120px){.scenario-summary{grid-template-columns:repeat(3,minmax(0,1fr))}.scenario-cards,.comparison-grid{grid-template-columns:1fr}.scenario-toolbar{position:static;grid-template-columns:1fr 1fr auto}}@media(max-width:760px){.scenario-page{width:min(calc(100% - 26px),1440px)!important}.scenario-section-head{align-items:start;flex-direction:column}.scenario-toolbar,.scenario-summary,.metric-strip,.scenario-facts{grid-template-columns:1fr 1fr}}@media(max-width:520px){.scenario-toolbar,.scenario-summary,.metric-strip,.scenario-facts{grid-template-columns:1fr}}
"""

SCENARIO_JS = r"""
(() => {
  const $ = id => document.getElementById(id);
  const en = (document.documentElement.lang || "").toLowerCase().startsWith("en");
  const t = (tr, enText) => en ? enText : tr;
  const esc = value => String(value ?? "").replace(/[<>&"]/g, c => ({"<":"&lt;",">":"&gt;","&":"&amp;",'"':"&quot;"}[c]));
  const reps = new Set(["S0","S7A","S7B","S8","S12","S13","S14","S15","S17","S18"]);
  const comments = {
    S0:["SIEM bulunmadığı için merkezi kanıt zinciri ve görünürlük tabanı kurulamamıştır.","Without a SIEM, the central evidence chain and visibility baseline cannot be established.","baseline"],
    S1:["Wazuh kurulmuştur; ancak varlık, telemetri ve kontrol kapsamı henüz tamamlanmamıştır.","Wazuh is deployed, but asset, telemetry and control coverage is not yet complete.","baseline"],
    S2:["Envanter beyan edilmiştir; gözlenen log kaynakları henüz beklenen kapsamı karşılamamaktadır.","The inventory is declared, but observed log sources do not yet satisfy the expected scope.","telemetry"],
    S3:["Log kaynakları bağlanmıştır; detection ve üst bağlam ilişkileri henüz tamamlanmamıştır.","Log sources are connected, while detection and higher-level context relations remain incomplete.","telemetry"],
    S4:["Detection kontrolleri etkinleşmiştir; MITRE ve CTI bağlamı henüz tam kapanmamıştır.","Detection controls are active, but MITRE and CTI context is not yet fully closed.","detection"],
    S5:["MITRE kapsamı tanımlıdır; bazı teknikler henüz detection kanıtıyla doğrulanmamıştır.","MITRE scope is declared, but some techniques are not yet validated by detection evidence.","mitre"],
    S6:["CTI enrichment etkinleştirilmiştir; lookup, hit ve alarm geri dönüş zinciri doğrulanmaktadır.","CTI enrichment is enabled; lookup, hit and alert-return relations are being validated.","cti"],
    S7:["Temel görünürlük çalışmaktadır; ancak bazı ilişkiler eksik olduğu için kapanış kısmidir.","Core visibility works, but closure remains partial because some relations are missing.","closure"],
    S7A:["Kritik DC01 üzerindeki Sysmon kaybı, kritiklik ağırlığı nedeniyle daha yüksek etki üretir.","Sysmon loss on critical DC01 has a greater impact because of asset criticality.","telemetry"],
    S7B:["Kritik olmayan WS01 Sysmon kaybı görünürlüğü azaltır; etkisi DC01 kaybından düşük olmalıdır.","Non-critical WS01 Sysmon loss reduces visibility, but should have less impact than the DC01 loss.","telemetry"],
    S8:["Tarihsel doğrulama serisindeki kapanış noktasıdır; yayın finaliyle birleştirilmez.","Closure point of the historical validation series; it is not merged with the publication final.","closure"],
    S9:["DC01 Security telemetrisi kaybı kimlik ve erişim davranışlarının görünürlüğünü azaltır.","Loss of DC01 Security telemetry reduces visibility into identity and access behavior.","telemetry"],
    S10:["PowerShell telemetrisi kaybı T1059.001 ve komut içeriği görünürlüğünü zayıflatır.","PowerShell telemetry loss weakens T1059.001 and command-content visibility.","telemetry"],
    S11:["Linux authlog kaybı SSH ve kimlik doğrulama kontrollerinin kanıt zincirini keser.","Linux auth-log loss interrupts evidence for SSH and authentication controls.","telemetry"],
    S12:["Firewall IOC alarmı görünürdür; ancak MISP/CTI bağlam zinciri tam kapanmamıştır.","The firewall IOC alert is visible, but the MISP/CTI context chain is not fully closed.","cti"],
    S13:["MISP lookup çalışmıştır; IOC hit oluşmaması entegrasyon arızasıyla aynı şey değildir.","The MISP lookup ran; absence of an IOC hit is not the same as an integration failure.","cti"],
    S14:["MITRE kapsamı genişlediğinde yeni teknik için detection boşluğu skora yansır.","When MITRE scope expands, the detection gap for the new technique is reflected in the score.","mitre"],
    S15:["Geçmişte gözlenen telemetri güncelliğini kaybettiğinde TF metriği düşer.","When previously observed telemetry becomes stale, the TF metric decreases.","freshness"],
    S16:["Telemetri mevcut olsa da beklenen Wazuh rule veya alarm kanıtı oluşmamıştır.","Telemetry exists, but the expected Wazuh-rule or alert evidence was not produced.","detection"],
    S17:["Düzeltme sonrasında eksik ilişkilerin yeniden gözlemlendiği toparlanma senaryosudur.","Recovery scenario in which missing relations become observed again after remediation.","recovery"],
    S18:["Legacy kontrol N/A kabul edilir; aktif ağırlıklar yeniden normalize edilir.","The legacy control is treated as N/A and active weights are renormalized.","scope"]
  };
  const tacticIds={"Reconnaissance":"TA0043","Resource Development":"TA0042","Initial Access":"TA0001","Execution":"TA0002","Persistence":"TA0003","Privilege Escalation":"TA0004","Defense Evasion":"TA0005","Credential Access":"TA0006","Discovery":"TA0007","Lateral Movement":"TA0008","Collection":"TA0009","Command and Control":"TA0011","Exfiltration":"TA0010","Impact":"TA0040"};
  async function text(url){if(!url)return"";const r=await fetch(url,{cache:"no-store"});if(!r.ok)throw new Error(`${url} HTTP ${r.status}`);return await r.text()}
  async function json(url){return JSON.parse(await text(url))}
  function csv(raw){if(!raw.trim())return[];const rows=[];let row=[],field="",q=false;for(let i=0;i<raw.length;i++){const c=raw[i],n=raw[i+1];if(q){if(c==='"'&&n==='"'){field+='"';i++}else if(c==='"')q=false;else field+=c}else if(c==='"')q=true;else if(c===','){row.push(field);field=""}else if(c==='\n'){row.push(field.replace(/\r$/,""));rows.push(row);row=[];field=""}else field+=c}if(field.length||row.length){row.push(field.replace(/\r$/,""));rows.push(row)}const h=(rows.shift()||[]).map(x=>x.trim());return rows.filter(r=>r.some(x=>String(x).trim())).map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]??""])))}
  function idOf(item){const raw=String(item.id||item.scenario||item.name||"");if(/final/i.test(raw)||String(item.kind||"").toLowerCase()==="canonical")return"FINAL";const m=raw.match(/S\d+[A-Za-z]?/i);return m?m[0].toUpperCase():raw.toUpperCase()}
  function field(item,keys,fallback){for(const k of keys)if(item[k])return item[k];const base=item.base||item.dir||"";return base&&fallback?`${String(base).replace(/\/$/,"")}/${fallback}`:""}
  function scores(rows){const out={};if(rows.length===1)for(const[k,v]of Object.entries(rows[0])){const n=k.toUpperCase();if(["CWLC","LC","CAC","MDC","CTIC","TF","SACI"].includes(n))out[n==="LC"?"CWLC":n]=v}for(const r of rows){const k=String(r.metric||r.name||r.component||"").toUpperCase();if(k)out[k==="LC"?"CWLC":k]=r.score??r.value??r.result??""}return out}
  function elements(raw){if(Array.isArray(raw))return raw;if(Array.isArray(raw.elements))return raw.elements;if(raw.elements?.nodes&&raw.elements?.edges)return[...raw.elements.nodes,...raw.elements.edges];if(raw.nodes&&raw.edges)return[...raw.nodes,...raw.edges];return[]}
  function stats(raw){const es=elements(raw),edges=es.filter(x=>x?.data?.source&&x?.data?.target),nodes=es.filter(x=>!(x?.data?.source&&x?.data?.target)),obs=edges.filter(x=>[1,true,"1","true"].includes(x.data.observed)).length;return{nodes:nodes.length,edges:edges.length,observed:obs,missing:edges.length-obs,elements:es}}
  function mitre(rows,es){if(rows.length)return rows.map(r=>({id:r.technique_id||r.technique||r.id||"",name:r.technique_name||r.name||r.technique||r.technique_id||"",tactic:r.tactic||r.tactics||"Unknown",covered:r.covered??r.observed??"1"}));return es.filter(x=>{const d=x.data||{},type=d.type||d.node_type||d.group||"";return type==="mitre_technique"||/^MITRE:T\d{4}/.test(String(d.id||""))}).map(x=>{const d=x.data||{};return{id:String(d.technique_id||d.id||"").replace(/^MITRE:/,""),name:d.technique_name||d.label||d.name||d.id||"",tactic:d.tactic||d.tactics||"Unknown",covered:d.covered??1}})}
  function techniqueUrl(id){const clean=String(id).replace(/^MITRE:/i,""),[base,sub]=clean.split(".");return`https://attack.mitre.org/techniques/${base}/${sub?sub+"/":""}`}
  function tacticUrl(name){const id=tacticIds[String(name).trim()];return id?`https://attack.mitre.org/tactics/${id}/`:"https://attack.mitre.org/tactics/enterprise/"}
  const covered=v=>[1,true,"1","true"].includes(v);
  function metric(d,k){const v=d.scores[k];return v===undefined||v===""?"-":v}
  function status(d){if(d.id==="S0")return["baseline",t("Başlangıç","Baseline")];if(Number(d.stats.missing)===0&&Number(d.scores.SACI)===100)return["complete",t("Kapanış tamam","Closure complete")];return["partial",t("Kısmi kapsama","Partial coverage")]}
  function graphLink(d){return`graph.html?scenario=${encodeURIComponent(d.id)}`}
  function metricStrip(d){return`<div class="metric-strip">${["CWLC","CAC","MDC","CTIC","TF","SACI"].map(k=>`<div class="metric-box"><span>${k}</span><strong>${esc(metric(d,k))}</strong></div>`).join("")}</div>`}
  function mitreHtml(d){if(!d.mitre.length)return`<div class="empty-state">${t("Bu senaryoda MITRE eşleşmesi bulunamadı.","No MITRE mapping was found for this scenario.")}</div>`;const g=new Map();for(const item of d.mitre)for(const tactic of String(item.tactic||"Unknown").split(/[\/,;]/).map(x=>x.trim()).filter(Boolean)){if(!g.has(tactic))g.set(tactic,[]);g.get(tactic).push(item)}return`<div class="mitre-panel"><h4>${t("MITRE ATT&CK eşleşmeleri","MITRE ATT&CK mappings")}</h4>${[...g.entries()].map(([t,items])=>`<div class="mitre-group"><a class="mitre-group-title" href="${tacticUrl(t)}" target="_blank" rel="noopener">${esc(t)}</a><div class="mitre-techniques">${items.map(i=>`<a class="mitre-technique" href="${techniqueUrl(i.id)}" target="_blank" rel="noopener"><strong>${esc(i.id)}</strong><span>${esc(i.name)}</span></a>`).join("")}</div></div>`).join("")}</div>`}
  function card(d){const[s,l]=status(d),cov=d.mitre.filter(x=>covered(x.covered)).length;return`<article class="scenario-card" data-category="${esc(d.category)}" data-search="${esc((d.id+" "+d.label+" "+d.comment).toLowerCase())}"><div class="scenario-card-head"><div><span class="scenario-id">${esc(d.id)}</span><h3>${esc(d.label)}</h3></div><span class="status-chip ${s}">${esc(l)}</span></div><p>${esc(d.comment)}</p>${metricStrip(d)}<div class="scenario-facts"><div class="scenario-fact"><span>Observed</span><strong>${d.stats.observed}</strong></div><div class="scenario-fact"><span>Missing</span><strong>${d.stats.missing}</strong></div><div class="scenario-fact"><span>MITRE</span><strong>${cov}/${d.mitre.length}</strong></div></div>${mitreHtml(d)}<div class="scenario-actions"><a href="${graphLink(d)}">${t("Graph'ta aç","Open in graph")}</a>${d.scorePath?`<a href="${esc(d.scorePath)}" target="_blank">${t("Skor CSV","Score CSV")}</a>`:""}${d.summaryPath?`<a href="${esc(d.summaryPath)}" target="_blank">${t("Özet","Summary")}</a>`:""}</div></article>`}
  function row(d){const cov=d.mitre.filter(x=>covered(x.covered)).length,score=Number(d.scores.SACI),pct=Number.isFinite(score)?Math.max(0,Math.min(100,score)):0;return`<tr data-category="${esc(d.category)}" data-search="${esc((d.id+" "+d.label+" "+d.comment).toLowerCase())}"><td><strong>${esc(d.id)}</strong></td><td><strong>${esc(d.label)}</strong><br>${esc(d.comment)}</td>${["CWLC","CAC","MDC","CTIC","TF"].map(k=>`<td>${esc(metric(d,k))}</td>`).join("")}<td><span class="score-value">${esc(metric(d,"SACI"))}</span><span class="score-bar"><span style="width:${pct}%"></span></span></td><td>${d.stats.observed}</td><td>${d.stats.missing}</td><td>${cov}/${d.mitre.length}</td><td><a class="table-link" href="${graphLink(d)}">Graph</a></td></tr>`}
  function compare(map){const a=map.get("S7A"),b=map.get("S7B"),s12=map.get("S12"),s13=map.get("S13");const delta=a&&b&&Number.isFinite(Number(a.scores.SACI))&&Number.isFinite(Number(b.scores.SACI))?Math.abs(Number(a.scores.SACI)-Number(b.scores.SACI)).toFixed(2):"-";const cards=[[t("Kritiklik duyarlılığı","Criticality sensitivity"),t(`S7A kritik DC01, S7B kritik olmayan WS01 kaybını gösterir. SACI farkı ${delta} puandır.`,`S7A represents critical DC01 loss and S7B non-critical WS01 loss. The SACI difference is ${delta} points.`)],[t("CTI aşamalarının ayrıştırılması","Separation of CTI stages"),t("S12 açık CTI bağlam zincirini, S13 ise lookup çalışmasına rağmen IOC hit bulunmamasını gösterir.","S12 shows an open CTI context chain, while S13 shows a lookup without an IOC hit.")],[t("Kapsam genişleme tepkisi","Scope-expansion response"),map.get("S14")?.comment||""],[t("Freshness duyarlılığı","Freshness sensitivity"),map.get("S15")?.comment||""],[t("Düzeltme sonrası toparlanma","Post-remediation recovery"),map.get("S17")?.comment||""],[t("N/A ve aktif ağırlık normalizasyonu","N/A and active-weight normalization"),map.get("S18")?.comment||""]];$("comparisonGrid").innerHTML=cards.map(c=>`<article class="comparison-card"><h3>${esc(c[0])}</h3><p>${esc(c[1])}</p></article>`).join("")}
  function filter(){const q=($("scenarioSearch").value||"").trim().toLowerCase(),cat=$("categoryFilter").value;document.querySelectorAll("[data-search]").forEach(n=>n.hidden=!((!q||(n.dataset.search||"").includes(q))&&(!cat||n.dataset.category===cat)))}
  function render(data){const hist=data.filter(x=>x.id!=="FINAL"),rep=hist.filter(x=>reps.has(x.id)),map=new Map(data.map(x=>[x.id,x]));$("summaryTotal").textContent=hist.length;$("summaryRepresentative").textContent=rep.length;$("summaryComplete").textContent=hist.filter(x=>x.stats.missing===0).length;$("summaryWithGaps").textContent=hist.filter(x=>x.stats.missing>0).length;$("summaryMitre").textContent=hist.reduce((s,x)=>s+x.mitre.length,0);$("representativeGrid").innerHTML=rep.map(card).join("");$("scenarioTableBody").innerHTML=hist.map(row).join("");compare(map);const labels={baseline:t("Başlangıç","Baseline"),telemetry:t("Telemetri","Telemetry"),detection:"Detection",mitre:"MITRE",cti:"CTI",freshness:t("Güncellik","Freshness"),closure:t("Kapanış","Closure"),recovery:t("Toparlanma","Recovery"),scope:t("Kapsam","Scope")};const cats=[...new Set(hist.map(x=>x.category))];$("categoryFilter").innerHTML=`<option value="">${t("Tüm kategoriler","All categories")}</option>`+cats.map(c=>`<option value="${c}">${esc(labels[c]||c)}</option>`).join("");$("scenarioSearch").oninput=filter;$("categoryFilter").onchange=filter;$("clearFilter").onclick=()=>{$("scenarioSearch").value="";$("categoryFilter").value="";filter()}}
  async function load(item){const id=idOf(item),graphPath=field(item,["graph","cyjs","graph_cyjs"],"saci_graph.cyjs"),scorePath=field(item,["scores","score","score_csv"],"saci_scores.csv"),mitrePath=field(item,["mitre","mitre_csv"],"mitre_coverage.csv"),summaryPath=field(item,["summary","graph_summary"],"saci_graph_summary.md");let sr=[],gr={},mr=[];try{sr=csv(await text(scorePath))}catch{}try{gr=await json(graphPath)}catch{}try{mr=csv(await text(mitrePath))}catch{}const st=stats(gr),sc=scores(sr),mi=mitre(mr,st.elements),meta=comments[id]||["Ara doğrulama senaryosu.","Intermediate validation scenario.","closure"];return{id,label:en?(item.label_en||item.label||item.title||id):(item.label_tr||item.label||item.title||id),comment:meta[en?1:0],category:meta[2],scores:sc,stats:st,mitre:mi,graphPath,scorePath,summaryPath}}
  async function init(){try{const m=await json("data/scenarios/manifest.json"),items=m.datasets||m.scenarios||[];if(!items.length)throw new Error("Scenario manifest is empty.");const data=await Promise.all(items.map(load));data.sort((a,b)=>{const pa=a.id==="FINAL"?[-1,""]:(a.id.match(/^S(\d+)([A-Z]?)$/)||[0,999,a.id]).slice(1),pb=b.id==="FINAL"?[-1,""]:(b.id.match(/^S(\d+)([A-Z]?)$/)||[0,999,b.id]).slice(1);return Number(pa[0])-Number(pb[0])||String(pa[1]).localeCompare(String(pb[1]))});$("loadingState").hidden=true;render(data)}catch(e){console.error(e);$("loadingState").textContent=t(`Senaryo verileri yüklenemedi: ${e.message}`,`Scenario data could not be loaded: ${e.message}`)}}
  document.readyState==="loading"?document.addEventListener("DOMContentLoaded",init):init();
})();
"""

SCENARIO_LINK_JS = r"""
(() => {
  const wanted = new URLSearchParams(location.search).get("scenario") || "";
  if (!wanted) return;
  let attempts = 0;
  const timer = setInterval(() => {
    attempts++;
    const select = document.getElementById("scenarioSelect");
    if (!select || !select.options.length) {
      if (attempts > 80) clearInterval(timer);
      return;
    }
    const upper = wanted.toUpperCase();
    const option = [...select.options].find(o => String(o.value).toUpperCase() === upper || String(o.value).toUpperCase().startsWith(upper + "_") || String(o.textContent).toUpperCase().startsWith(upper + " "));
    if (option) {
      select.value = option.value;
      select.dispatchEvent(new Event("change", { bubbles: true }));
    }
    clearInterval(timer);
  }, 100);
})();
"""

NAV_PAGES = [
    ("index.html", "Home"),
    ("methodology.html", "Methodology"),
    ("architecture.html", "Architecture"),
    ("evidence.html", "Evidence"),
    ("scenarios.html", "Scenarios"),
    ("artifacts.html", "Artifacts"),
    ("graph.html", "Graph"),
    ("explanation.html", "Explanation"),
    ("paper.html", "Paper View"),
]

def nav(active: str) -> str:
    return "\n      ".join(
        f'<a{" class=\"active\"" if f == active else ""} href="{f}">{label}</a>'
        for f, label in NAV_PAGES
    )

def header(english: bool) -> str:
    skip = "Skip to main content" if english else "Ana içeriğe geç"
    return f'''<a class="skip-link" href="#main">{skip}</a>
<header class="top">
  <div class="top-inner">
    <a class="brand" href="index.html">SACI Final Evidence</a>
    <nav class="nav" aria-label="Primary navigation">
      {nav("scenarios.html")}
    </nav>
    <div class="top-actions" aria-label="Display controls">
      <div class="top-control"><span>Language</span><button type="button" id="langTR">TR</button><button type="button" id="langEN">EN</button></div>
      <div class="top-control"><span>Font</span><button type="button" id="fontDown">A-</button><button type="button" id="fontReset">A</button><button type="button" id="fontUp">A+</button></div>
      <div class="top-control"><span>Theme</span><button type="button" data-theme-btn="dark">Dark</button><button type="button" data-theme-btn="dim">Dim</button><button type="button" data-theme-btn="light">Light</button></div>
    </div>
  </div>
</header>'''

def page(english: bool) -> str:
    prefix = "../" if english else ""
    lang = "en" if english else "tr"
    if english:
        title, kicker = "Scenario analysis", "SCENARIO ANALYSIS"
        lead = "This page evaluates how SACI responds to telemetry losses, detection gaps, MITRE scope changes, CTI interruptions, freshness decay and remediation."
        note = "The publication final and the historical S0-S18 validation series are kept separate. Scenario node, edge and score values are not merged into the final publication dataset."
        rep_title, rep_desc = "Detailed scenario reviews", "Detailed views of the scenarios that best demonstrate sensitivity, explainability and recovery behavior."
        comp_title, comp_desc = "Methodological comparisons", "These comparisons show why the scenario series is more informative than a single final score."
        all_title, all_desc = "All historical scenarios", "Every scenario is listed with component scores, observed and missing relations, MITRE coverage and a short interpretation."
        search, category, clear = "Search scenarios", "Category", "Clear"
        columns = ["Scenario","Change and interpretation","CWLC","CAC","MDC","CTIC","TF","SACI","Observed","Missing","MITRE","Open"]
    else:
        title, kicker = "Senaryo analizi", "SENARYO ANALİZİ"
        lead = "Bu sayfa SACI modelinin telemetri kayıpları, detection boşlukları, MITRE kapsam değişiklikleri, CTI kesintileri, freshness düşüşü ve düzeltmeler karşısındaki davranışını değerlendirir."
        note = "Yayına esas final veri kümesi ile S0-S18 tarihsel doğrulama serisi ayrı tutulur. Senaryo node, edge ve skor değerleri final yayın veri kümesiyle birleştirilmez."
        rep_title, rep_desc = "Ayrıntılı incelenen senaryolar", "Duyarlılık, açıklanabilirlik ve toparlanma davranışını en güçlü biçimde gösteren senaryolar."
        comp_title, comp_desc = "Metodolojik karşılaştırmalar", "Bu karşılaştırmalar, tek bir final skor yerine senaryo serisinin neden gerekli olduğunu gösterir."
        all_title, all_desc = "Tüm tarihsel senaryolar", "Her senaryo bileşen skorları, observed ve missing ilişkiler, MITRE kapsamı ve kısa yorumuyla listelenir."
        search, category, clear = "Senaryolarda ara", "Kategori", "Temizle"
        columns = ["Senaryo","Değişiklik ve kısa yorum","CWLC","CAC","MDC","CTIC","TF","SACI","Observed","Missing","MITRE","Aç"]
    global_css = f'<link rel="stylesheet" href="{prefix}assets/saci-global-ui.css?v={VERSION}">' if (ASSETS / "saci-global-ui.css").exists() else ""
    return f'''<!doctype html>
<html lang="{lang}" data-theme="dim" data-font-level="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} - SACI Final Evidence</title>
  <link rel="stylesheet" href="{prefix}assets/saci-standard.css?v={VERSION}">
  {global_css}
  <link rel="stylesheet" href="{prefix}assets/scenarios.css?v={VERSION}">
</head>
<body data-page="scenarios">
{header(english)}
<main id="main" class="scenario-page">
  <section class="scenario-hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="lead">{lead}</p><p class="scenario-context">{note}</p></section>
  <section class="scenario-summary">
    <div class="scenario-summary-card"><span>{'Historical scenarios' if english else 'Tarihsel senaryo'}</span><strong id="summaryTotal">-</strong></div>
    <div class="scenario-summary-card"><span>{'Detailed scenarios' if english else 'Ayrıntılı senaryo'}</span><strong id="summaryRepresentative">-</strong></div>
    <div class="scenario-summary-card"><span>{'No missing relations' if english else 'Missing ilişkisi olmayan'}</span><strong id="summaryComplete">-</strong></div>
    <div class="scenario-summary-card"><span>{'Scenarios with gaps' if english else 'Boşluk içeren senaryo'}</span><strong id="summaryWithGaps">-</strong></div>
    <div class="scenario-summary-card"><span>{'MITRE mapping rows' if english else 'MITRE eşleşme satırı'}</span><strong id="summaryMitre">-</strong></div>
  </section>
  <div id="loadingState" class="empty-state">{'Loading scenario data...' if english else 'Senaryo verileri yükleniyor...'}</div>
  <section class="scenario-section"><div class="scenario-section-head"><h2>{rep_title}</h2><p>{rep_desc}</p></div><div id="representativeGrid" class="scenario-cards"></div></section>
  <section class="scenario-section"><div class="scenario-section-head"><h2>{comp_title}</h2><p>{comp_desc}</p></div><div id="comparisonGrid" class="comparison-grid"></div></section>
  <section class="scenario-section"><div class="scenario-section-head"><h2>{all_title}</h2><p>{all_desc}</p></div>
    <div class="scenario-toolbar"><div><label for="scenarioSearch">{search}</label><input id="scenarioSearch" type="search" placeholder="S7A, CTI, freshness..."></div><div><label for="categoryFilter">{category}</label><select id="categoryFilter"></select></div><button type="button" id="clearFilter">{clear}</button></div>
    <div class="table-shell"><table class="scenario-table"><thead><tr>{''.join(f'<th>{c}</th>' for c in columns)}</tr></thead><tbody id="scenarioTableBody"></tbody></table></div>
  </section>
</main>
<script src="{prefix}assets/scenarios.js?v={VERSION}"></script>
<script src="{prefix}assets/saci-ui.js?v={VERSION}"></script>
</body></html>'''

def backup(path: Path) -> None:
    if path.exists():
        target = BACKUP / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)

def patch_nav(path: Path) -> None:
    html = path.read_text(encoding="utf-8", errors="replace")
    html = re.sub(r'\s*<a[^>]*href=["\'](?:\.\./)?scenarios\.html[^"\']*["\'][^>]*>.*?</a>\s*', '\n', html, flags=re.I|re.S)
    pattern = re.compile(r'(<a[^>]*href=["\']evidence\.html[^"\']*["\'][^>]*>.*?</a>)', re.I|re.S)
    if pattern.search(html):
        html = pattern.sub(r'\1\n      <a href="scenarios.html">Scenarios</a>', html, count=1)
    path.write_text(html, encoding="utf-8")

def patch_graph(path: Path, prefix: str) -> None:
    html = path.read_text(encoding="utf-8", errors="replace")
    html = re.sub(r'\s*<script[^>]+scenario-link\.js[^>]*></script>\s*','\n',html,flags=re.I)
    html = html.replace('</body>', f'  <script src="{prefix}assets/scenario-link.js?v={VERSION}"></script>\n</body>', 1)
    path.write_text(html, encoding="utf-8")

def main() -> None:
    if not DOCS.exists():
        raise SystemExit("[!] docs/ bulunamadı. Script repo kökünde çalıştırılmalı.")
    ASSETS.mkdir(parents=True, exist_ok=True)
    EN.mkdir(parents=True, exist_ok=True)
    for path in [DOCS/"scenarios.html", EN/"scenarios.html", ASSETS/"scenarios.css", ASSETS/"scenarios.js", ASSETS/"scenario-link.js"]:
        backup(path)
    (ASSETS/"scenarios.css").write_text(SCENARIO_CSS.strip()+"\n",encoding="utf-8")
    (ASSETS/"scenarios.js").write_text(SCENARIO_JS.strip()+"\n",encoding="utf-8")
    (ASSETS/"scenario-link.js").write_text(SCENARIO_LINK_JS.strip()+"\n",encoding="utf-8")
    (DOCS/"scenarios.html").write_text(page(False),encoding="utf-8")
    (EN/"scenarios.html").write_text(page(True),encoding="utf-8")
    for path in list(DOCS.glob("*.html"))+list(EN.glob("*.html")):
        if path.name != "scenarios.html":
            backup(path)
            patch_nav(path)
    if (DOCS/"graph.html").exists(): patch_graph(DOCS/"graph.html","")
    if (EN/"graph.html").exists(): patch_graph(EN/"graph.html","../")
    print("=== SCENARIO ANALYSIS PAGE BUILT ===")
    print("TR:", DOCS/"scenarios.html")
    print("EN:", EN/"scenarios.html")
    print("Backup:", BACKUP)

if __name__ == "__main__":
    main()
