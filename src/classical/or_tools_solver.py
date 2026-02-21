import sys
import json
import time
from pathlib import Path
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.common.utils import load_optimal_cost, load_tsp_data, get_raw_dir, get_results_dir


class ORToolsTSPSolver:
    """Solves TSP using Google OR-Tools (PATH_CHEAPEST_ARC strategy).
    
    Used as a deterministic industry-standard benchmark (Plan B).
    Distances are rounded to integers for OR-Tools, but the real
    floating-point cost is recalculated from the original matrix.
    """

    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)

        self.manager = pywrapcp.RoutingIndexManager(self.num_cities, 1, 0)
        self.routing = pywrapcp.RoutingModel(self.manager)

        self._register_distance_callback()
        self._set_search_parameters()

    def _register_distance_callback(self):
        def distance_callback(from_index, to_index):
            from_node = self.manager.IndexToNode(from_index)
            to_node = self.manager.IndexToNode(to_index)
            # OR-Tools requires integer costs — round to nearest integer
            return int(round(self.distance_matrix[from_node][to_node]))

        transit_idx = self.routing.RegisterTransitCallback(distance_callback)
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

    def _set_search_parameters(self):
        self.search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        self.search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

    def solve(self):
        """Solves TSP and returns best tour with real float cost.

        Returns:
            dict with: best_tour, best_cost, duration_sec
            None if no solution found.
        """
        start_time = time.time()
        solution = self.routing.SolveWithParameters(self.search_parameters)
        duration = time.time() - start_time

        if solution is None:
            return None

        # Extract route
        route = []
        index = self.routing.Start(0)
        while not self.routing.IsEnd(index):
            route.append(int(self.manager.IndexToNode(index)))
            index = solution.Value(self.routing.NextVar(index))
        route.append(route[0])  # close the tour

        # Recalculate real float cost (OR-Tools solved on rounded ints)
        real_cost = sum(
            self.distance_matrix[route[i]][route[i + 1]]
            for i in range(len(route) - 1)
        )

        return {
            "best_tour": route,
            "best_cost": real_cost,
            "duration_sec": duration
        }


if __name__ == "__main__":
    print("Solving TSP using Google OR-Tools...")
    print("-" * 60)

    raw_data_dir = get_raw_dir()
    output_dir = get_results_dir("ortools")
    scenarios = [5, 6, 7]

    for n in scenarios:
        input_path = raw_data_dir / f"tsp_n{n}.json"
        output_path = output_dir / f"tsp_n{n}_ortools_solution.json"

        if not input_path.exists():
            print(f" [N={n}] WARNING: Input file not found ({input_path.name})")
            continue

        print(f" [N={n}] Processing: tsp_n{n}.json")
        try:
            distance_matrix, _, _ = load_tsp_data(n)
            solver = ORToolsTSPSolver(distance_matrix)
            result = solver.solve()

            if result is None:
                print(f"    -> ERROR: No solution found.")
                continue

            # Load optimal cost from brute force solution for gap calculation
            optimal_cost = load_optimal_cost(n)
            best_cost = result["best_cost"]
            gap = ((best_cost - optimal_cost) / optimal_cost * 100
                   if optimal_cost > 0 else None)

            output_data = {
                "algorithm": "Google OR-Tools",
                "num_cities": n,
                "best_tour": result["best_tour"],
                "best_cost": float(best_cost),
                "optimal_cost": float(optimal_cost),
                "optimality_gap_percent": round(gap, 4) if gap is not None else None,
                "duration_sec": round(result["duration_sec"], 6),
                "run_params": {
                    "strategy": "PATH_CHEAPEST_ARC"
                }
            }

            with open(output_path, "w") as f:
                json.dump(output_data, f, indent=4)

            print(f"    -> Best Tour: {result['best_tour']}")
            print(f"    -> Cost: {best_cost:.4f}")
            if gap is not None:
                print(f"    -> Optimality Gap: {gap:.2f}%")
            print(f"    -> SAVED: {output_path.name}\n")

        except Exception as e:
            print(f"    -> ERROR: {e}")
            import traceback; traceback.print_exc()

    print("-" * 60)
    print("All tasks completed.")