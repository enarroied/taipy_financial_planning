import taipy as tp
import taipy.gui.builder as tgb
from taipy.gui import notify

from config.config import generate_investment_scenario_config
from context import Asset, InvestmentAssumption


def _select_pecentages(state):
    with state as s:
        return [
            s.percentage_1,
            s.percentage_2,
            s.percentage_3,
            s.percentage_4,
            s.percentage_5,
            s.percentage_6,
        ]


def _select_products(state):
    with state as s:
        return [
            s.product_name_1,
            s.product_name_2,
            s.product_name_3,
            s.product_name_4,
            s.product_name_5,
            s.product_name_6,
        ]


def _create_investment_assumption(state, portfolio_composition):
    with state as s:
        return InvestmentAssumption(
            initial_capital=s.initial_capital,
            horizon_years=s.investment_horizon_years,
            num_trials=s.number_trials,
            portfolio_composition=portfolio_composition,
            asset_names=[asset.name for asset, _ in portfolio_composition],
        )


def create_scenario(state):
    with state as s:
        if s.new_scenario_name == "":
            notify(s, "e", "You need to have a name for your Scenario!")
            return

        all_percentages = _select_pecentages(s)
        all_products = _select_products(s)
        asset_node_dict = s.asset_nodes.read()
        portfolio_composition = []
        total_percentage = 0
        for product, percentage in zip(all_products, all_percentages):
            if product != "":
                asset_dict = asset_node_dict.get(product)
                asset = Asset(
                    name=product,
                    distribution_type=asset_dict.get("distribution_type"),
                    mean_return=asset_dict.get("mean_return"),
                    std_dev=asset_dict.get("std_dev"),
                )
                portfolio_composition.append((asset, percentage / 100))
                total_percentage += percentage

        if total_percentage != 100:
            notify(s, "e", "All products must sum 100%!")
            return

        investment_assumption = _create_investment_assumption(s, portfolio_composition)
        new_scenario = tp.create_scenario(
            generate_investment_scenario_config, name=s.new_scenario_name
        )
        print(investment_assumption)
        new_scenario.investment_assumption.write(investment_assumption)
        new_scenario.submit()
        s.selected_scenario_outcome = new_scenario.result_portfolio.read()
        s.selected_scenario = new_scenario


with tgb.Page() as scenario_creation_page:
    tgb.text("## Create **Portfolio** Scenario", mode="md")

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
    tgb.scenario_selector("{selected_scenario}")
    tgb.scenario_dag("{selected_scenario}")
    tgb.table("{selected_scenario_outcome}", rebuild=True)
