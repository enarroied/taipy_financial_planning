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
        tgb.chart(figure="{comp_mean_pct_return_figure}")
        tgb.chart(figure="{comp_mean_cagr_figure}")
        tgb.chart(figure="{comp_mean_final_value_figure}")

    tgb.html("hr")
    tgb.text("### Risk Metrics", mode="md")
    with tgb.layout("1 1 1"):
        tgb.chart(figure="{comp_std_total_return_figure}")
        tgb.chart(figure="{comp_std_pct_return_figure}")
        tgb.chart(figure="{comp_prob_loss_figure}")

    tgb.html("hr")
    tgb.text("### Distribution Metrics", mode="md")
    with tgb.layout("1 1"):
        tgb.chart(figure="{comp_percentile_5_figure}")
        tgb.chart(figure="{comp_percentile_95_figure}")

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
