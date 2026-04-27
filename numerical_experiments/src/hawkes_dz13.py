"""
Reproducible simulation utilities for Hawkes processes.

Main reference:
Dassios and Zhao (2013), Algorithm 3.1.

Model used in Chapter 7:
    lambda_t = a + (lambda0 - a) exp(-delta t)
               + sum_{T_i < t} X_i exp(-delta(t - T_i))

Default numerical specification:
    X_i ~ Exp(beta_x)
    (a, delta; beta_x; lambda0) = (0.9, 1.0; 1.2; 0.9)
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class HawkesPath:
    event_times: np.ndarray
    jump_sizes: np.ndarray
    horizon: float
    a: float
    delta: float
    beta_x: float
    lambda0: float


def simulate_dz13_path(
    horizon: float = 100.0,
    a: float = 0.9,
    delta: float = 1.0,
    beta_x: float = 1.2,
    lambda0: float = 0.9,
    seed: int | None = None,
    max_events: int = 1_000_000,
) -> HawkesPath:
    """
    Simulate one sample path using the exact Dassios-Zhao interarrival decomposition.

    Parameters
    ----------
    horizon:
        Final simulation time.
    a:
        Reversion/baseline level.
    delta:
        Exponential decay rate.
    beta_x:
        Rate parameter of exponential jump sizes X_i.
    lambda0:
        Initial intensity.
    seed:
        Random seed.
    max_events:
        Safety cap.
    """
    rng = np.random.default_rng(seed)

    t = 0.0
    lambda_plus = float(lambda0)
    event_times = []
    jump_sizes = []

    while t < horizon and len(event_times) < max_events:
        if lambda_plus <= a + 1e-14:
            # If lambda_{T_k^+} = a, the self-exciting clock is defective/inactive.
            s = rng.exponential(scale=1.0 / a)
        else:
            u1 = rng.random()
            u2 = rng.random()

            d = 1.0 + delta * np.log(u1) / (lambda_plus - a)
            s2 = -np.log(u2) / a

            if d > 0.0:
                s1 = -(1.0 / delta) * np.log(d)
                s = min(s1, s2)
            else:
                s = s2

        t_next = t + s
        if t_next > horizon:
            break

        lambda_minus = (lambda_plus - a) * np.exp(-delta * (t_next - t)) + a
        x_next = rng.exponential(scale=1.0 / beta_x)

        event_times.append(t_next)
        jump_sizes.append(x_next)

        lambda_plus = lambda_minus + x_next
        t = t_next

    return HawkesPath(
        event_times=np.asarray(event_times),
        jump_sizes=np.asarray(jump_sizes),
        horizon=horizon,
        a=a,
        delta=delta,
        beta_x=beta_x,
        lambda0=lambda0,
    )


def counting_process(path: HawkesPath, grid: np.ndarray) -> np.ndarray:
    """Evaluate N_t on a time grid."""
    return np.searchsorted(path.event_times, grid, side="right")


def intensity_process(path: HawkesPath, grid: np.ndarray) -> np.ndarray:
    """Evaluate the left-continuous conditional intensity lambda_t on a time grid."""
    out = np.empty_like(grid, dtype=float)
    T = path.event_times
    X = path.jump_sizes

    for i, t in enumerate(grid):
        idx = np.searchsorted(T, t, side="left")
        out[i] = (
            path.a
            + (path.lambda0 - path.a) * np.exp(-path.delta * t)
            + np.sum(X[:idx] * np.exp(-path.delta * (t - T[:idx])))
        )

    return out


def theoretical_moments_dz13(
    times: np.ndarray,
    a: float = 0.9,
    delta: float = 1.0,
    beta_x: float = 1.2,
    lambda0: float = 0.9,
) -> dict[str, np.ndarray]:
    """
    Theoretical formulas used for the Chapter 7 Monte Carlo comparison.

    For X ~ Exp(beta_x):
        mu1 = E[X] = 1 / beta_x
        mu2 = E[X^2] = 2 / beta_x^2
        kappa = delta - mu1
    """
    t = np.asarray(times, dtype=float)

    mu1 = 1.0 / beta_x
    mu2 = 2.0 / (beta_x**2)
    kappa = delta - mu1

    exp1 = np.exp(-kappa * t)
    exp2 = np.exp(-2.0 * kappa * t)

    e_lambda = a * delta / kappa + (lambda0 - a * delta / kappa) * exp1

    var_lambda = (mu2 / kappa) * (
        (a * delta / (2.0 * kappa) - lambda0) * exp2
        + (lambda0 - a * delta / kappa) * exp1
        + a * delta / (2.0 * kappa)
    )

    e_N = (a * delta / kappa) * t + (
        (lambda0 - a * delta / kappa) / kappa
    ) * (1.0 - exp1)

    return {
        "E_lambda": e_lambda,
        "Var_lambda": var_lambda,
        "E_N": e_N,
    }


def monte_carlo_terminal_statistics(
    times: np.ndarray,
    n_paths: int = 100_000,
    a: float = 0.9,
    delta: float = 1.0,
    beta_x: float = 1.2,
    lambda0: float = 0.9,
    seed: int = 2026,
) -> dict[str, np.ndarray]:
    """
    Simulate many paths and estimate:
        E[lambda_T | lambda0], Var(lambda_T | lambda0), E[N_T | lambda0].
    """
    rng = np.random.default_rng(seed)
    times = np.asarray(times, dtype=float)
    max_time = float(np.max(times))

    N_values = np.zeros((n_paths, len(times)))
    lambda_values = np.zeros((n_paths, len(times)))

    for m in range(n_paths):
        path = simulate_dz13_path(
            horizon=max_time,
            a=a,
            delta=delta,
            beta_x=beta_x,
            lambda0=lambda0,
            seed=int(rng.integers(0, 2**32 - 1)),
        )

        N_values[m, :] = counting_process(path, times)
        lambda_values[m, :] = intensity_process(path, times)

    return {
        "E_lambda_sim": lambda_values.mean(axis=0),
        "Var_lambda_sim": lambda_values.var(axis=0, ddof=0),
        "E_N_sim": N_values.mean(axis=0),
    }
