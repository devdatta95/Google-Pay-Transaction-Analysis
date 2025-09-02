# gpay_insights/figures/txn_count.py
from __future__ import annotations
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from .. import config


def monthly_txn_count_figure(df: pd.DataFrame, date_col: str) -> go.Figure:
    """
    Completed-only dataframe expected (we pass dff_c from callbacks).
    Builds a monthly transaction count bar chart with MoM coloring and a 3-month rolling average line.
    """
    fig = go.Figure()

    # Empty / missing date column guard
    if df is None or df.empty or date_col not in df.columns:
        fig.update_layout(
            template="plotly_white",
            title="Monthly Transaction Count (with 3-mo Average)",
            height=getattr(config, "FIG_H", 360),
            autosize=True,
            margin=dict(t=70, l=50, r=30, b=40),
        )
        fig.add_annotation(
            text="No data in current filter",
            showarrow=False, x=0.5, y=0.5, xref="paper", yref="paper"
        )
        return fig

    # Ensure datetime dtype (tz-naive OK)
    dff = df.copy()
    dff[date_col] = pd.to_datetime(dff[date_col], errors="coerce")
    dff = dff[dff[date_col].notna()].copy()
    if dff.empty:
        return fig

    # Monthly bucket: convert to monthly period, then to timestamp at period start
    # NOTE: DO NOT pass "MS" to to_timestamp(); just call without args (defaults to start for monthly).
    dff["_month"] = dff[date_col].dt.to_period("M").dt.to_timestamp()

    # Aggregate counts by month (robust: use .size())
    monthly = (
        dff.groupby("_month")
           .size()
           .rename("txn")
           .reset_index()
           .rename(columns={"_month": "month"})
           .sort_values("month")
    )

    if monthly.empty:
        fig.update_layout(
            template="plotly_white",
            title="Monthly Transaction Count (with 3-mo Average)",
            height=getattr(config, "FIG_H", 360),
            autosize=True,
            margin=dict(t=70, l=50, r=30, b=40),
        )
        fig.add_annotation(
            text="No data in current filter",
            showarrow=False, x=0.5, y=0.5, xref="paper", yref="paper"
        )
        return fig

    # Rolling 3-month average
    monthly["txn_ma3"] = monthly["txn"].rolling(3, min_periods=1).mean()

    # MoM deltas
    monthly["mom_abs"] = monthly["txn"].diff()
    monthly["mom_pct"] = monthly["txn"].pct_change() * 100
    monthly["is_up"]   = monthly["mom_abs"].fillna(0) >= 0

    # Display helpers for hover
    monthly["mom_abs_disp"] = monthly["mom_abs"].fillna(0).astype(int)
    monthly["mom_pct_disp"] = monthly["mom_pct"].fillna(0.0)

    # Bars colored by up/down
    bar_colors = np.where(monthly["is_up"], "seagreen", "crimson")
    fig.add_bar(
        x=monthly["month"],
        y=monthly["txn"],
        name="# Transactions",
        marker=dict(color=bar_colors),
        text=monthly["txn"].map(lambda v: f"{v:,}"),
        textposition="outside",
        customdata=np.c_[monthly["mom_abs_disp"], monthly["mom_pct_disp"]],
        hovertemplate=(
            "%{x|%b %Y}<br>"
            "# Txn: %{y:,}"
            "<br>MoM: %{customdata[0]:,} "
            "(%{customdata[1]:.1f}%)"
            "<extra></extra>"
        ),
    )

    # Legend-only markers to explain bar colors
    fig.add_scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color="seagreen"),
        name="MoM Up (≥ 0)", showlegend=True
    )
    fig.add_scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color="crimson"),
        name="MoM Down (< 0)", showlegend=True
    )

    # Rolling average line
    fig.add_scatter(
        x=monthly["month"],
        y=monthly["txn_ma3"],
        mode="lines+markers",
        name="3-mo Avg",
        line=dict(dash="dot"),
        hovertemplate="%{x|%b %Y}<br>3-mo Avg: %{y:,.0f}<extra></extra>",
    )

    # Axes + layout
    fig.update_yaxes(title_text="# Transactions", tickformat=",.0f", automargin=True)
    fig.update_xaxes(title_text="", automargin=True)
    fig.update_layout(
        title="Monthly Transaction Count (with 3-mo Average)",
        template="plotly_white",
        bargap=0.25,
        legend_title_text="",
        margin=dict(t=70, l=50, r=30, b=40),
        height=getattr(config, "FIG_H", 360),
        autosize=True,
        uirevision="keep",
    )
    return fig
