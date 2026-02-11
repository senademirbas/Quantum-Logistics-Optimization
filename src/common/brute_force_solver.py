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
    """
    Traveling Salesman Problem (TSP) için Brute Force (Kaba Kuvvet) Çözücü.
    Tüm permütasyonları deneyerek en kısa yolu bulur.
    """

    def __init__(self, distance_matrix):
        self.matrix = distance_matrix
        # Şeklin (N, N) olduğundan emin oluyoruz.
        # Eğer matris kare değilse en küçük boyutu alarak hata almayı önleriz.
        self.num_cities = min(distance_matrix.shape)

    def solve(self):
        """
        Optimal rotayı ve minimum maliyeti hesaplar.
        """
        # Şehir listesi: 0, 1, 2, ... N-1
        cities = list(range(self.num_cities))
        
        min_cost = float('inf')
        best_path = []

        # Başlangıç şehri (0) hariç diğerlerinin tüm permütasyonlarını al
        # Complexity: O((N-1)!)
        for perm in itertools.permutations(cities[1:]):
            current_path = [0] + list(perm) + [0]  # 0'dan başla, dolaş, 0'a dön
            
            current_cost = 0
            valid_path = True
            
            for i in range(len(current_path) - 1):
                u, v = current_path[i], current_path[i+1]
                
                # Güvenlik Kontrolü: Eğer indeks matris sınırlarını aşarsa atla
                if u >= self.num_cities or v >= self.num_cities:
                    valid_path = False
                    break
                
                current_cost += self.matrix[u][v]
            
            if valid_path and current_cost < min_cost:
                min_cost = current_cost
                best_path = current_path
                
        return best_path, min_cost


if __name__ == "__main__":
    """
    Ana çalıştırma bloğu.
    1. JSON'dan mesafe matrisini oku.
    2. Brute Force ile çöz.
    3. Sonucu AYRI BİR JSON dosyasına kaydet.
    """

    print("Starting Brute Force Solver for Ground Truth generation...")
    print("-" * 60)

    # Raw data klasörü
    raw_data_dir = project_root / "data" / "raw"
    
    # İşlenecek senaryolar (Şehir sayıları)
    scenarios = [5, 6, 7]

    for n in scenarios:
        # Girdi dosyası: tsp_n5.json
        input_path = raw_data_dir / f"tsp_n{n}.json"
        
        # Çıktı dosyası (AYRI): tsp_n5_solution.json
        output_path = raw_data_dir / f"tsp_n{n}_solution.json"
        
        if input_path.exists():
            print(f" [N={n}] Processing file: {input_path.name}")
            
            try:
                # 1. Mesafe matrisini yükle (JSON formatında)
                with open(input_path, 'r') as f:
                    tsp_data = json.load(f)
                
                # Veriyi numpy dizisine çevir
                matrix = np.array(tsp_data["distance_matrix"])
                
                # DEBUG: Matris boyutunu yazdır
                print(f"    -> [Debug] Matrix Shape: {matrix.shape}")

                # Matris kare değilse uyar
                if matrix.shape[0] != matrix.shape[1]:
                    print("    -> UYARI: Matris kare değil! JSON formatını kontrol edin.")
                
                # 2. Çözücüyü başlat ve çöz
                solver = BruteForceSolver(matrix)
                path, cost = solver.solve()
                
                # 3. Sonuçları AYRI BİR JSON olarak hazırla
                # Numpy tipleri (int64, float64) JSON ile uyumsuz olduğu için dönüştürüyoruz.
                solution_data = {
                    "num_cities": n,
                    "optimal_path": [int(city) for city in path],
                    "optimal_cost": float(cost)
                }
                
                # Dosyayı kaydet
                with open(output_path, 'w') as f:
                    json.dump(solution_data, f, indent=4)
                
                # Başarı mesajı
                print(f"    -> Optimal Path found: {path}")
                print(f"    -> Minimum Cost: {cost:.4f}")
                print(f"    -> SAVED TO NEW FILE: {output_path.name}")
                print("")
                
            except Exception as e:
                print(f"    -> ERROR: Failed to process file.")
                print(f"    -> Reason: {e}")
                import traceback; traceback.print_exc()
        else:
            print(f" [N={n}] WARNING: Input file not found ({input_path.name})")

    print("-" * 60)
    print("All tasks completed.")