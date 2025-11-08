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
