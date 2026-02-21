# Proje İlerleme Durumu
[Türkçe] | [English](progress_en.md)
<!-- Son güncelleme: 2026-02-21 -->

## Genel Durum: Hedef 1 ✅ Tamamlandı — Hedef 2 Bekleniyor

---

## Algoritma Durumu

| Algoritma | Dosya | Durum | Not |
|-----------|-------|-------|-----|
| TSP Generator | `src/common/tsp_generator.py` | ✅ | seed=2026, N=5,6,7 |
| Brute Force | `src/common/brute_force_solver.py` | ✅ | ground_truth/ çıktısı |
| Genetik Algoritma | `src/classical/genetic_algo.py` | ✅ | OX crossover, tournament sel. |
| Simulated Annealing | `src/classical/sim_annealing.py` | ✅ | 2-opt, Metropolis |
| Google OR-Tools | `src/classical/or_tools_solver.py` | ✅ | PATH_CHEAPEST_ARC |
| QUBO Dönüştürücü | `src/quantum/qubo_converter.py` | ⏳ | Plan A — boş |
| Standart QAOA | `src/quantum/qaoa_standard.py` | ⏳ | Plan A — boş |
| GA-QAOA Hibrit | `src/quantum/hybrid_ga_qaoa.py` | ⏳ | Plan A — boş |

---

## Veri Durumu

| Dosya | Konum | Durum |
|-------|-------|-------|
| `tsp_n5.json`, `tsp_n6.json`, `tsp_n7.json` | `data/raw/` | ✅ |
| `tsp_n{5,6,7}_solution.json` | `data/ground_truth/` | ✅ |
| `tsp_n{5,6,7}_ga_solution.json` | `data/results/classical/ga/` | ✅ |
| `tsp_n{5,6,7}_sa_solution.json` | `data/results/classical/sa/` | ✅ |
| `tsp_n{5,6,7}_ortools_solution.json` | `data/results/classical/ortools/` | ✅ |
| 30-run benchmark JSON'ları | `data/results/classical/*/` | ✅ Hedef 4 |
| Quantum çıktıları | `data/results/quantum/*/` | ⏳ Plan A |

---

## Tamamlanan Düzeltmeler (2026-02-21)

| # | Sorun | Çözüm |
|---|-------|-------|
| 1 | SA `load_tsp_data()` kopyalıyordu | `utils.py` import edildi |
| 2 | SA ve OR-Tools PascalCase key | snake_case'e geçildi |
| 3 | SA ve OR-Tools gap hesaplamıyordu | `load_optimal_cost()` eklendi |
| 4 | GA convergence_history yoktu | Her nesil kaydediliyor |
| 5 | GA `generations=100` (tutarsız) | `500` yapıldı |
| 6 | `tsp_generator` seed=42 (default) | `seed=2026` yapıldı |
| 7 | Tüm çıktılar `data/raw/` içindeydi | Yeni klasör yapısı oluşturuldu |
| 8 | `data/results/ga/` eski formatlıydı | Silinip yenisi oluşturuldu |

---

## Sonraki Adımlar

### Go/No-Go Karar Aşaması (Hedef 2)
- [ ] QAOA prototipi geliştir (3-4 şehir)
- [ ] Ekibin konuya hakimiyetini değerlendir
- [ ] Plan A veya Plan B kararını ver

### Plan B seçilirse (Hedef 3-4)
- [ ] GA ve SA için hiperparametre optimizasyonu
- [ ] 30 bağımsız çalıştırma scripti yaz
- [ ] 30-run sonuçlarını `data/results/classical/*/tsp_n{N}_{algo}_30runs.json` formatında kaydet
- [ ] İstatistiksel özetleri hesapla (mean, std, variance)

### Plan A seçilirse (Hedef 3-4)
- [ ] `qubo_converter.py` — TSP → QUBO dönüşümü
- [ ] `qaoa_standard.py` — SPSA/COBYLA optimizörlü QAOA
- [ ] `hybrid_ga_qaoa.py` — GA parametresiyle driven QAOA
- [ ] Her model için 30-run benchmark

### Hedef 5 (Anova & Görselleştirme)
- [x] ANOVA analizi scripti (`scipy.stats.f_oneway`)
- [x] Box plot (seaborn)
- [x] Yakınsama grafikleri (matplotlib)
- [ ] Nihai rapor (Quantum sonrası)
