import taipy.gui.builder as tgb

from algorithms.scenario_creation_callbacks import change_scenario
from pages.page_helpers import (
    investment_scenario_selector,
    scenario_results_section,
)

with tgb.Page() as scenario_comparison_page:
    tgb.text("## **Compare** Scenarios", mode="md")

    with tgb.expandable(title="Select Scenarios for Comparison", expanded=True):
        with tgb.layout("1 1"):
            investment_scenario_selector(
                "comparison_scenario_1",
                "comparison_scenario_1_assumption",
                change_scenario,
            )
            investment_scenario_selector(
                "comparison_scenario_2",
                "comparison_scenario_2_assumption",
                change_scenario,
            )
    tgb.text("## **Scenario Comparison** Metrics", mode="md")

    tgb.text("### Return Metrics", mode="md")
    with tgb.layout("1 1 1 1"):
        tgb.chart(figure="{comp_mean_total_return_figure}")

        tgb.metric(
            "{comp_mean_pct_return_value}",
            delta="{comp_mean_pct_return_delta}",
            threshold="{comp_mean_pct_return_threshold}",
            max="{comp_mean_pct_return_max_value}",
            title="Mean % Return",
        )
        tgb.metric(
            "{comp_mean_cagr_value}",
            delta="{comp_mean_cagr_delta}",
            threshold="{comp_mean_cagr_threshold}",
            max="{comp_mean_cagr_max_value}",
            title="Mean CAGR",
        )
        tgb.metric(
            "{comp_mean_final_value_value}",
            delta="{comp_mean_final_value_delta}",
            threshold="{comp_mean_final_value_threshold}",
            max="{comp_mean_final_value_max_value}",
            title="Mean Final Value",
        )

    tgb.html("hr")
    tgb.text("### Risk Metrics", mode="md")
    with tgb.layout("1 1 1"):
        tgb.metric(
            "{comp_std_total_return_value}",
            delta="{comp_std_total_return_delta}",
            threshold="{comp_std_total_return_threshold}",
            max="{comp_std_total_return_max_value}",
            title="Std Dev - Total Return",
        )
        tgb.metric(
            "{comp_std_pct_return_value}",
            delta="{comp_std_pct_return_delta}",
            threshold="{comp_std_pct_return_threshold}",
            max="{comp_std_pct_return_max_value}",
            title="Std Dev - % Return",
        )
        tgb.metric(
            "{comp_prob_loss_value}",
            delta="{comp_prob_loss_delta}",
            threshold="{comp_prob_loss_threshold}",
            max="{comp_prob_loss_max_value}",
            title="Probability of Loss (%)",
        )

    tgb.html("hr")
    tgb.text("### Distribution Metrics", mode="md")
    with tgb.layout("1 1"):
        tgb.metric(
            "{comp_percentile_5_value}",
            delta="{comp_percentile_5_delta}",
            threshold="{comp_percentile_5_threshold}",
            max="{comp_percentile_5_max_value}",
            title="5th Percentile (Downside)",
        )
        tgb.metric(
            "{comp_percentile_95_value}",
            delta="{comp_percentile_95_delta}",
            threshold="{comp_percentile_95_threshold}",
            max="{comp_percentile_95_max_value}",
            title="95th Percentile (Upside)",
        )

    tgb.text("## **Side by Side** Comparison", mode="md")
    with tgb.layout("1 1"):
        scenario_results_section(
            "comparison_scenario_1_outcome",
            "comparison_scenario_1_summary_stats",
            "comparison_scenario_1_time_series",
            "comparison_scenario_1_confidence_bands",
        )
        scenario_results_section(
            "comparison_scenario_2_outcome",
            "comparison_scenario_2_summary_stats",
            "comparison_scenario_2_time_series",
            "comparison_scenario_2_confidence_bands",
        )
