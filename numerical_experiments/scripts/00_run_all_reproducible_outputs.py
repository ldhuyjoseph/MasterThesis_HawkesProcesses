"""
Run all reproducible scripts.

By default, this uses 10000 Monte Carlo paths to keep runtime reasonable.
For the thesis-level replication, run script 03 directly with --n-paths 100000.
"""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(command):
    print("Running:", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main():
    run([sys.executable, "scripts/01_make_fig2_1_classical_hawkes_continuity.py"])
    run([sys.executable, "scripts/02_make_fig7_1_dz13_one_path.py"])
    run([
        sys.executable,
        "scripts/03_make_fig7_2_and_table7_1_monte_carlo.py",
        "--n-paths",
        "10000",
    ])


if __name__ == "__main__":
    main()
