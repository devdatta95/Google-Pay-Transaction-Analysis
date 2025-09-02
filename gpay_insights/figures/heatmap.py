import plotly.graph_objects as go
import pandas as pd
from .. import config

def heatmap_figure(dff, amt_col, metric="count"):
    base = dff.loc[dff["_flow"]=="Outflow"].copy()
    if base.empty:
        return go.Figure().update_layout(title="When do you spend? (Outflow, Completed)")
    if metric == "amount":
        hm = base.groupby(["_dow","_hour"])[amt_col].sum().reset_index(name="value")
    else:
        hm = base.groupby(["_dow","_hour"]).size().reset_index(name="value")

    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    hm["_dow"] = pd.Categorical(hm["_dow"], categories=dow_order, ordered=True)
    hm = hm.sort_values(["_dow","_hour"])
    pivot = hm.pivot(index="_dow", columns="_hour", values="value").fillna(0)

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=list(pivot.columns), y=list(pivot.index),
        hovertemplate="Hour %{x}:00<br>%{y}<br>%{z:.0f}<extra></extra>"
    ))
    fig.update_layout(title="When do you spend? (Outflow, Completed)",
                      xaxis_title="Hour of Day", yaxis_title="Day of Week",
                      height=config.FIG_H, autosize=False,
                      margin=dict(t=42, r=20, b=50, l=70))
    return fig
