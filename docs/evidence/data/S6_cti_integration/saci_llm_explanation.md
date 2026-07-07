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
