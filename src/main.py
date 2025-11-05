# from config.config import calculate_investment_scenario
from config.config import asset_nodes_config
from pages import (
    asset_creation_page,
    compare_scenarios_page,
    root,
    scenario_creation_page,
)
from taipy.gui import Gui

import taipy as tp
from taipy import Orchestrator

pages = {
    "/": root,
    "asset_creation": asset_creation_page,
    "scenario_creation": scenario_creation_page,
    "compare_scenarios": compare_scenarios_page,
}
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

    Gui(pages=pages).run(
        use_reloader=True,
        title="Investment 💵 Scenarios",
        dark_mode=False,
    )
