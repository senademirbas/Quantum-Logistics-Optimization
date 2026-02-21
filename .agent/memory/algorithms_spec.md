# Algoritma Spesifikasyonları
<!-- Her algoritmanın beklenen I/O, parametreleri ve mevcut durumu -->

## 1. Genetik Algoritma (GA)
**Dosya:** `src/classical/genetic_algo.py`
**Sınıf:** `GeneticAlgorithmTSP`
**Durum:** ✅ Tamamlandı

### Parametreler
| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| `num_cities` | — | Şehir sayısı (5, 6, 7) |
| `pop_size` | 100 | Popülasyon büyüklüğü |
| `mutation_rate` | 0.01 | Mutasyon olasılığı |
| `generations` | 500 | Nesil sayısı |

### Operatörler
- **Seçilim:** Tournament selection (turnuva boyutu: 5)
- **Çaprazlama:** Ordered Crossover (OX)
- **Mutasyon:** Swap mutation (2 şehir değişimi)
- **Elitizm:** En iyi birey sonraki nesle aktarılır

### Girdi
- `data/raw/tsp_n{N}.json` → `distance_matrix` key'i via `load_tsp_data()`
- Optimal cost: önce JSON'dan, yoksa `tsp_n{N}_solution.json`'dan okunur

### Çıktı (JSON)
```json
{
  "num_cities": 5,
  "generations": 500,
  "pop_size": 100,
  "mutation_rate": 0.01,
  "execution_time": 1.234,
  "best_distance": 42.5,
  "optimal_distance": 40.0,
  "optimality_gap_percent": 6.25,
  "best_route": [0, 2, 4, 1, 3, 0]
}
```
**Çıktı yolu:** `data/raw/tsp_n{N}_ga_solution.json`

> ⚠️ **SPEC UYUMSUZLUĞU:** Çıktı `data/raw/` altına yazılıyor, `data/results/ga/` altına değil. Tutarsızlık var.

---

## 2. Simulated Annealing (SA)
**Dosya:** `src/classical/sim_annealing.py`
**Sınıf:** `SimulatedAnnealingTSP`
**Durum:** ✅ Tamamlandı

### Parametreler
| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| `num_cities` | — | Şehir sayısı |
| `initial_temp` | 1000.0 | Başlangıç sıcaklığı |
| `alpha` | 0.99 | Soğuma katsayısı |
| `stopping_temp` | 1e-6 | Durdurma sıcaklığı |

### Algoritma Detayları
- **Komşu üretimi:** 2-Opt (2 şehir arası segment ters çevirme)
- **Kabul kriteri:** Metropolis kriteri (exp(-ΔE/T))
- **Yeniden ısıtma yok** — saf soğuma

### Girdi
- Kendi `load_tsp_data()` fonksiyonunu kullanır (utils'ten bağımsız, dosyanın içinde)
- `data/raw/tsp_n{N}.json` → `distance_matrix`, `coordinates`

### Çıktı (JSON)
```json
{
  "Algorithm": "Standard Simulated Annealing",
  "Cities_N": 5,
  "Best_Path": [0, 2, 4, 1, 3, 0],
  "Best_Cost": 42.5,
  "Duration_Sec": 0.123
}
```
**Çıktı yolu:** `data/raw/tsp_n{N}_sa_solution.json`

> ⚠️ **SPEC UYUMSUZLUĞU:** GA ile aynı sorun — `data/raw/` yerine `data/results/sa/` olmalı.
> ⚠️ **FORMAT FARKI:** GA çıktısı snake_case key kullanıyor, SA PascalCase kullanıyor (`Best_Path`, `Duration_Sec`). Tutarsız.

---

## 3. OR-Tools Çözücü
**Dosya:** `src/classical/or_tools_solver.py`
**Sınıf:** `ORToolsTSPSolver`
**Durum:** ✅ Tamamlandı

### Parametreler
- Strateji: `PATH_CHEAPEST_ARC` (ilk çözüm)
- Mesafeler integer'a yuvarlanır (OR-Tools gereksinimi)
- Gerçek maliyet float olarak ayrıca hesaplanır

### Girdi
- `data/raw/tsp_n{N}.json` → `distance_matrix` key'i (doğrudan JSON okur)

### Çıktı (JSON)
```json
{
  "Algorithm": "Google OR-Tools",
  "Cities_N": 5,
  "Best_Path": [0, 1, 3, 2, 4, 0],
  "Best_Cost": 40.0,
  "Duration_Sec": 0.01
}
```
**Çıktı yolu:** `data/raw/tsp_n{N}_ortools_solution.json`

---

## 4. Brute Force Çözücü (Referans / Ground Truth)
**Dosya:** `src/common/brute_force_solver.py`
**Sınıf:** `BruteForceSolver`
**Durum:** ✅ Tamamlandı

### Girdi
- `data/raw/tsp_n{N}.json` → `distance_matrix`

### Çıktı (JSON)
```json
{
  "num_cities": 5,
  "optimal_path": [0, 2, 4, 1, 3, 0],
  "optimal_cost": 40.0
}
```
**Çıktı yolu:** `data/raw/tsp_n{N}_solution.json`

> Bu dosya GA'nın `optimal_cost` referansı olarak okunur.

---

## 5. QAOA (Standart)
**Dosya:** `src/quantum/qaoa_standard.py`
**Durum:** ⬜ BOŞ DOSYA — Plan A aktif olursa kodlanacak

### Beklenen Özellikler (Spec)
- Kütüphane: `qiskit`, `qiskit-aer`, `qiskit-algorithms`
- Optimizör: SPSA veya COBYLA (`qiskit_algorithms.optimizers`)
- Problem boyutu: N = 3-4 önce, sonra 5-7
- QUBO dönüşümü: `src/quantum/qubo_converter.py`'dan alacak

---

## 6. QUBO Dönüştürücü
**Dosya:** `src/quantum/qubo_converter.py`
**Durum:** ⬜ BOŞ DOSYA — Plan A aktif olursa kodlanacak

### Beklenen Özellikler (Spec)
- TSP → QUBO Hamiltonian dönüşümü (Lucas, 2014 formülasyonu)
- `qiskit_optimization` kütüphanesi kullanılacak

---

## 7. GA-QAOA Hibrit
**Dosya:** `src/quantum/hybrid_ga_qaoa.py`
**Durum:** ⬜ BOŞ DOSYA — Plan A onayından sonra kodlanacak (özgün katkı)

### Beklenen Özellikler (Spec)
- GA, QAOA'nın β ve γ parametre uzayında arama yapar
- Her GA bireyi = (β_1...β_p, γ_1...γ_p) parametre vektörü
- Fitness = QAOA devresinin beklenen enerji değeri (ekspektasyon)
- `src/classical/genetic_algo.py`'daki GA altyapısı yeniden kullanılacak
