import plotly.graph_objects as go


def indicator_metric(
    value,
    delta=None,
    threshold=None,
    max_value=None,
    title="",  # The 'title' argument is still needed
    number_format=None,
    delta_format=None,
    gauge_bar_color="hotpink",
    threshold_color="red",
    width=600,
    height=500,
):
    """
    Create a Plotly indicator figure similar to Taipy's tgb.metric() component.
    """

    max_val = max_value if max_value is not None else value * 1.2
    gauge_cfg = {
        "axis": {"range": [0, max_val]},
        "bar": {"color": gauge_bar_color},
    }
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

    number_cfg = {"valueformat": number_format} if number_format else {}
    if title:
        number_cfg["suffix"] = (
            f"<br>{title}"  # Instead of using title argument that messes with layout...
        )

    fig = go.Figure(
        go.Indicator(
            mode="number+gauge+delta" if delta is not None else "number+gauge",
            value=value,
            number=number_cfg,
            delta=delta_cfg,
            gauge=gauge_cfg,
            title={},
        )
    )
    fig.update_layout(width=width, height=height, margin=dict(t=5, b=5, l=5, r=5))
    return fig
