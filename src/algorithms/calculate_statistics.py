"""This module calculates stats from the pandas DataFrame that holds the portfolio
estimates
"""

from typing import Dict

import pandas as pd

from context import InvestmentAssumption


def calculate_summary_statistics(
    results_df: pd.DataFrame, investment_assumption: InvestmentAssumption
) -> Dict[str, float]:
    """
    Calculate key summary statistics for the entire simulation.

    Args:
        results_df: Results from simulate_portfolio_evolution
        investment_assumption: Needed for initial investment amount

    Returns:
        Dictionary with summary metrics
    """
    initial_capital = investment_assumption.initial_capital
    # Get final year values for each iteration
    final_year = results_df["year"].max()
    final_values = results_df[results_df["year"] == final_year]["total"]
    # Calculate returns
    total_returns = final_values - initial_capital
    total_returns = total_returns.reset_index(drop=True)
    pct_returns = (final_values / initial_capital - 1) * 100

    # Annualized returns (CAGR)
    cagr = ((final_values / initial_capital) ** (1 / final_year) - 1) * 100

    return {
        # Absolute returns
        "mean_total_return": total_returns.mean(),
        "median_total_return": total_returns.median(),
        "std_total_return": total_returns.std(),
        # Percentage returns
        "mean_pct_return": pct_returns.mean(),
        "median_pct_return": pct_returns.median(),
        "std_pct_return": pct_returns.std(),
        # Annualized returns (CAGR)
        "mean_cagr": cagr.mean(),
        "median_cagr": cagr.median(),
        # Final portfolio values
        "mean_final_value": final_values.mean(),
        "median_final_value": final_values.median(),
        # Risk metrics
        "min_final_value": final_values.min(),
        "max_final_value": final_values.max(),
        "percentile_5": final_values.quantile(0.05),
        "percentile_25": final_values.quantile(0.25),
        "percentile_75": final_values.quantile(0.75),
        "percentile_95": final_values.quantile(0.95),
        # Probability of loss
        "prob_loss": (final_values < initial_capital).sum() / len(final_values) * 100,
    }
