# TSP QUBO Converter — Documentation

## Overview

This script converts a **Traveling Salesperson Problem (TSP)** into a
**QUBO (Quadratic Unconstrained Binary Optimization)** format, which is the
required input for quantum annealers (e.g., D-Wave) and quantum-inspired solvers.

---

## Background Concepts

### What is TSP?
Given N cities and the distances between them, find the shortest route that
visits every city exactly once and returns to the start.

### What is QUBO?
A mathematical framework where all variables are binary (0 or 1), and the
goal is to minimize an energy function:

```
E = x^T * Q * x
```

where `x` is a vector of binary variables and `Q` is a matrix of coefficients.

---

## How TSP is Converted to QUBO

### Decision Variables
We define `x[i][t]` for every city `i` and time step `t`:

```
x[i][t] = 1  →  city i is visited at position t in the tour
x[i][t] = 0  →  otherwise
```

For N cities this gives **N × N binary variables** in total.

### Energy Function

A valid tour must satisfy two hard constraints, both encoded as penalty terms:

```
E = A · Σ_i  ( Σ_t x[i,t] − 1 )²       ← Constraint 1
  + A · Σ_t  ( Σ_i x[i,t] − 1 )²       ← Constraint 2
  +     Σ_{i,j,t} d[i,j]·x[i,t]·x[j,t+1]   ← Objective
```

| Symbol | Meaning |
|--------|---------|
| `A` | Penalty weight — must dominate the distance term so violations are never optimal |
| `d[i,j]` | Distance from city i to city j |
| `t+1` | Taken modulo N to wrap the last leg back to the start |

### Why Penalty Terms Work
Each squared constraint equals **zero only when exactly one variable in its
sum is 1**. Any violation raises the energy, making the solver naturally avoid
infeasible solutions.

### Expanding the Squared Constraints
Taking `( Σ_t x[i,t] − 1 )²` and expanding algebraically (using `x² = x`
since x is binary):

- **Diagonal terms** → `Q[(i,t),(i,t)] -= A` (one per variable)
- **Off-diagonal terms** → `Q[(i,t1),(i,t2)] += 2A` (for each pair in the sum)
- **Constant** → contributes to `offset`

---

## Q Dictionary Format

The QUBO is stored as a sparse dictionary instead of a full matrix:

```
Key:   ((city_u, time_u), (city_v, time_v))
Value: float coefficient
```

- **Diagonal key** `((i,t),(i,t))` → linear (single-variable) term
- **Off-diagonal key** `((i,t),(j,s))` → quadratic (two-variable) term

> **Note on asymmetric distances:** Key order is never swapped because
> `d[i,j] ≠ d[j,i]` in the general case. Each directed edge gets its own key.

---

## Offset

When the squared penalties are expanded, constant `+1` terms appear.
With 2N constraints total:

```
offset = 2 × N × penalty_weight
```

This value does not affect which solution is optimal, but must be added back
when computing the true tour cost:

```
true_energy = (x^T Q x) + offset
```

---

## Penalty Weight Selection

Automatically set to:
```
penalty_weight = max(distance_matrix) × N + 1
```

This guarantees that violating even a single constraint is always more
costly than completing the worst possible valid tour.

---

## File Pipeline

```
tsp_n5.json  ──►  create_tsp_qubo()  ──►  serialize keys  ──►  tsp_n5_qubo.json
```

### Input JSON format
```json
{
    "num_cities": 5,
    "distance_matrix": [
        [0, 2, 9, 10, 5],
        [2, 0, 6,  4, 3],
        ...
    ]
}
```

### Output JSON format
```json
{
    "num_cities": 5,
    "offset": 328.0,
    "qubo": {
        "0,0_0,1": -82.0,
        "0,0_1,0": 164.0,
        ...
    }
}
```

### Key Serialization
JSON cannot store Python tuples as keys, so they are converted to strings:

```
((0, 1), (1, 2))  →  "0,1_1,2"
```

To reconstruct the original tuple from a string key:
```python
parts = key_str.split("_")
u = tuple(map(int, parts[0].split(",")))  # (0, 1)
v = tuple(map(int, parts[1].split(",")))  # (1, 2)
```

---

## Project Directory Structure

```
project_root/
├── data/
│   └── raw/
│       ├── tsp_n5.json          ← input
│       ├── tsp_n5_qubo.json     ← output (auto-generated)
│       └── ...
└── src/
    └── quantum/
        └── tsp_qubo.py          ← this script
```

The script resolves all paths relative to its own location, so the project
can be moved or cloned anywhere without breaking the file paths.

---

## Reference

Lucas, A. (2014). *Ising formulations of many NP problems.*
Frontiers in Physics. DOI: [10.3389/fphy.2014.00005](https://doi.org/10.3389/fphy.2014.00005)
