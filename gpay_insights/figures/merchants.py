import numpy as np
import plotly.graph_objects as go
from .. import config
from ..utils.formatting import indian_number

def merchant_pareto_figure(dff, merchant_col, amt_col, topn=25):
    """
    Pareto of merchants (Completed Outflow), with:
    - X labels outside (rotated 90°)
    - Legend centered under title (no overlap)
    - Y axis in ₹ with Indian commas (no k/M)
    - Double height for readability
    """
    if not merchant_col or dff.empty:
        return go.Figure().update_layout(title=f"Merchant Pareto (Top {topn})")

    m = (
        dff.loc[dff["_flow"] == "Outflow"]
           .groupby(merchant_col)[amt_col].sum()
           .sort_values(ascending=False).head(int(topn)).reset_index()
    )
    if m.empty:
        return go.Figure().update_layout(title=f"Merchant Pareto (Top {topn})")

    total = float(m[amt_col].sum()) or 1.0
    m["cum_share"] = m[amt_col].cumsum() / total

    fig = go.Figure()

    # Bars
    fig.add_bar(
        x=m[merchant_col],
        y=m[amt_col],
        name="Outflow",
        hovertemplate="%{x}<br>₹%{y:,.0f}<extra></extra>",
    )

    # Cumulative share line (right axis)
    fig.add_scatter(
        x=m[merchant_col],
        y=m["cum_share"],
        yaxis="y2",
        mode="lines+markers",
        name="Cumulative share",
        hovertemplate="%{y:.0%}<extra></extra>",
        line=dict(width=2),
        marker=dict(size=6),
    )

    # Stable rupee y-axis (no k/M), with Indian commas
    ymax = float(m[amt_col].max()) * 1.08
    ticks = np.linspace(0, ymax, 6)
    tickvals = [float(t) for t in ticks]
    ticktext = [indian_number(t) for t in ticks]

    fig.update_layout(
        title=f"Merchant Pareto (Top {int(topn)}, Completed Outflow)",
        autosize=True,
        margin=dict(t=80, r=80, b=190, l=76), # big bottom for 90° labels
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,                            # just below the title
            xanchor="center",
            x=0.5,
        ),
        xaxis=dict(
            title="Merchant",
            tickangle=90,                      # vertical labels
            tickfont=dict(size=10),
            title_standoff=6,
        ),
        yaxis=dict(
            title="Amount (₹)",
            range=[0, ymax],
            tickmode="array",
            tickvals=tickvals,
            ticktext=ticktext,
        ),
        yaxis2=dict(
            title="Cumulative share",
            overlaying="y",
            side="right",
            range=[0, 1.05],
            tickformat=".0%",
        ),
        hovermode="x unified",
    )

    return fig
