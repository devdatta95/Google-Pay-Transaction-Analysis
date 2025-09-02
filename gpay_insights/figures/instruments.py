import plotly.express as px
from .. import config

def instruments_donut_figure(dff, instr_col, amt_col):
    if not instr_col: return px.pie(title="Payment Method Split (Outflow, Completed)")
    ins = (dff.loc[dff["_flow"]=="Outflow"].groupby(instr_col)[amt_col]
             .sum().sort_values(ascending=False).reset_index())
    fig = px.pie(ins, names=instr_col, values=amt_col, hole=0.55,
                 title="Payment Method Split (Outflow, Completed)")
    fig.update_traces(textposition="inside", texttemplate="%{label}<br>%{percent:.0%}")
    fig.update_layout(height=config.FIG_H, autosize=False, margin=dict(t=42, r=20, b=40, l=64))
    return fig
