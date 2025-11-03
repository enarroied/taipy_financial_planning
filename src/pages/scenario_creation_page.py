import taipy.gui.builder as tgb

with tgb.Page() as scenario_creation_page:
    tgb.text("## Portfolio Estimator", mode="md")

    with tgb.layout("1 1 1"):
        tgb.slider("{number_trials}", min=500, max=10_000, labem="Number of Trials")
        tgb.number("{initial_capital}", min=0, label="Initial Capital")
        tgb.number(
            "{investment_horizon_years}", min=0, label="Investment Horizon (Years)"
        )

    with tgb.part():
        with tgb.layout("1 1 1"):
            tgb.text("**Select Product 1**")
            tgb.selector("{product_name_1}", lov="{asset_list}", dropdown=True)
            tgb.number("{percentage_1}", min=0, max=100)
        with tgb.layout("1 1 1"):
            tgb.text("**Select Product 2**")
            tgb.selector("{product_name_2}", lov="{asset_list}", dropdown=True)
            tgb.number("{percentage_2}", min=0, max=100)
