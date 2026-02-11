import random
import sys
import time
import json
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]

if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.common.utils import load_tsp_data


class GeneticAlgorithmTSP:
    """Class to solve TSP using a Genetic Algorithm."""

    def __init__(self, num_cities, pop_size=100, mutation_rate=0.01, generations=500):
        self.num_cities = num_cities
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        
        # Veriyi yükle
        self.distance_matrix, _, self.optimal_cost = load_tsp_data(num_cities)

        # --- HATA DÜZELTME: Optimal Cost 0 ise Solution dosyasından oku ---
        if self.optimal_cost == 0:
            try:
                # data/raw klasörüne git
                solution_path = project_root / "data" / "raw" / f"tsp_n{num_cities}_solution.json"
                if solution_path.exists():
                    with open(solution_path, 'r') as f:
                        sol_data = json.load(f)
                        self.optimal_cost = sol_data.get("optimal_cost", 0.0)
                        print(f"Optimal cost loaded from solution file: {self.optimal_cost}")
            except Exception as e:
                print(f"Warning: Could not load optimal cost from solution file: {e}")
        # ------------------------------------------------------------------

    def calculate_distance(self, route):
        """Calculates the total distance of the given route."""
        distance = 0
        for i in range(len(route) - 1):
            u, v = route[i], route[i + 1]
            distance += self.distance_matrix[u][v]

        distance += self.distance_matrix[route[-1]][route[0]]  # Return to start
        return distance

    def create_population(self):
        """Creates the initial population of random routes."""
        population = []
        base_route = list(range(self.num_cities))
        for _ in range(self.pop_size):
            route = random.sample(base_route, self.num_cities)
            population.append(route)
        return population

    def selection(self, population, distances):
        """Selects a parent route using tournament selection."""
        tournament_size = 5
        candidates_indices = random.sample(range(len(population)), tournament_size)
        best_idx = candidates_indices[0]
        for idx in candidates_indices:
            if distances[idx] < distances[best_idx]:
                best_idx = idx
        return population[best_idx]

    def crossover(self, parent1, parent2):
        """Performs ordered crossover between two parent routes."""
        size = self.num_cities
        start, end = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[start:end] = parent1[start:end]

        pointer = 0
        for city in parent2:
            if city not in child:
                while pointer < size and child[pointer] != -1:
                    pointer += 1
                if pointer < size:
                    child[pointer] = city
        return child

    def mutate(self, route):
        """Mutates a route by swapping two cities with a certain probability."""
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.num_cities), 2)
            route[i], route[j] = route[j], route[i]
        return route

    def run(self):
        """Runs the genetic algorithm to solve the TSP."""
        print(f"Starting Genetic Algorithm for TSP (N={self.num_cities})")

        start_time = time.time()
        population = self.create_population()
        global_best_distance = float("inf")
        global_best_route = []

        for gen in range(self.generations):
            distances = [self.calculate_distance(ind) for ind in population]

            min_dist = min(distances)
            if min_dist < global_best_distance:
                global_best_distance = min_dist
                bes_idx_in_pop = distances.index(min_dist)
                global_best_route = population[bes_idx_in_pop]

            new_population = []

            bes_idx = distances.index(min_dist)
            new_population.append(population[bes_idx])

            while len(new_population) < self.pop_size:
                parent1 = self.selection(population, distances)
                parent2 = self.selection(population, distances)

                child = self.crossover(parent1, parent2)
                child = self.mutate(child)

                new_population.append(child)

            population = new_population

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Genetic Algorithm completed in {elapsed_time:.4f} seconds")
        print(f"Best distance found: {global_best_distance:.4f}")
        print(f"Known optimal distance: {self.optimal_cost:.4f}")

        # --- HATA DÜZELTME: Sıfıra bölme hatasını engelle ---
        if self.optimal_cost > 0:
            gap = ((global_best_distance - self.optimal_cost) / self.optimal_cost) * 100
            print(f"   -> Optimality gap: %{gap:.2f}")
        else:
            gap = 0.0
            print("   -> Optimality gap: N/A (Optimal cost not found)")
        # ---------------------------------------------------

        # --- Rotayı 0 ile kapatma ---
        closed_path = [int(city) for city in global_best_route]
        if closed_path:
            closed_path.append(closed_path[0])
        # ---------------------------

        # --- SAVE RESULTS TO JSON ---
        result_data = {
            "num_cities": self.num_cities,
            "generations": self.generations,
            "pop_size": self.pop_size,
            "mutation_rate": self.mutation_rate,
            "execution_time": elapsed_time,
            "best_distance": float(global_best_distance),
            "optimal_distance": float(self.optimal_cost),
            "optimality_gap_percent": gap,
            "best_route": closed_path
        }

        output_dir = project_root / "data" / "raw"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"tsp_n{self.num_cities}_ga_solution.json"

        try:
            with open(output_file, "w") as f:
                json.dump(result_data, f, indent=4)
            print(f"Results saved to separate file: {output_file.name}")
        except Exception as e:
            print(f"Error saving results to JSON: {e}")
        print("-" * 40)


if __name__ == "__main__":
    """Example usage of the GeneticAlgorithmTSP class."""
    
    scenarios = [5, 6, 7]
    print(f"Running Genetic Algorithm for scenarios: {scenarios}\n")

    for n in scenarios:
        try:
            ga = GeneticAlgorithmTSP(num_cities=n, generations=100)
            ga.run()
        except Exception as e:
            print(f"Error running scenario N={n}: {e}")
            print("-" * 40)