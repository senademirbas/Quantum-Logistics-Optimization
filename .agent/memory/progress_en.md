# Project Progress
[Türkçe](progress.md) | [English]
<!-- Last updated: 2026-02-21 -->

## Overall Status: Target 1 ✅ Completed — Waiting for Target 2

---

## Algorithm Status

| Algorithm | File | Status | Note |
|-----------|------|--------|------|
| TSP Generator | `src/common/tsp_generator.py` | ✅ | seed=2026, N=5,6,7 |
| Brute Force | `src/common/brute_force_solver.py` | ✅ | ground_truth/ output |
| Genetic Algorithm | `src/classical/genetic_algo.py` | ✅ | OX crossover, tournament sel. |
| Simulated Annealing | `src/classical/sim_annealing.py` | ✅ | 2-opt, Metropolis |
| Google OR-Tools | `src/classical/or_tools_solver.py` | ✅ | PATH_CHEAPEST_ARC |
| QUBO Converter | `src/quantum/qubo_converter.py` | ⏳ | Plan A — empty |
| Standard QAOA | `src/quantum/qaoa_standard.py` | ⏳ | Plan A — empty |
| GA-QAOA Hybrid | `src/quantum/hybrid_ga_qaoa.py` | ⏳ | Plan A — empty |

---

## Data Status

| File | Location | Status |
|------|----------|--------|
| `tsp_n5.json`, `tsp_n6.json`, `tsp_n7.json` | `data/raw/` | ✅ |
| `tsp_n{5,6,7}_solution.json` | `data/ground_truth/` | ✅ |
| `tsp_n{5,6,7}_ga_solution.json` | `data/results/classical/ga/` | ✅ |
| `tsp_n{5,6,7}_sa_solution.json` | `data/results/classical/sa/` | ✅ |
| `tsp_n{5,6,7}_ortools_solution.json` | `data/results/classical/ortools/` | ✅ |
| 30-run benchmark JSONs | `data/results/classical/*/` | ⏳ Target 4 |
| Quantum outputs | `data/results/quantum/*/` | ⏳ Plan A |

---

## Completed Fixes (2026-02-21)

| # | Issue | Solution |
|---|-------|----------|
| 1 | SA `load_tsp_data()` was duplicated | Imported from `utils.py` |
| 2 | SA and OR-Tools PascalCase keys | Switched to snake_case |
| 3 | SA and OR-Tools didn't calculate gap | Added `load_optimal_cost()` |
| 4 | GA had no convergence_history | Recording every generation now |
| 5 | GA `generations=100` (inconsistent) | Updated to `500` |
| 6 | `tsp_generator` seed=42 (default) | Updated to `seed=2026` |
| 7 | All outputs were in `data/raw/` | Created new folder structure |
| 8 | `data/results/ga/` was old format | Deleted and recreated |

---

## Next Steps

### Go/No-Go Decision Phase (Target 2)
- [ ] Develop QAOA prototype (3-4 cities)
- [ ] Evaluate team's mastery of the subject
- [ ] Decide on Plan A or Plan B

### If Plan B is selected (Targets 3-4)
- [ ] Hyperparameter optimization for GA and SA
- [ ] Write script for 30 independent runs
- [ ] Save 30-run results in `data/results/classical/*/tsp_n{N}_{algo}_30runs.json` format
- [ ] Calculate statistical summaries (mean, std, variance)

### If Plan A is selected (Targets 3-4)
- [ ] `qubo_converter.py` — TSP → QUBO transformation
- [ ] `qaoa_standard.py` — QAOA with SPSA/COBYLA optimizer
- [ ] `hybrid_ga_qaoa.py` — GA-driven QAOA
- [ ] 30-run benchmark for each model

### Target 5 (Both Plans)
- [ ] ANOVA analysis script (`scipy.stats.f_oneway`)
- [ ] Box plots (seaborn)
- [ ] Convergence plots (matplotlib)
- [ ] Final report
