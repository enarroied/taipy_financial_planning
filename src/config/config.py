from taipy import Config, Scope

from algorithms import (
    calculate_drawdown_statistics,
    calculate_initial_allocations,
    calculate_portfolio_evolution,
    calculate_return_matrix,
    calculate_summary_statistics,
    calculate_time_series_statistics,
    plot_confidence_bands,
)

# data nodes
asset_nodes_config = Config.configure_json_data_node(
    id="assets", default_path="./data/assets.json", scope=Scope.GLOBAL
)
investment_assumption_node_config = Config.configure_data_node(
    id="investment_assumption",
)
initial_allocation_node_config = Config.configure_data_node(
    id="initial_allocation",
)
return_matrix_node_config = Config.configure_data_node(
    id="return_matrix",
)
result_portfolio_node_config = Config.configure_csv_data_node(
    id="result_portfolio",
)
summary_statistics_node_config = Config.configure_data_node(
    id="summary_stats",
)
drawdown_statistics_node_config = Config.configure_data_node(
    id="drawdown_statistics",
)
time_series_node_config = Config.configure_csv_data_node(
    id="time_series",
)
confidence_bands_node_config = Config.configure_data_node(
    id="confidence_bands",
)
# Tasks
calculate_initial_allocation_task_congig = Config.configure_task(
    id="calculate_initial_allocation",
    function=calculate_initial_allocations,
    input=investment_assumption_node_config,
    output=initial_allocation_node_config,
)
calculate_return_matrix_task_config = Config.configure_task(
    id="calculate_return_matrix",
    function=calculate_return_matrix,
    input=investment_assumption_node_config,
    output=return_matrix_node_config,
)
calculate_portfolio_evolution_task_config = Config.configure_task(
    id="calculate_portfolio_evolution",
    function=calculate_portfolio_evolution,
    input=[
        initial_allocation_node_config,
        return_matrix_node_config,
        investment_assumption_node_config,
    ],
    output=result_portfolio_node_config,
)
calculate_summary_statistics_task_config = Config.configure_task(
    id="calculate_summary_statistics",
    function=calculate_summary_statistics,
    input=[result_portfolio_node_config, investment_assumption_node_config],
    output=summary_statistics_node_config,
)
calculate_drawdown_statistics_task_config = Config.configure_task(
    id="calculate_drawdown_statistics",
    function=calculate_drawdown_statistics,
    input=[result_portfolio_node_config],
    output=drawdown_statistics_node_config,
)
calculate_time_series_statistics_task_config = Config.configure_task(
    id="calculate_time_series_statistics",
    function=calculate_time_series_statistics,
    input=[result_portfolio_node_config, investment_assumption_node_config],
    output=time_series_node_config,
)
plot_confidence_bands_task_config = Config.configure_task(
    id="plot_confidence_bands",
    function=plot_confidence_bands,
    input=[time_series_node_config, investment_assumption_node_config],
    output=confidence_bands_node_config,
)

# Scenario
generate_investment_scenario_config = Config.configure_scenario(
    id="calculate_investment",
    task_configs=[
        calculate_initial_allocation_task_congig,
        calculate_return_matrix_task_config,
        calculate_portfolio_evolution_task_config,
        calculate_summary_statistics_task_config,
        calculate_drawdown_statistics_task_config,
        calculate_time_series_statistics_task_config,
        plot_confidence_bands_task_config,
    ],
    additional_data_node_configs=asset_nodes_config,
)
Config.export("config.toml")
