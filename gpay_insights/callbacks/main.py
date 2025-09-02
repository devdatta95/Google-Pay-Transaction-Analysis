from dash import Input, Output
import numpy as np
from .. import config
from ..utils.filters import apply_filters, apply_completed_only
from ..utils.formatting import indian_number, fmt_currency_indian
from ..figures.time_series import monthly_spend_figure, cumulative_spend_figure
from ..figures.categories import top_categories_figure
from ..figures.heatmap import heatmap_figure
from ..figures.merchants import merchant_pareto_figure
from ..figures.treemap import treemap_figure
from ..figures.status import status_bar_figure
from ..figures.forecast import forecast_figure
from ..rfm import compute_rfm
from ..figures.flow_pie import flow_pie_figure
from ..figures.txn_count import monthly_txn_count_figure  # <-- make sure this import exists
from ..figures.instruments import instruments_donut_figure



def register_main_callbacks(app, datactx):
    @app.callback(
        Output("kpi-row", "children"),
        Output("fig_ts", "figure"),
        Output("fig_cum", "figure"),
        Output("fig_cat", "figure"),
        Output("fig_flow_pie", "figure"),
        Output("fig_txn_count", "figure"),        # <-- NEW in outputs (matches layout)
        Output("fig_instr_donut", "figure"),  # NEW
        Output("fig_cal", "figure"),
        Output("fig_merch_pareto", "figure"),
        Output("treemap-total", "children"),
        Output("fig_treemap", "figure"),
        Output("fig_status_bar", "figure"),
        Output("tbl_rfm", "columns"),
        Output("tbl_rfm", "data"),
        Output("fig_forecast", "figure"),
        Input("filters-store", "data"),
        Input("flow-pie-metric", "value"),
        Input("heatmap-metric-local", "value"),
        Input("opt-topn-local", "value"),
    )
    def rebuild_main(flt, pie_metric, heat_metric, topn):
        # ---- filter data ----
        s = flt.get("start", str(datactx.min_date))
        e = flt.get("end", str(datactx.max_date))
        dff = apply_filters(datactx.df, datactx.date_col, s, e)
        dff_c = apply_completed_only(dff, datactx.status_col)

        # ---- KPIs (Completed only) ----
        total_money = float(dff_c.loc[dff_c["_flow"].isin(["Outflow", "Inflow"]), datactx.amt_col].sum()) if not dff_c.empty else 0.0
        total_out = float(dff_c.loc[dff_c["_flow"] == "Outflow", datactx.amt_col].sum()) if not dff_c.empty else 0.0
        total_in  = float(dff_c.loc[dff_c["_flow"] == "Inflow", datactx.amt_col].sum()) if not dff_c.empty else 0.0
        median_amt = float(dff_c[datactx.amt_col].median()) if not dff_c.empty else np.nan
        mean_amt   = float(dff_c[datactx.amt_col].mean()) if not dff_c.empty else np.nan

        top10_share = np.nan
        if datactx.merchant_col and not dff_c.empty:
            out_by_merch = (dff_c.loc[dff_c["_flow"] == "Outflow"]
                                .groupby(datactx.merchant_col)[datactx.amt_col].sum()
                                .sort_values(ascending=False))
            tot_out = float(out_by_merch.sum()) if len(out_by_merch) else 0.0
            if tot_out > 0:
                top10_share = float(out_by_merch.head(10).sum() / tot_out) * 100.0

        def _card(label, value, sub=None):
            return {"label": label, "value": value, "sub": sub}

        def _render_card(d):
            from dash import html
            return html.Div([
                html.Div(d["label"], style={"fontSize":"12px","color":"#555","marginBottom":"4px"}),
                html.Div(d["value"], style={"fontSize":"22px","fontWeight":700}),
                html.Div(d.get("sub") or "", style={"fontSize":"11px","color":"#888","marginTop":"4px"}),
            ], style=config.CARD_STYLE)

        kpi_cards = [
            _card("Total Money Transacted", fmt_currency_indian(total_money), "Completed • Inflow + Outflow"),
            _card("Total Outflow", fmt_currency_indian(total_out)),
            _card("Total Inflow", fmt_currency_indian(total_in)),
            _card("Median txn", fmt_currency_indian(median_amt)),
            _card("Mean txn", fmt_currency_indian(mean_amt)),
            _card("# Transactions", indian_number(len(dff_c))),
            _card("# Active merchants", indian_number(dff_c[datactx.merchant_col].nunique()) if datactx.merchant_col and not dff_c.empty else "—"),
            _card("Top-10 merchant share", f"{top10_share:.1f}%" if not np.isnan(top10_share) else "—"),
        ]

        # ---- figures (Completed only where applicable) ----
        fig_ts   = monthly_spend_figure(dff_c, datactx.date_col, datactx.amt_col)
        fig_cum  = cumulative_spend_figure(dff_c, datactx.amt_col)
        fig_cat  = top_categories_figure(dff_c, datactx.cat_col, datactx.amt_col)
        fig_flow = flow_pie_figure(dff_c, datactx.tx_col, datactx.amt_col, metric=pie_metric or "amount")
        fig_txn_count = monthly_txn_count_figure(dff_c, datactx.date_col)  # <-- NEW
        fig_cal  = heatmap_figure(dff_c, datactx.amt_col, metric=heat_metric or "count")
        fig_m    = merchant_pareto_figure(dff_c, datactx.merchant_col, datactx.amt_col, topn or 25)
        fig_tree = treemap_figure(dff_c, datactx.cat_col, datactx.merchant_col, datactx.amt_col)
        fig_instr = instruments_donut_figure(dff_c, datactx.instr_col, datactx.amt_col)

        # Treemap total text (Completed Outflow)
        tot_outflow = float(dff_c.loc[dff_c["_flow"] == "Outflow", datactx.amt_col].sum()) if not dff_c.empty else 0.0
        treemap_total_text = f"Total (Completed Outflow): {fmt_currency_indian(tot_outflow)}"

        # Status bar uses raw dff (group by status), but still filtered by date/year
        fig_stat = status_bar_figure(dff, datactx.status_col, datactx.amt_col) if datactx.status_col \
                   else status_bar_figure(dff, "status", datactx.amt_col)

        # RFM table
        rfm = compute_rfm(dff_c, datactx.merchant_col, datactx.date_col, datactx.amt_col)
        rfm_cols = [
            {"name":"Merchant","id":"merchant"},
            {"name":"R","id":"R"},
            {"name":"F","id":"F"},
            {"name":"M","id":"M"},
            {"name":"RFM Score","id":"RFM_Score"},
            {"name":"Last Transaction","id":"last_date_str"},
            {"name":"Frequency","id":"frequency"},
            {"name":"Monetary (₹)","id":"monetary"},
        ]
        rfm_data = rfm.to_dict("records")

        # Forecast (trained on full history, not filtered)
        fig_fc, _ = forecast_figure(datactx.df, datactx.date_col, datactx.amt_col, status_col=datactx.status_col)

        return (
            [_render_card(c) for c in kpi_cards],
            fig_ts,
            fig_cum,
            fig_cat,
            fig_flow,
            fig_txn_count,     # <-- keep the order in sync with Outputs
            fig_instr,
            fig_cal,
            fig_m,
            treemap_total_text,
            fig_tree,
            fig_stat,
            rfm_cols,
            rfm_data,
            fig_fc,
        )
