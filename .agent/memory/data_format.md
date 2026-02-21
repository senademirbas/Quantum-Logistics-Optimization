# Veri Formatları
<!-- Projedeki tüm JSON dosyalarının yapısı ve path'leri -->

## Klasör Yapısı

```
data/
├── raw/                        ← Girdi ve algoritma çıktıları
│   ├── tsp_n5.json             ← TSP problem verisi (N=5)
│   ├── tsp_n6.json
│   ├── tsp_n7.json
│   ├── tsp_n5_solution.json    ← Brute Force optimal çözüm
│   ├── tsp_n6_solution.json
│   ├── tsp_n7_solution.json
│   ├── tsp_n5_ga_solution.json ← GA çözümü
│   ├── tsp_n5_sa_solution.json ← SA çözümü
│   └── tsp_n5_ortools_solution.json ← OR-Tools çözümü
└── results/
    ├── ga/                     ← (Şu an kullanılmıyor, boş dizin)
    └── sa/                     ← (Şu an kullanılmıyor, boş dizin)
```

> ⚠️ **SORUN:** Algoritmalar `data/raw/` altına yazıyor ama `data/results/` klasörü de var. Birleştirilmeli veya tutarsızlık giderilmeli.

---

## Girdi Verisi: `tsp_n{N}.json`

**Üretici:** `src/common/tsp_generator.py` → `TSPGenerator.save_to_csv()`
**Seed:** `seed=2026`
**Koordinatlar:** 0-100 arası rasgele tam sayı, Öklid mesafesi

```json
{
  "num_cities": 5,
  "coordinates": [
    [37, 52],
    [49, 49],
    [52, 64],
    [31, 62],
    [52, 33]
  ],
  "distance_matrix": [
    [0.0,  12.21, 18.03, 18.03, 19.02],
    [12.21, 0.0,  15.26, 20.22, 16.03],
    ...
  ]
}
```

### Dikkat
- `distance_matrix` float değerler içerir
- OR-Tools kullanırken `int(round(...))` yapılır
- `optimal_cost` key'i **yok** — bu `tsp_n{N}_solution.json`'dan okunur

---

## Brute Force Çıktısı: `tsp_n{N}_solution.json`

```json
{
  "num_cities": 5,
  "optimal_path": [0, 2, 4, 1, 3, 0],
  "optimal_cost": 40.123
}
```

**Okunduğu yer:** `genetic_algo.py` → optimal_cost referansı için

---

## GA Çıktısı: `tsp_n{N}_ga_solution.json`

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

---

## SA Çıktısı: `tsp_n{N}_sa_solution.json`

```json
{
  "Algorithm": "Standard Simulated Annealing",
  "Cities_N": 5,
  "Best_Path": [0, 2, 4, 1, 3, 0],
  "Best_Cost": 42.5,
  "Duration_Sec": 0.123
}
```

> ⚠️ **TUTARSIZLIK:** GA snake_case kullanıyor (`best_route`, `execution_time`), SA PascalCase kullanıyor (`Best_Path`, `Duration_Sec`). Karşılaştırma scripti yazıldığında bu problem yaratır.

---

## OR-Tools Çıktısı: `tsp_n{N}_ortools_solution.json`

```json
{
  "Algorithm": "Google OR-Tools",
  "Cities_N": 5,
  "Best_Path": [0, 1, 3, 2, 4, 0],
  "Best_Cost": 40.0,
  "Duration_Sec": 0.01
}
```

> OR-Tools ile SA aynı format kullanıyor — ancak GA farklı. Standartlaştırılmalı.

---

## Önerilen Standart Çıktı Formatı (Gelecek)

Karşılaştırma analizi için tüm algoritmalar **aynı JSON şemasını** kullanmalı:

```json
{
  "algorithm": "GA",
  "num_cities": 5,
  "best_tour": [0, 2, 4, 1, 3, 0],
  "best_cost": 42.5,
  "optimal_cost": 40.0,
  "optimality_gap_pct": 6.25,
  "duration_sec": 1.234,
  "run_params": {}
}
```
