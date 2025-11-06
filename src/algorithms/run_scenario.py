from typing import List, Tuple

import numpy as np
import pandas as pd

from context import Asset


def generate_return_matrix(
    portfolio_composition: List[Tuple[Asset, float]],
    horizon_years: int,
    num_trials: int,
    seed: int = 42,
) -> Tuple[np.ndarray, List[str]]:
    """
    Generate random returns for each asset based on their distribution parameters.

    Args:
        portfolio_composition: List of (Asset, weight) tuples
        horizon_years: Number of years to simulate
        num_trials: Number of Monte Carlo iterations
        seed: Random seed for reproducibility

    Returns:
        Tuple of:
            - np.ndarray with shape (num_trials, horizon_years, num_assets)
              Values as multiplicative returns (e.g., 1.08 for 8% gain)
            - List of asset names (to track which column is which)
    """
    np.random.seed(seed)

    num_assets = len(portfolio_composition)

    # Pre-allocate 3D array: (trials, years, assets)
    returns = np.zeros((num_trials, horizon_years, num_assets))

    for i, (asset, _) in enumerate(portfolio_composition):
        distribution = asset.distribution_type.lower()

        if distribution == "normal":
            annual_returns = np.random.normal(
                loc=asset.mean_return,
                scale=asset.std_dev,
                size=(num_trials, horizon_years),
            )
            returns[:, :, i] = 1 + annual_returns

        elif distribution == "lognormal":
            mu_log, sigma_log = _get_lognormal_parameters(
                asset.mean_return, asset.std_dev
            )
            returns[:, :, i] = np.random.lognormal(
                mean=mu_log, sigma=sigma_log, size=(num_trials, horizon_years)
            )

        else:
            raise ValueError(f"Distribution type '{distribution}' not supported")

    return returns


def simulate_portfolio_evolution(
    initial_allocations: np.ndarray,  # Shape: (num_assets,)
    return_matrix: np.ndarray,  # Shape: (num_trials, horizon_years, num_assets)
    asset_names: List[str],
) -> pd.DataFrame:
    """
    Simulate portfolio evolution (using vectorized operations).

    Args:
        initial_allocations: Initial dollar amount for each asset (num_assets,)
        return_matrix: Returns array (num_trials, horizon_years, num_assets)
        asset_names: List of asset names

    Returns:
        DataFrame with columns: ['iteration', 'year', asset_names..., 'total']
    """
    num_trials, horizon_years, num_assets = return_matrix.shape

    cumulative_returns = np.cumprod(return_matrix, axis=1)

    asset_values = cumulative_returns * initial_allocations[np.newaxis, np.newaxis, :]

    # Calculate portfolio total for each (trial, year)
    total_values = asset_values.sum(axis=2)  # Shape: (num_trials, horizon_years)

    iterations = np.repeat(np.arange(1, num_trials + 1), horizon_years)
    years = np.tile(np.arange(1, horizon_years + 1), num_trials)

    # Reshape asset values to 2D (num_trials * horizon_years, num_assets)
    asset_values_2d = asset_values.reshape(-1, num_assets)
    total_values_1d = total_values.reshape(-1)

    data = {
        "iteration": iterations,
        "year": years,
        "total": total_values_1d,
    }

    for i, asset_name in enumerate(asset_names):
        data[asset_name] = asset_values_2d[:, i]

    columns = ["iteration", "year"] + asset_names + ["total"]
    return pd.DataFrame(data)[columns]


def calculate_initial_allocations(
    initial_capital: float, portfolio_composition: List[Tuple[Asset, float]]
) -> Tuple[np.ndarray, List[str]]:
    """
    Calculate initial dollar allocations as a NumPy array.

    Returns:
        Tuple of:
            - np.ndarray with shape (num_assets,)
            - List of asset names
    """
    asset_names = [asset.name for asset, _ in portfolio_composition]
    allocations = np.array(
        [initial_capital * weight for _, weight in portfolio_composition]
    )

    return allocations, asset_names


def _get_lognormal_parameters(
    mean_return: float, std_dev: float
) -> Tuple[float, float]:
    """
    Convert normal space (mean_return, std_dev) to log-space (mu_log, sigma_log).
    """
    mean_multiplier = 1 + mean_return
    variance_ratio = (std_dev / mean_multiplier) ** 2

    sigma_log = np.sqrt(np.log(1 + variance_ratio))
    mu_log = np.log(mean_multiplier) - 0.5 * sigma_log**2

    return mu_log, sigma_log
