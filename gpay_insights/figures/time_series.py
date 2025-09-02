import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .. import config
from ..utils.formatting import indian_number
from ..utils.filters import apply_completed_only

def _set_stable_y(fig: go.Figure, max_y: float, *, bottom=42, left=64):
    ymax = 0.0 if max_y <= 0 else max_y * 1.08
    ticks = np.linspace(0, ymax, 6)
    fig.update_layout(
        autosize=True,
        margin=dict(t=42, r=20, b=bottom, l=left),
        yaxis=dict(
            range=[0, ymax],
            tickmode="array",
            tickvals=[float(t) for t in ticks],
            ticktext=[indian_number(t) for t in ticks],
            title="Amount (₹)",
        ),
        xaxis=dict(title="Month")
    )
    fig.update_xaxes(title_standoff=28)
    fig.update_yaxes(title_standoff=8)

def add_year_bands(fig: go.Figure, months: pd.Series):
    if months.empty: return
    years = sorted(months.dt.year.unique().tolist())
    for i, y in enumerate(years):
        x0 = pd.Timestamp(year=y, month=1, day=1)
        x1 = pd.Timestamp(year=y, month=12, day=31, hour=23, minute=59, second=59)
        fig.add_vrect(x0=x0, x1=x1,
                      fillcolor="rgba(0,0,0,0.03)" if i % 2 == 0 else "rgba(0,0,0,0.00)",
                      line_width=0, layer="below")
        fig.add_vline(x=x0, line_width=1, line_color="rgba(0,0,0,0.25)")
        fig.add_annotation(x=x0, y=1.02, xref="x", yref="paper",
                           text=str(y), showarrow=False, font=dict(size=10, color="#666"))

def monthly_spend_figure(dff: pd.DataFrame, date_col: str, amt_col: str) -> go.Figure:
    ts = (dff.loc[dff["_flow"]=="Outflow"].groupby("_month")[amt_col].sum().reset_index())
    if ts.empty:
        return go.Figure().update_layout(title="Monthly Spend (Outflow, Completed)")
    ts["y_fmt"] = ts[amt_col].map(indian_number)
    ts["month_label"] = ts["_month"].dt.strftime("%b %Y")
    fig = px.bar(ts, x="_month", y=amt_col, title="Monthly Spend (Outflow, Completed)")
    fig.update_traces(
        hovertemplate="%{x|%b %Y}<br>₹%{customdata}<extra></extra>",
        customdata=ts["y_fmt"],
        text=ts["month_label"], textangle=-90, textposition="inside", insidetextanchor="end",
        cliponaxis=True
    )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    _set_stable_y(fig, ts[amt_col].max())
    add_year_bands(fig, ts["_month"])
    return fig

def cumulative_spend_figure(dff: pd.DataFrame, amt_col: str) -> go.Figure:
    ts2 = (dff.loc[dff["_flow"]=="Outflow"]
             .groupby("_month")[amt_col].sum()
             .reset_index().sort_values("_month"))
    fig = px.line(ts2, x="_month", y=amt_col, markers=True, title="Cumulative Spend (Outflow, Completed)")
    if not ts2.empty:
        ts2["cum"] = ts2[amt_col].cumsum()
        fig = px.line(ts2, x="_month", y="cum", markers=True, title="Cumulative Spend (Outflow, Completed)")
        fig.update_traces(hovertemplate="%{x|%b %Y}<br>₹%{y:.0f}<extra></extra>")
        _set_stable_y(fig, ts2["cum"].max(), left=70)
    return fig
