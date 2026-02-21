# Kodlama Kuralları ve Konvansiyonlar
[Türkçe] | [English](conventions_en.md)
<!-- Antigravity kod yazarken bu kurallara uyar — Son güncelleme: 2026-02-21 -->

## Genel

- **Dil:** Python 3.12
- **Ortam:** `.venv` (proje kökünde) — `python -m venv .venv`
- **Çalıştırma:** `.\.venv\Scripts\python.exe src/classical/genetic_algo.py`
- **Branch:** `dev` (main'e PR ile birleştirilecek)

---

## Proje Yapısı

```
Quantum-Logistics-Optimization/
├── data/
│   ├── raw/                     ← TSP girdileri (tsp_generator çıktısı)
│   ├── ground_truth/            ← Brute force referans çözümler
│   └── results/
│       ├── classical/ga/        ← GA çıktıları
│       ├── classical/sa/        ← SA çıktıları
│       ├── classical/ortools/   ← OR-Tools çıktıları
│       └── quantum/             ← Plan A (gelecekte)
├── src/
│   ├── common/
│   │   ├── utils.py             ← Path yardımcıları + veri yükleme
│   │   ├── tsp_generator.py     ← TSP problem üreteci
│   │   └── brute_force_solver.py ← Ground truth üreteci
│   ├── classical/
│   │   ├── genetic_algo.py      ← GA (tamamlandı ✅)
│   │   ├── sim_annealing.py     ← SA (tamamlandı ✅)
│   │   └── or_tools_solver.py   ← OR-Tools (tamamlandı ✅)
│   └── quantum/                 ← Plan A (beklemede)
│       ├── qubo_converter.py    ← BOŞTU
│       ├── qaoa_standard.py     ← BOŞTU
│       └── hybrid_ga_qaoa.py    ← BOŞTU
└── .agent/memory/               ← Proje belleği (bu klasör)
```

---

## Path Yardımcıları (`utils.py`)

Dosya yolunu asla hard-code etme — hep `utils.py` fonksiyonlarını kullan:

```python
from src.common.utils import get_raw_dir, get_ground_truth_dir, get_results_dir

raw_dir      = get_raw_dir()                   # data/raw/
gt_dir       = get_ground_truth_dir()          # data/ground_truth/
ga_out_dir   = get_results_dir("ga")           # data/results/classical/ga/
sa_out_dir   = get_results_dir("sa")           # data/results/classical/sa/
ort_out_dir  = get_results_dir("ortools")      # data/results/classical/ortools/
```

---

## Import Kuralı

Her `src/classical/` ya da `src/common/` dosyasında:

```python
from pathlib import Path
import sys
current_file = Path(__file__).resolve()
project_root = current_file.parents[2]  # her zaman 2 yukarı = proje kökü
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
```

---

## JSON Anahtar Standardı

Tüm algoritma çıktıları **snake_case** kullanır — **zorunlu:**

| ✅ Kullan | ❌ Kullanma |
|----------|------------|
| `algorithm` | `Algorithm` |
| `best_tour` | `Best_Path` |
| `best_cost` | `Best_Cost` |
| `duration_sec` | `Duration_Sec` |
| `num_cities` | `Cities_N` |
| `run_params` | `parameters` |
| `convergence_history` | `history` |

---

## Sınıf Yapısı

```python
class AlgorithmNameTSP:
    def __init__(self, num_cities, ...params):
        self.distance_matrix, _, _ = load_tsp_data(num_cities)
        self.optimal_cost = load_optimal_cost(num_cities)

    def run(self) -> tuple:
        # return: (best_tour, best_cost, duration_sec, convergence_history)
        pass

if __name__ == "__main__":
    scenarios = [5, 6, 7]
    output_dir = get_results_dir("algo_name")
    for n in scenarios:
        ...
        with open(output_dir / f"tsp_n{n}_algo_solution.json", "w") as f:
            json.dump(result_data, f, indent=4)
```

---

## Performans Ölçümü

```python
import time
start_time = time.time()
# ... algoritma ...
duration = time.time() - start_time  # saniye (float)
```

- `duration_sec` → `round(duration, 6)` ile JSON'a yazılır
- `convergence_history` → `[round(v, 4) for v in history]`

---

## Bağımlılıklar (`requirements.txt`)

| Paket | Versiyon | Kullanım |
|-------|---------|----------|
| `numpy` | 2.4.2 | Matris işlemleri |
| `pandas` | 3.0.1 | (Henüz kullanılmıyor) |
| `ortools` | 9.11.4210 | OR-Tools çözücü (**9.11** — Python 3.12 uyumlu) |
| `qiskit` | 2.3.0 | Kuantum devre (Plan A) |
| `qiskit-aer` | 0.17.2 | Simülasyon backend (Plan A) |
| `qiskit-algorithms` | 0.4.0 | QAOA, SPSA, COBYLA (Plan A) |
| `qiskit-optimization` | 0.7.0 | QUBO dönüşümü (Plan A) |
| `scipy` | 1.17.0 | ANOVA analizi |
| `matplotlib` | 3.10.8 | Grafikler |
| `seaborn` | 0.13.2 | Box plot |

> ⚠️ `ortools` 9.11.4210 (9.9.x değil — Python 3.12'de DLL hatası verir).
