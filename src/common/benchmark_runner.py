import json
import time
import sys
import numpy as np
from pathlib import Path

# Adjust path to import solvers
current_file = Path(__file__).resolve()
project_root = current_file.parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.classical.genetic_algo import GeneticAlgorithmTSP
from src.classical.sim_annealing import SimulatedAnnealingTSP
from src.classical.or_tools_solver import ORToolsTSPSolver
from src.common.utils import get_results_dir, load_tsp_data, load_optimal_cost

def run_30_tests(algorithm_name, n, runs=30):
    """Runs designated algorithm 30 times with different seeds."""
    print(f"\n[BENCHMARK] Algorithm: {algorithm_name} | N: {n} | Runs: {runs}")
    
    results = []
    output_dir = get_results_dir(algorithm_name.lower().replace(" ", ""))
    optimal_cost = load_optimal_cost(n)
    
    # OR-Tools is deterministic by default in our setup, but we'll loop it for structural consistency
    for i in range(runs):
        seed = 2000 + i
        
        if algorithm_name == "ga":
            solver = GeneticAlgorithmTSP(num_cities=n, seed=seed)
            _, best_cost, duration, _ = solver.run()
        elif algorithm_name == "sa":
            solver = SimulatedAnnealingTSP(num_cities=n, seed=seed)
            _, best_cost, duration, _ = solver.run()
        elif algorithm_name == "ortools":
            # For OR-Tools, load matrix first
            distance_matrix, _, _ = load_tsp_data(n)
            solver = ORToolsTSPSolver(distance_matrix)
            res = solver.solve()
            best_cost = res["best_cost"]
            duration = res["duration_sec"]
        
        # Calculate gap if optimal cost is available
        gap = None
        if optimal_cost > 0:
            gap = round((best_cost - optimal_cost) / optimal_cost * 100, 4)

        results.append({
            "run": i + 1,
            "seed": seed,
            "best_cost": float(best_cost),
            "duration_sec": float(duration),
            "optimality_gap_percent": gap
        })

    # Statistical Calculations
    costs = [r["best_cost"] for r in results]
    durations = [r["duration_sec"] for r in results]
    
    summary = {
        "algorithm": algorithm_name,
        "num_cities": n,
        "total_runs": runs,
        "stats": {
            "mean_cost": float(np.mean(costs)),
            "std_cost": float(np.std(costs)),
            "variance_cost": float(np.var(costs)),
            "min_cost": float(np.min(costs)),
            "max_cost": float(np.max(costs)),
            "mean_duration_sec": float(np.mean(durations))
        },
        "raw_results": results
    }

    output_file = output_dir / f"tsp_n{n}_benchmark_30runs.json"
    with open(output_file, "w") as f:
        json.dump(summary, f, indent=4)
        
    print(f"[COMPLETED] Stats for N={n}: Mean Cost={summary['stats']['mean_cost']:.2f}")
    return summary

if __name__ == "__main__":
    for n in [5, 6, 7]:
        for algo in ["ga", "sa", "ortools"]:
            run_30_tests(algo, n)
