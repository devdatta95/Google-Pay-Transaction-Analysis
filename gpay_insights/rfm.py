import numpy as np
import pandas as pd

def compute_rfm(d, merchant_col, date_col, amt_col):
    """
    RFM per merchant using COMPLETED + OUTFLOW only.
    Returns: merchant, R, F, M, RFM_Score, last_date_str, frequency, monetary
    """
    if merchant_col is None or d.empty:
        return pd.DataFrame(columns=["merchant","R","F","M","RFM_Score","last_date_str","frequency","monetary"])

    out = d[d["_flow"] == "Outflow"].copy()
    if out.empty:
        return pd.DataFrame(columns=["merchant","R","F","M","RFM_Score","last_date_str","frequency","monetary"])

    asof = out[date_col].max()
    g = (out.groupby(merchant_col)
             .agg(last_date=(date_col, "max"),
                  frequency=(merchant_col, "size"),
                  monetary=(amt_col, "sum"))
             .reset_index())
    g["recency_days"] = (asof - g["last_date"]).dt.days.astype(float)

    def score_quant(s: pd.Series, reverse: bool=False) -> pd.Series:
        if s.nunique() == 1:
            return pd.Series([3]*len(s), index=s.index)
        ranks = s.rank(pct=True)
        if reverse: ranks = 1 - ranks
        bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        labels = [1,2,3,4,5]
        ranks = np.clip(ranks, 1e-9, 0.999999)
        return pd.cut(ranks, bins=bins, labels=labels, include_lowest=True).astype(int)

    g["R"] = score_quant(g["recency_days"], reverse=True)
    g["F"] = score_quant(g["frequency"])
    g["M"] = score_quant(g["monetary"])
    g["RFM_Score"] = g[["R","F","M"]].sum(axis=1)
    g["last_date_str"] = g["last_date"].dt.strftime("%Y-%m-%d")
    g = g.sort_values(["RFM_Score","monetary","frequency"], ascending=[False, False, False])
    g = g.rename(columns={merchant_col: "merchant"})
    return g
