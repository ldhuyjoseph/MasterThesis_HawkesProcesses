
# Hawkes Stochastic Processes: Theory and Simulation

This repository contains the full material for my MSc thesis on Hawkes processes, including theoretical development, exact simulation methods, and reproducible numerical experiments.

---

## Overview

Hawkes processes are self-exciting point processes in which past events increase the likelihood of future events. They are widely used to model clustered phenomena in fields such as finance, seismology, and cybersecurity.

This thesis focuses on:

- Theoretical foundations of self-exciting point processes of Hawkes processes  
- Branching (cluster) representation  
- Exact simulation using the Dassios–Zhao (2013) algorithm  
- Monte Carlo validation of theoretical results  

---

## Repository Structure

```text
.
├── thesis_latex/          # Full LaTeX source of the thesis
├── thesis_pdf/            # Final compiled thesis PDF
├── numerical_experiments/      # Reproducible Python code
│   ├── src/        # Core implementation (simulation, plotting, tables)
│   ├── scripts/    # Reproducible experiment scripts
│   └── outputs/    # (ignored) generated figures and tables
├── README.md
└── .gitignore
````

---

## Numerical Experiments

The numerical section reproduces results based on:

**Dassios & Zhao (2013)**
*Exact simulation of Hawkes processes with exponentially decaying intensity*

We implement the exact event-driven simulation scheme and reproduce:

* One simulated sample path of intensity and counting process dynamics
* Monte Carlo comparison with theoretical moments

---

## Model Specification

We consider the Hawkes process:

[
\lambda_t
=========

a + (\lambda_0 - a)e^{-\delta t}

* \sum_{T_i < t} X_i e^{-\delta(t - T_i)}
  ]

with:

[
X_i \sim \mathrm{Exp}(1.2), \quad
(a, \delta; \beta; \lambda_0) = (0.9, 1.0; 1.2; 0.9)
]

---

## Reproducibility

### Install dependencies

```bash
pip install -r numerical/requirements.txt
```

### Run all experiments

```bash
python numerical/scripts/00_run_all_reproducible_outputs.py
```

### Full Monte Carlo replication (100,000 paths)

```bash
python numerical/scripts/03_make_fig7_2_and_table7_1_monte_carlo.py --n-paths 100000
```

---

## Key Outputs

The code reproduces:

* Sample path of ((N_t, \lambda_t))
* Histogram of arrivals
* Theoretical vs simulated expectations
* Monte Carlo validation tables

---

## Author

**Duc Huy Lam**
MSc in Applied Economics (Economic Data Analytics)
University of Padova

---


