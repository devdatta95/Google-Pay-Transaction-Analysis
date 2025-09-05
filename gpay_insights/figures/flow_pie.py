import pandas as pd
import plotly.express as px
from .. import config

_PAID_KEYS = ("paid", "payment", "purchase", "bill", "charge", "debit")
_SENT_KEYS = ("sent",)          # keep "sent" distinct if present
_RECV_KEYS = ("received", "credit", "refund", "cashback")

def _class_from_tx_str(s: str) -> str | None:
    if not s: return None
    s = str(s).lower()
    if any(k in s for k in _RECV_KEYS): return "Received"
    if any(k in s for k in _SENT_KEYS): return "Sent"
    if any(k in s for k in _PAID_KEYS): return "Paid"
    return None

def flow_pie_figure(dff: pd.DataFrame, tx_col: str | None, amt_col: str, metric: str = "amount"):
    """
    Pie of Paid / Sent / Received. Works best when a transaction type column exists.
    - Uses only Completed rows (the caller should pass filtered dff).
    - metric: 'amount' (sum) or 'count'
    """
    if dff.empty:
        return px.pie(title="Paid / Sent / Received")

    df = dff.copy()
    if tx_col and tx_col in df.columns:
        lab = df[tx_col].map(_class_from_tx_str)
    else:
        # Fallback: infer from direction
        lab = df["_flow"].map(lambda v: "Received" if v == "Inflow" else ("Paid/Sent" if v == "Outflow" else None))

    df["_psr"] = lab
    df = df[df["_psr"].isin(["Paid","Sent","Received","Paid/Sent"])]

    if metric == "count":
        agg = df.groupby("_psr").size().reset_index(name="value")
        # title = "Count for - "
    else:
        agg = df.groupby("_psr")[amt_col].sum().reset_index(name="value")
        # title = "Amount for - "

    fig = px.pie(agg, names="_psr",
                 values="value",
                 hole=0.55,
                 # title=title
                 )
    fig.update_traces(textposition="inside", texttemplate="%{label}<br>%{percent:.0%}",
                      hovertemplate="%{label}<br>%{value:,.0f}<extra></extra>")
    fig.update_layout(autosize=True, margin=dict(t=42, r=20, b=40, l=64),
                      legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5))
    return fig
