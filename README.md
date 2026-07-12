# SACI responsive header hotfix

Bu hotfix üst menüyü sabit breakpoint yerine gerçek içerik genişliğine göre dinamik olarak daraltır.

## Davranış

- Marka + tüm menü öğeleri + Language/Font/Theme kontrolleri sığdığı sürece klasik yatay header korunur.
- Sığmadığı anda otomatik olarak Menu/Menü düğmesine geçilir.
- Menü açıldığında sayfa bağlantıları 3, 2 veya 1 sütun olarak ekran genişliğine uyarlanır.
- Language, Font ve Theme kontrolleri açılır panelin altında kalır.
- Dışarı tıklama, Escape ve bir bağlantı seçimi menüyü kapatır.
- Font seviyesi değiştiğinde genişlik yeniden hesaplanır.
- TR ve EN sayfaları aynı davranışı kullanır.

## Kurulum

```bash
cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_responsive_header_hotfix.zip -d .
python3 apply_responsive_header.py
```

## Kontrol

```bash
node --check docs/assets/saci-ui.js
python3 tools/validate_academic_site.py
python3 -m http.server 8000 --directory docs
```

Tarayıcıda Ctrl+Shift+R yapın.
