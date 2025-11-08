import taipy.gui.builder as tgb

with tgb.Page() as root:
    with tgb.layout("5 1"):
        tgb.text("# Compare Portfolios", mode="md")
        tgb.navbar()
    tgb.html("hr")
