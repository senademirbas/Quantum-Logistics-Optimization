import json
import numpy as np
from pathlib import Path


def _project_root() -> Path:
    """Returns the absolute project root directory."""
    return Path(__file__).resolve().parents[2]


# ── Data directory helpers ─────────────────────────────────────────────────

def get_raw_dir() -> Path:
    """data/raw/ — TSP problem instances (generator output, read-only)."""
    return _project_root() / "data" / "raw"


def get_ground_truth_dir() -> Path:
    """data/ground_truth/ — Brute Force optimal solutions (reference)."""
    return _project_root() / "data" / "ground_truth"


def get_results_dir(algorithm: str) -> Path:
    """data/results/classical/{algorithm}/ — Algorithm output directory.

    Args:
        algorithm: 'ga', 'sa', or 'ortools'

    Returns:
        Path to the results directory (created if missing).
    """
    path = _project_root() / "data" / "results" / "classical" / algorithm
    path.mkdir(parents=True, exist_ok=True)
    return path


# ── Data loading helpers ───────────────────────────────────────────────────

def load_tsp_data(num_cities: int):
    """Load TSP distance matrix and coordinates from data/raw/.

    Returns:
        distance_matrix (np.ndarray): NxN distance matrix
        coordinates     (np.ndarray): Nx2 coordinate array
        best_cost       (float):      0.0 (legacy field, unused)
    """
    file_path = get_raw_dir() / f"tsp_n{num_cities}.json"

    if not file_path.exists():
        raise FileNotFoundError(
            f"TSP data file for {num_cities} cities not found at {file_path}"
        )

    with open(file_path, "r") as f:
        tsp_data = json.load(f)

    distance_matrix = np.array(tsp_data["distance_matrix"])
    coordinates = np.array(tsp_data["coordinates"])

    print(f"Loaded TSP data for {num_cities} cities from {file_path}")
    return distance_matrix, coordinates, 0.0


def load_optimal_cost(num_cities: int) -> float:
    """Load the known optimal cost from data/ground_truth/.

    Used by GA, SA, and OR-Tools to calculate optimality_gap_percent.

    Returns:
        float: optimal_cost, or 0.0 if solution file not found.
    """
    solution_path = get_ground_truth_dir() / f"tsp_n{num_cities}_solution.json"

    if not solution_path.exists():
        print(f"  [WARN] Ground truth not found: {solution_path.name}")
        return 0.0

    with open(solution_path, "r") as f:
        sol_data = json.load(f)

    return float(sol_data.get("optimal_cost", 0.0))