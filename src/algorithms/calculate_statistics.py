"""This module calculates stats from the pandas DataFrame that holds the portfolio
estimates
"""

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
