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
