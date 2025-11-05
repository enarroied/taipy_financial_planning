from dataclasses import dataclass


@dataclass
class Scenario:
    """All parameters for one simulation run defined in Tab 2."""

    initial_capital: float
    horizon_years: int
    num_trials: int
    # List of (Asset, Weight) tuples for the portfolio composition

    # portfolio_composition: List[tuple[Asset, float]]
