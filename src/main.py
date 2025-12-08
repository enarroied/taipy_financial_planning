# from config.config import calculate_investment_scenario
import taipy as tp
from taipy import Orchestrator
from taipy.gui import Gui

from config import asset_nodes_config
from create_demo_scenarios import scenario1, scenario2, scenario3
from pages import (
    asset_creation_page,
    root,
    scenario_comparison_page,
    scenario_creation_page,
)
from algorithms.scenario_creation_callbacks import calculate_scenario_comparison

pages = {
    "/": root,
    "asset_creation": asset_creation_page,
    "scenario_creation": scenario_creation_page,
    "compare_scenarios": scenario_comparison_page,
}
stylekit = {
    "color_primary": "#5c0329",
}


def get_scenario_data(scenario_object):
    return (
        scenario_object,
        scenario_object.result_portfolio.read(),
        scenario_object.investment_assumption.read(),
        scenario_object.summary_stats.read(),
        scenario_object.drawdown_statistics.read(),
        scenario_object.time_series.read(),
        scenario_object.confidence_bands.read(),
    )


if __name__ == "__main__":
    number_trials = 1_000
    initial_capital = 10_000
    investment_horizon_years = 10

    product_name_1 = ""
    percentage_1 = 0
    product_name_2 = ""
    percentage_2 = 0
    product_name_3 = ""
    percentage_3 = 0
    product_name_4 = ""
    percentage_4 = 0
    product_name_5 = ""
    percentage_5 = 0
    product_name_6 = ""
    percentage_6 = 0

    new_scenario_name = ""

    Orchestrator().run()

    asset_nodes = tp.create_global_data_node(asset_nodes_config)
    asset_nodes_dict = asset_nodes.read()
    asset_list = list(asset_nodes_dict.keys())
    # selected_asset_for_edit = asset_list[0]

    # For asset edits:
    selected_asset_for_edit = ""
    asset_for_edit_distribution_type = ""
    asset_for_edit_mean_return = 0
    asset_for_edit_std_dev = 0

    new_asset_name = ""
    selected_asset_for_deletion = ""
    delete_asset_dialog = False

    # Submit demo scenarios:
    for scenario in [scenario1, scenario2, scenario3]:
        scenario.submit()
    (
        selected_scenario,
        selected_scenario_outcome,
        selected_scenario_assumption,
        selected_summary_stats,
        selected_drawdown_statistics,
        selected_time_series,
        selected_confidence_bands,
    ) = get_scenario_data(scenario1)
    (
        comparison_scenario_1,
        comparison_scenario_1_outcome,
        comparison_scenario_1_assumption,
        comparison_scenario_1_summary_stats,
        comparison_scenario_1_drawdown_statistics,
        comparison_scenario_1_time_series,
        comparison_scenario_1_confidence_bands,
    ) = get_scenario_data(scenario1)
    (
        comparison_scenario_2,
        comparison_scenario_2_outcome,
        comparison_scenario_2_assumption,
        comparison_scenario_2_summary_stats,
        comparison_scenario_2_drawdown_statistics,
        comparison_scenario_2_time_series,
        comparison_scenario_2_confidence_bands,
    ) = get_scenario_data(scenario2)

    comparison_metrics = calculate_scenario_comparison(
        comparison_scenario_1,
        comparison_scenario_2
    )

    # Unpack all comparison values
    comp_mean_total_return_value = comparison_metrics['comp_mean_total_return_value']
    comp_mean_total_return_threshold = comparison_metrics['comp_mean_total_return_threshold']
    comp_mean_total_return_delta = comparison_metrics['comp_mean_total_return_delta']

    comp_mean_pct_return_value = comparison_metrics['comp_mean_pct_return_value']
    comp_mean_pct_return_threshold = comparison_metrics['comp_mean_pct_return_threshold']
    comp_mean_pct_return_delta = comparison_metrics['comp_mean_pct_return_delta']

    comp_mean_cagr_value = comparison_metrics['comp_mean_cagr_value']
    comp_mean_cagr_threshold = comparison_metrics['comp_mean_cagr_threshold']
    comp_mean_cagr_delta = comparison_metrics['comp_mean_cagr_delta']

    comp_mean_final_value_value = comparison_metrics['comp_mean_final_value_value']
    comp_mean_final_value_threshold = comparison_metrics['comp_mean_final_value_threshold']
    comp_mean_final_value_delta = comparison_metrics['comp_mean_final_value_delta']

    comp_std_total_return_value = comparison_metrics['comp_std_total_return_value']
    comp_std_total_return_threshold = comparison_metrics['comp_std_total_return_threshold']
    comp_std_total_return_delta = comparison_metrics['comp_std_total_return_delta']

    comp_std_pct_return_value = comparison_metrics['comp_std_pct_return_value']
    comp_std_pct_return_threshold = comparison_metrics['comp_std_pct_return_threshold']
    comp_std_pct_return_delta = comparison_metrics['comp_std_pct_return_delta']

    comp_prob_loss_value = comparison_metrics['comp_prob_loss_value']
    comp_prob_loss_threshold = comparison_metrics['comp_prob_loss_threshold']
    comp_prob_loss_delta = comparison_metrics['comp_prob_loss_delta']

    comp_percentile_5_value = comparison_metrics['comp_percentile_5_value']
    comp_percentile_5_threshold = comparison_metrics['comp_percentile_5_threshold']
    comp_percentile_5_delta = comparison_metrics['comp_percentile_5_delta']

    comp_percentile_95_value = comparison_metrics['comp_percentile_95_value']
    comp_percentile_95_threshold = comparison_metrics['comp_percentile_95_threshold']
    comp_percentile_95_delta = comparison_metrics['comp_percentile_95_delta']



    Gui(pages=pages, css_file="css/main.css").run(
        title="Investment 💵 Scenarios",
        favicon="img/favicon.ico",
        dark_mode=False,
        stylekit=stylekit,
        use_reloader=True,
    )
