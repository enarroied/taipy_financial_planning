import plotly.graph_objects as go


def indicator_metric(
    value,
    delta=None,
    threshold=None,
    max_value=None,
    title="",
    number_format=None,
    delta_format=None,
    gauge_bar_color="hotpink",
    threshold_color="red",
    width=300,
    height=200,
):
    """
    Create a Plotly indicator figure similar to Taipy's tgb.metric() component.
    """

    max_val = max_value if max_value is not None else value * 1.2

    # Configure gauge block
    gauge_cfg = {
        "axis": {"range": [0, max_val]},
        "bar": {"color": gauge_bar_color},
    }

    # Add threshold if provided
    if threshold is not None:
        gauge_cfg["threshold"] = {
            "line": {"color": threshold_color, "width": 3},
            "thickness": 0.75,
            "value": threshold,
        }

    # Delta must be dict for plotly
    delta_cfg = None
    if delta is not None:
        delta_cfg = {
            "reference": value - delta,
            "valueformat": delta_format if delta_format else None,
        }

    fig = go.Figure(
        go.Indicator(
            mode="number+gauge+delta" if delta is not None else "number+gauge",
            value=value,
            number={"valueformat": number_format} if number_format else {},
            delta=delta_cfg,
            gauge=gauge_cfg,  #  <<<<<< FIXED
            title={"text": title},
        )
    )

    fig.update_layout(width=width, height=height, margin=dict(t=40, b=20))
    return fig
