SACI PAPER VIEW — ALL SCENARIOS

Bu sürüm Paper View içine doğrudan senaryo görünümü ekler.

İçerik:
- Final ve manifestte bulunan bütün S0–S18 senaryoları
- Senaryo seçim menüsü
- Önceki / sonraki senaryo geçişi
- Graph ve Evidence bağlantıları
- CWLC, CAC, MDC, CTIC, TF ve SACI
- observed / missing edge ve node özeti
- birincil etki boyutu
- kısa akademik yorum
- seçilen senaryoya ait dinamik bileşen figürü
- senaryo bazlı SVG dışa aktarma
- URL üzerinden doğrudan senaryo açma:
  paper.html?scenario=S7A
  paper.html?scenario=S15
  paper.html?scenario=FINAL

Kurulum:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_paper_view_all_scenarios.zip -d .

Test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/paper.html?scenario=FINAL
http://127.0.0.1:8000/paper.html?scenario=S7A
http://127.0.0.1:8000/en/paper.html?scenario=S15
