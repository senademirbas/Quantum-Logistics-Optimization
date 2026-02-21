# Data Formats
[Türkçe](data_format.md) | [English]
<!-- Structure and paths of all JSON files in the project — Last updated: 2026-02-21 -->

## Directory Structure

```
data/
├── raw/                              ← TSP problem inputs (read-only)
│   ├── tsp_n5.json
│   ├── tsp_n6.json
│   └── tsp_n7.json
│
├── ground_truth/                     ← Brute Force optimal solutions (reference)
│   ├── tsp_n5_solution.json
│   ├── tsp_n6_solution.json
│   └── tsp_n7_solution.json
│
└── results/
    ├── classical/                    ← Classical algorithm outputs
    │   ├── ga/                       ← GA outputs
    │   │   └── tsp_n{N}_ga_solution.json
    │   ├── sa/                       ← SA outputs
    │   │   └── tsp_n{N}_sa_solution.json
    │   └── ortools/                  ← OR-Tools outputs
    │       └── tsp_n{N}_ortools_solution.json
    └── quantum/                      ← Plan A (future)
        ├── qaoa_standard/            ← Standard QAOA (.gitkeep)
        └── ga_qaoa/                  ← GA-QAOA hybrid (.gitkeep)
```

**Every folder is managed by `utils.py` path helpers:**
- `get_raw_dir()` → `data/raw/`
- `get_ground_truth_dir()` → `data/ground_truth/`
- `get_results_dir("ga"|"sa"|"ortools")` → `data/results/classical/{algo}/`

---

## Input Data: `data/raw/tsp_n{N}.json`

**Generator:** `src/common/tsp_generator.py` → `TSPGenerator.save_to_json()`  
**Seed:** `seed=2026` (both class default and __main__ block)  
**Coordinates:** Random integers between 0-100, Euclidean distance

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

> **Note:** `distance_matrix` is float. When passed to OR-Tools, it is converted to `int(round(...))`, and the final result is recalculated back to true float.

---

## Brute Force: `data/ground_truth/tsp_n{N}_solution.json`

**Generator:** `src/common/brute_force_solver.py`

```json
{
  "algorithm": "Brute Force",
  "num_cities": 5,
  "optimal_path": [0, 3, 2, 4, 1, 0],
  "optimal_cost": 215.4846
}
```

**Read by:** `utils.load_optimal_cost(N)` — used by GA, SA, and OR-Tools for gap calculation.

---

## Standard Algorithm Output Format

Common JSON schema for GA, SA, OR-Tools (**snake_case** mandatory):

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

> `convergence_history`: Recorded every generation in GA, and every 100 iterations in SA. This field **does not exist** for OR-Tools as it is deterministic.

---

## Target 4 — 30-Run Benchmark Files

Format for files added when Plan B is confirmed:

```
data/results/classical/ga/tsp_n5_benchmark_30runs.json
```

```json
{
  "algorithm": "Genetic Algorithm",
  "num_cities": 5,
  "raw_results": [
    { "run": 1, "seed": 2000, "best_cost": 215.48, "duration_sec": 0.74, "optimality_gap_percent": 0.0 },
    ...
  ],
  "stats": {
    "mean_cost": 215.48,
    "std_cost": 0.0,
    "variance_cost": 0.0,
    "min_cost": 215.48,
    "max_cost": 220.10,
    "mean_duration_sec": 0.74
  }
}
```
