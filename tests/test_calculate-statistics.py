import numpy as np
import pandas as pd
import pytest

from context import Asset, InvestmentAssumption, SummaryStatistics
from src.algorithms.calculate_statistics import (
    calculate_drawdown_statistics,
    calculate_summary_statistics,
    calculate_time_series_statistics,
)

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def make_investment_assumption(
    initial_capital: float = 100_000,
    horizon_years: int = 10,
    num_trials: int = 100,
) -> InvestmentAssumption:
    stocks = Asset(
        name="Stocks", distribution_type="normal", mean_return=0.08, std_dev=0.15
    )
    bonds = Asset(
        name="Bonds", distribution_type="normal", mean_return=0.04, std_dev=0.05
    )
    portfolio_composition = [(stocks, 0.6), (bonds, 0.4)]
    return InvestmentAssumption(
        initial_capital=initial_capital,
        horizon_years=horizon_years,
        num_trials=num_trials,
        portfolio_composition=portfolio_composition,
        asset_names=["Stocks", "Bonds"],
        simple_portfolio_composition=[("Stocks", 0.6), ("Bonds", 0.4)],
    )


def make_results_df(
    final_values: list[float],
    horizon_years: int = 10,
    initial_capital: float = 100_000,
) -> pd.DataFrame:
    """
    Build a minimal results DataFrame that mirrors the output of
    calculate_portfolio_evolution. Each iteration has a monotonically
    growing total so drawdown tests behave predictably unless overridden.
    """
    num_trials = len(final_values)
    rows = []
    for i, final_val in enumerate(final_values, start=1):
        for year in range(1, horizon_years + 1):
            # Linear interpolation from initial_capital to final_val
            value = initial_capital + (final_val - initial_capital) * (
                year / horizon_years
            )
            rows.append({"iteration": i, "year": year, "total": value})
    return pd.DataFrame(rows)


def make_flat_df(
    total_per_year: float = 100_000,
    num_trials: int = 5,
    horizon_years: int = 5,
) -> pd.DataFrame:
    """All iterations have the same constant total every year."""
    rows = [
        {"iteration": i, "year": y, "total": total_per_year}
        for i in range(1, num_trials + 1)
        for y in range(1, horizon_years + 1)
    ]
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# calculate_summary_statistics
# ---------------------------------------------------------------------------


class TestCalculateSummaryStatistics:
    def test_returns_summary_statistics_instance(self):
        assumption = make_investment_assumption()
        df = make_results_df([120_000] * 10)
        result = calculate_summary_statistics(df, assumption)
        assert isinstance(result, SummaryStatistics)

    def test_no_gain_no_loss_scenario(self):
        """When all final values equal initial capital, returns should be zero."""
        assumption = make_investment_assumption(initial_capital=100_000)
        df = make_flat_df(total_per_year=100_000)
        result = calculate_summary_statistics(df, assumption)

        assert result.mean_total_return == 0.0
        assert result.median_total_return == 0.0
        assert result.mean_pct_return == 0.0
        assert result.prob_loss == 0.0

    def test_all_trials_gain(self):
        assumption = make_investment_assumption(initial_capital=100_000)
        df = make_results_df([150_000] * 20)
        result = calculate_summary_statistics(df, assumption)

        assert result.mean_total_return > 0
        assert result.mean_pct_return > 0
        assert result.prob_loss == 0.0

    def test_all_trials_loss(self):
        assumption = make_investment_assumption(initial_capital=100_000)
        df = make_results_df([80_000] * 20)
        result = calculate_summary_statistics(df, assumption)

        assert result.mean_total_return < 0
        assert result.prob_loss == 100.0

    def test_prob_loss_is_percentage(self):
        """Half the trials below initial capital → prob_loss == 50.0."""
        assumption = make_investment_assumption(initial_capital=100_000)
        gains = [120_000] * 10
        losses = [80_000] * 10
        df = make_results_df(gains + losses)
        result = calculate_summary_statistics(df, assumption)
        assert result.prob_loss == 50.0

    def test_percentile_ordering(self):
        assumption = make_investment_assumption(initial_capital=100_000)
        final_values = list(range(80_000, 180_000, 1_000))  # 100 distinct values
        df = make_results_df(final_values)
        result = calculate_summary_statistics(df, assumption)

        assert result.percentile_5 <= result.percentile_25
        assert result.percentile_25 <= result.median_final_value
        assert result.median_final_value <= result.percentile_75
        assert result.percentile_75 <= result.percentile_95

    def test_min_max_bounds(self):
        assumption = make_investment_assumption(initial_capital=100_000)
        final_values = [90_000, 110_000, 130_000, 150_000]
        df = make_results_df(final_values)
        result = calculate_summary_statistics(df, assumption)

        assert result.min_final_value == pytest.approx(90_000, rel=1e-3)
        assert result.max_final_value == pytest.approx(150_000, rel=1e-3)

    def test_mean_and_median_final_value_equal_for_symmetric_distribution(self):
        """Symmetric set of final values → mean ≈ median."""
        assumption = make_investment_assumption(initial_capital=100_000)
        # Symmetric around 120_000
        final_values = [80_000, 100_000, 120_000, 140_000, 160_000]
        df = make_results_df(final_values)
        result = calculate_summary_statistics(df, assumption)
        assert result.mean_final_value == pytest.approx(
            result.median_final_value, rel=1e-3
        )

    def test_cagr_positive_when_portfolio_grows(self):
        assumption = make_investment_assumption(
            initial_capital=100_000, horizon_years=10
        )
        df = make_results_df([200_000] * 10, horizon_years=10)
        result = calculate_summary_statistics(df, assumption)
        assert result.mean_cagr > 0
        assert result.median_cagr > 0

    def test_all_fields_are_rounded_to_two_decimals(self):
        assumption = make_investment_assumption(initial_capital=100_000)
        df = make_results_df([123_456.789] * 10)
        result = calculate_summary_statistics(df, assumption)
        for field in SummaryStatistics.__dataclass_fields__:
            value = getattr(result, field)
            assert round(value, 2) == value, (
                f"Field '{field}' is not rounded to 2dp: {value}"
            )

    def test_uses_final_year_only(self):
        """Intermediate year values should not affect the summary stats."""
        assumption = make_investment_assumption(
            initial_capital=100_000, horizon_years=3
        )
        rows = [
            # iteration 1: crashes in year 2, recovers strongly by year 3
            {"iteration": 1, "year": 1, "total": 50_000},
            {"iteration": 1, "year": 2, "total": 10_000},
            {"iteration": 1, "year": 3, "total": 200_000},
            # iteration 2: steady growth
            {"iteration": 2, "year": 1, "total": 110_000},
            {"iteration": 2, "year": 2, "total": 120_000},
            {"iteration": 2, "year": 3, "total": 200_000},
        ]
        df = pd.DataFrame(rows)
        result = calculate_summary_statistics(df, assumption)
        # Both end at 200_000, so mean_final_value should be exactly 200_000
        assert result.mean_final_value == pytest.approx(200_000, rel=1e-6)


# ---------------------------------------------------------------------------
# calculate_drawdown_statistics
# ---------------------------------------------------------------------------


class TestCalculateDrawdownStatistics:
    def test_returns_dict_with_expected_keys(self):
        df = make_results_df([120_000] * 5)
        result = calculate_drawdown_statistics(df)
        assert set(result.keys()) == {
            "mean_max_drawdown",
            "median_max_drawdown",
            "worst_max_drawdown",
            "best_max_drawdown",
        }

    def test_monotonically_increasing_portfolio_has_zero_drawdown(self):
        """If portfolio never falls, max drawdown should be 0."""
        df = make_results_df([150_000] * 10)  # linear growth, never drops
        result = calculate_drawdown_statistics(df)
        assert result["mean_max_drawdown"] == pytest.approx(0.0, abs=1e-6)
        assert result["worst_max_drawdown"] == pytest.approx(0.0, abs=1e-6)

    def test_drawdown_values_are_non_positive(self):
        """Drawdown is a loss metric — all values should be ≤ 0."""
        df = make_results_df([80_000, 100_000, 130_000, 60_000, 120_000])
        result = calculate_drawdown_statistics(df)
        for key, value in result.items():
            assert value <= 0, (
                f"Expected non-positive drawdown for '{key}', got {value}"
            )

    def test_worst_drawdown_le_best_drawdown(self):
        df = make_results_df([70_000, 90_000, 110_000, 50_000, 130_000])
        result = calculate_drawdown_statistics(df)
        assert result["worst_max_drawdown"] <= result["best_max_drawdown"]

    def test_known_drawdown_value(self):
        """
        Single iteration: values go 100 → 150 → 75.
        Peak is 150, trough is 75 → drawdown = (75-150)/150 * 100 = -50%.
        """
        rows = [
            {"iteration": 1, "year": 1, "total": 100_000},
            {"iteration": 1, "year": 2, "total": 150_000},
            {"iteration": 1, "year": 3, "total": 75_000},
        ]
        df = pd.DataFrame(rows)
        result = calculate_drawdown_statistics(df)
        assert result["worst_max_drawdown"] == pytest.approx(-50.0, rel=1e-4)

    def test_flat_portfolio_has_zero_drawdown(self):
        df = make_flat_df(total_per_year=100_000, num_trials=5, horizon_years=5)
        result = calculate_drawdown_statistics(df)
        assert result["mean_max_drawdown"] == pytest.approx(0.0, abs=1e-6)

    def test_multiple_iterations_aggregated(self):
        """Mean should lie between the best and worst drawdown."""
        df = make_results_df([60_000, 80_000, 120_000, 140_000])
        result = calculate_drawdown_statistics(df)
        assert (
            result["worst_max_drawdown"]
            <= result["mean_max_drawdown"]
            <= result["best_max_drawdown"]
        )


# ---------------------------------------------------------------------------
# calculate_time_series_statistics
# ---------------------------------------------------------------------------


class TestCalculateTimeSeriesStatistics:
    @pytest.fixture
    def base_setup(self):
        assumption = make_investment_assumption(
            initial_capital=100_000, horizon_years=5
        )
        df = make_results_df([120_000] * 20, horizon_years=5)
        stats = calculate_time_series_statistics(df, assumption)
        return stats, assumption

    def test_returns_dataframe(self, base_setup):
        stats, _ = base_setup
        assert isinstance(stats, pd.DataFrame)

    def test_row_count_equals_horizon_years(self, base_setup):
        stats, assumption = base_setup
        assert len(stats) == assumption.horizon_years

    def test_expected_columns_present(self, base_setup):
        stats, _ = base_setup
        expected = {
            "year",
            "mean",
            "median",
            "std",
            "p5",
            "p10",
            "p25",
            "p75",
            "p90",
            "p95",
            "min",
            "max",
            "mean_return_pct",
            "median_return_pct",
        }
        assert expected.issubset(set(stats.columns))

    def test_year_column_is_sequential(self, base_setup):
        stats, assumption = base_setup
        assert list(stats["year"]) == list(range(1, assumption.horizon_years + 1))

    def test_percentile_ordering_per_year(self, base_setup):
        stats, _ = base_setup
        for _, row in stats.iterrows():
            assert row["p5"] <= row["p25"] <= row["median"] <= row["p75"] <= row["p95"]

    def test_mean_return_pct_positive_when_growing(self, base_setup):
        stats, _ = base_setup
        assert (stats["mean_return_pct"] > 0).all()

    def test_mean_return_pct_formula(self):
        """mean_return_pct = (mean / initial_capital - 1) * 100."""
        assumption = make_investment_assumption(
            initial_capital=100_000, horizon_years=3
        )
        df = make_flat_df(total_per_year=110_000, num_trials=10, horizon_years=3)
        stats = calculate_time_series_statistics(df, assumption)
        expected_pct = (110_000 / 100_000 - 1) * 100
        np.testing.assert_allclose(
            stats["mean_return_pct"].values, expected_pct, rtol=1e-6
        )

    def test_flat_portfolio_has_zero_std(self):
        assumption = make_investment_assumption(
            initial_capital=100_000, horizon_years=4
        )
        df = make_flat_df(total_per_year=120_000, num_trials=10, horizon_years=4)
        stats = calculate_time_series_statistics(df, assumption)
        np.testing.assert_allclose(stats["std"].values, 0.0, atol=1e-6)

    def test_min_le_mean_le_max(self, base_setup):
        stats, _ = base_setup
        assert (stats["min"] <= stats["mean"]).all()
        assert (stats["mean"] <= stats["max"]).all()

    def test_return_pct_is_zero_at_initial_capital(self):
        """If all values equal initial_capital, return pct should be 0."""
        assumption = make_investment_assumption(
            initial_capital=100_000, horizon_years=3
        )
        df = make_flat_df(total_per_year=100_000, num_trials=5, horizon_years=3)
        stats = calculate_time_series_statistics(df, assumption)
        np.testing.assert_allclose(stats["mean_return_pct"].values, 0.0, atol=1e-6)
        np.testing.assert_allclose(stats["median_return_pct"].values, 0.0, atol=1e-6)
