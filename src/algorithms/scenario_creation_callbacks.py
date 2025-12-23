import taipy as tp

from algorithms.callback_helpers import (
    cond_eq_notify,
    cond_in_notify,
    cond_neq_notify,
    has_nonempty_duplicates_notify,
)
from algorithms.plot_kpis import indicator_metric
from config import generate_investment_scenario_config
from context import Asset, InvestmentAssumption


def create_scenario(state):
    with state as s:
        all_percentages = _select_pecentages(s)
        all_products = _select_products(s)
        portfolio_composition, total_percentage = _create_portfolio_composition(
            s, all_products, all_percentages
        )
        if _check_conditions(s, total_percentage, all_products):
            return

        investment_assumption = _create_investment_assumption(s, portfolio_composition)
        new_scenario = tp.create_scenario(
            generate_investment_scenario_config, name=s.new_scenario_name
        )
        new_scenario.investment_assumption.write(investment_assumption)
        new_scenario.submit()
        s.selected_scenario_outcome = new_scenario.result_portfolio.read()
        s.selected_scenario = new_scenario
        change_scenario(s, var_name="selected_scenario", scenario_var=new_scenario)


def change_scenario(state, var_name, scenario_var):
    if var_name == "selected_scenario":
        with state as s:
            s.selected_scenario_outcome = scenario_var.result_portfolio.read()
            s.selected_scenario_assumption = scenario_var.investment_assumption.read()
            s.selected_summary_stats = scenario_var.summary_stats.read()
            s.selected_time_series = scenario_var.time_series.read()
            s.selected_confidence_bands = scenario_var.confidence_bands.read()
    elif var_name == "comparison_scenario_1":
        with state as s:
            s.comparison_scenario_1_outcome = scenario_var.result_portfolio.read()
            s.comparison_scenario_1_assumption = (
                scenario_var.investment_assumption.read()
            )
            s.comparison_scenario_1_summary_stats = scenario_var.summary_stats.read()
            s.comparison_scenario_1_time_series = scenario_var.time_series.read()
            s.comparison_scenario_1_confidence_bands = (
                scenario_var.confidence_bands.read()
            )
            create_comparison(s)
    elif var_name == "comparison_scenario_2":
        with state as s:
            s.comparison_scenario_2_outcome = scenario_var.result_portfolio.read()
            s.comparison_scenario_2_assumption = (
                scenario_var.investment_assumption.read()
            )
            s.comparison_scenario_2_summary_stats = scenario_var.summary_stats.read()
            s.comparison_scenario_2_time_series = scenario_var.time_series.read()
            s.comparison_scenario_2_confidence_bands = (
                scenario_var.confidence_bands.read()
            )
            create_comparison(s)


def create_comparison(state):
    """Creates the values to compare one Scenario to another"""
    with state as s:
        reference_scenario = s.comparison_scenario_1
        scenario_for_comparison = s.comparison_scenario_2

        # Get all comparison metrics
        comparison_results = calculate_scenario_comparison(
            reference_scenario, scenario_for_comparison
        )

        # Update state with all results
        for key, value in comparison_results.items():
            setattr(s, key, value)


def calculate_scenario_comparison(reference_scenario, comparison_scenario):
    """
    Compare two scenarios and return all comparison metrics.

    Args:
        reference_scenario: First scenario object (Scenario 1)
        comparison_scenario: Second scenario object (Scenario 2)

    Returns:
        Dictionary with all comparison metrics
    """
    reference_stats = reference_scenario.summary_stats.read()
    comparison_stats = comparison_scenario.summary_stats.read()

    # List of metrics to compare: (attribute_name, prefix_for_state_vars)
    metrics = [
        ("mean_total_return", "comp_mean_total_return"),
        ("mean_pct_return", "comp_mean_pct_return"),
        ("mean_cagr", "comp_mean_cagr"),
        ("mean_final_value", "comp_mean_final_value"),
        ("std_total_return", "comp_std_total_return"),
        ("std_pct_return", "comp_std_pct_return"),
        ("prob_loss", "comp_prob_loss"),
        ("percentile_5", "comp_percentile_5"),
        ("percentile_95", "comp_percentile_95"),
    ]

    comparison_results = {}

    for attr_name, prefix in metrics:
        reference_value = getattr(reference_stats, attr_name)
        comparison_value = getattr(comparison_stats, attr_name)

        comparison_results[f"{prefix}_value"] = reference_value
        comparison_results[f"{prefix}_threshold"] = comparison_value
        delta = reference_value - comparison_value
        comparison_results[f"{prefix}_delta"] = delta
        max_value = max(reference_value, comparison_value)
        comparison_results[f"{prefix}_max_value"] = max_value
        comparison_results[f"{prefix}_figure"] = indicator_metric(
            value=reference_value,
            threshold=comparison_value,
            delta=delta,
            max_value=max_value,
            title=prefix,
        )
    return comparison_results


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
            simple_portfolio_composition=[
                (asset.name, percentage) for asset, percentage in portfolio_composition
            ],
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


def _check_conditions(state, total_percentage, all_products):
    sc_names = [scenario.name for scenario in tp.get_scenarios()]

    with state as s:
        return any(
            [
                cond_eq_notify(s, (s.new_scenario_name, ""), "Scenario has no name!"),
                cond_in_notify(
                    s, (s.new_scenario_name, sc_names), "Scenario name Exists!"
                ),
                has_nonempty_duplicates_notify(s, all_products, "Duplicate Assets!"),
                cond_neq_notify(
                    s, (total_percentage, 100), "All products must sum 100%!"
                ),
            ]
        )
