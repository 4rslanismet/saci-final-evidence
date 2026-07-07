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
