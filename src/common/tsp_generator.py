import numpy as np
from pathlib import Path
import json


class TSPGenerator:
    """Class to generate and save TSP instances with random coordinates."""

    def __init__(self, num_cities, seed=2026):
        self.num_cities = num_cities
        self.seed = seed
        np.random.seed(self.seed)
        self.coordinates = []
        self.distance_matrix = []

    def generate_data(self):
        """Generates random coordinates between 0-100 and computes the distance matrix."""

        self.coordinates = np.random.randint(0, 101, size=(self.num_cities, 2))
        return self.coordinates

    def calculate_distance_matrix(self):
        """Calculates the Euclidean distance matrix from the coordinates."""

        if len(self.coordinates) == 0:
            self.generate_data()

        matrix = np.zeros((self.num_cities, self.num_cities))

        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    # euclidian distance = sqrt((x2-x1)^2 + (y2-y1)^2)
                    dist = np.linalg.norm(self.coordinates[i] - self.coordinates[j])
                    matrix[i][j] = dist
                else:
                    matrix[i][j] = 0.0

        self.distance_matrix = matrix
        return matrix

    def save_to_json(self):
        """Saves TSP instance (coordinates + distance matrix) to data/raw/ as JSON."""

        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent

        output_dir = project_root / "data" / "raw"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Standardized filename to tsp_n{n}.json format
        json_file = output_dir / f"tsp_n{self.num_cities}.json"
        
        data_to_save = {
            "num_cities": self.num_cities,
            "coordinates": self.coordinates.tolist(),
            "distance_matrix": self.distance_matrix.tolist()
        }

        with open(json_file, 'w') as f:
            json.dump(data_to_save, f, indent=4)

        print(f"Instance saved to {json_file}")


if __name__ == "__main__":
    """Example usage of TSPGenerator."""

    scenarios = [5, 6, 7]

    print("Generating TSP instances...")
    for n in scenarios:
        """Generate TSP instance with n cities."""
        tsp_gen = TSPGenerator(num_cities=n, seed=2026)
        tsp_gen.generate_data()
        tsp_gen.calculate_distance_matrix()
        tsp_gen.save_to_json()

    print(f"TSP instances with {scenarios} cities generated and saved.")