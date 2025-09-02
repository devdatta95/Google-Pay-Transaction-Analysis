from dash import Input, Output
from .. import config
from ..utils.filters import apply_filters, apply_completed_only
from ..utils.formatting import fmt_currency_indian, indian_number

def register_merchant_callbacks(app, datactx):
    @app.callback(
        Output("merchant-rfm-cards", "children"),
        Output("tbl_merchant_tx", "columns"),
        Output("tbl_merchant_tx", "data"),
        Input("filters-store", "data"),
        Input("merchant-search", "value"),
    )
    def merchant_explorer(flt, merchant_val):
        from dash import html
        if not merchant_val or datactx.merchant_col is None:
            return [], [], []

        s = flt.get("start", str(datactx.min_date))
        e = flt.get("end", str(datactx.max_date))
        dff = apply_filters(datactx.df, datactx.date_col, s, e)

        dsel_all = dff[dff[datactx.merchant_col].astype(str) == str(merchant_val)].copy()
        if dsel_all.empty: return [], [], []

        dsel_c = apply_completed_only(dsel_all, datactx.status_col)

        last_dt = dsel_c[datactx.date_col].max()
        freq = len(dsel_c)
        money = float(dsel_c[datactx.amt_col].sum())
        out_sel = dsel_c[dsel_c["_flow"]=="Outflow"]
        in_sel  = dsel_c[dsel_c["_flow"]=="Inflow"]

        cards = [
            _card("Merchant", str(merchant_val).upper()),
            _card("Transactions", indian_number(freq)),
            _card("Total Amount", fmt_currency_indian(money)),
            _card("Outflow Amount", fmt_currency_indian(float(out_sel[datactx.amt_col].sum()))),
            _card("Inflow Amount", fmt_currency_indian(float(in_sel[datactx.amt_col].sum()))),
            _card("Last Txn", last_dt.strftime("%Y-%m-%d") if last_dt is not None else "—"),
        ]

        prefer_cols = [datactx.date_col, datactx.amt_col]
        for c in (datactx.cat_col, datactx.merchant_col, datactx.status_col, datactx.instr_col, "_flow"):
            if c and c in dsel_all.columns: prefer_cols.append(c)
        for extra in ["description","details","note","label"]:
            if extra in dsel_all.columns and extra not in prefer_cols: prefer_cols.append(extra)

        seen = set()
        show_cols = [c for c in prefer_cols if not (c in seen or seen.add(c)) and c in dsel_all.columns]
        tbl_cols = [{"name": c, "id": c} for c in show_cols]
        tbl_data = dsel_all[show_cols].sort_values(datactx.date_col, ascending=False).to_dict("records")
        return cards, tbl_cols, tbl_data

    def _card(label, value, sub=None):
        from dash import html
        return html.Div([
            html.Div(label, style={"fontSize":"12px","color":"#555","marginBottom":"4px"}),
            html.Div(value, style={"fontSize":"22px","fontWeight":700}),
            html.Div(sub or "", style={"fontSize":"11px","color":"#888","marginTop":"4px"}),
        ], style=config.CARD_STYLE)
