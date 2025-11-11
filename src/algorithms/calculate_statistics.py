"""This module calculates stats from the pandas DataFrame that holds the portfolio
estimates
"""

from typing import Dict

import numpy as np
import pandas as pd

from context import InvestmentAssumption, SummaryStatistics


def calculate_summary_statistics(
    results_df: pd.DataFrame, investment_assumption: InvestmentAssumption
) -> SummaryStatistics:
    """
    Calculate key summary statistics for the entire simulation.

    Args:
        results_df: Results from simulate_portfolio_evolution
        investment_assumption: Needed for initial investment amount

    Returns:
        SummaryStatistics instance with all summary metrics
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

    # Create and return the dataclass instance
    return SummaryStatistics(
        # Final portfolio values
        mean_final_value=round(final_values.mean(), 2),
        median_final_value=round(final_values.median(), 2),
        # Absolute returns
        mean_total_return=round(total_returns.mean(), 2),
        median_total_return=round(total_returns.median(), 2),
        std_total_return=round(total_returns.std(), 2),
        # Percentage returns
        mean_pct_return=round(pct_returns.mean(), 2),
        median_pct_return=round(pct_returns.median(), 2),
        std_pct_return=round(pct_returns.std(), 2),
        # Annualized returns (CAGR)
        mean_cagr=round(cagr.mean(), 2),
        median_cagr=round(cagr.median(), 2),
        # Risk metrics
        min_final_value=round(final_values.min(), 2),
        max_final_value=round(final_values.max(), 2),
        percentile_5=round(final_values.quantile(0.05), 2),
        percentile_25=round(final_values.quantile(0.25), 2),
        percentile_75=round(final_values.quantile(0.75), 2),
        percentile_95=round(final_values.quantile(0.95), 2),
        # Probability of loss
        prob_loss=round(
            (final_values < initial_capital).sum() / len(final_values) * 100, 2
        ),
    )


def calculate_drawdown_statistics(results_df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate maximum drawdown statistics (worst peak-to-trough decline).

    Args:
        results_df: Results from simulate_portfolio_evolution

    Returns:
        Dictionary with drawdown metrics
    """
    max_drawdowns = []

    for iteration in results_df["iteration"].unique():
        iteration_data = results_df[results_df["iteration"] == iteration].sort_values(
            "year"
        )
        values = iteration_data["total"].to_numpy()

        running_max = np.maximum.accumulate(values)
        drawdowns = (values - running_max) / running_max * 100
        max_drawdowns.append(drawdowns.min())

    max_drawdowns = np.array(max_drawdowns)
    return {
        "mean_max_drawdown": max_drawdowns.mean(),
        "median_max_drawdown": np.median(max_drawdowns),
        "worst_max_drawdown": max_drawdowns.min(),
        "best_max_drawdown": max_drawdowns.max(),
    }


def calculate_time_series_statistics(
    results_df: pd.DataFrame, investment_assumption: InvestmentAssumption
) -> pd.DataFrame:
    """
    Calculate mean, median, and percentiles for each year across all iterations.

    Args:
        results_df: Results from simulate_portfolio_evolution
        investment_assumption: Used to get the starting investment amount

    Returns:
        DataFrame with columns: year, mean, median, std, p5, p25, p75, p95, min, max
    """
    initial_capital = investment_assumption.initial_capital
    time_stats = (
        results_df.groupby("year")["total"]
        .agg(
            [
                ("mean", "mean"),
                ("median", "median"),
                ("std", "std"),
                ("p5", lambda x: x.quantile(0.05)),
                ("p10", lambda x: x.quantile(0.10)),
                ("p25", lambda x: x.quantile(0.25)),
                ("p75", lambda x: x.quantile(0.75)),
                ("p90", lambda x: x.quantile(0.90)),
                ("p95", lambda x: x.quantile(0.95)),
                ("min", "min"),
                ("max", "max"),
            ]
        )
        .reset_index()
    )

    # Add percentage return columns
    time_stats["mean_return_pct"] = (time_stats["mean"] / initial_capital - 1) * 100
    time_stats["median_return_pct"] = (time_stats["median"] / initial_capital - 1) * 100

    return time_stats
