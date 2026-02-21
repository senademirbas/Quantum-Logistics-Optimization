# Kodlama Kuralları ve Konvansiyonlar
<!-- Antigravity kod yazarken bu kurallara uyar -->

## Genel

- **Dil:** Python 3.12
- **Ortam:** `.venv` (proje kökünde)
- **Çalıştırma:** `python src/classical/genetic_algo.py` gibi modül olarak
- **Branch:** `dev` (main'e PR ile birleştirilecek)

## Dosya / Klasör Yapısı

```
src/
├── common/          ← Paylaşılan yardımcı araçlar
│   ├── utils.py           ← load_tsp_data() fonksiyonu
│   ├── tsp_generator.py   ← TSPGenerator sınıfı
│   └── brute_force_solver.py
├── classical/       ← Klasik algoritmalar
│   ├── genetic_algo.py
│   ├── sim_annealing.py
│   └── or_tools_solver.py
└── quantum/         ← Kuantum algoritmalar (Plan A)
    ├── qubo_converter.py    ← BOŞTU
    ├── qaoa_standard.py     ← BOŞTU
    └── hybrid_ga_qaoa.py    ← BOŞTU
```

## Import Kuralı

Her dosyada proje kökünü `sys.path`'e ekle:

```python
from pathlib import Path
import sys
current_file = Path(__file__).resolve()
project_root = current_file.parents[2]  # src/classical → 2 yukarı
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
```

> `src/common/` için `parents[2]` = proje kökü
> `src/classical/` için `parents[2]` = proje kökü

## Veri Yolları

```python
# Doğru — her zaman project_root'u baz al
data_raw = project_root / "data" / "raw"
input_file = data_raw / f"tsp_n{n}.json"

# Yanlış — hard-coded relative path kullanma
```

## JSON Anahtar Standardı (Hedef)

Tüm algoritma çıktıları **snake_case** kullanmalı:

| ✅ Doğru | ❌ Yanlış |
|---------|---------|
| `best_tour` | `Best_Path` |
| `best_cost` | `Best_Cost` |
| `duration_sec` | `Duration_Sec` |
| `num_cities` | `Cities_N` |

> SA ve OR-Tools hâlâ PascalCase kullanıyor — düzeltilmesi gerekiyor.

## Sınıf Yapısı

Her algoritma için standart yapı:

```python
class AlgorithmNameTSP:
    def __init__(self, num_cities, ...params):
        # Veriyi yükle, parametreleri ayarla
        pass
    
    def run(self) -> tuple:
        # Algoritmayı çalıştır
        # return: (best_route, best_cost, duration)
        pass

if __name__ == "__main__":
    # Standalone çalıştırma — senaryoları döngüyle çalıştır
    scenarios = [5, 6, 7]
    for n in scenarios:
        ...
```

## Performans Ölçümü

```python
import time
start_time = time.time()
# ... algoritma ...
duration = time.time() - start_time  # saniye cinsinden float
```

- Milisaniye hassasiyeti yeterli (float saniye kullan)
- Her `__main__` bloğu sonuçları JSON'a kaydetmeli

## Bağımlılıklar

| Paket | Versiyon | Kullanım |
|-------|---------|---------|
| `numpy` | 2.4.2 | Matris işlemleri |
| `pandas` | 3.0.1 | (Henüz kullanılmıyor) |
| `ortools` | 9.9.3963 | OR-Tools çözücü |
| `qiskit` | 2.3.0 | Kuantum devre |
| `qiskit-aer` | 0.17.2 | Simülasyon backend |
| `qiskit-algorithms` | 0.4.0 | QAOA, SPSA, COBYLA |
| `qiskit-optimization` | 0.7.0 | QUBO dönüşümü |
| `scipy` | 1.17.0 | ANOVA analizi |
| `matplotlib` | 3.10.8 | Grafikler |
| `seaborn` | 0.13.2 | Box plot |
