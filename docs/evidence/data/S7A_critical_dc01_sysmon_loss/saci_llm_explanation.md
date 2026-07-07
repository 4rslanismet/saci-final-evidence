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
