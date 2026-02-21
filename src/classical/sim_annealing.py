import math
import random
import sys
import time
import json
from pathlib import Path
from typing import List, Tuple

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]

if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.common.utils import load_tsp_data, load_optimal_cost, get_results_dir


class SimulatedAnnealingTSP:
    """Solves TSP using Simulated Annealing (SA).
    
    Neighbour : 2-opt (reverse a random segment)
    Acceptance: Metropolis criterion exp(-ΔE / T)
    Cooling   : Geometric cooling T *= alpha each step
    """

    def __init__(self, num_cities: int, initial_temp: float = 1000.0,
                 alpha: float = 0.99, stopping_temp: float = 1e-6, seed: int = None):
        self.num_cities = num_cities
        self.initial_temp = initial_temp
        self.alpha = alpha
        self.stopping_temp = stopping_temp
        self.seed = seed

        if self.seed is not None:
            random.seed(self.seed)

        self.distance_matrix, self.coordinates, _ = load_tsp_data(num_cities)
        self.optimal_cost = load_optimal_cost(num_cities)
        if self.optimal_cost == 0.0:
            print(f"  [WARN] Optimal cost unavailable for N={num_cities}. Gap will be N/A.")

    def calculate_distance(self, route: List[int]) -> float:
        """Closed-loop total distance of a tour."""
        total = sum(self.distance_matrix[route[i]][route[i + 1]]
                    for i in range(len(route) - 1))
        total += self.distance_matrix[route[-1]][route[0]]
        return total

    def _two_opt_neighbour(self, route: List[int]) -> List[int]:
        """2-opt move: reverse a random segment of the route."""
        i, j = sorted(random.sample(range(self.num_cities), 2))
        new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
        return new_route

    def run(self) -> Tuple[List[int], float, float, List[float]]:
        """
        Runs Simulated Annealing.

        Returns:
            best_tour (list): Closed tour [city, ..., city, start]
            best_cost (float): Total distance of best tour
            duration (float): Execution time in seconds
            convergence_history (list[float]): Best cost sampled every 100 iterations
        """
        print(f"Starting Simulated Annealing (N={self.num_cities}, "
              f"T0={self.initial_temp}, alpha={self.alpha})")

        start_time = time.time()
        current_route = list(range(self.num_cities))
        random.shuffle(current_route)

        current_cost = self.calculate_distance(current_route)
        best_route = current_route[:]
        best_cost = current_cost

        temp = self.initial_temp
        iteration = 0
        convergence_history: List[float] = []

        while temp > self.stopping_temp:
            new_route = self._two_opt_neighbour(current_route)
            new_cost = self.calculate_distance(new_route)
            delta = new_cost - current_cost

            if delta < 0 or random.random() < math.exp(-delta / temp):
                current_route = new_route
                current_cost = new_cost

            if current_cost < best_cost:
                best_cost = current_cost
                best_route = current_route[:]

            temp *= self.alpha
            iteration += 1

            # Sample convergence every 100 iterations
            if iteration % 100 == 0:
                convergence_history.append(best_cost)

        duration = time.time() - start_time

        # Build closed tour
        closed_tour = best_route + [best_route[0]]

        # Optimality gap
        if self.optimal_cost > 0:
            gap = (best_cost - self.optimal_cost) / self.optimal_cost * 100
        else:
            gap = None

        print(f"   -> Completed in {duration:.4f}s | Iterations: {iteration}")
        print(f"   -> SA Best Cost: {best_cost:.4f}")
        if gap is not None:
            print(f"   -> Optimality Gap: {gap:.2f}%")
        else:
            print("   -> Optimality Gap: N/A")
        print("-" * 40)

        return closed_tour, best_cost, duration, convergence_history


if __name__ == "__main__":
    scenarios = [5, 6, 7]
    output_dir = get_results_dir("sa")
    print(f"Running Simulated Annealing for scenarios: {scenarios}\n")

    for n in scenarios:
        try:
            sa = SimulatedAnnealingTSP(num_cities=n, initial_temp=1000.0,
                                       alpha=0.99, stopping_temp=1e-6, seed=2026)
            best_tour, best_cost, duration, convergence = sa.run()

            optimal_cost = sa.optimal_cost
            gap = ((best_cost - optimal_cost) / optimal_cost * 100
                   if optimal_cost > 0 else None)

            result_data = {
                "algorithm": "Simulated Annealing",
                "num_cities": n,
                "best_tour": best_tour,
                "best_cost": float(best_cost),
                "optimal_cost": float(optimal_cost),
                "optimality_gap_percent": round(gap, 4) if gap is not None else None,
                "duration_sec": round(duration, 6),
                "run_params": {
                    "initial_temp": sa.initial_temp,
                    "alpha": sa.alpha,
                    "stopping_temp": sa.stopping_temp
                },
                "convergence_history": [round(v, 4) for v in convergence]
            }

            output_file = output_dir / f"tsp_n{n}_sa_solution.json"
            with open(output_file, "w") as f:
                json.dump(result_data, f, indent=4)
            print(f" [SAVED] N={n} -> {output_file.name}\n")

        except Exception as e:
            print(f" [ERROR] N={n}: {e}")
            import traceback; traceback.print_exc()
            print("-" * 40)