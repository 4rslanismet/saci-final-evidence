# SACI Explanation Report

Generated at: 2026-07-06T21:32:53.321122

This report consolidates policy-guided SACI scenario explanations. The report does not calculate or modify SACI scores; it explains deterministic SACI outputs and graph completeness values.

## Scenario Summary

| Scenario | Name | Type | LC | CAC | MDC | CTIC | TF | SACI | Missing |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| S0 | no_siem | controlled_evaluation_scenario | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 167 |

## S0 - no_siem

# SACI Policy-Guided Explanation

Stage: S0 - no_siem

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S0 senaryosu, SACI değerlendirme sürecindeki aşamalı görünürlük kazanımını temsil eder. SIEM, varlık envanteri, domain controller telemetrisi, endpoint telemetrisi, firewall görünürlüğü ve CTI entegrasyonu gibi bileşenler aşamalı olarak eklenir.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **0.0** olarak ölçülmüştür. Bu değer, ölçülebilir görünürlüğün bulunmadığını ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **MDC düşüşü**, kapsam dahilindeki MITRE ATT&CK tekniklerinden bazılarının gözlemlenen kontrol veya alarm ile kapatılamadığını gösterir. Rule-to-technique mapping ve ilgili telemetri kaynağı gözden geçirilmelidir.
- **CTIC düşüşü**, IOC/CTI/MISP/Wazuh alarm zincirinin tam kapanmadığını gösterir. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 6 observed edge ve 167 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
3. Eksik MITRE teknikleri için rule-to-technique mapping ve ilgili telemetri desteği doğrulanmalıdır.
4. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
5. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S1 | siem_deployed | controlled_evaluation_scenario | 18.52 | 0.0 | 0.0 | 0.0 | 50.0 | 10.56 | 163 |

## S1 - siem_deployed

# SACI Policy-Guided Explanation

Stage: S1 - siem_deployed

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S1 senaryosu, SACI değerlendirme sürecindeki aşamalı görünürlük kazanımını temsil eder. SIEM, varlık envanteri, domain controller telemetrisi, endpoint telemetrisi, firewall görünürlüğü ve CTI entegrasyonu gibi bileşenler aşamalı olarak eklenir.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **10.56** olarak ölçülmüştür. Bu değer, düşük görünürlük seviyesini ve temel SIEM/telemetri ilişkilerinin eksik olduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **MDC düşüşü**, kapsam dahilindeki MITRE ATT&CK tekniklerinden bazılarının gözlemlenen kontrol veya alarm ile kapatılamadığını gösterir. Rule-to-technique mapping ve ilgili telemetri kaynağı gözden geçirilmelidir.
- **CTIC düşüşü**, IOC/CTI/MISP/Wazuh alarm zincirinin tam kapanmadığını gösterir. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 10 observed edge ve 163 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
3. Eksik MITRE teknikleri için rule-to-technique mapping ve ilgili telemetri desteği doğrulanmalıdır.
4. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
5. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S2 | inventory_defined | controlled_evaluation_scenario | 18.52 | 0.0 | 0.0 | 0.0 | 60.0 | 11.56 | 163 |

## S2 - inventory_defined

# SACI Policy-Guided Explanation

Stage: S2 - inventory_defined

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S2 senaryosu, SACI değerlendirme sürecindeki aşamalı görünürlük kazanımını temsil eder. SIEM, varlık envanteri, domain controller telemetrisi, endpoint telemetrisi, firewall görünürlüğü ve CTI entegrasyonu gibi bileşenler aşamalı olarak eklenir.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **11.56** olarak ölçülmüştür. Bu değer, düşük görünürlük seviyesini ve temel SIEM/telemetri ilişkilerinin eksik olduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **MDC düşüşü**, kapsam dahilindeki MITRE ATT&CK tekniklerinden bazılarının gözlemlenen kontrol veya alarm ile kapatılamadığını gösterir. Rule-to-technique mapping ve ilgili telemetri kaynağı gözden geçirilmelidir.
- **CTIC düşüşü**, IOC/CTI/MISP/Wazuh alarm zincirinin tam kapanmadığını gösterir. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 10 observed edge ve 163 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
3. Eksik MITRE teknikleri için rule-to-technique mapping ve ilgili telemetri desteği doğrulanmalıdır.
4. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
5. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S3 | dc_visibility | controlled_evaluation_scenario | 37.04 | 40.0 | 69.23 | 0.0 | 80.0 | 42.96 | 109 |

## S3 - dc_visibility

# SACI Policy-Guided Explanation

Stage: S3 - dc_visibility

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S3 senaryosu, SACI değerlendirme sürecindeki aşamalı görünürlük kazanımını temsil eder. SIEM, varlık envanteri, domain controller telemetrisi, endpoint telemetrisi, firewall görünürlüğü ve CTI entegrasyonu gibi bileşenler aşamalı olarak eklenir.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **42.96** olarak ölçülmüştür. Bu değer, düşük görünürlük seviyesini ve temel SIEM/telemetri ilişkilerinin eksik olduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **MDC düşüşü**, kapsam dahilindeki MITRE ATT&CK tekniklerinden bazılarının gözlemlenen kontrol veya alarm ile kapatılamadığını gösterir. Rule-to-technique mapping ve ilgili telemetri kaynağı gözden geçirilmelidir.
- **CTIC düşüşü**, IOC/CTI/MISP/Wazuh alarm zincirinin tam kapanmadığını gösterir. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 64 observed edge ve 109 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
3. Eksik MITRE teknikleri için rule-to-technique mapping ve ilgili telemetri desteği doğrulanmalıdır.
4. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
5. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S4 | endpoint_visibility | controlled_evaluation_scenario | 66.67 | 84.0 | 100.0 | 0.0 | 80.0 | 69.0 | 42 |

## S4 - endpoint_visibility

# SACI Policy-Guided Explanation

Stage: S4 - endpoint_visibility

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S4 senaryosu, SACI değerlendirme sürecindeki aşamalı görünürlük kazanımını temsil eder. SIEM, varlık envanteri, domain controller telemetrisi, endpoint telemetrisi, firewall görünürlüğü ve CTI entegrasyonu gibi bileşenler aşamalı olarak eklenir.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **69.0** olarak ölçülmüştür. Bu değer, önemli görünürlük gerilemesi veya eksik telemetri/kontrol kapsaması bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **CTIC düşüşü**, IOC/CTI/MISP/Wazuh alarm zincirinin tam kapanmadığını gösterir. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 131 observed edge ve 42 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
3. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
4. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S5 | firewall_visibility | controlled_evaluation_scenario | 85.19 | 84.0 | 100.0 | 0.0 | 80.0 | 74.56 | 40 |

## S5 - firewall_visibility

# SACI Policy-Guided Explanation

Stage: S5 - firewall_visibility

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S5 senaryosu, SACI değerlendirme sürecindeki aşamalı görünürlük kazanımını temsil eder. SIEM, varlık envanteri, domain controller telemetrisi, endpoint telemetrisi, firewall görünürlüğü ve CTI entegrasyonu gibi bileşenler aşamalı olarak eklenir.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **74.56** olarak ölçülmüştür. Bu değer, önemli görünürlük gerilemesi veya eksik telemetri/kontrol kapsaması bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **CTIC düşüşü**, IOC/CTI/MISP/Wazuh alarm zincirinin tam kapanmadığını gösterir. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 133 observed edge ve 40 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
3. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.
4. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S6 | cti_integration | controlled_evaluation_scenario | 100.0 | 84.0 | 100.0 | 100.0 | 80.0 | 94.0 | 30 |

## S6 - cti_integration

# SACI Policy-Guided Explanation

Stage: S6 - cti_integration

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S6 senaryosu, SACI değerlendirme sürecindeki aşamalı görünürlük kazanımını temsil eder. SIEM, varlık envanteri, domain controller telemetrisi, endpoint telemetrisi, firewall görünürlüğü ve CTI entegrasyonu gibi bileşenler aşamalı olarak eklenir.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **94.0** olarak ölçülmüştür. Bu değer, anlamlı görünürlük sağlandığını, ancak incelenmesi gereken görünürlük boşlukları bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 143 observed edge ve 30 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
2. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S7A | critical_dc01_sysmon_loss | controlled_visibility_regression | 90.74 | 64.0 | 61.54 | 100.0 | 80.0 | 78.53 | 57 |

## S7A - critical_dc01_sysmon_loss

# SACI Policy-Guided Explanation

Stage: S7A - critical_dc01_sysmon_loss

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S7A senaryosu, kritik A01/DC01 varlığında Sysmon telemetri kaybını temsil eder. Bu senaryo, kritik varlık üzerindeki telemetri kaybının SACI skoruna ve kanıt grafındaki missing edge sayısına etkisini ölçmek için kullanılır.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **78.53** olarak ölçülmüştür. Bu değer, önemli görünürlük gerilemesi veya eksik telemetri/kontrol kapsaması bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **MDC düşüşü**, kapsam dahilindeki MITRE ATT&CK tekniklerinden bazılarının gözlemlenen kontrol veya alarm ile kapatılamadığını gösterir. Rule-to-technique mapping ve ilgili telemetri kaynağı gözden geçirilmelidir.
- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 57 missing edge bulunmaktadır. Bu missing edge’lerin kritik DC01/Sysmon görünürlük zinciriyle ilişkili olması, kritik varlık telemetri kaybının graph completeness üzerinde güçlü etki ürettiğini gösterir.

## 4. Operasyonel Anlam

Kritik domain controller telemetrisindeki kayıp, SOC görünürlüğü açısından yüksek öncelikli bir eksikliktir. Bu tür bir kayıp, kimlik, discovery ve lateral movement ile ilişkili tekniklerin görünürlüğünü zayıflatabilir.

## 5. Önerilen Kontroller

1. A01/DC01 üzerindeki Sysmon servis durumu, Sysmon event channel ve Wazuh agent event collection yapılandırması öncelikli doğrulanmalıdır.
2. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
3. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
4. Eksik MITRE teknikleri için rule-to-technique mapping ve ilgili telemetri desteği doğrulanmalıdır.
5. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S7B | noncritical_ws01_sysmon_loss | controlled_visibility_regression | 95.06 | 84.0 | 100.0 | 100.0 | 80.0 | 92.52 | 32 |

## S7B - noncritical_ws01_sysmon_loss

# SACI Policy-Guided Explanation

Stage: S7B - noncritical_ws01_sysmon_loss

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S7B senaryosu, kritik olmayan A04/WS01 endpoint üzerinde Sysmon telemetri kaybını temsil eder. Bu senaryo, kritik olmayan bir endpoint kaybının S7A’daki kritik DC01 kaybına göre daha düşük etki üretip üretmediğini karşılaştırmak için kullanılır.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **92.52** olarak ölçülmüştür. Bu değer, anlamlı görünürlük sağlandığını, ancak incelenmesi gereken görünürlük boşlukları bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 32 missing edge bulunmaktadır. Bu eksiklik WS01 endpoint görünürlüğüyle ilişkilidir. Kritik olmayan endpoint kaybı skor düşürür; ancak kritik DC01 kaybına göre daha sınırlı etki üretir.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
3. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S8 | final_closure | final_lab_measurement | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 0 |

## S8 - final_closure

# SACI Policy-Guided Explanation

Stage: S8 - final_closure

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S8 senaryosu final görünürlük kapanışını temsil eder. Bu aşamada kapsam dahilindeki beklenen görünürlük ilişkilerinin tamamı gözlemlenmiş, SACI skoru 100 ve missing edge sayısı 0 olarak ölçülmüştür.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **100.0** olarak ölçülmüştür. Bu değer, beklenen görünürlük ilişkilerinin kapsam dahilinde tamamen kapandığını ifade eder.

Bileşen bazlı yorum:

- Tüm SACI bileşenleri 100 değerindedir. Bu durum, tanımlı kapsam içinde beklenen görünürlük bileşenlerinin gözlemlendiğini gösterir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node ve 173 edge bulunmaktadır. Observed edge sayısı 173, missing edge sayısı 0’dır. Bu durum, kapsam dahilindeki beklenen graph ilişkilerinin yapısal olarak kapandığını gösterir.

## 4. Operasyonel Anlam

Bu sonuç güvenlik garantisi değildir. Operasyonel olarak, yalnızca tanımlı değerlendirme kapsamındaki beklenen SOC görünürlük ilişkilerinin gözlemlenebildiğini gösterir.

## 5. Önerilen Kontroller

1. Final kapanış durumunun korunması için agent health, log freshness ve rule eşleşmeleri periyodik olarak izlenmelidir.
2. Yeni varlık, log source, MITRE teknik veya IOC eklendiğinde SACI kapsamı yeniden hesaplanmalıdır.
3. SACI=100 sonucunun güvenlik garantisi olmadığı, yalnızca kapsam dahilindeki görünürlük kapanışını ifade ettiği raporlarda korunmalıdır.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S9 | critical_dc01_security_loss | fault_injection | 90.74 | 97.0 | 100.0 | 100.0 | 100.0 | 96.47 | 7 |

## S9 - critical_dc01_security_loss

# SACI Policy-Guided Explanation

Stage: S9 - critical_dc01_security_loss

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S9 senaryosu, kritik DC01 üzerinde Security log görünürlüğü kaybını temsil eden bir fault-injection senaryosudur.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **96.47** olarak ölçülmüştür. Bu değer, neredeyse tam görünürlük sağlandığını, ancak küçük bir tazelik, kapsam veya kontrol etkisi bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 166 observed edge ve 7 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S10 | endpoint_powershell_loss | fault_injection | 95.06 | 92.27 | 92.31 | 100.0 | 100.0 | 95.05 | 12 |

## S10 - endpoint_powershell_loss

# SACI Policy-Guided Explanation

Stage: S10 - endpoint_powershell_loss

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S10 senaryosu, endpoint PowerShell telemetrisi kaybını temsil eden bir fault-injection senaryosudur.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **95.05** olarak ölçülmüştür. Bu değer, neredeyse tam görünürlük sağlandığını, ancak küçük bir tazelik, kapsam veya kontrol etkisi bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **MDC düşüşü**, kapsam dahilindeki MITRE ATT&CK tekniklerinden bazılarının gözlemlenen kontrol veya alarm ile kapatılamadığını gösterir. Rule-to-technique mapping ve ilgili telemetri kaynağı gözden geçirilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 161 observed edge ve 12 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
3. Eksik MITRE teknikleri için rule-to-technique mapping ve ilgili telemetri desteği doğrulanmalıdır.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S11 | linux_authlog_loss | fault_injection | 95.06 | 95.71 | 92.31 | 100.0 | 100.0 | 95.91 | 7 |

## S11 - linux_authlog_loss

# SACI Policy-Guided Explanation

Stage: S11 - linux_authlog_loss

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S11 senaryosu, Linux authlog görünürlüğü kaybını temsil eden bir fault-injection senaryosudur.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **95.91** olarak ölçülmüştür. Bu değer, neredeyse tam görünürlük sağlandığını, ancak küçük bir tazelik, kapsam veya kontrol etkisi bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **LC düşüşü**, beklenen varlık-log kaynağı ilişkisinin tamamen gözlemlenemediğini gösterir. Agent durumu, log forwarding, event channel, syslog veya ingestion pipeline kontrol edilmelidir.
- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **MDC düşüşü**, kapsam dahilindeki MITRE ATT&CK tekniklerinden bazılarının gözlemlenen kontrol veya alarm ile kapatılamadığını gösterir. Rule-to-technique mapping ve ilgili telemetri kaynağı gözden geçirilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 166 observed edge ve 7 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Etkilenen varlıklar için Wazuh agent durumu, log forwarding ve beklenen log source akışı doğrulanmalıdır.
2. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
3. Eksik MITRE teknikleri için rule-to-technique mapping ve ilgili telemetri desteği doğrulanmalıdır.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S12 | firewall_ioc_without_cti | cti_failure | 100.0 | 100.0 | 100.0 | 50.0 | 100.0 | 92.5 | 6 |

## S12 - firewall_ioc_without_cti

# SACI Policy-Guided Explanation

Stage: S12 - firewall_ioc_without_cti

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S12 senaryosu, firewall üzerinde IOC görülmesine rağmen CTI kapanışının sağlanamadığı durumu temsil eder.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **92.5** olarak ölçülmüştür. Bu değer, anlamlı görünürlük sağlandığını, ancak incelenmesi gereken görünürlük boşlukları bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **CTIC düşüşü**, IOC/CTI/MISP/Wazuh alarm zincirinin tam kapanmadığını gösterir. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 167 observed edge ve 6 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

CTI zinciri kapanmadığında IOC bilgisinin SIEM alarmına ve MITRE kapsamına bağlanması zayıflar. Bu durum threat intelligence entegrasyonunun operasyonel doğrulamasını gerektirir.

## 5. Önerilen Kontroller

1. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S13 | misp_lookup_without_ioc_hit | cti_failure | 100.0 | 100.0 | 100.0 | 50.0 | 100.0 | 92.5 | 6 |

## S13 - misp_lookup_without_ioc_hit

# SACI Policy-Guided Explanation

Stage: S13 - misp_lookup_without_ioc_hit

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S13 senaryosu, MISP sorgusunun çalıştığı ancak IOC hit üretmediği CTI failure durumunu temsil eder.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **92.5** olarak ölçülmüştür. Bu değer, anlamlı görünürlük sağlandığını, ancak incelenmesi gereken görünürlük boşlukları bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **CTIC düşüşü**, IOC/CTI/MISP/Wazuh alarm zincirinin tam kapanmadığını gösterir. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 167 observed edge ve 6 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

CTI zinciri kapanmadığında IOC bilgisinin SIEM alarmına ve MITRE kapsamına bağlanması zayıflar. Bu durum threat intelligence entegrasyonunun operasyonel doğrulamasını gerektirir.

## 5. Önerilen Kontroller

1. MISP bağlantısı, IOC feed, enrichment script, API anahtarı ve IOC-to-alert dönüşümü kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S14 | mitre_scope_expansion_gap | coverage_gap | 100.0 | 95.88 | 92.86 | 100.0 | 100.0 | 97.54 | 5 |

## S14 - mitre_scope_expansion_gap

# SACI Policy-Guided Explanation

Stage: S14 - mitre_scope_expansion_gap

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S14 senaryosu, MITRE kapsamı genişletildiğinde ilgili kontrol veya alarm gözlemlenmezse oluşan coverage gap durumunu temsil eder.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **97.54** olarak ölçülmüştür. Bu değer, neredeyse tam görünürlük sağlandığını, ancak küçük bir tazelik, kapsam veya kontrol etkisi bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.
- **MDC düşüşü**, kapsam dahilindeki MITRE ATT&CK tekniklerinden bazılarının gözlemlenen kontrol veya alarm ile kapatılamadığını gösterir. Rule-to-technique mapping ve ilgili telemetri kaynağı gözden geçirilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 98 node, 178 edge, 173 observed edge ve 5 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.
2. Eksik MITRE teknikleri için rule-to-technique mapping ve ilgili telemetri desteği doğrulanmalıdır.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S15 | freshness_decay | sensitivity_test | 100.0 | 100.0 | 100.0 | 100.0 | 50.0 | 95.0 | 0 |

## S15 - freshness_decay

# SACI Policy-Guided Explanation

Stage: S15 - freshness_decay

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S15 senaryosu freshness decay etkisini temsil eder. Bu senaryoda kanıt grafı yapısal olarak kapalı kalır; ancak TF bileşeni düştüğü için SACI skoru azalır.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **95.0** olarak ölçülmüştür. Bu değer, neredeyse tam görünürlük sağlandığını, ancak küçük bir tazelik, kapsam veya kontrol etkisi bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **TF düşüşü**, telemetrinin yapısal olarak mevcut olsa bile tazelik açısından zayıfladığını gösterir. Event timestamp, ingestion delay, agent gecikmesi, index freshness ve NTP senkronizasyonu kontrol edilmelidir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında missing edge bulunmamaktadır; observed edge sayısı 173/173 seviyesindedir. Buna rağmen SACI skorunun 100 olmaması, düşüşün yapısal graph eksikliğinden değil, freshness gibi ayrı bir skor bileşeninden kaynaklandığını gösterir.

## 4. Operasyonel Anlam

Bu senaryoda operasyonel sorun graph ilişkisinin eksik olması değil, telemetrinin güncelliğini kaybetmesidir. Bu nedenle olay zamanları, ingestion gecikmesi ve NTP senkronizasyonu öncelikli incelenmelidir.

## 5. Önerilen Kontroller

1. Event timestamp, ingestion delay, index freshness, agent gecikmesi ve NTP senkronizasyonu kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S16 | detection_rule_gap | control_failure | 100.0 | 95.71 | 100.0 | 100.0 | 100.0 | 98.93 | 5 |

## S16 - detection_rule_gap

# SACI Policy-Guided Explanation

Stage: S16 - detection_rule_gap

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S16 senaryosu detection rule gap durumunu temsil eder. Telemetri mevcut olsa bile beklenen detection control veya Wazuh rule çıktısı oluşmadığında skorun nasıl etkilendiğini gösterir.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **98.93** olarak ölçülmüştür. Bu değer, neredeyse tam görünürlük sağlandığını, ancak küçük bir tazelik, kapsam veya kontrol etkisi bulunduğunu ifade eder.

Bileşen bazlı yorum:

- **CAC düşüşü**, beklenen detection control veya Wazuh rule çıktısının tam oluşmadığını gösterir. Decoder, rule matching, control mapping ve alert üretimi doğrulanmalıdır.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node, 173 edge, 168 observed edge ve 5 missing edge bulunmaktadır. Missing edge değeri, beklenen görünürlük ilişkisinin kanıt grafı üzerinde doğrulanamadığı durumları ifade eder.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Detection control kayıtları, Wazuh decoder/rule eşleşmeleri ve beklenen alert üretimi kontrol edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S17 | recovery_after_fix | recovery | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 0 |

## S17 - recovery_after_fix

# SACI Policy-Guided Explanation

Stage: S17 - recovery_after_fix

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S17 senaryosu recovery sonrası durumu temsil eder. Eksik görünürlük ilişkileri giderildiğinde SACI skorunun final kapanış seviyesine dönebildiğini gösterir.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **100.0** olarak ölçülmüştür. Bu değer, beklenen görünürlük ilişkilerinin kapsam dahilinde tamamen kapandığını ifade eder.

Bileşen bazlı yorum:

- Tüm SACI bileşenleri 100 değerindedir. Bu durum, tanımlı kapsam içinde beklenen görünürlük bileşenlerinin gözlemlendiğini gösterir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node ve 173 edge bulunmaktadır. Observed edge sayısı 173, missing edge sayısı 0’dır. Bu durum, kapsam dahilindeki beklenen graph ilişkilerinin yapısal olarak kapandığını gösterir.

## 4. Operasyonel Anlam

Bu sonuç, ilgili senaryoda SOC görünürlüğünün hangi bileşen üzerinden eksildiğini veya hangi bileşenle güçlendiğini yorumlamak için kullanılmalıdır.

## 5. Önerilen Kontroller

1. Final kapanış durumunun korunması için agent health, log freshness ve rule eşleşmeleri periyodik olarak izlenmelidir.
2. Yeni varlık, log source, MITRE teknik veya IOC eklendiğinde SACI kapsamı yeniden hesaplanmalıdır.
3. SACI=100 sonucunun güvenlik garantisi olmadığı, yalnızca kapsam dahilindeki görünürlük kapanışını ifade ettiği raporlarda korunmalıdır.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


| S18 | legacy_control_out_of_scope | scope_validation | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 0 |

## S18 - legacy_control_out_of_scope

# SACI Policy-Guided Explanation

Stage: S18 - legacy_control_out_of_scope

Bu açıklama, SACI skor bileşenleri ve kanıt grafı çıktıları üzerinden kural-tabanlı raporlama politikası ile üretilmiştir. SACI skoru bu rapor tarafından hesaplanmaz; skor daha önce deterministik SACI engine tarafından üretilmiştir.

## 1. Senaryo Özeti

S18 senaryosu legacy control out-of-scope durumunu temsil eder. Eski kontrol kayıtları izlenebilirlik için korunur; ancak aktif skor kapsamını bozmayacak şekilde değerlendirme dışında tutulur.

## 2. Skor Yorumu

Bu senaryoda SACI skoru **100.0** olarak ölçülmüştür. Bu değer, beklenen görünürlük ilişkilerinin kapsam dahilinde tamamen kapandığını ifade eder.

Bileşen bazlı yorum:

- Tüm SACI bileşenleri 100 değerindedir. Bu durum, tanımlı kapsam içinde beklenen görünürlük bileşenlerinin gözlemlendiğini gösterir.

## 3. Graph/Görünürlük Yorumu

Kanıt grafında 95 node ve 173 edge bulunmaktadır. Observed edge sayısı 173, missing edge sayısı 0’dır. Bu durum, kapsam dahilindeki beklenen graph ilişkilerinin yapısal olarak kapandığını gösterir.

## 4. Operasyonel Anlam

Legacy kayıtların aktif skor kapsamından ayrılması, eski mapping’lerin final skoru yapay olarak düşürmesini engellerken izlenebilirliği korur.

## 5. Önerilen Kontroller

1. Legacy control kayıtlarının aktif scoring kapsamı dışında, ancak traceability amacıyla ayrı tutulduğu dokümante edilmelidir.

## Not

SACI=100 sonucu kurumun güvenli olduğunu göstermez. Yalnızca tanımlı kapsam içindeki beklenen görünürlük ilişkilerinin gözlemlendiğini ifade eder. SACI; IDS/IPS, EDR veya saldırı tespit algoritması değil, açıklanabilir SOC görünürlük skorlama modelidir.


