import json
import os
from pathlib import Path
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler

class QuantumTSPSolver:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        # Klasör yoksa oluştur
        os.makedirs(self.output_dir, exist_ok=True)
        
        # En hafif konfigürasyon (Bilgisayarı yormamak için)
        # Sampler: Yerel simülatör
        # COBYLA: Hızlı ve hafif klasik optimizasyon algoritması
        # reps=1: Kuantum devresinin derinliğini minimumda tutar
        self.sampler = StatevectorSampler()
        self.optimizer = COBYLA(maxiter=30) 
        self.qaoa = QAOA(sampler=self.sampler, optimizer=self.optimizer, reps=1)
        self.optimizer_algo = MinimumEigenOptimizer(self.qaoa)

    def solve(self, file_path):
        if not os.path.exists(file_path):
            print(f"HATA: Dosya bulunamadı -> {file_path}")
            return

        print(f"\n--- {os.path.basename(file_path)} İşleniyor ---")
        
        # 1. QUBO verisini JSON'dan oku
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        num_cities = data["num_cities"]
        qubo_dict_str = data["qubo"]
        offset = data["offset"]

        required_qubits = num_cities ** 2
        print(f"Şehir Sayısı: {num_cities} | Gereken Qubit Sayısı: {required_qubits}")
        
        if num_cities > 5:
            print("UYARI: 25'ten fazla qubit yerel bilgisayarlarda yüksek RAM tüketimi nedeniyle programın çökmesine (MemoryError) sebep olabilir!")

        # 2. Qiskit Quadratic Program'ı oluştur
        qp = QuadraticProgram()
        
        # Değişkenleri ekle (x_sehir_adim)
        for i in range(num_cities):
            for t in range(num_cities):
                qp.binary_var(f"x_{i}_{t}")

        linear = {}
        quadratic = {}

        # String anahtarları Qiskit'in anlayacağı formata geri çevir
        for key_str, weight in qubo_dict_str.items():
            u_str, v_str = key_str.split("_")
            i1, t1 = u_str.split(",")
            i2, t2 = v_str.split(",")
            
            var1 = f"x_{i1}_{t1}"
            var2 = f"x_{i2}_{t2}"
            
            if var1 == var2:
                linear[var1] = weight
            else:
                # Çiftleri (Tuple) sıralayarak tekrarı önle
                pair = tuple(sorted([var1, var2]))
                quadratic[pair] = quadratic.get(pair, 0) + weight

        # Hedefi minimize et olarak ayarla
        qp.minimize(linear=linear, quadratic=quadratic)

        # 3. Modeli Çöz
        try:
            print("Kuantum simülasyonu başlatılıyor. Lütfen bekleyin...")
            result = self.optimizer_algo.solve(qp)
            
            # 4. Sonuçları ayrıştır ve rotayı bul
            route = [-1] * num_cities
            for var, val in zip(qp.variables, result.x):
                if val == 1.0:
                    # var.name formatı: x_i_t
                    parts = var.name.split('_')
                    city = int(parts[1])
                    step = int(parts[2])
                    route[step] = city

            # Gerçek mesafe değerini bulmak için offset'i geri ekliyoruz
            actual_distance = result.fval + offset

            print(f"Bulunan En İyi Rota: {route}")
            print(f"Tahmini Toplam Mesafe: {actual_distance}")

            # 5. Sonuçları JSON olarak kaydet
            self.save_result(num_cities, route, actual_distance, str(result.status))

        except MemoryError:
            print(f"HATA: {num_cities} şehir ({required_qubits} qubit) simülasyonu için sistem belleği (RAM) yetersiz kaldı!")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")

    def save_result(self, num_cities, route, distance, status):
        result_data = {
            "num_cities": num_cities,
            "optimal_route": route,
            "total_distance": distance,
            "status": status
        }
        
        output_file = os.path.join(self.output_dir, f"tsp_n{num_cities}_result.json")
        with open(output_file, 'w') as f:
            json.dump(result_data, f, indent=4)
            
        print(f"Başarılı! Sonuç kaydedildi -> {output_file}")


if __name__ == "__main__":
    # İstediğin kesin çıktı dizini
    target_output_dir = r"C:\Users\zelha\Desktop\Quantum-Logistics-Optimization\data\raw"
    
    # Okunacak QUBO dosyalarının dizini (çıktı ile aynı dizinde olduğunu varsayıyoruz)
    input_dir = target_output_dir
    
    target_files = [
        "tsp_n5_qubo.json",
        "tsp_n6_qubo.json",
        "tsp_n7_qubo.json"
    ]
    
    solver = QuantumTSPSolver(output_dir=target_output_dir)
    
    for file_name in target_files:
        full_path = os.path.join(input_dir, file_name)
        solver.solve(full_path)