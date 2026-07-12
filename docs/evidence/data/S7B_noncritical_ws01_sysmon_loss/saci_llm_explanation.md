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
