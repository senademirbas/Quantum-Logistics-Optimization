# Algorithm Specifications
[Türkçe](algorithms_spec.md) | [English]
<!-- Expected I/O, parameters, and current status — Last updated: 2026-02-21 -->

## 1. Genetic Algorithm (GA)
**File:** `src/classical/genetic_algo.py`  
**Class:** `GeneticAlgorithmTSP`  
**Status:** ✅ Completed

### Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_cities` | — | Number of cities (5, 6, 7) |
| `pop_size` | 100 | Population size |
| `mutation_rate` | 0.01 | Mutation probability |
| `generations` | 500 | Number of generations |
| `seed` | None | Random seed for reproducibility |

### Operators
- **Selection:** Tournament selection (tournament size: 5)
- **Crossover:** Ordered Crossover (OX)
- **Mutation:** Swap mutation (exchange 2 cities)
- **Elitism:** Best individual survives to next generation

### Input
- `data/raw/tsp_n{N}.json` → `distance_matrix` via `load_tsp_data(N)`
- Ground truth: `data/ground_truth/tsp_n{N}_solution.json` → `optimal_cost` via `load_optimal_cost(N)`

### Output (JSON) → `data/results/classical/ga/tsp_n{N}_ga_solution.json`
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
**File:** `src/classical/sim_annealing.py`  
**Class:** `SimulatedAnnealingTSP`  
**Status:** ✅ Completed

### Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_cities` | — | Number of cities |
| `initial_temp` | 1000.0 | Initial temperature |
| `alpha` | 0.99 | Geometric cooling coefficient |
| `stopping_temp` | 1e-6 | Stopping temperature |
| `seed` | None | Random seed for reproducibility |

### Algorithm Details
- **Neighbor Generation:** 2-Opt (reverse random segment)
- **Acceptance Criterion:** Metropolis — `exp(-ΔE / T)`
- **Convergence Sampling:** 1 record every 100 iterations

### Input
- `data/raw/tsp_n{N}.json` → `load_tsp_data(N)` via `utils.py`
- Ground truth: `data/ground_truth/tsp_n{N}_solution.json` → `load_optimal_cost(N)`

### Output (JSON) → `data/results/classical/sa/tsp_n{N}_sa_solution.json`
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
**File:** `src/classical/or_tools_solver.py`  
**Class:** `ORToolsTSPSolver`  
**Status:** ✅ Completed

### Parameters
- **Strategy:** `PATH_CHEAPEST_ARC` (deterministic, same result every run)
- Distances are passed to OR-Tools as integers, real float is calculated separately

### Input
- `data/raw/tsp_n{N}.json` → `distance_matrix` via `get_raw_dir()`
- Ground truth: `data/ground_truth/tsp_n{N}_solution.json` → `load_optimal_cost(N)`

### Output (JSON) → `data/results/classical/ortools/tsp_n{N}_ortools_solution.json`
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

> The `convergence_history` field **does not exist** for OR-Tools as it is deterministic.

---

## 4. Brute Force (Ground Truth Generator)
**File:** `src/common/brute_force_solver.py`  
**Class:** `BruteForceSolver`  
**Status:** ✅ Completed

### Complexity: O((N-1)!) — practical only for N ≤ 10

### Input
- `data/raw/tsp_n{N}.json` → `distance_matrix` via `get_raw_dir()`

### Output (JSON) → `data/ground_truth/tsp_n{N}_solution.json`
```json
{
  "algorithm": "Brute Force",
  "num_cities": 5,
  "optimal_path": [0, 3, 2, 4, 1, 0],
  "optimal_cost": 215.4846
}
```

> This file is read by `load_optimal_cost(N)` for GA, SA, and OR-Tools.

---

## 5. QAOA (Standard) — Plan A
**File:** `src/quantum/qaoa_standard.py`  
**Status:** ⏳ EMPTY — To be coded after Plan A Go decision

### Expected Features
- Libraries: `qiskit`, `qiskit-aer`, `qiskit-algorithms`
- Optimizer: **SPSA** or **COBYLA**
- QUBO transformation: from `src/quantum/qubo_converter.py`
- Problem size: Prototype N=3-4, final N=5,6,7

---

## 6. QUBO Converter — Plan A
**File:** `src/quantum/qubo_converter.py`  
**Status:** ⏳ EMPTY — To be coded if Plan A is active

### Expected Features
- TSP → QUBO Hamiltonian (Lucas, 2014)
- `qiskit_optimization` library

---

## 7. GA-QAOA Hybrid — Plan A (Original Contribution)
**File:** `src/quantum/hybrid_ga_qaoa.py`  
**Status:** ⏳ EMPTY — To be coded after Plan A Go decision

### Original Value
In Standard QAOA, β/γ parameters are optimized with SPSA/COBYLA → gets stuck in local minima.  
In this model, **GA performs global search** in the parameter space.

### Expected Features
- Each GA individual = `(β₁,...,βₚ, γ₁,...,γₚ)` — 2p dimensional float vector
- Fitness function = Hamiltonian expectation value of the QAOA circuit
- Mutation: On real numbers (not OX)
- Backend: `qiskit-aer` simulation

### Plan A Comparison Set (4 Models)
| Model | Parameter Optimization |
|-------|------------------------|
| **GA-QAOA** | GA (original contribution of this project) |
| **Standard QAOA** | SPSA or COBYLA |
| **GA** | Direct TSP solver |
| **SA** | Direct TSP solver |

---

## 8. Benchmark Runner
**File:** `src/common/benchmark_runner.py`  
**Status:** ✅ Completed

### Function
- Runs designated algorithms 30 independent times.
- Uses a different `seed` (2000 + i) for each run.
- Produces statistical summary (mean, std, min, max).
- Output: `data/results/classical/{algo}/tsp_n{N}_benchmark_30runs.json`
