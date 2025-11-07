from taipy import Config, Scope

from algorithms import (
    calculate_initial_allocations,
    generate_return_matrix,
    simulate_portfolio_evolution,
)

asset_nodes_config = Config.configure_json_data_node(
    id="assets", default_path="./data/assets.json", scope=Scope.GLOBAL
)
investment_scenario_node_config = Config.configure_data_node(
    id="investment_scenario",
)


# Scenario
calculate_investment_scenario = Config.configure_scenario(id="calculate_investment")
