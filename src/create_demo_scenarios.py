"""this module creates mock Scenarios, useful for development"""

import taipy as tp

from config import generate_investment_scenario_config
from context import Asset, InvestmentAssumption

asset_a = Asset(
    name="Index Fund (S&P 500)",
    distribution_type="lognormal",
    mean_return=0.08,
    std_dev=0.15,
)
asset_b = Asset(
    name="Aggressive Tech Stock",
    distribution_type="lognormal",
    mean_return=0.12,
    std_dev=0.35,
)
asset_c = Asset(
    name="Corporate Bonds",
    distribution_type="lognormal",
    mean_return=0.04,
    std_dev=0.06,
)

investment_assumption_1 = InvestmentAssumption(
    initial_capital=100_000,
    horizon_years=10,
    num_trials=1000,
    portfolio_composition=[(asset_a, 0.5), (asset_b, 0.3), (asset_c, 0.2)],
    asset_names=["Index Fund (S&P 500)", "Aggressive Tech Stock", "Corporate Bonds"],
    simple_portfolio_composition=[
        ("Index Fund (S&P 500)", 0.50),
        ("Aggressive Tech Stock", 0.30),
        ("Corporate Bonds", 0.20),
    ],
)
investment_assumption_2 = InvestmentAssumption(
    initial_capital=10_000,
    horizon_years=20,
    num_trials=1000,
    portfolio_composition=[(asset_a, 0.50), (asset_b, 0.30), (asset_c, 0.20)],
    asset_names=["Index Fund (S&P 500)", "Aggressive Tech Stock", "Corporate Bonds"],
    simple_portfolio_composition=[
        ("Index Fund (S&P 500)", 0.50),
        ("Aggressive Tech Stock", 0.30),
        ("Corporate Bonds", 0.20),
    ],
)
investment_assumption_3 = InvestmentAssumption(
    initial_capital=10_000,
    horizon_years=20,
    num_trials=1000,
    portfolio_composition=[(asset_c, 1)],
    asset_names=["Corporate Bonds"],
    simple_portfolio_composition=[
        ("Corporate Bonds", 1),
    ],
)

scenario1 = new_scenario = tp.create_scenario(
    generate_investment_scenario_config, name="test_1"
)
scenario1.investment_assumption.write(investment_assumption_1)

scenario2 = new_scenario = tp.create_scenario(
    generate_investment_scenario_config, name="test_2"
)
scenario2.investment_assumption.write(investment_assumption_2)

scenario3 = new_scenario = tp.create_scenario(
    generate_investment_scenario_config, name="test_3"
)
scenario3.investment_assumption.write(investment_assumption_3)
