# Veri Formatları
[Türkçe] | [English](data_format_en.md)
<!-- Projedeki tüm JSON dosyalarının yapısı ve path'leri — Son güncelleme: 2026-02-21 -->

## Klasör Yapısı

```
data/
├── raw/                              ← TSP problem girdileri (sadece okunur)
│   ├── tsp_n5.json
│   ├── tsp_n6.json
│   └── tsp_n7.json
│
├── ground_truth/                     ← Brute Force optimal çözümler (referans)
│   ├── tsp_n5_solution.json
│   ├── tsp_n6_solution.json
│   └── tsp_n7_solution.json
│
└── results/
    ├── classical/                    ← Klasik algoritma çıktıları
    │   ├── ga/                       ← GA çıktıları
    │   │   └── tsp_n{N}_ga_solution.json
    │   ├── sa/                       ← SA çıktıları
    │   │   └── tsp_n{N}_sa_solution.json
    │   └── ortools/                  ← OR-Tools çıktıları
    │       └── tsp_n{N}_ortools_solution.json
    └── quantum/                      ← Plan A (gelecekte)
        ├── qaoa_standard/            ← Standart QAOA (.gitkeep)
        └── ga_qaoa/                  ← GA-QAOA hibrit (.gitkeep)
```

**Her klasör `utils.py` path yardımcılarıyla yönetilir:**
- `get_raw_dir()` → `data/raw/`
- `get_ground_truth_dir()` → `data/ground_truth/`
- `get_results_dir("ga"|"sa"|"ortools")` → `data/results/classical/{algo}/`

---

## Girdi Verisi: `data/raw/tsp_n{N}.json`

**Üretici:** `src/common/tsp_generator.py` → `TSPGenerator.save_to_csv()`  
**Seed:** `seed=2026` (hem sınıf default'u, hem __main__ bloğu)  
**Koordinatlar:** 0-100 arası rastgele tam sayı, Öklid mesafesi

```json
{
  "num_cities": 5,
  "coordinates": [[37,52],[49,49],[52,64],[31,62],[52,33]],
  "distance_matrix": [
    [0.0, 12.21, 18.03, 18.03, 19.02],
    ...
  ]
}
```

> **Not:** `distance_matrix` float. OR-Tools'a geçerken `int(round(...))` yapılır, sonuç gerçek float'a geri hesaplanır.

---

## Brute Force: `data/ground_truth/tsp_n{N}_solution.json`

**Üretici:** `src/common/brute_force_solver.py`

```json
{
  "algorithm": "Brute Force",
  "num_cities": 5,
  "optimal_path": [0, 3, 2, 4, 1, 0],
  "optimal_cost": 215.4846
}
```

**Okunduğu yer:** `utils.load_optimal_cost(N)` — GA, SA, OR-Tools tarafından gap hesabı için kullanılır.

---

## Standart Algoritma Çıktı Formatı

GA, SA, OR-Tools'un ortak JSON şeması (**snake_case** zorunlu):

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
  "convergence_history": [215.4846, ...]
}
```

> `convergence_history`: GA'da her nesil, SA'da her 100 iterasyon kaydedilir. OR-Tools deterministik olduğu için bu alan **yoktur**.

---

## Hedef 4 — 30-Run Benchmark Dosyaları

Plan B onaylanınca eklenecek dosya formatı:

```
data/results/classical/ga/tsp_n5_ga_30runs.json
```

```json
{
  "algorithm": "Genetic Algorithm",
  "num_cities": 5,
  "num_runs": 30,
  "runs": [
    { "run_id": 1, "best_cost": 215.48, "optimality_gap_percent": 0.0, "duration_sec": 0.74 },
    ...
  ],
  "summary": {
    "mean_cost": 215.48,
    "std_cost": 0.0,
    "mean_gap_percent": 0.0,
    "mean_duration_sec": 0.74
  }
}
```
