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
