from dataclasses import dataclass
from typing import List


@dataclass
class Asset:
    """Product defined in Tab 1 (Asset Management)."""

    name: str
    distribution_type: str  # e.g., "normal"
    mean_return: float  # e.g., 0.08
    std_dev: float  # e.g., 0.15


@dataclass
class InvestmentAssumption:
    """All parameters for one simulation run defined in Tab 2."""

    initial_capital: float
    horizon_years: int
    num_trials: int
    portfolio_composition: List[tuple[Asset, float]]
    asset_names: List[str]
    simple_portfolio_composition: List[tuple[str, float]]


@dataclass(frozen=True)
class SummaryStatistics:
    """
    A dataclass to hold the key summary statistics for a portfolio simulation.
    All fields are floats representing monetary values, percentages, or ratios.
    """

    # Absolute returns
    mean_total_return: float
    median_total_return: float
    std_total_return: float

    # Percentage returns
    mean_pct_return: float
    median_pct_return: float
    std_pct_return: float

    # Annualized returns (CAGR)
    mean_cagr: float
    median_cagr: float

    # Final portfolio values
    mean_final_value: float
    median_final_value: float

    # Risk metrics
    min_final_value: float
    max_final_value: float
    percentile_5: float
    percentile_25: float
    percentile_75: float
    percentile_95: float

    # Probability of loss (as a percentage)
    prob_loss: float
