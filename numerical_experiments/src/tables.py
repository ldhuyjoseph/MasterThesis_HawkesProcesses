"""Table helpers for the Monte Carlo comparison."""

import pandas as pd


def build_monte_carlo_table(times, theory, simulation) -> pd.DataFrame:
    """Return Table 7.1-style comparison with relative errors."""
    df = pd.DataFrame({
        "T": times,
        "E_lambda_theory": theory["E_lambda"],
        "E_lambda_sim": simulation["E_lambda_sim"],
        "E_lambda_error_pct": 100.0 * (simulation["E_lambda_sim"] - theory["E_lambda"]) / theory["E_lambda"],
        "Var_lambda_theory": theory["Var_lambda"],
        "Var_lambda_sim": simulation["Var_lambda_sim"],
        "Var_lambda_error_pct": 100.0 * (simulation["Var_lambda_sim"] - theory["Var_lambda"]) / theory["Var_lambda"],
        "E_N_theory": theory["E_N"],
        "E_N_sim": simulation["E_N_sim"],
        "E_N_error_pct": 100.0 * (simulation["E_N_sim"] - theory["E_N"]) / theory["E_N"],
    })
    return df


def save_table_outputs(df: pd.DataFrame, csv_file: str, latex_file: str) -> None:
    """Save table as CSV and LaTeX tabular."""
    df.to_csv(csv_file, index=False)

    latex = df.to_latex(
        index=False,
        float_format="%.4f",
        caption="Comparison between theoretical formulas and simulation results.",
        label="tab:moment-comparison",
    )

    with open(latex_file, "w", encoding="utf-8") as f:
        f.write(latex)
