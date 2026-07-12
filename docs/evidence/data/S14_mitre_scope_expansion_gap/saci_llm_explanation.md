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
