import numpy as np
import pandas as pd
import pytest

from algorithms.calculate_evolution import (
    _get_lognormal_parameters,
    calculate_initial_allocations,
    calculate_portfolio_evolution,
    calculate_return_matrix,
)
from context import Asset, InvestmentAssumption

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def make_asset(
    name: str = "Stocks",
    distribution_type: str = "normal",
    mean_return: float = 0.08,
    std_dev: float = 0.15,
) -> Asset:
    return Asset(
        name=name,
        distribution_type=distribution_type,
        mean_return=mean_return,
        std_dev=std_dev,
    )


def make_investment_assumption(
    initial_capital: float = 100_000,
    horizon_years: int = 10,
    num_trials: int = 500,
    portfolio_composition=None,
) -> InvestmentAssumption:
    if portfolio_composition is None:
        stocks = make_asset("Stocks", mean_return=0.08, std_dev=0.15)
        bonds = make_asset("Bonds", mean_return=0.04, std_dev=0.05)
        portfolio_composition = [(stocks, 0.6), (bonds, 0.4)]

    asset_names = [asset.name for asset, _ in portfolio_composition]
    simple_portfolio_composition = [
        (asset.name, weight) for asset, weight in portfolio_composition
    ]

    return InvestmentAssumption(
        initial_capital=initial_capital,
        horizon_years=horizon_years,
        num_trials=num_trials,
        portfolio_composition=portfolio_composition,
        asset_names=asset_names,
        simple_portfolio_composition=simple_portfolio_composition,
    )


# ---------------------------------------------------------------------------
# calculate_initial_allocations
# ---------------------------------------------------------------------------


class TestCalculateInitialAllocations:
    def test_basic_allocation(self):
        stocks = make_asset("Stocks")
        bonds = make_asset("Bonds")
        assumption = make_investment_assumption(
            initial_capital=100_000,
            portfolio_composition=[(stocks, 0.6), (bonds, 0.4)],
        )
        result = calculate_initial_allocations(assumption)

        assert isinstance(result, np.ndarray)
        assert result.shape == (2,)
        np.testing.assert_allclose(result, [60_000, 40_000])

    def test_allocations_sum_to_initial_capital(self):
        stocks = make_asset("Stocks")
        bonds = make_asset("Bonds")
        cash = make_asset("Cash")
        assumption = make_investment_assumption(
            initial_capital=250_000,
            portfolio_composition=[(stocks, 0.5), (bonds, 0.3), (cash, 0.2)],
        )
        result = calculate_initial_allocations(assumption)
        np.testing.assert_allclose(result.sum(), 250_000)

    def test_single_asset_full_allocation(self):
        stocks = make_asset("Stocks")
        assumption = make_investment_assumption(
            initial_capital=50_000,
            portfolio_composition=[(stocks, 1.0)],
        )
        result = calculate_initial_allocations(assumption)
        assert result.shape == (1,)
        np.testing.assert_allclose(result[0], 50_000)

    def test_returns_numpy_array(self):
        assumption = make_investment_assumption()
        result = calculate_initial_allocations(assumption)
        assert isinstance(result, np.ndarray)

    def test_asset_order_preserved(self):
        """Allocations should follow the same order as portfolio_composition."""
        stocks = make_asset("Stocks")
        bonds = make_asset("Bonds")
        cash = make_asset("Cash")
        assumption = make_investment_assumption(
            initial_capital=100_000,
            portfolio_composition=[(stocks, 0.5), (bonds, 0.3), (cash, 0.2)],
        )
        result = calculate_initial_allocations(assumption)
        np.testing.assert_allclose(result, [50_000, 30_000, 20_000])


# ---------------------------------------------------------------------------
# _get_lognormal_parameters
# ---------------------------------------------------------------------------


class TestGetLognormalParameters:
    def test_returns_tuple_of_floats(self):
        mu_log, sigma_log = _get_lognormal_parameters(0.08, 0.15)
        assert isinstance(mu_log, float)
        assert isinstance(sigma_log, float)

    def test_sigma_log_is_positive(self):
        _, sigma_log = _get_lognormal_parameters(0.08, 0.15)
        assert sigma_log > 0

    def test_known_values(self):
        """Cross-check against manual derivation."""
        mean_return, std_dev = 0.08, 0.15
        mean_multiplier = 1 + mean_return
        variance_ratio = (std_dev / mean_multiplier) ** 2
        expected_sigma = np.sqrt(np.log(1 + variance_ratio))
        expected_mu = np.log(mean_multiplier) - 0.5 * expected_sigma**2

        mu_log, sigma_log = _get_lognormal_parameters(mean_return, std_dev)
        np.testing.assert_allclose(mu_log, expected_mu)
        np.testing.assert_allclose(sigma_log, expected_sigma)

    def test_zero_std_dev_gives_zero_sigma_log(self):
        _, sigma_log = _get_lognormal_parameters(0.05, 0.0)
        np.testing.assert_allclose(sigma_log, 0.0, atol=1e-10)

    def test_lognormal_mean_recovers_expected_multiplier(self):
        """E[lognormal] = exp(mu + 0.5 * sigma^2) should equal 1 + mean_return."""
        mean_return, std_dev = 0.07, 0.12
        mu_log, sigma_log = _get_lognormal_parameters(mean_return, std_dev)
        recovered = np.exp(mu_log + 0.5 * sigma_log**2)
        np.testing.assert_allclose(recovered, 1 + mean_return, rtol=1e-6)


# ---------------------------------------------------------------------------
# calculate_return_matrix
# ---------------------------------------------------------------------------


class TestCalculateReturnMatrix:
    def test_output_shape(self):
        assumption = make_investment_assumption(num_trials=200, horizon_years=10)
        result = calculate_return_matrix(assumption, seed=0)
        assert result.shape == (200, 10, 2)

    def test_reproducibility_with_same_seed(self):
        assumption = make_investment_assumption()
        r1 = calculate_return_matrix(assumption, seed=99)
        r2 = calculate_return_matrix(assumption, seed=99)
        np.testing.assert_array_equal(r1, r2)

    def test_different_seeds_give_different_results(self):
        assumption = make_investment_assumption()
        r1 = calculate_return_matrix(assumption, seed=1)
        r2 = calculate_return_matrix(assumption, seed=2)
        assert not np.array_equal(r1, r2)

    def test_normal_distribution_rarely_negative(self):
        """Multiplicative returns from normal dist should be >0 for typical equity params."""
        stocks = make_asset(
            "Stocks", distribution_type="normal", mean_return=0.08, std_dev=0.15
        )
        assumption = make_investment_assumption(
            portfolio_composition=[(stocks, 1.0)],
            num_trials=1000,
            horizon_years=5,
        )
        result = calculate_return_matrix(assumption, seed=42)
        negative_ratio = (result <= 0).mean()
        assert negative_ratio < 0.01, (
            f"Too many non-positive returns: {negative_ratio:.2%}"
        )

    def test_lognormal_distribution_always_positive(self):
        stocks = make_asset(
            "Stocks", distribution_type="lognormal", mean_return=0.08, std_dev=0.15
        )
        assumption = make_investment_assumption(
            portfolio_composition=[(stocks, 1.0)],
            num_trials=500,
            horizon_years=10,
        )
        result = calculate_return_matrix(assumption, seed=42)
        assert (result > 0).all(), "Lognormal returns must always be strictly positive"

    def test_unsupported_distribution_raises_value_error(self):
        bad_asset = make_asset("X", distribution_type="cauchy")
        assumption = make_investment_assumption(
            portfolio_composition=[(bad_asset, 1.0)]
        )
        with pytest.raises(ValueError, match="not supported"):
            calculate_return_matrix(assumption, seed=0)

    def test_distribution_type_is_case_insensitive(self):
        """distribution_type matching should be case-insensitive per the lower() call."""
        stocks = make_asset(
            "Stocks", distribution_type="Normal", mean_return=0.07, std_dev=0.1
        )
        assumption = make_investment_assumption(
            portfolio_composition=[(stocks, 1.0)],
            num_trials=50,
            horizon_years=3,
        )
        result = calculate_return_matrix(assumption, seed=42)
        assert result.shape == (50, 3, 1)

    def test_mixed_distributions(self):
        stocks = make_asset("Stocks", distribution_type="normal")
        bonds = make_asset("Bonds", distribution_type="lognormal")
        assumption = make_investment_assumption(
            portfolio_composition=[(stocks, 0.6), (bonds, 0.4)],
            num_trials=100,
            horizon_years=5,
        )
        result = calculate_return_matrix(assumption, seed=42)
        assert result.shape == (100, 5, 2)

    def test_third_axis_matches_num_assets(self):
        assets = [make_asset(f"Asset{i}") for i in range(5)]
        composition = [(a, 0.2) for a in assets]
        assumption = make_investment_assumption(
            portfolio_composition=composition,
            num_trials=50,
            horizon_years=3,
        )
        result = calculate_return_matrix(assumption, seed=0)
        assert result.shape[2] == 5


# ---------------------------------------------------------------------------
# calculate_portfolio_evolution
# ---------------------------------------------------------------------------


class TestCalculatePortfolioEvolution:
    @pytest.fixture
    def base_setup(self):
        assumption = make_investment_assumption(num_trials=50, horizon_years=5)
        initial_allocations = calculate_initial_allocations(assumption)
        return_matrix = calculate_return_matrix(assumption, seed=42)
        df = calculate_portfolio_evolution(
            initial_allocations, return_matrix, assumption
        )
        return df, assumption

    def test_returns_dataframe(self, base_setup):
        df, _ = base_setup
        assert isinstance(df, pd.DataFrame)

    def test_row_count(self, base_setup):
        df, assumption = base_setup
        assert len(df) == assumption.num_trials * assumption.horizon_years

    def test_required_columns_present(self, base_setup):
        df, assumption = base_setup
        for col in ["iteration", "year", "total"] + assumption.asset_names:
            assert col in df.columns

    def test_column_order(self, base_setup):
        df, assumption = base_setup
        expected = ["iteration", "year"] + assumption.asset_names + ["total"]
        assert list(df.columns) == expected

    def test_total_equals_sum_of_assets(self, base_setup):
        df, assumption = base_setup
        asset_sum = df[assumption.asset_names].sum(axis=1)
        np.testing.assert_allclose(df["total"].values, asset_sum.values, rtol=1e-10)

    def test_iteration_range(self, base_setup):
        df, assumption = base_setup
        assert df["iteration"].min() == 1
        assert df["iteration"].max() == assumption.num_trials

    def test_year_range(self, base_setup):
        df, assumption = base_setup
        assert df["year"].min() == 1
        assert df["year"].max() == assumption.horizon_years

    def test_each_iteration_has_all_years(self, base_setup):
        df, assumption = base_setup
        for iteration, group in df.groupby("iteration"):
            assert sorted(group["year"].tolist()) == list(
                range(1, assumption.horizon_years + 1)
            )

    def test_portfolio_grows_on_average(self, base_setup):
        """With positive expected returns, the mean final value should exceed initial capital."""
        df, _ = base_setup
        final_year_totals = df[df["year"] == df["year"].max()]["total"]
        assert final_year_totals.mean() > 100_000

    def test_all_values_positive(self, base_setup):
        df, assumption = base_setup
        for col in assumption.asset_names + ["total"]:
            assert (df[col] > 0).all(), f"Column '{col}' contains non-positive values"

    def test_single_asset_total_matches_asset_column(self):
        stocks = make_asset(
            "Stocks", distribution_type="lognormal", mean_return=0.07, std_dev=0.12
        )
        assumption = make_investment_assumption(
            initial_capital=100_000,
            portfolio_composition=[(stocks, 1.0)],
            num_trials=10,
            horizon_years=3,
        )
        initial_allocations = calculate_initial_allocations(assumption)
        return_matrix = calculate_return_matrix(assumption, seed=7)
        df = calculate_portfolio_evolution(
            initial_allocations, return_matrix, assumption
        )

        np.testing.assert_allclose(df["total"].values, df["Stocks"].values, rtol=1e-10)

    def test_year_one_values_reflect_initial_capital(self):
        """Year-1 totals should be initial_capital × the single-year return, not compounded."""
        stocks = make_asset("Stocks", distribution_type="lognormal")
        assumption = make_investment_assumption(
            initial_capital=100_000,
            portfolio_composition=[(stocks, 1.0)],
            num_trials=200,
            horizon_years=5,
        )
        initial_allocations = calculate_initial_allocations(assumption)
        return_matrix = calculate_return_matrix(assumption, seed=0)
        df = calculate_portfolio_evolution(
            initial_allocations, return_matrix, assumption
        )

        year1 = df[df["year"] == 1]["total"].values
        expected = return_matrix[:, 0, 0] * 100_000
        np.testing.assert_allclose(year1, expected, rtol=1e-10)
