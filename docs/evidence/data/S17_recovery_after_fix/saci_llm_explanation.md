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
