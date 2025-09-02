import plotly.express as px
from .. import config
from ..utils.formatting import indian_number

def top_categories_figure(dff, cat_col, amt_col):
    if not cat_col: return px.bar(title="Top Categories (Outflow, Completed)")
    cat = (dff.loc[dff["_flow"]=="Outflow"]
             .groupby(cat_col)[amt_col].sum().reset_index())
    cat = cat[~cat[cat_col].astype(str).str.lower().isin(config.EXCLUDE_CATS)]
    cat = cat.sort_values(amt_col, ascending=False).head(20)
    fig = px.bar(cat, x=cat_col, y=amt_col, title="Top Categories (Outflow, Completed)",
                 labels={cat_col:"Category", amt_col:"Amount (₹)"})
    fig.update_traces(hovertemplate="%{x}<br>₹%{y:.0f}<extra></extra>")
    fig.update_xaxes(tickangle=-28, title_standoff=36)
    fig.update_layout(autosize=True, margin=dict(t=42, r=20, b=120, l=64))
    return fig
