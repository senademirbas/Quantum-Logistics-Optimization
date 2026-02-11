# Quantum-Logistics-Optimization

# ⚛️ AI-Enhanced Quantum-Hybrid Logistics Optimization

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![Qiskit](https://img.shields.io/badge/Quantum-Qiskit-purple?style=flat&logo=qiskit)
![Optimization](https://img.shields.io/badge/Optimization-OR--Tools-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active_Development-orange)

## Overview

This project aims to develop an innovative solution approach for the **Traveling Salesman Problem (TSP)**, a fundamental NP-hard problem in the logistics sector.

By bridging the gap between **Quantum Computing** and **Artificial Intelligence**, we propose a hybrid model that utilizes **Genetic Algorithms (GA)** to optimize the parameters ($\beta$ and $\gamma$) of the **Quantum Approximate Optimization Algorithm (QAOA)**. This approach is designed to overcome the limitations of the NISQ (Noisy Intermediate-Scale Quantum) era.

### Key Objectives

1.  **Hybrid Innovation:** Develop a **GA-QAOA** model where the Genetic Algorithm acts as a global optimizer for the quantum circuit parameters.
2.  **Comprehensive Benchmarking:** Compare the hybrid model against:
    - **Standard QAOA** (using classical optimizers like COBYLA/SPSA).
    - **Classical Meta-heuristics:** Genetic Algorithm (GA) and Simulated Annealing (SA).
    - **Industry Standard:** Google OR-Tools.
3.  **Scientific Analysis:** Conduct statistical analysis (ANOVA) on solution quality and runtime for TSP instances of N=5, 6, and 7 cities.

---

## Project Structure

The project is organized to support reproducibility and clear separation of concerns:

````text
Quantum-Logistics-Optimization/
│
├── README.md               # Project overview and instructions
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore rules
├── requirements.txt        # Dependencies (Qiskit, Numpy, Pandas, etc.)
│
├── data/                   # Data Management
│   ├── tsp_n5.json         # Input Coordinates + Ground Truth (Exact Solution)
│   ├── tsp_n6.json
│   └── tsp_n7.json
│
├── src/                    # Source Code
│   ├── __init__.py
│   ├── common/             # Shared Utilities
│   │   ├── tsp_generator.py    # Generates Data & Calculates Ground Truth
│   │   ├── brute_force_solver.py # Exact solver for small N (Ground Truth)
│   │   └── utils.py            # Data loading & Helper functions
│   │
│   ├── classical/          # Classical Methods (Plan B & Benchmarks)
│   │   ├── genetic_algo.py     # Pure Genetic Algorithm implementation
│   │   ├── sim_annealing.py    # Simulated Annealing implementation
│   │
│   └── quantum/            # Quantum Methods (Plan A)
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

````

##  Installation
To set up the project locally, follow these steps:

### 1. Clone the Repository

```bash

git clone [https://github.com/senademirbas/Quantum-Logistics-Optimization.git](https://github.com/senademirbas/Quantum-Logistics-Optimization.git)
cd Quantum-Logistics-Optimization

````

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Generating Data

Before running any algorithms, generate the synthetic TSP maps to ensure all models compete on the exact same graph (using a fixed seed for reproducibility).

```bash
python src/common/tsp_generator.py
```

This will create CSV files in data/raw/ for N=5, 6, and 7 cities.

### 2. Running Classical Benchmarks

To test the classical Genetic Algorithm or Simulated Annealing:

```bash
python src/classical/genetic_algo.py
# or
python src/classical/sim_annealing.py
```

### 3. Running Quantum Simulation

To run the hybrid QAOA model:

```bash
python src/quantum/hybrid_ga_qaoa.py
```

## Methodology

The project follows a two-phase research plan:

Plan A (Quantum-Hybrid): Focuses on converting TSP to QUBO (Quadratic Unconstrained Binary Optimization) and solving it using QAOA. The novelty lies in replacing standard classical optimizers with a population-based Genetic Algorithm to navigate the quantum landscape more effectively.

Plan B (Classical Pivot): Serves as a risk management strategy and a rigorous benchmark baseline, utilizing optimized GA, SA, and exact solvers (OR-Tools).

## Team

Researchers:

- Zeliha Baysan
- Şehri Sena Demirbaş
- Yaren Kaya

Advisor:

- Asst. Prof. Dr. Ensar Arif Sağbaş - Muğla Sıtkı Koçman University
