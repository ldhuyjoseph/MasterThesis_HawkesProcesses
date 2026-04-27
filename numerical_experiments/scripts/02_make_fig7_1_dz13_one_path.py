"""
Generate Fig7.1:
One simulated sample path from the Dassios-Zhao numerical specification.

Output:
    outputs/figures/Fig7_1_dz13_one_path.png
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.hawkes_dz13 import simulate_dz13_path
from src.plotting import save_figure_7_1_one_path_with_theory


def main():
    out_dir = ROOT / "outputs" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    path = simulate_dz13_path(
        horizon=100.0,
        a=0.9,
        delta=1.0,
        beta_x=1.2,
        lambda0=0.9,
        seed=12345,
    )

    save_figure_7_1_one_path_with_theory(
        path=path,
        out_file=str(out_dir / "Fig7_1_dz13_one_path.png"),
    )


if __name__ == "__main__":
    main()
