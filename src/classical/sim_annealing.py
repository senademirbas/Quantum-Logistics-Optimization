import math
import random
import sys
import time
import copy
import json  # JSON modülü eklendi
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Tuple

# File paths and project root settings
current_file = Path(__file__).resolve()
project_root = current_file.parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# --- Function moved from utils ---
def load_tsp_data(num_cities: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Loads ONLY the TSP distance matrix and coordinates from JSON.
    NO Ground Truth, NO Brute Force dependency.
    """
    # Using the global project_root variable defined above
    data_dir = project_root / "data" / "raw"

    # JSON input file path: tsp_n{n}.json
    json_file = data_dir / f"tsp_n{num_cities}.json"

    if not json_file.exists():
        raise FileNotFoundError(f"TSP data file not found! Run tsp_generator.py first.\nPath: {json_file}")

    try:
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Matrix only
        distance_matrix = np.array(data["distance_matrix"])

        # Coordinates only
        if "coordinates" in data:
            coordinates = np.array(data["coordinates"])
        else:
            coordinates = np.array([])

        # Third parameter (best_cost) is NO LONGER present.
        return distance_matrix, coordinates

    except Exception as e:
        raise Exception(f"Data loading error: {e}")
# -----------------------------------

class SimulatedAnnealingTSP:
    """Class to solve TSP using Standard Simulated Annealing (SA).
    This implementation focuses on the core SA algorithm without any advanced features like reheating or adaptive cooling.  
    """

    def __init__(self, 
                 num_cities: int, 
                 initial_temp: float = 1000.0, 
                 alpha: float = 0.99, 
                 stopping_temp: float = 1e-6):
        
        self.num_cities = num_cities
        self.initial_temp = initial_temp
        self.alpha = alpha
        self.stopping_temp = stopping_temp
        
        # We only retrieve the matrix; reference cost (optimal_cost) is NO LONGER present.
        # Now using the function inside the file which reads JSON
        self.distance_matrix, _ = load_tsp_data(num_cities)

    def calculate_total_distance(self, route: List[int]) -> float:
        """Calculates the total Euclidean distance of a given route."""
        dist = 0.0
        for i in range(len(route) - 1):
            dist += self.distance_matrix[route[i]][route[i + 1]]
        dist += self.distance_matrix[route[-1]][route[0]]
        return dist

    def get_neighbor_2opt(self, route: List[int]) -> List[int]:
        """Generates a neighbor solution using 2-Opt."""
        new_route = route[:]
        i, j = sorted(random.sample(range(self.num_cities), 2))
        new_route[i:j+1] = new_route[i:j+1][::-1]
        return new_route

    def run(self):
        """Executes the Standard SA optimization."""
        print(f"Starting Standard Simulated Annealing (N={self.num_cities})")
        
        start_time = time.time()
        
        current_route = list(range(self.num_cities))
        random.shuffle(current_route)
        current_cost = self.calculate_total_distance(current_route)
        
        best_route = current_route[:]
        best_cost = current_cost
        
        temperature = self.initial_temp
        iter_count = 0

        while temperature > self.stopping_temp:
            iter_count += 1
            
            neighbor_route = self.get_neighbor_2opt(current_route)
            neighbor_cost = self.calculate_total_distance(neighbor_route)

            delta_E = neighbor_cost - current_cost
            acceptance_prob = 1.0
            
            if delta_E > 0:
                try:
                    acceptance_prob = math.exp(-delta_E / temperature)
                except OverflowError:
                    acceptance_prob = 0.0
            
            if random.random() < acceptance_prob:
                current_route = neighbor_route
                current_cost = neighbor_cost
                
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_route = current_route[:]
            
            # Only cooling exists, NO re-heating.
            temperature *= self.alpha

        end_time = time.time()
        duration = end_time - start_time
        
        # Reporting (Only its own found result)
        print(f"   -> Completed in {duration:.4f}s | Iterations: {iter_count}")
        print(f"   -> SA Best Cost: {best_cost:.4f}")
        print("-" * 40)
        
        return best_route, best_cost, duration


if __name__ == "__main__":
    print("Running Standard SA Benchmark (Standalone Mode)...")
    print("=" * 60)
    
    scenarios = [5, 6, 7]
    output_dir = project_root / "data" / "raw"
    
    for n in scenarios:
        try:
            # Now initializing the Standard SA class
            sa_solver = SimulatedAnnealingTSP(num_cities=n)
            best_route, sa_cost, duration = sa_solver.run()
            
            # Output filename changed to JSON
            output_filename = output_dir / f"tsp_n{n}_sa_solution.json"
            
            # --- EKLENEN KISIM: Rotayı 0 ile kapatma ---
            closed_path = [int(city) for city in best_route]
            closed_path.append(closed_path[0])
            # -------------------------------------------

            # Data structure for JSON saving
            # Numpy types must be converted to native Python types (int, float)
            result_data = {
                "Algorithm": "Standard Simulated Annealing",
                "Cities_N": n,
                "Best_Path": closed_path, # closed_path kullanıldı
                "Best_Cost": float(sa_cost),
                "Duration_Sec": duration
            }
            
            # Saving to separate JSON file
            with open(output_filename, "w") as f:
                json.dump(result_data, f, indent=4)

            print(f" [SAVED] Results for N={n} saved to: {output_filename.name}")
            print("=" * 60)
            
        except Exception as e:
            print(f" [ERROR] Failed for N={n}: {e}")