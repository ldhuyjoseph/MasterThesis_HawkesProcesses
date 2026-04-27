# Reproducible Python Code for Hawkes Thesis Numerical Results

This folder reproduces the numerical outputs used in the thesis:

**Hawkes Stochastic Processes: Theory and Simulation** by Duc Huy Lam

It returns:

- `Fig2_1_classical_hawkes_continuity.png`
- `Fig7_1_dz13_one_path.png`
- `Fig7_2_dz13_monte_carlo_comparison.png`
- `Table7_1_dz13_monte_carlo.csv`
- `Table7_1_dz13_monte_carlo.tex`

## Folder structure

```text
hawkes_reproducible_python/
├── src/
│   ├── hawkes_dz13.py
│   ├── plotting.py
│   └── tables.py
├── scripts/
│   ├── 00_run_all_reproducible_outputs.py
│   ├── 01_make_fig2_1_classical_hawkes_continuity.py
│   ├── 02_make_fig7_1_dz13_one_path.py
│   └── 03_make_fig7_2_and_table7_1_monte_carlo.py
├── outputs/
│   ├── figures/
│   └── tables/
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Run everything

```bash
python scripts/00_run_all_reproducible_outputs.py
```

The default `run_all` script uses `10000` Monte Carlo paths for speed.

## Full Monte Carlo replication

To reproduce the thesis-level Monte Carlo output using `100000` paths:

```bash
python scripts/03_make_fig7_2_and_table7_1_monte_carlo.py --n-paths 100000
```

## Individual scripts

```bash
python scripts/01_make_fig2_1_classical_hawkes_continuity.py
python scripts/02_make_fig7_1_dz13_one_path.py
python scripts/03_make_fig7_2_and_table7_1_monte_carlo.py --n-paths 100000
```

