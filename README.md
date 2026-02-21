# Quantum-Logistics-Optimization

# AI-Enhanced Quantum-Hybrid Logistics Optimization

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![Qiskit](https://img.shields.io/badge/Quantum-Qiskit-purple?style=flat&logo=qiskit)
![Optimization](https://img.shields.io/badge/Optimization-OR--Tools-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active_Development-orange)

> **TÜBİTAK 2209-A University Students Research Projects Support Program**  
> Muğla Sıtkı Koçman University  
> **Advisor:** Asst. Prof. Dr. Ensar Arif Sağbaş

---

## Overview

This project focuses on developing an innovative solution for the **Traveling Salesman Problem (TSP)**, a fundamental NP-hard challenge in logistics. 

The core contribution is a hybrid model that optimizes the parameters ($\beta$ and $\gamma$) of the **Quantum Approximate Optimization Algorithm (QAOA)** using a **Genetic Algorithm (GA)**. This approach aims to enhance the performance of quantum circuits in the NISQ (Noisy Intermediate-Scale Quantum) era.

### Key Objectives

1.  **Hybrid Innovation:** Implement a **GA-QAOA** model where the Genetic Algorithm serves as a global optimizer for quantum circuit parameters.
2.  **Comparative Benchmarking:** Evaluate the hybrid model against:
    - **Standard QAOA** (using classical optimizers such as SPSA/COBYLA).
    - **Classical Meta-heuristics:** Genetic Algorithm (GA) and Simulated Annealing (SA).
    - **Industry Standard:** Google OR-Tools.
3.  **Statistical Rigor:** Perform ANOVA tests and visual analysis on TSP instances of size N=5, 6, and 7 to validate performance stability and quality.

---

## Project Structure

The repository is organized into distinct modules for data management, classical solvers, and quantum simulation:

```text
Quantum-Logistics-Optimization/
│
├── data/                       # Data Management
│   ├── raw/                    # TSP problem inputs (seed=2026)
│   ├── ground_truth/           # Brute Force optimal reference solutions
│   └── results/                # Algorithm outputs and benchmarks
│
├── src/                        # Source Code
│   ├── common/                 # Utilities and Data Generators
│   │   ├── utils.py            # Path management and data loaders
│   │   ├── tsp_generator.py    # Synthetic TSP data generator
│   │   ├── brute_force_solver.py # Exact solver for ground truth
│   │   └── benchmark_runner.py # Automated 30-run test system
│   │
│   ├── classical/              # Classical Benchmarks
│   │   ├── genetic_algo.py     # GA implementation (OX crossover)
│   │   ├── sim_annealing.py    # SA implementation (2-opt neighbor)
│   │   └── or_tools_solver.py  # OR-Tools implementation
│   │
│   └── quantum/                # Quantum-Hybrid Methods (Plan A)
│       ├── qubo_converter.py   # TSP to QUBO formulation
│       ├── qaoa_standard.py    # Standard QAOA implementation
│       └── hybrid_ga_qaoa.py   # NOVELTY: GA-QAOA Hybrid Model
│
├── notebooks/              # Jupyter Notebooks (Experiments)
│   ├── 01_data_generation.ipynb    # Demo: Data generation
│   ├── 02_classical_benchmark.ipynb # Experiments: GA, SA
│   └── 04_result_analysis.ipynb    # Analysis: ANOVA & Plots
│
└── reports/                # Documentation & Outputs
    ├── figures/            # Box plots and convergence curves
    └── final_report/       # final report drafts
├── .agent/memory/              # Project memory bank (Bilingual support)
├── requirements.txt            # Project dependencies
└── README.md                   # Project overview
```

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/senademirbas/Quantum-Logistics-Optimization.git
cd Quantum-Logistics-Optimization
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

### Phase 1: Data Generation
Generate synthetic TSP coordinates and calculate the exact optimal costs (Ground Truth):
```bash
python src/common/tsp_generator.py
python src/common/brute_force_solver.py
```

### Phase 2: Classical Benchmarks
Run the classical heuristic and exact solvers:
```bash
python src/classical/genetic_algo.py
python src/classical/sim_annealing.py
python src/classical/or_tools_solver.py
```

### Phase 3: Automated Benchmarking (30 Runs)
Execute the benchmark runner to perform 30 independent tests for statistical validity (Target 4):
```bash
python src/common/benchmark_runner.py
```

---

## Methodology

The research is structured around a two-phase strategy:

- **Plan A (Quantum-Hybrid):** Our primary research goal. It involves transforming TSP into Quadratic Unconstrained Binary Optimization (QUBO) form and solving it via QAOA. The novelty lies in using a population-based Genetic Algorithm to optimize quantum parameters, potentially avoiding local minima common in standard optimizers.
- **Plan B (Classical Pivot):** A robust baseline strategy utilizing optimized meta-heuristics and industry-standard exact solvers.

---

## Team

**Researchers:**
- Zeliha Baysan
- Şehri Sena Demirbaş
- Yaren Kaya

**Advisor:**
- Asst. Prof. Dr. Ensar Arif Sağbaş — Muğla Sıtkı Koçman University

---

## Key References

- Blekos et al. (2024) — Review on QAOA parameters and NISQ limitations.
- Lucas (2014) — QUBO formulations of various NP problems.
- Preskill (2018) — Quantum Computing in the NISQ era and beyond.
- Pihkakoski et al. (2025) — Hybrid quantum-classical computing workflows.
- Lo & Shih (2021) — Genetic Algorithms for complex optimization.
