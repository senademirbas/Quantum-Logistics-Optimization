# Coding Rules and Conventions
[Türkçe](conventions.md) | [English]
<!-- Antigravity follows these rules when writing code — Last updated: 2026-02-21 -->

## General

- **Language:** Python 3.12
- **Environment:** `.venv` (at project root) — `python -m venv .venv`
- **Execution:** `.\.venv\Scripts\python.exe src/classical/genetic_algo.py`
- **Branch:** `dev` (to be merged into main via PR)

---

## Project Structure

```
Quantum-Logistics-Optimization/
├── data/
│   ├── raw/                     ← TSP inputs (tsp_generator output)
│   ├── ground_truth/            ← Brute force reference solutions
│   └── results/
│       ├── classical/ga/        ← GA outputs
│       ├── classical/sa/        ← SA outputs
│       ├── classical/ortools/   ← OR-Tools outputs
│       └── quantum/             ← Plan A (future)
├── src/
│   ├── common/
│   │   ├── utils.py             ← Path helpers + data loading
│   │   ├── tsp_generator.py     ← TSP problem generator
│   │   └── brute_force_solver.py ← Ground truth generator
│   ├── classical/
│   │   ├── genetic_algo.py      ← GA (completed ✅)
│   │   ├── sim_annealing.py     ← SA (completed ✅)
│   │   └── or_tools_solver.py   ← OR-Tools (completed ✅)
│   └── quantum/                 ← Plan A (pending)
│       ├── qubo_converter.py    ← (Empty)
│       ├── qaoa_standard.py     ← (Empty)
│       └── hybrid_ga_qaoa.py    ← (Empty)
└── .agent/memory/               ← Project memory (this folder)
```

---

## Path Helpers (`utils.py`)

Never hard-code file paths — always use `utils.py` functions:

```python
from src.common.utils import get_raw_dir, get_ground_truth_dir, get_results_dir

raw_dir      = get_raw_dir()                   # data/raw/
gt_dir       = get_ground_truth_dir()          # data/ground_truth/
ga_out_dir   = get_results_dir("ga")           # data/results/classical/ga/
sa_out_dir   = get_results_dir("sa")           # data/results/classical/sa/
ort_out_dir  = get_results_dir("ortools")      # data/results/classical/ortools/
```

---

## Import Rules

In every `src/classical/` or `src/common/` file:

```python
from pathlib import Path
import sys
current_file = Path(__file__).resolve()
project_root = current_file.parents[2]  # always 2 levels up = project root
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
```

---

## JSON Key Standards

All algorithm outputs use **snake_case** — **mandatory:**

| ✅ Use | ❌ Don't Use |
|--------|--------------|
| `algorithm` | `Algorithm` |
| `best_tour` | `Best_Path` |
| `best_cost` | `Best_Cost` |
| `duration_sec` | `Duration_Sec` |
| `num_cities` | `Cities_N` |
| `run_params` | `parameters` |
| `convergence_history` | `history` |

---

## Class Structure

```python
class AlgorithmNameTSP:
    def __init__(self, num_cities, ...params):
        self.distance_matrix, _, _ = load_tsp_data(num_cities)
        self.optimal_cost = load_optimal_cost(num_cities)

    def run(self) -> tuple:
        # return: (best_tour, best_cost, duration_sec, convergence_history)
        pass

if __name__ == "__main__":
    scenarios = [5, 6, 7]
    output_dir = get_results_dir("algo_name")
    for n in scenarios:
        ...
        with open(output_dir / f"tsp_n{n}_algo_solution.json", "w") as f:
            json.dump(result_data, f, indent=4)
```

---

## Performance Measurement

```python
import time
start_time = time.time()
# ... algorithm ...
duration = time.time() - start_time  # seconds (float)
```

- `duration_sec` → saved to JSON with `round(duration, 6)`
- `convergence_history` → `[round(v, 4) for v in history]`

---

## Dependencies (`requirements.txt`)

| Package | Version | Usage |
|---------|---------|-------|
| `numpy` | 2.4.2 | Matrix operations |
| `pandas` | 3.0.1 | (Not used yet) |
| `ortools` | 9.11.4210 | OR-Tools solver (**9.11** — Python 3.12 compatible) |
| `qiskit` | 2.3.0 | Quantum circuit (Plan A) |
| `qiskit-aer` | 0.17.2 | Simulation backend (Plan A) |
| `qiskit-algorithms` | 0.4.0 | QAOA, SPSA, COBYLA (Plan A) |
| `qiskit-optimization` | 0.7.0 | QUBO conversion (Plan A) |
| `scipy` | 1.17.0 | ANOVA analysis |
| `matplotlib` | 3.10.8 | Plots |
| `seaborn` | 0.13.2 | Box plot |

> ⚠️ Use `ortools` 9.11.4210 (not 9.9.x — causes DLL errors on Python 3.12).
