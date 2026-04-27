"""Plotting functions for the thesis figures."""

import numpy as np
import matplotlib.pyplot as plt

from .hawkes_dz13 import counting_process, intensity_process, theoretical_moments_dz13


def save_figure_2_1_classical_hawkes_continuity(
    out_file: str,
    eta: float = 0.5,
    alpha: float = 1.0,
    beta: float = 2.0,
) -> None:
    """
    Create Fig2.1-style illustration:
    - top: right-continuous counting process N_t
    - bottom: left-continuous intensity lambda_t
    - open/filled circles indicate one-sided continuity at jump times

    This is an illustrative deterministic event-time figure, not a Monte Carlo experiment.
    """
    event_times = np.array([0.55, 3.60, 7.25, 10.25, 13.35, 14.20, 14.85, 15.70, 16.02, 16.10])
    horizon = 16.7

    grid = np.linspace(0, horizon, 2000)

    # Counting path
    N_grid = np.searchsorted(event_times, grid, side="right")

    # Classical exponential Hawkes intensity with fixed jump alpha.
    lambda_grid = eta + np.sum(
        alpha * np.exp(-beta * (grid[:, None] - event_times[None, :]))
        * (grid[:, None] > event_times[None, :]),
        axis=1,
    )

    fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

    # N_t step plot without artificial vertical lines at discontinuities.
    t_points = np.r_[0, event_times, horizon]
    n_before = np.arange(0, len(event_times) + 1)
    for i in range(len(t_points) - 1):
        ax[0].hlines(n_before[i], t_points[i], t_points[i + 1])
    for i, ti in enumerate(event_times):
        ax[0].plot(ti, i, marker="o", markerfacecolor="none", markersize=8)
        ax[0].plot(ti, i + 1, marker="o", markersize=6)
    ax[0].set_ylabel(r"$N_t$")

    # lambda_t: left-continuous value filled, right-limit open.
    ax[1].plot(grid, lambda_grid)
    for ti in event_times:
        lambda_left = eta + np.sum(alpha * np.exp(-beta * (ti - event_times[event_times < ti])))
        lambda_right = lambda_left + alpha
        ax[1].plot(ti, lambda_left, marker="o", markersize=6)
        ax[1].plot(ti, lambda_right, marker="o", markerfacecolor="none", markersize=8)

    ax[1].set_ylabel(r"$\lambda_t$")
    ax[1].set_xlabel(r"$t$")

    plt.tight_layout()
    fig.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_figure_7_1_one_path_with_theory(path, out_file: str) -> None:
    """
    Create Fig7.1-style one-path plot:
    - histogram of arrivals
    - N_t with E[N_t | lambda0]
    - lambda_t with E[lambda_t | lambda0]
    """
    grid = np.linspace(0.0, path.horizon, 5000)
    N_grid = counting_process(path, grid)
    lambda_grid = intensity_process(path, grid)
    theory = theoretical_moments_dz13(grid, path.a, path.delta, path.beta_x, path.lambda0)

    fig, ax = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    ax[0].hist(path.event_times, bins=50, range=(0, path.horizon), label="Histogram of arrivals")
    ax[0].set_ylabel("Count")
    ax[0].legend(loc="upper right")

    ax[1].plot(grid, N_grid, label=r"$N_t$ (one path)")
    ax[1].plot(grid, theory["E_N"], label=r"$\mathbb{E}[N_t\mid\lambda_0]$")
    ax[1].set_ylabel(r"$N_t$")
    ax[1].legend(loc="upper left")

    ax[2].plot(grid, lambda_grid, label=r"$\lambda_t$ (one path)")
    ax[2].plot(grid, theory["E_lambda"], label=r"$\mathbb{E}[\lambda_t\mid\lambda_0]$")
    ax[2].set_ylabel(r"$\lambda_t$")
    ax[2].set_xlabel("Time t")
    ax[2].legend(loc="upper right")

    plt.tight_layout()
    fig.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_figure_7_2_monte_carlo_comparison(
    times,
    theory,
    simulation,
    out_file: str,
) -> None:
    """
    Create Fig7.2-style comparison:
    theoretical curves and simulated star markers for:
    Var(lambda_T | lambda0), E[N_T | lambda0], E[lambda_T | lambda0].
    """
    fig, ax = plt.subplots(figsize=(12, 4.8))

    ax.plot(times, theory["Var_lambda"], label=r"$\mathrm{Var}(\lambda_T\mid\lambda_0)$")
    ax.plot(times, simulation["Var_lambda_sim"], marker="*", linestyle="None", label="Simulation")

    ax.plot(times, theory["E_N"], label=r"$\mathbb{E}[N_T\mid\lambda_0]$")
    ax.plot(times, simulation["E_N_sim"], marker="*", linestyle="None", label="Simulation")

    ax.plot(times, theory["E_lambda"], label=r"$\mathbb{E}[\lambda_T\mid\lambda_0]$")
    ax.plot(times, simulation["E_lambda_sim"], marker="*", linestyle="None", label="Simulation")

    ax.set_xlabel("Time T")
    ax.legend(loc="upper left")
    fig.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close(fig)
