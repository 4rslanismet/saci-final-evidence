SACI SCENARIO ANALYSIS PAGE

Uygulama:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_scenario_analysis_builder.zip -d .
python3 tools/build_scenario_analysis_page.py

Test:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/scenarios.html?scenario_analysis=2
http://127.0.0.1:8000/en/scenarios.html?scenario_analysis=2

İçerik:
- S0-S18 bütün tarihsel senaryolar
- Temsilî senaryolar: S0, S7A, S7B, S8, S12, S13, S14, S15, S17, S18
- CWLC, CAC, MDC, CTIC, TF, SACI
- Observed edge, missing edge ve kısa yorum
- MITRE tactic/technique resmi bağlantıları
- Graph sayfasına senaryo seçili geçiş
- TR ve EN sayfalar
