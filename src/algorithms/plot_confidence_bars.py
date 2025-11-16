import pandas as pd
import plotly.graph_objects as go


def plot_confidence_bands(
    time_stats: pd.DataFrame,
    initial_capital: float,
    title: str = "Portfolio Value Over Time with Confidence Bands",
):
    """
    Plot mean/median with percentile confidence bands.

    Args:
        time_stats: DataFrame from calculate_time_series_statistics
        initial_capital: Starting investment amount
        title: Chart title

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    # Add confidence bands - 90% confidence band (p5 to p95)
    fig.add_trace(
        go.Scatter(
            x=time_stats["year"],
            y=time_stats["p95"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=time_stats["year"],
            y=time_stats["p5"],
            mode="lines",
            line=dict(width=0),
            fillcolor="rgba(68, 168, 228, 0.15)",
            fill="tonexty",
            name="5th-95th Percentile",
            hovertemplate="5th: $%{y:,.0f}<extra></extra>",
        )
    )

    # 50% confidence band (p25 to p75)
    fig.add_trace(
        go.Scatter(
            x=time_stats["year"],
            y=time_stats["p75"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=time_stats["year"],
            y=time_stats["p25"],
            mode="lines",
            line=dict(width=0),
            fillcolor="rgba(68, 168, 228, 0.3)",
            fill="tonexty",
            name="25th-75th Percentile",
            hovertemplate="25th: $%{y:,.0f}<extra></extra>",
        )
    )

    # mean line
    fig.add_trace(
        go.Scatter(
            x=time_stats["year"],
            y=time_stats["mean"],
            mode="lines+markers",
            name="Mean",
            line=dict(color="rgb(31, 119, 180)", width=3),
            hovertemplate="Mean: $%{y:,.0f}<extra></extra>",
        )
    )

    # median line
    fig.add_trace(
        go.Scatter(
            x=time_stats["year"],
            y=time_stats["median"],
            mode="lines+markers",
            name="Median",
            line=dict(color="rgb(255, 127, 14)", width=3, dash="dash"),
            hovertemplate="Median: $%{y:,.0f}<extra></extra>",
        )
    )

    # initial capital reference line
    fig.add_hline(
        y=initial_capital,
        line_dash="dot",
        line_color="gray",
        annotation_text="Initial Capital",
        annotation_position="right",
    )

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Portfolio Value ($)",
        hovermode="x unified",
        template="plotly_white",
        height=500,
    )

    return fig
