# Project Overview
[Türkçe](project_overview.md) | [English]
<!-- This file is read by Antigravity in every session to understand the project -->

## Identity

- **Applicant:** Zeliha Baysan
- **Advisor:** Asst. Prof. Ensar Arif Sağbaş
- **Institution:** Muğla Sıtkı Koçman University
- **Funding:** TÜBİTAK 2209-A

## Project Title

> AI-Powered Quantum-Hybrid Logistics Optimization: Comparative Analysis of QAOA Simulation and Classical Methods

## Problem

**Traveling Salesman Problem (TSP)** — NP-hard, the fundamental problem of logistics optimization.
Number of Cities: **N = 5, 6, 7** (synthetic, random coordinates, Euclidean distance)

## Two-Plan Structure (Go/No-Go)

### Plan A — Quantum-Hybrid (Primary Goal)
> Active if the QAOA prototype at Month 4 is successful → Go decision

| Model | Description | Status |
|-------|-------------|--------|
| **GA-QAOA** | Original hybrid model optimizing β/γ parameters of QAOA using GA | ⬜ Not started |
| **Standard QAOA** | Benchmark model with SPSA or COBYLA optimizer | ⬜ Not started |
| **GA** | Pure Genetic Algorithm | ✅ Completed |
| **SA** | Pure Simulated Annealing | ✅ Completed |

### Plan B — Comprehensive Classical Comparison (Backup)
> Active if the QAOA prototype at Month 4 is unsuccessful → No-Go decision

| Model | Description | Status |
|-------|-------------|--------|
| **GA** | Genetic Algorithm (requires hyper-parameter optimization) | ✅ Basic Completed |
| **SA** | Simulated Annealing (requires hyper-parameter optimization) | ✅ Basic Completed |
| **OR-Tools** | Google OR-Tools — industry standard, deterministic | ✅ Completed |

> ⚠️ In Plan B, **hyper-parameter optimization** for GA and SA is expected (as per spec). Current parameters are default/unoptimized.

**Current Status:** Target 1 completed ✅ — Waiting for **Target 2** (QAOA prototype) for the Go/No-Go decision.

## Timeline

| Period | Phase | Content |
|--------|-------|---------|
| Months 1-3 | Parallel Development | Classical: GA + SA coding / Quantum: QUBO + QAOA prototype |
| **End of Month 3 – First half of Month 4** | **Go/No-Go Decision** | QAOA prototype evaluation → Plan A or B? |
| Months 5-8 | Algorithmic Development | Plan A: GA-QAOA + Standard QAOA / Plan B: OR-Tools + hyper-param |
| Months 9-10 | Data Collection | All models × TSP sets × 30 independent runs |
| Months 11-12 | Analysis & Reporting | ANOVA, box plots, convergence graphs, final report |

## Research Questions & Hypotheses

**H1 (Plan A):** GA's global search capability optimizes QAOA's β/γ parameters more efficiently than SPSA/COBYLA → GA-QAOA produces higher quality and lower variance results than Standard QAOA.

**H2 (Plan B):** GA finds better solutions than SA due to population-based search; OR-Tools is fast due to being deterministic, but GA remains competitive for small N (5-7).

## Performance Metrics

| Metric | Measurement |
|--------|-------------|
| Solution Quality | Optimality Gap % = `(found - optimal) / optimal * 100` |
| Solution Stability | **Variance** of 30 independent runs |
| Computation Time | In seconds with float, millisecond precision |

- combination of Each algorithm × problem size: **30 independent runs**
- Optimal reference: **Brute Force** (applicable for N=5,6,7)

## Analysis Methods

- **ANOVA** (One-Way Analysis of Variance) — `scipy.stats.f_oneway`
- **Box plots** — performance distribution / stability
- **Convergence plots** — best_cost change per generation/iteration

## Keywords

Quantum Computing, QAOA, QUBO, Hybrid Optimization, Genetic Algorithm, Simulated Annealing, Traveling Salesman Problem, OR-Tools, NISQ

## Literature References (Mentioned in Spec)

- Lucas (2014) — TSP → QUBO formulation
- Salehi, Glos, and Miszczak (2022) — QUBO transformation
- Blekos et al. (2024) — QAOA parameter optimization, NISQ
- Preskill (2018) — NISQ era
- Lo and Shih (2021) — GA strong global search
- Pihkakoski et al. (2025) — practical value of hybrid quantum-classical
- Padmasola et al. (2024) — hybrid workflows
- Fitzek et al. (2024) — QAOA for vehicle routing
