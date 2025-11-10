import taipy.gui.builder as tgb

from algorithms.scenario_creation_callbacks import create_scenario
from pages.page_helpers import create_card, product_selector_block


def change_scenario(state):
    with state as s:
        s.selected_scenario_outcome = s.selected_scenario.result_portfolio.read()
        s.summary_stats = s.selected_scenario.summary_stats.read()


with tgb.Page() as scenario_creation_page:
    tgb.text("## Create **Portfolio** Scenario", mode="md")

    with tgb.expandable(title="Scenario Creation", expanded=False):
        with tgb.layout("1 1 1"):
            tgb.slider(
                "{number_trials}",
                min=500,
                max=2_000,
                labem="Number of Trials",
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
            "Create Scenario", on_action=create_scenario, class_name="fullwidth plain"
        )
    # New Part:
    # tgb.scenario_dag("{selected_scenario}")  # TODO: remove
    with tgb.layout("1 2"):
        tgb.scenario_selector("{selected_scenario}", on_change=change_scenario)
        with tgb.part():
            tgb.text("## Scneario Results", mode="md")
            tgb.table(
                "{selected_scenario_outcome}",
                rebuild=True,
                page_size=20,
                number_format="%,d",
            )
            with tgb.layout("1 1 1 1"):
                create_card("Mean Final Value", "{summary_stats.mean_final_value}")
                create_card("Median Final Value", "{summary_stats.median_final_value}")
                create_card("Mean Total Return", "{summary_stats.mean_total_return}")
                create_card(
                    "Median Total Return", "{summary_stats.median_total_return}"
                )
                create_card(
                    "Standard Deviation for Total Return",
                    "{summary_stats.std_total_return}",
                )
                create_card("Mean Percentage Return", "{summary_stats.mean_pct_return}")
                create_card(
                    "Median Percentage Return", "{summary_stats.median_pct_return}"
                )
                create_card(
                    "Standard Deviation of Percentage Return",
                    "{summary_stats.std_pct_return}",
                )
                create_card("Mean Anualized Return", "{summary_stats.mean_cagr}")
                create_card("Median Anualized Return", "{summary_stats.median_cagr}")
                # Risk Metrics
                create_card("Minimal Final Value", "{summary_stats.min_final_value}")
                create_card("Maximum Final Value", "{summary_stats.max_final_value}")
                create_card("5th Percentile", "{summary_stats.percentile_5}")
                create_card("25th Percentile", "{summary_stats.percentile_25}")
                create_card("75th Percentile", "{summary_stats.percentile_75}")
                create_card("95th Percentile", "{summary_stats.percentile_95}")
                create_card("Probability Loss", "{summary_stats.prob_loss}")
