import numpy as np
import pandas as pd
from pathlib import Path


class TSPGenerator:
    """Class to generate and save TSP instances with random coordinates."""

    def __init__(self, num_cities, seed=42):
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

    def save_to_csv(self):
        """Saves the coordinates and distance matrix to CSV files."""

        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent

        output_dir = project_root / "data" / "raw"

        output_dir.mkdir(parents=True, exist_ok=True)

        coords_file = output_dir / f"tsp_{self.num_cities}_coords.csv"
        pd.DataFrame(self.coordinates, columns=["x", "y"]).to_csv(
            coords_file, index=False
        )

        dist_file = output_dir / f"tsp_{self.num_cities}_distance_matrix.csv"
        pd.DataFrame(self.distance_matrix).to_csv(dist_file, index=False)

        print(f"Coordinates N={self.num_cities} saved to {output_dir}")


if __name__ == "__main__":
    """Example usage of TSPGenerator."""

    scenarios = [5, 6, 7]

    print("Generating TSP instances...")
    for n in scenarios:
        """Generate TSP instance with n cities."""
        tsp_gen = TSPGenerator(num_cities=n, seed=2026)
        tsp_gen.generate_data()
        tsp_gen.calculate_distance_matrix()
        tsp_gen.save_to_csv()

    print(f"TSP instance with {scenarios} cities generated and saved.")
