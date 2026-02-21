# Proje İlerleme Durumu
<!-- Her oturumda güncellenir — mevcut durum ve yapılacaklar -->

Son güncelleme: 2026-02-21

## Branch Durumu

- **Aktif branch:** `dev`
- **Commit edilmemiş:** `pyrightconfig.json` (eklenip commit edilmeli)

## Algoritma Durumu

| Algoritma | Dosya | Durum |
|-----------|-------|-------|
| TSP Generator | `src/common/tsp_generator.py` | ✅ Tamamlandı |
| Brute Force | `src/common/brute_force_solver.py` | ✅ Tamamlandı |
| Utils (load_tsp_data) | `src/common/utils.py` | ✅ Tamamlandı |
| Genetik Algoritma | `src/classical/genetic_algo.py` | ✅ Tamamlandı |
| Simulated Annealing | `src/classical/sim_annealing.py` | ✅ Tamamlandı |
| OR-Tools | `src/classical/or_tools_solver.py` | ✅ Tamamlandı |
| QUBO Dönüştürücü | `src/quantum/qubo_converter.py` | ⬜ Boş — Plan A bekliyor |
| Standart QAOA | `src/quantum/qaoa_standard.py` | ⬜ Boş — Plan A bekliyor |
| GA-QAOA Hibrit | `src/quantum/hybrid_ga_qaoa.py` | ⬜ Boş — Plan A bekliyor |

## Veri Durumu

| Dosya | Durum |
|-------|-------|
| `data/raw/tsp_n5.json` | ✅ Var |
| `data/raw/tsp_n6.json` | ✅ Var |
| `data/raw/tsp_n7.json` | ✅ Var |
| `data/raw/tsp_n5_solution.json` | ✅ Brute Force çözümü |
| `data/raw/tsp_n5_ga_solution.json` | ✅ GA çözümü |
| `data/raw/tsp_n5_sa_solution.json` | ✅ SA çözümü |
| `data/results/ga/` | ⬜ Eski sonuçlar — temizlenmeli |
| `data/results/sa/` | ⬜ Eski sonuçlar — temizlenmeli |

## Tespit Edilen Spec Uyumsuzlukları

### 🔴 Yüksek Öncelik
1. **JSON çıktı key formatı tutarsız:**
   - GA: snake_case (`best_route`, `execution_time`)
   - SA, OR-Tools: PascalCase (`Best_Path`, `Duration_Sec`)
   - → Karşılaştırma scripti yazıldığında sorun çıkaracak

2. **Çıktı klasörü tutarsız:**
   - Tüm algoritmalar `data/raw/` altına yazıyor
   - `data/results/` klasörü boş duruyor
   - → Organizasyon planına karar verilmeli

### 🟡 Orta Öncelik
3. **SA'nın kendi `load_tsp_data()` var:** `utils.py`'deki fonksiyonu kullanmıyor, kendi kopyasını içeriyor. DRY ihlali.

4. **Karşılaştırma scripti yok:** 30 çalıştırma, ANOVA analizi, box plot için henüz kod yok.

5. **Hedef 4 metrikleri eksik:** Hiçbir algoritma "30 bağımsız çalıştırma" döngüsü içermiyor.

### 🟢 Düşük Öncelik
6. `pyrightconfig.json` git'e eklenmemiş.

## Sıradaki Adımlar

### Plan B ise (Klasik):
- [ ] Tüm algoritma çıktılarını ortak JSON formatına getir
- [ ] SA'yı `utils.load_tsp_data()` kullanacak şekilde düzelt
- [ ] 30 çalıştırma döngüsü ve istatistik toplama scripti yaz
- [ ] ANOVA analizi scripti yaz (`scipy.stats.f_oneway`)
- [ ] Box plot ve yakınsama grafikleri

### Plan A ise (Kuantum+Klasik):
- [ ] `qubo_converter.py` — TSP → QUBO dönüşümü
- [ ] `qaoa_standard.py` — Qiskit ile QAOA (SPSA/COBYLA)
- [ ] `hybrid_ga_qaoa.py` — GA ile QAOA parametre optimizasyonu
- [ ] Yukarıdaki Plan B adımlarının tamamı
