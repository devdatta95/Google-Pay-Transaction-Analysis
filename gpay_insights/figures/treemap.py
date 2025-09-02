import plotly.express as px
from .. import config

def treemap_figure(dff, cat_col, merchant_col, amt_col):
    if not (cat_col and merchant_col): return px.treemap(title="Category → Merchant (Outflow, Completed)")
    tdf = dff.loc[dff["_flow"]=="Outflow", [cat_col, merchant_col, amt_col]].copy()
    tdf = tdf[~tdf[cat_col].astype(str).str.lower().isin(config.EXCLUDE_CATS)]
    tdf = tdf.groupby([cat_col, merchant_col])[amt_col].sum().reset_index()
    fig = px.treemap(tdf, path=[cat_col, merchant_col], values=amt_col,
                     title="Category → Merchant (Outflow, Completed)")
    fig.update_layout(height=config.FIG_H, autosize=False, margin=dict(t=42, r=20, b=40, l=64))
    return fig
