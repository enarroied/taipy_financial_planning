from dataclasses import dataclass
from typing import List

import taipy.gui.builder as tgb
from taipy.gui import notify


@dataclass
class Asset:
    """Product defined in Tab 1 (Asset Management)."""

    name: str
    distribution_type: str  # e.g., "normal"
    mean_return: float  # e.g., 0.08
    std_dev: float  # e.g., 0.15


@dataclass
class InvestmentScenario:
    """All parameters for one simulation run defined in Tab 2."""

    initial_capital: float
    horizon_years: int
    num_trials: int
    # List of (Asset, Weight) tuples for the portfolio composition
    portfolio_composition: List[tuple[Asset, float]]


def create_scenario(state):
    with state as s:
        if s.new_scenario_name == "":
            notify(s, "e", "You need to have a name for your Scenario!")
            return

        all_percentages = [
            s.percentage_1,
            s.percentage_2,
            s.percentage_3,
            s.percentage_4,
            s.percentage_5,
            s.percentage_6,
        ]
        all_products = [
            s.product_name_1,
            s.product_name_2,
            s.product_name_3,
            s.product_name_4,
            s.product_name_5,
            s.product_name_6,
        ]
        asset_node_dict = s.asset_nodes.read()
        portfolio_composition = []
        total_percentage = 0
        for product, percentage in zip(all_products, all_percentages):
            if product != "":
                asset_dict = asset_node_dict.get(product)
                print(asset_dict)

                asset = Asset(
                    name=product,
                    distribution_type=asset_dict.get("distribution_type"),
                    mean_return=asset_dict.get("mean_retrun"),
                    std_dev=asset_dict.get("std_dev"),
                )
                portfolio_composition.append((asset, percentage / 100))
                total_percentage += percentage

        investment_scenario = InvestmentScenario(
            initial_capital=s.initial_capital,
            horizon_years=s.investment_horizon_years,
            num_trials=s.number_trials,
            portfolio_composition=portfolio_composition,
        )

        if total_percentage != 100:
            notify(s, "e", "All products must sum 100%!")
            return


with tgb.Page() as scenario_creation_page:
    tgb.text("## Portfolio Estimator", mode="md")

    with tgb.layout("1 1 1"):
        tgb.slider(
            "{number_trials}", min=500, max=2_000, labem="Number of Trials", step=500
        )
        tgb.number(
            "{initial_capital}",
            min=1_000,
            label="Initial Capital",
            class_name="fullwidth",
        )
        tgb.number(
            "{investment_horizon_years}",
            min=0,
            label="Investment Horizon (Years)",
            class_name="fullwidth",
        )

    with tgb.part():
        with tgb.layout("1 1 1"):
            tgb.text("**Select Product 1**", mode="md")
            tgb.selector("{product_name_1}", lov="{asset_list}", dropdown=True)
            tgb.number(
                "{percentage_1}",
                min=0,
                max=100,
                class_name="fullwidth",
            )
        with tgb.layout("1 1 1"):
            tgb.text("**Select Product 2**", mode="md")
            tgb.selector("{product_name_2}", lov="{asset_list}", dropdown=True)
            tgb.number(
                "{percentage_2}",
                min=0,
                max=100,
                class_name="fullwidth",
            )
        with tgb.layout("1 1 1"):
            tgb.text("**Select Product 3**", mode="md")
            tgb.selector("{product_name_3}", lov="{asset_list}", dropdown=True)
            tgb.number(
                "{percentage_3}",
                min=0,
                max=100,
                class_name="fullwidth",
            )
        with tgb.layout("1 1 1"):
            tgb.text("**Select Product 4**", mode="md")
            tgb.selector("{product_name_4}", lov="{asset_list}", dropdown=True)
            tgb.number(
                "{percentage_4}",
                min=0,
                max=100,
                class_name="fullwidth",
            )
        with tgb.layout("1 1 1"):
            tgb.text("**Select Product 5**", mode="md")
            tgb.selector("{product_name_5}", lov="{asset_list}", dropdown=True)
            tgb.number(
                "{percentage_5}",
                min=0,
                max=100,
                class_name="fullwidth",
            )
        with tgb.layout("1 1 1"):
            tgb.text("**Select Product 6**", mode="md")
            tgb.selector("{product_name_6}", lov="{asset_list}", dropdown=True)
            tgb.number(
                "{percentage_6}",
                min=0,
                max=100,
                class_name="fullwidth",
            )

    with tgb.layout("1 2"):
        tgb.input("{new_scenario_name}", label="Enter Scenario Name")
        tgb.button(
            "Create Scenario", on_action=create_scenario, class_name="fullwidth plain"
        )
