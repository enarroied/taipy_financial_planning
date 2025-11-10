import taipy as tp

from algorithms.callback_helpers import (
    cond_eq_notify,
    cond_in_notify,
    cond_neq_notify,
    has_nonempty_duplicates_notify,
)
from config import generate_investment_scenario_config
from context import Asset, InvestmentAssumption


def _select_pecentages(state):
    with state as s:
        return [
            int(s.percentage_1),
            int(s.percentage_2),
            int(s.percentage_3),
            int(s.percentage_4),
            int(s.percentage_5),
            int(s.percentage_6),
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
            initial_capital=int(s.initial_capital),
            horizon_years=int(s.investment_horizon_years),
            num_trials=int(s.number_trials),
            portfolio_composition=portfolio_composition,
            asset_names=[asset.name for asset, _ in portfolio_composition],
        )


def _create_portfolio_composition(state, all_products, all_percentages):
    with state as s:
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
        return portfolio_composition, total_percentage


def create_scenario(state):
    with state as s:
        if cond_eq_notify(s, (s.new_scenario_name, ""), "Scenario has no name!"):
            return
        sc_names = [scenario.name for scenario in tp.get_scenarios()]
        if cond_in_notify(s, (s.new_scenario_name, sc_names), "Scenario name Exists!"):
            return

        all_percentages = _select_pecentages(s)
        all_products = _select_products(s)

        if has_nonempty_duplicates_notify(s, all_products, "Duplicate Assets!"):
            return

        portfolio_composition, total_percentage = _create_portfolio_composition(
            state, all_products, all_percentages
        )

        if cond_neq_notify(s, (total_percentage, 100), "All products must sum 100%!"):
            return

        investment_assumption = _create_investment_assumption(s, portfolio_composition)
        new_scenario = tp.create_scenario(
            generate_investment_scenario_config, name=s.new_scenario_name
        )
        new_scenario.investment_assumption.write(investment_assumption)
        new_scenario.submit()
        s.selected_scenario_outcome = new_scenario.result_portfolio.read()
        s.selected_scenario = new_scenario
