import taipy.gui.builder as tgb

from algorithms.scenario_creation_callbacks import change_scenario, create_scenario
from pages.page_helpers import (
    investment_scenario_selector,
    product_selector_block,
    scenario_results_section,
)

with tgb.Page() as scenario_creation_page:
    tgb.text("## Create **Portfolio** Scenario", mode="md")

    with tgb.expandable(title="Scenario Creation", expanded=False):
        with tgb.layout("1 1 1"):
            with tgb.layout("1 1"):
                tgb.text("Number of Trials", mode="md")
                tgb.slider(
                    "{number_trials}",
                    min=500,
                    max=2_000,
                    step=500,
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
            product_selector_block(
                "1", "{product_name_1}", "{asset_list}", "{percentage_1}"
            )
            product_selector_block(
                "2", "{product_name_2}", "{asset_list}", "{percentage_2}"
            )
            product_selector_block(
                "3", "{product_name_3}", "{asset_list}", "{percentage_3}"
            )
            product_selector_block(
                "4", "{product_name_4}", "{asset_list}", "{percentage_4}"
            )
            product_selector_block(
                "5", "{product_name_5}", "{asset_list}", "{percentage_5}"
            )
            product_selector_block(
                "6", "{product_name_6}", "{asset_list}", "{percentage_6}"
            )

        with tgb.layout("1 2"):
            tgb.input("{new_scenario_name}", label="Enter Scenario Name")
            tgb.button(
                "Create Scenario",
                on_action=create_scenario,
                class_name="fullwidth plain",
            )

    with tgb.expandable(title="Scenario Results", expanded=True):
        with tgb.layout("1 2"):
            investment_scenario_selector(
                "selected_scenario", "selected_scenario_assumption", change_scenario
            )
            scenario_results_section(
                "selected_scenario_outcome",
                "selected_summary_stats",
                "selected_time_series",
                "selected_confidence_bands",
            )
