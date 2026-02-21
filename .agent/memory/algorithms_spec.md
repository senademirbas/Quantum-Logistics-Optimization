# Algoritma Spesifikasyonları
[Türkçe] | [English](algorithms_spec_en.md)
<!-- Her algoritmanın beklenen I/O, parametreleri ve güncel durumu — Son güncelleme: 2026-02-21 -->

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
| `seed` | None | Tekrarlanabilirlik için rastgele tohum |

### Operatörler
- **Seçilim:** Tournament selection (turnuva boyutu: 5)
- **Çaprazlama:** Ordered Crossover (OX)
- **Mutasyon:** Swap mutation (2 şehir değişimi)
- **Elitizm:** En iyi birey sonraki nesle aktarılır

### Girdi
- `data/raw/tsp_n{N}.json` → `distance_matrix` via `load_tsp_data(N)`
- Ground truth: `data/ground_truth/tsp_n{N}_solution.json` → `optimal_cost` via `load_optimal_cost(N)`

### Çıktı (JSON) → `data/results/classical/ga/tsp_n{N}_ga_solution.json`
```json
{
  "algorithm": "Genetic Algorithm",
  "num_cities": 5,
  "best_tour": [0, 3, 2, 4, 1, 0],
  "best_cost": 215.4846,
  "optimal_cost": 215.4846,
  "optimality_gap_percent": 0.0,
  "duration_sec": 0.741432,
  "run_params": {
    "pop_size": 100,
    "mutation_rate": 0.01,
    "generations": 500
  },
  "convergence_history": [250.12, 230.45, ..., 215.48]
}
```

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
| `alpha` | 0.99 | Geometrik soğuma katsayısı |
| `stopping_temp` | 1e-6 | Durdurma sıcaklığı |
| `seed` | None | Tekrarlanabilirlik için rastgele tohum |

### Algoritma Detayları
- **Komşu üretimi:** 2-Opt (rastgele segment ters çevirme)
- **Kabul kriteri:** Metropolis — `exp(-ΔE / T)`
- **Yakınsama örnekleme:** Her 100 iterasyonda 1 kayıt

### Girdi
- `data/raw/tsp_n{N}.json` → `load_tsp_data(N)` via `utils.py`
- Ground truth: `data/ground_truth/tsp_n{N}_solution.json` → `load_optimal_cost(N)`

### Çıktı (JSON) → `data/results/classical/sa/tsp_n{N}_sa_solution.json`
```json
{
  "algorithm": "Simulated Annealing",
  "num_cities": 5,
  "best_tour": [0, 3, 2, 4, 1, 0],
  "best_cost": 215.4846,
  "optimal_cost": 215.4846,
  "optimality_gap_percent": 0.0,
  "duration_sec": 1.123456,
  "run_params": {
    "initial_temp": 1000.0,
    "alpha": 0.99,
    "stopping_temp": 1e-06
  },
  "convergence_history": [280.5, 250.1, ..., 215.48]
}
```

---

## 3. Google OR-Tools
**Dosya:** `src/classical/or_tools_solver.py`  
**Sınıf:** `ORToolsTSPSolver`  
**Durum:** ✅ Tamamlandı

### Parametreler
- **Strateji:** `PATH_CHEAPEST_ARC` (deterministik, her çalıştırmada aynı sonuç)
- Mesafeler OR-Tools'a integer olarak geçirilir, gerçek float hesaplanır ayrıca

### Girdi
- `data/raw/tsp_n{N}.json` → `distance_matrix` via `get_raw_dir()`
- Ground truth: `data/ground_truth/tsp_n{N}_solution.json` → `load_optimal_cost(N)`

### Çıktı (JSON) → `data/results/classical/ortools/tsp_n{N}_ortools_solution.json`
```json
{
  "algorithm": "Google OR-Tools",
  "num_cities": 5,
  "best_tour": [0, 1, 3, 2, 4, 0],
  "best_cost": 215.4846,
  "optimal_cost": 215.4846,
  "optimality_gap_percent": 0.0,
  "duration_sec": 0.000123,
  "run_params": {
    "strategy": "PATH_CHEAPEST_ARC"
  }
}
```

> OR-Tools deterministik olduğundan `convergence_history` alanı **yoktur**.

---

## 4. Brute Force (Ground Truth Üreteci)
**Dosya:** `src/common/brute_force_solver.py`  
**Sınıf:** `BruteForceSolver`  
**Durum:** ✅ Tamamlandı

### Kompleksite: O((N-1)!) — yalnızca N ≤ 10 için pratik

### Girdi
- `data/raw/tsp_n{N}.json` → `distance_matrix` via `get_raw_dir()`

### Çıktı (JSON) → `data/ground_truth/tsp_n{N}_solution.json`
```json
{
  "algorithm": "Brute Force",
  "num_cities": 5,
  "optimal_path": [0, 3, 2, 4, 1, 0],
  "optimal_cost": 215.4846
}
```

> Bu dosya `load_optimal_cost(N)` tarafından GA, SA ve OR-Tools için okunur.

---

## 5. QAOA (Standart) — Plan A
**Dosya:** `src/quantum/qaoa_standard.py`  
**Durum:** ⏳ BOŞ — Plan A Go kararından sonra kodlanacak

### Beklenen Özellikler
- Kütüphane: `qiskit`, `qiskit-aer`, `qiskit-algorithms`
- Optimizör: **SPSA** veya **COBYLA**
- QUBO dönüşümü: `src/quantum/qubo_converter.py`'dan
- Problem boyutu: Prototip N=3-4, final N=5,6,7

---

## 6. QUBO Dönüştürücü — Plan A
**Dosya:** `src/quantum/qubo_converter.py`  
**Durum:** ⏳ BOŞ — Plan A aktif olursa kodlanacak

### Beklenen Özellikler
- TSP → QUBO Hamiltonian (Lucas, 2014)
- `qiskit_optimization` kütüphanesi

---

## 7. GA-QAOA Hibrit — Plan A (Özgün Katkı)
**Dosya:** `src/quantum/hybrid_ga_qaoa.py`  
**Durum:** ⏳ BOŞ — Plan A Go kararından sonra kodlanacak

### Özgün Değer
Standart QAOA'da β/γ parametreleri SPSA/COBYLA ile optimize edilir → yerel minimumlara takılır.  
Bu modelde **GA, parametre uzayında global arama** yapar.

### Beklenen Özellikler
- Her GA bireyi = `(β₁,...,βₚ, γ₁,...,γₚ)` — 2p boyutlu float vektör
- Fitness fonksiyonu = QAOA devresinin Hamiltonian beklenti değeri
- Mutasyon: gerçek sayı üzerinde (OX değil)
- Backend: `qiskit-aer` simülasyonu

### Plan A Kıyaslama Seti (4 Model)
| Model | Parametre Optimizasyonu |
|-------|------------------------|
| **GA-QAOA** | GA (bu projenin özgün katkısı) |
| **Standart QAOA** | SPSA veya COBYLA |
| **GA** | Doğrudan TSP çözücü |
| **SA** | Doğrudan TSP çözücü |

---

## 8. Benchmark Runner
**Dosya:** `src/common/benchmark_runner.py`  
**Durum:** ✅ Tamamlandı

### İşlev
- Belirlenen algoritmaları 30 bağımsız kez çalıştırır.
- Her çalıştırma için farklı bir `seed` (2000 + i) kullanır.
- İstatistiksel özet (mean, std, min, max) üretir.
- Çıktı: `data/results/classical/{algo}/tsp_n{N}_benchmark_30runs.json`
