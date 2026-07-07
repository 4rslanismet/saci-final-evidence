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
