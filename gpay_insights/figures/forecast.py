import numpy as np
import pandas as pd
import plotly.graph_objects as go

try:
    import statsmodels.api as sm
    HAS_SM = True
except Exception:
    HAS_SM = False

from .. import config
from ..utils.formatting import fmt_currency_indian

def fit_sarimax_grid(y_log: pd.Series):
    if not HAS_SM: return None
    best_aic, best_res, best_spec = float("inf"), None, None
    orders = [(1,1,1), (2,1,1), (1,1,2)]
    seasonals = [(1,0,1,12), (0,1,1,12), (1,1,1,12)]
    for order in orders:
        for seasonal in seasonals:
            try:
                mod = sm.tsa.statespace.SARIMAX(
                    y_log, order=order, seasonal_order=seasonal, trend="c",
                    enforce_stationarity=False, enforce_invertibility=False
                )
                res = mod.fit(disp=False)
                if res.aic < best_aic:
                    best_aic, best_res, best_spec = res.aic, res, (order, seasonal)
            except Exception:
                pass
    if best_res is None:
        try:
            mod = sm.tsa.statespace.SARIMAX(y_log, order=(1,1,1), trend="c",
                                            enforce_stationarity=False, enforce_invertibility=False)
            best_res = mod.fit(disp=False)
        except Exception:
            return None
    return best_res

def forecast_figure(df, date_col, amt_col, status_col=None):
    """12-month forecast of Completed + Outflow monthly sums using log1p SARIMAX."""
    if not HAS_SM:
        fig = go.Figure().update_layout(title="12-Month Transaction Forecast (install statsmodels to enable)")
        fig.add_annotation(text="pip install statsmodels", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)
        return fig, pd.DataFrame()

    d = df.copy()

    # Completed-only (if status is present)
    if status_col and status_col in d.columns:
        ss = d[status_col].astype(str).str.lower().str.strip()
        d = d[ss.isin(config.COMPLETED_TOKENS)]

    # Outflow only
    d = d[d["_flow"] == "Outflow"]
    if d.empty:
        return go.Figure().update_layout(title="12-Month Transaction Forecast"), pd.DataFrame()

    monthly = (d.set_index(date_col)[amt_col]
                 .resample("MS").sum().rename("y").to_frame())
    monthly["y"] = monthly["y"].fillna(0.0)

    y_log = np.log1p(monthly["y"])
    res = fit_sarimax_grid(y_log)
    if res is None:
        return go.Figure().update_layout(title="12-Month Transaction Forecast (model failed)"), pd.DataFrame()

    pred = res.get_forecast(steps=12)
    mean_log = pred.predicted_mean
    ci_log = pred.conf_int(alpha=0.05)

    lower_col = [c for c in ci_log.columns if "lower" in c.lower()][0]
    upper_col = [c for c in ci_log.columns if "upper" in c.lower()][0]

    fdf = pd.DataFrame({
        "ds": mean_log.index,
        "yhat": np.expm1(mean_log.values),
        "yhat_lower": np.maximum(0.0, np.expm1(ci_log[lower_col].values)),
        "yhat_upper": np.maximum(0.0, np.expm1(ci_log[upper_col].values)),
    })

    ymin = float(min(monthly["y"].min(), fdf["yhat_lower"].min()))
    ymax = float(max(monthly["y"].max(), fdf["yhat_upper"].max()))
    ymin = min(0.0, ymin)
    ticks = np.linspace(ymin, ymax, 7)
    tickvals = [float(t) for t in ticks]
    ticktext = [fmt_currency_indian(t) for t in ticks]

    hist_hover = [f"Month={idx.strftime('%b %Y')}<br>Amount={fmt_currency_indian(val)}"
                  for idx, val in zip(monthly.index, monthly["y"])]
    fcst_hover = [f"Month={idx.strftime('%b %Y')}<br>Forecast={fmt_currency_indian(val)}"
                  for idx, val in zip(fdf['ds'], fdf['yhat'])]

    COLOR_ACTUAL = "#2A9D8F"
    COLOR_FORECAST = "#7B61FF"
    COLOR_BAND = "#7B61FF"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly.index, y=monthly["y"], mode="lines+markers",
                             name="Actual (Completed Outflow)", line=dict(color=COLOR_ACTUAL, width=2.2),
                             marker=dict(size=6, color=COLOR_ACTUAL), hoverinfo="text", hovertext=hist_hover))
    fig.add_trace(go.Scatter(x=fdf["ds"], y=fdf["yhat_upper"], mode="lines",
                             line=dict(width=0, color=COLOR_BAND), name="95% CI",
                             hoverinfo="skip", showlegend=True))
    fig.add_trace(go.Scatter(x=fdf["ds"], y=fdf["yhat_lower"], mode="lines",
                             line=dict(width=0, color=COLOR_BAND), fill="tonexty", opacity=0.20,
                             hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=fdf["ds"], y=fdf["yhat"], mode="lines+markers",
                             name="Forecast", line=dict(color=COLOR_FORECAST, width=2.2),
                             marker=dict(size=6, color=COLOR_FORECAST), hoverinfo="text", hovertext=fcst_hover))
    fig.add_vrect(x0=fdf["ds"].min(), x1=fdf["ds"].max(), fillcolor=COLOR_FORECAST, opacity=0.08, line_width=0)

    fig.update_layout(
        title=dict(text="12-Month Transaction Forecast", x=0.5, xanchor="center", y=0.98),
        xaxis_title="Month", yaxis_title="Amount (₹)", template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.12, xanchor="center", x=0.5,
                    bgcolor="rgba(255,255,255,0.85)", bordercolor="rgba(0,0,0,0.1)", borderwidth=1),
        autosize=True, margin=dict(l=80, r=40, t=110, b=60)
    )
    fig.update_yaxes(tickmode="array", tickvals=tickvals, ticktext=ticktext)
    return fig, fdf
