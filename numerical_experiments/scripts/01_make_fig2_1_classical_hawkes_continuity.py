"""
Generate Fig2.1:
Classical exponential Hawkes continuity illustration.

Output:
    outputs/figures/Fig2_1_classical_hawkes_continuity.png
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.plotting import save_figure_2_1_classical_hawkes_continuity


def main():
    out_dir = ROOT / "outputs" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    save_figure_2_1_classical_hawkes_continuity(
        out_file=str(out_dir / "Fig2_1_classical_hawkes_continuity.png")
    )


if __name__ == "__main__":
    main()
