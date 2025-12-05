import taipy.gui.builder as tgb


def product_selector_block(
    product_number: str, product_name: str, asset_list: list, percentage: str
):
    with tgb.layout("1 1 1"):
        tgb.text(f"**Select Product {product_number}**", mode="md")
        tgb.selector(product_name, lov=asset_list, dropdown=True)
        tgb.number(
            percentage,
            min=0,
            max=100,
            class_name="fullwidth",
        )


def create_card(title, data, units=""):
    with tgb.part(class_name="card"):
        tgb.text(f"### {title}", mode="md")
        with tgb.layout("3 1"):
            tgb.text(f"{data}", mode="md", format="%,f", class_name="card-number")
            tgb.text(f"### {units}", mode="md")


def tpl(expr: str):
    return "{" + expr + "}"


def investment_scenario_selector(
    selected_scenario, selected_scenario_assumption, change_callback
):
    with tgb.part():
        tgb.scenario_selector(
            tpl(selected_scenario), on_change=change_callback, show_add_button=False
        )

        create_card(
            "Initial Capital",
            tpl(f"{selected_scenario_assumption}.initial_capital"),
            units="USD",
        )

        create_card(
            "Investment Horizon",
            tpl(f"{selected_scenario_assumption}.horizon_years"),
            units="years",
        )
        with tgb.part(class_name="card"):
            tgb.text("### Portfolio Composition", mode="md")
            tgb.text(
                tpl(f"{selected_scenario_assumption}.simple_portfolio_composition"),
                mode="pre",
            )


def scenario_results_section(
    outcome_var: str, ss: str, time_series: str, selected_confidence_bands: str
):
    """
    outcome_var (str): The name of the pandas DataFrame with the Scenario's raw results
    ss (str): The name of the  SummaryStatistics instance
    """
    with tgb.part():
        tgb.text("## Scenario Results", mode="md")

        with tgb.expandable("Raw Results", expanded=False):
            tgb.table(
                tpl(outcome_var),
                rebuild=True,
                page_size=20,
                number_format="%,d",
            )
        with tgb.expandable("Final values", expanded=False):
            with tgb.layout("1 1 1 1"):
                create_card("Mean Final Value", tpl(f"{ss}.mean_final_value"))
                create_card("Median Final Value", tpl(f"{ss}.median_final_value"))

            tgb.text("## **Return** values", mode="md")
            with tgb.layout("1 1 1 1"):
                create_card("Mean Total Return", tpl(f"{ss}.mean_total_return"))
                create_card("Median Total Return", tpl(f"{ss}.median_total_return"))
                create_card("StD - Total Return", tpl(f"{ss}.std_total_return"))
                create_card("Mean Percentage Return", tpl(f"{ss}.mean_pct_return"))
                create_card("Median Percentage Return", tpl(f"{ss}.median_pct_return"))
                create_card("StD - Percentage Return", tpl(f"{ss}.std_pct_return"))
                create_card("Mean Annualized Return", tpl(f"{ss}.mean_cagr"))
                create_card("Median Annualized Return", tpl(f"{ss}.median_cagr"))

            tgb.text("## **Risk** metrics", mode="md")
            with tgb.layout("1 1 1 1"):
                create_card("Minimal Final Value", tpl(f"{ss}.min_final_value"))
                create_card("Maximum Final Value", tpl(f"{ss}.max_final_value"))
                create_card("5th Percentile", tpl(f"{ss}.percentile_5"))
                create_card("25th Percentile", tpl(f"{ss}.percentile_25"))
                create_card("75th Percentile", tpl(f"{ss}.percentile_75"))
                create_card("95th Percentile", tpl(f"{ss}.percentile_95"))
                create_card("Probability Loss", tpl(f"{ss}.prob_loss"))

        with tgb.expandable("Time Series", expanded=False):
            tgb.table(
                tpl(f"{time_series}"),
                rebuild=True,
                page_size=5,
                number_format="%,d",
            )

            tgb.chart(figure=tpl(f"{selected_confidence_bands}"), rebuild=True)
