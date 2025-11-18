import taipy.gui.builder as tgb

from algorithms.scenario_creation_callbacks import change_scenario
from pages.page_helpers import (
    investment_scenario_selector,
    scenario_results_section,
)

with tgb.Page() as scenario_comparison_page:
    tgb.text("## **Compare** Scenarios", mode="md")

    with tgb.expandable(title="Scenario Results", expanded=True):
        with tgb.layout("1 1"):
            with tgb.part():
                # TODO: make scenario variable in change_scenario callback!!
                investment_scenario_selector(
                    "comparison_scenario_1",
                    "comparison_scenario_1_assumption",
                    change_scenario,
                )
                scenario_results_section(
                    "comparison_scenario_1_outcome",
                    "comparison_scenario_1_summary_stats",
                    "comparison_scenario_1_time_series",
                    "comparison_scenario_1_confidence_bands",
                )
            with tgb.part():
                investment_scenario_selector(
                    "comparison_scenario_2",
                    "comparison_scenario_2_assumption",
                    change_scenario,
                )
                scenario_results_section(
                    "comparison_scenario_2_outcome",
                    "comparison_scenario_2_summary_stats",
                    "comparison_scenario_2_time_series",
                    "comparison_scenario_2_confidence_bands",
                )
