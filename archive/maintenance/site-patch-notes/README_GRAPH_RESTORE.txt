SACI GRAPH EXPLORER RESTORE PACKAGE

Bu paket yalnızca graph sayfasını düzeltir.

Ne yapar?
- Mevcut site temasını ve üst menüyü korur.
- Sol menü kullanmaz.
- Senaryo seçimini üst toolbar içindeki dropdown ile verir.
- docs_backup_*/evidence/data içindeki S0-S18 klasörlerini otomatik bulup docs/evidence/data altına geri getirir.
- final-v2 kanonik verisini _saci_final_seed/data/final kaynağından docs/evidence/lab/final altına kopyalar.
- TR ve EN manifest üretir.
- Graph alanını sayfanın ana odağı yapar.
- Graph yorumunu ve SACI metriklerini altta dinamik gösterir.
- MITRE taktiklerini ve tekniklerini resmi ATT&CK sayfalarına bağlantılı gösterir.
- Node/edge çift tıklamasında sağ detay paneli açar.

Uygulama:

cd /mnt/e/Downloads/saci_github_pages_site
unzip -o saci_graph_explorer_restore.zip -d .
python3 tools/restore_graph_explorer.py

Kontrol:

python3 -m http.server 8000 --directory docs

http://127.0.0.1:8000/graph.html?restore=1
http://127.0.0.1:8000/en/graph.html?restore=1

Beklenen:
- Dropdown içinde final-v2 + S0-S18 senaryoları
- Büyük ve sayfaya yayılan graph
- Altta graph yorumlaması
- Altta bağlantılı MITRE tactic/technique listesi
- Çift tıklamada node/edge görev açıklaması
- Dark / Dim / Light ve font kontrolleri mevcut siteyle aynı

Önemli:
Tarihsel senaryoların görünmesi için repo içinde şu kaynaklardan biri bulunmalıdır:
- docs/evidence/data/S*_*/
- docs_backup_*/evidence/data/S*_*/
- backups/**/evidence/data/S*_*/
- _local_backups/**/evidence/data/S*_*/
