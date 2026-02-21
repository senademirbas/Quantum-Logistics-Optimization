import random
import sys
import time
import json
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]

if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.common.utils import load_tsp_data, load_optimal_cost, get_results_dir


class GeneticAlgorithmTSP:
    """Solves TSP using a Genetic Algorithm (GA).
    
    Operators:
        Selection  : Tournament selection (size=5)
        Crossover  : Ordered Crossover (OX)
        Mutation   : Swap mutation
        Elitism    : Best individual always survives
    """

    def __init__(self, num_cities, pop_size=100, mutation_rate=0.01, generations=500, seed=None):
        self.num_cities = num_cities
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.seed = seed

        if self.seed is not None:
            random.seed(self.seed)

        # Load TSP data
        self.distance_matrix, _, _ = load_tsp_data(num_cities)

        # Load optimal cost from Brute Force solution for gap calculation
        self.optimal_cost = load_optimal_cost(num_cities)
        if self.optimal_cost == 0.0:
            print(f"  [WARN] Optimal cost unavailable for N={num_cities}. Gap will be N/A.")

    def calculate_distance(self, route):
        """Calculates closed-loop total distance of a route."""
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distance_matrix[route[i]][route[i + 1]]
        distance += self.distance_matrix[route[-1]][route[0]]
        return distance

    def create_population(self):
        """Creates initial population of random routes."""
        base_route = list(range(self.num_cities))
        return [random.sample(base_route, self.num_cities) for _ in range(self.pop_size)]

    def selection(self, population, distances):
        """Tournament selection (tournament size = 5)."""
        candidates = random.sample(range(len(population)), 5)
        best_idx = min(candidates, key=lambda i: distances[i])
        return population[best_idx]

    def crossover(self, parent1, parent2):
        """Ordered Crossover (OX)."""
        size = self.num_cities
        start, end = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[start:end] = parent1[start:end]

        pointer = 0
        for city in parent2:
            if city not in child:
                while child[pointer] != -1:
                    pointer += 1
                child[pointer] = city
        return child

    def mutate(self, route):
        """Swap mutation: randomly swap two cities."""
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.num_cities), 2)
            route[i], route[j] = route[j], route[i]
        return route

    def run(self):
        """
        Runs the GA.

        Returns:
            best_route (list): Closed tour [0, ..., 0]
            best_cost (float): Total distance of best tour
            duration (float): Execution time in seconds
            convergence_history (list[float]): Best cost at each generation
        """
        print(f"Starting Genetic Algorithm (N={self.num_cities}, "
              f"pop={self.pop_size}, gen={self.generations}, "
              f"mut={self.mutation_rate})")

        start_time = time.time()
        population = self.create_population()
        global_best_distance = float("inf")
        global_best_route = []
        convergence_history = []  # best cost per generation

        for gen in range(self.generations):
            distances = [self.calculate_distance(ind) for ind in population]
            min_dist = min(distances)

            if min_dist < global_best_distance:
                global_best_distance = min_dist
                best_idx = distances.index(min_dist)
                global_best_route = population[best_idx][:]

            convergence_history.append(global_best_distance)

            # Build next generation with elitism
            elite_idx = distances.index(min_dist)
            new_population = [population[elite_idx]]
            while len(new_population) < self.pop_size:
                p1 = self.selection(population, distances)
                p2 = self.selection(population, distances)
                child = self.mutate(self.crossover(p1, p2))
                new_population.append(child)

            population = new_population

        duration = time.time() - start_time

        # Build closed tour
        closed_path = [int(c) for c in global_best_route]
        closed_path.append(closed_path[0])

        # Optimality gap
        if self.optimal_cost > 0:
            gap = (global_best_distance - self.optimal_cost) / self.optimal_cost * 100
        else:
            gap = None

        print(f"   -> Completed in {duration:.4f}s | Generations: {self.generations}")
        print(f"   -> GA Best Cost: {global_best_distance:.4f}")
        if gap is not None:
            print(f"   -> Optimality Gap: {gap:.2f}%")
        else:
            print("   -> Optimality Gap: N/A")
        print("-" * 40)

        return closed_path, global_best_distance, duration, convergence_history


if __name__ == "__main__":
    scenarios = [5, 6, 7]
    output_dir = get_results_dir("ga")
    print(f"Running Genetic Algorithm for scenarios: {scenarios}\n")

    for n in scenarios:
        try:
            ga = GeneticAlgorithmTSP(num_cities=n, pop_size=100,
                                     mutation_rate=0.01, generations=500, seed=2026)
            best_route, best_cost, duration, convergence = ga.run()

            optimal_cost = ga.optimal_cost
            gap = ((best_cost - optimal_cost) / optimal_cost * 100
                   if optimal_cost > 0 else None)

            result_data = {
                "algorithm": "Genetic Algorithm",
                "num_cities": n,
                "best_tour": best_route,
                "best_cost": float(best_cost),
                "optimal_cost": float(optimal_cost),
                "optimality_gap_percent": round(gap, 4) if gap is not None else None,
                "duration_sec": round(duration, 6),
                "run_params": {
                    "pop_size": ga.pop_size,
                    "mutation_rate": ga.mutation_rate,
                    "generations": ga.generations
                },
                "convergence_history": [round(v, 4) for v in convergence]
            }

            output_file = output_dir / f"tsp_n{n}_ga_solution.json"
            # Saved to: data/results/classical/ga/
            with open(output_file, "w") as f:
                json.dump(result_data, f, indent=4)
            print(f" [SAVED] N={n} -> {output_file.name}\n")

        except Exception as e:
            print(f" [ERROR] N={n}: {e}")
            import traceback; traceback.print_exc()
            print("-" * 40)