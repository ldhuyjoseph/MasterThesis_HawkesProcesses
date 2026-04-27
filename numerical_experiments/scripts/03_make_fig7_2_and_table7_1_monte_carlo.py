"""
Generate Fig7.2 and Table7.1:
Monte Carlo verification of the Dassios-Zhao exact simulation algorithm.

Outputs:
    outputs/figures/Fig7_2_dz13_monte_carlo_comparison.png
    outputs/tables/Table7_1_dz13_monte_carlo.csv
    outputs/tables/Table7_1_dz13_monte_carlo.tex

Full replication:
    python scripts/03_make_fig7_2_and_table7_1_monte_carlo.py --n-paths 100000

Quick test:
    python scripts/03_make_fig7_2_and_table7_1_monte_carlo.py --n-paths 1000
"""

from pathlib import Path
import argparse
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.hawkes_dz13 import theoretical_moments_dz13, monte_carlo_terminal_statistics
from src.plotting import save_figure_7_2_monte_carlo_comparison
from src.tables import build_monte_carlo_table, save_table_outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-paths", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    out_fig = ROOT / "outputs" / "figures"
    out_tab = ROOT / "outputs" / "tables"
    out_fig.mkdir(parents=True, exist_ok=True)
    out_tab.mkdir(parents=True, exist_ok=True)

    times = np.arange(1, 21)

    theory = theoretical_moments_dz13(
        times,
        a=0.9,
        delta=1.0,
        beta_x=1.2,
        lambda0=0.9,
    )

    simulation = monte_carlo_terminal_statistics(
        times,
        n_paths=args.n_paths,
        a=0.9,
        delta=1.0,
        beta_x=1.2,
        lambda0=0.9,
        seed=args.seed,
    )

    save_figure_7_2_monte_carlo_comparison(
        times=times,
        theory=theory,
        simulation=simulation,
        out_file=str(out_fig / "Fig7_2_dz13_monte_carlo_comparison.png"),
    )

    table = build_monte_carlo_table(times, theory, simulation)
    save_table_outputs(
        table,
        csv_file=str(out_tab / "Table7_1_dz13_monte_carlo.csv"),
        latex_file=str(out_tab / "Table7_1_dz13_monte_carlo.tex"),
    )


if __name__ == "__main__":
    main()
