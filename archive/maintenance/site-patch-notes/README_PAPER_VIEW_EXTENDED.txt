SACI PAPER VIEW — EXTENDED FIGURE SET

Kurulum:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_paper_view_extended.zip -d .

Test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/paper.html?paper_view=2
http://127.0.0.1:8000/en/paper.html?paper_view=2

Değişiklikler:

- "Makaleye hazır figürler", "Kısa akademik yorum" gibi çalışma sırasında
  kullanılan meta başlıklar kaldırıldı.
- Sayfa akademik içerik başlıklarıyla yeniden düzenlendi:
  Final sonuçlar, Sistem ve kanıt yapısı, Senaryo tabanlı doğrulama,
  Yorum ve sınırlılıklar.
- Figür sayısı 10'a çıkarıldı:
  1. Laboratuvar mimarisi
  2. Final SACI bileşen profili
  3. Kanıt graph'ı kapanışı
  4. MITRE/CTI kapsamı
  5. S0-S18 SACI değişimi
  6. Missing edge değişimi
  7. S7A-S7B kritiklik duyarlılığı
  8. CTI aşamaları
  9. Freshness düşüşü ve toparlanma
  10. S18 aktif kapsam normalizasyonu
- Dinamik SVG dışa aktarma korunur.
- TR ve EN sayfalar birlikte güncellenir.
