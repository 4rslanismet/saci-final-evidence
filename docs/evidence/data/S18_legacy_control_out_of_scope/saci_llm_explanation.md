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
