import plotly.express as px
from .. import config

def status_bar_figure(dff, status_col, amt_col):
    st = dff.groupby(status_col)[amt_col].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(st, x=status_col, y=amt_col, title="Status (Amount)",
                 labels={status_col:"Status", amt_col:"Amount (₹)"})
    fig.update_traces(hovertemplate="%{x}<br>₹%{y:.0f}<extra></extra>")
    fig.update_xaxes(tickangle=-10, title_standoff=30)
    fig.update_layout(autosize=True, margin=dict(t=42, r=20, b=80, l=64))
    return fig
