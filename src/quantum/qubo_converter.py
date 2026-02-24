import numpy as np
import json
import os

def create_tsp_qubo(distance_matrix, penalty_weight=None):
    matrix = np.array(distance_matrix)
    N = len(matrix)
    Q = {}

    if penalty_weight is None:
        penalty_weight = float(np.max(matrix)) * N + 1  # ← Düzeltildi

    # Kısıt 1: Her şehir tam 1 kez
    for i in range(N):
        for t1 in range(N):
            Q[((i, t1), (i, t1))] = Q.get(((i, t1), (i, t1)), 0) - penalty_weight
            for t2 in range(t1 + 1, N):
                Q[((i, t1), (i, t2))] = Q.get(((i, t1), (i, t2)), 0) + 2 * penalty_weight

    # Kısıt 2: Her adımda tam 1 şehir
    for t in range(N):
        for i1 in range(N):
            Q[((i1, t), (i1, t))] = Q.get(((i1, t), (i1, t)), 0) - penalty_weight
            for i2 in range(i1 + 1, N):
                Q[((i1, t), (i2, t))] = Q.get(((i1, t), (i2, t)), 0) + 2 * penalty_weight

    # Amaç: Mesafeyi minimize et — swap YOK
    for i in range(N):
        for j in range(N):
            if i != j:
                for t in range(N):
                    t_next = (t + 1) % N
                    key = ((i, t), (j, t_next))   # ← Düzeltildi
                    Q[key] = Q.get(key, 0) + matrix[i][j]

    offset = 2 * N * penalty_weight
    return Q, offset

def process_files(input_files):
    """Reads JSON files, converts them to QUBO, and saves them."""
    for file_path in input_files:
        if not os.path.exists(file_path):
            print(f"ERROR: File not found -> {file_path}")
            continue

        # 1. Read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        distance_matrix = data["distance_matrix"]
        num_cities = data["num_cities"]
        
        print(f"Processing: {file_path} ({num_cities} Cities)")

        # 2. Calculate the QUBO matrix and offset value
        qubo, offset = create_tsp_qubo(distance_matrix)

        # 3. Convert tuple keys to String (required for JSON format)
        # Ex: ((0, 1), (1, 2)) -> "0,1_1,2"
        stringified_qubo = {}
        for (u, v), weight in qubo.items():
            key_str = f"{u[0]},{u[1]}_{v[0]},{v[1]}"
            stringified_qubo[key_str] = weight

        # 4. Prepare the output data
        output_data = {
            "num_cities": num_cities,
            "offset": offset,
            "qubo": stringified_qubo
        }

        # 5. Save the new file (Ex: tsp_n5_qubo.json)
        output_path = file_path.replace(".json", "_qubo.json")
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=4)
        
        print(f"Successfully saved: {output_path}\n")

# --- EXECUTION SECTION ---
if __name__ == "__main__":
    # Find the directory where the script is running (.../src/quantum)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up two levels to reach the project root directory
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    
    # Create the path for the 'data/raw' directory starting from the project root
    data_dir = os.path.join(project_root, "data", "raw")
    
    # The exact files you specifically want to process
    target_files = [
        "tsp_n5.json",
        "tsp_n6.json",
        "tsp_n7.json"
    ]
    
    # Join file names with the directory path
    files_to_process = [os.path.join(data_dir, file) for file in target_files]
    
    # Start the process
    process_files(files_to_process)