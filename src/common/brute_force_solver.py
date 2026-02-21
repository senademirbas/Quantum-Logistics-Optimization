import sys
import json
import numpy as np
import itertools
from pathlib import Path

# Proje kök dizinini ayarla (Importların çalışması için)
current_file = Path(__file__).resolve()
project_root = current_file.parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


class BruteForceSolver:
    """Solves TSP by exhaustive permutation search — Ground Truth generator.

    Complexity: O((N-1)!)  — only suitable for N ≤ ~10.
    Output goes to data/ground_truth/ as the reference for all algorithms.
    """

    def __init__(self, distance_matrix):
        self.matrix = distance_matrix
        self.num_cities = min(distance_matrix.shape)

    def solve(self):
        """Returns (best_path, min_cost) over all permutations."""
        cities = list(range(self.num_cities))
        min_cost = float("inf")
        best_path = []

        for perm in itertools.permutations(cities[1:]):
            current_path = [0] + list(perm) + [0]
            current_cost = 0
            valid = True

            for i in range(len(current_path) - 1):
                u, v = current_path[i], current_path[i + 1]
                if u >= self.num_cities or v >= self.num_cities:
                    valid = False
                    break
                current_cost += self.matrix[u][v]

            if valid and current_cost < min_cost:
                min_cost = current_cost
                best_path = current_path

        return best_path, min_cost


if __name__ == "__main__":
    print("Starting Brute Force Solver → data/ground_truth/")
    print("-" * 60)

    from src.common.utils import get_raw_dir, get_ground_truth_dir

    raw_dir = get_raw_dir()
    gt_dir = get_ground_truth_dir()
    gt_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [5, 6, 7]

    for n in scenarios:
        input_path = raw_dir / f"tsp_n{n}.json"
        output_path = gt_dir / f"tsp_n{n}_solution.json"

        if not input_path.exists():
            print(f" [N={n}] WARNING: {input_path.name} not found.")
            continue

        print(f" [N={n}] Processing: {input_path.name}")
        try:
            with open(input_path, "r") as f:
                tsp_data = json.load(f)

            matrix = np.array(tsp_data["distance_matrix"])
            print(f"    -> Matrix shape: {matrix.shape}")

            if matrix.shape[0] != matrix.shape[1]:
                print("    -> WARNING: Non-square matrix!")

            solver = BruteForceSolver(matrix)
            path, cost = solver.solve()

            solution_data = {
                "algorithm": "Brute Force",
                "num_cities": n,
                "optimal_path": [int(c) for c in path],
                "optimal_cost": float(cost)
            }

            with open(output_path, "w") as f:
                json.dump(solution_data, f, indent=4)

            print(f"    -> Optimal Path: {path}")
            print(f"    -> Cost: {cost:.4f}")
            print(f"    -> SAVED: data/ground_truth/{output_path.name}\n")

        except Exception as e:
            print(f"    -> ERROR: {e}")
            import traceback; traceback.print_exc()

    print("-" * 60)
    print("All tasks completed.")