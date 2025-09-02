from dash import Input, Output, State, ctx
from ..utils.filters import resolve_dates_by_trigger, month_to_index, apply_filters

def register_sync_callbacks(app, datactx):
    @app.callback(
        Output("filters-store", "data"),
        Output("merchant-search", "options"),
        Output("date-start", "value"),
        Output("date-end", "value"),
        Output("month-slider", "value"),
        Input("date-start", "value"),
        Input("date-end", "value"),
        Input("year-dropdown", "value"),
        Input("month-slider", "value"),
        State("filters-store", "data"),
    )
    def sync_filters(date_start, date_end, year_val, slider_range, current_store):
        trig = ctx.triggered_id
        if not date_start and current_store: date_start = current_store.get("start", str(datactx.min_date))
        if not date_end and current_store:   date_end   = current_store.get("end",   str(datactx.max_date))

        s, e = resolve_dates_by_trigger(trig, date_start, date_end, year_val, slider_range, datactx)
        dff = apply_filters(datactx.df, datactx.date_col, s, e)

        if datactx.merchant_col and not dff.empty:
            opts = sorted(dff[datactx.merchant_col].dropna().astype(str).unique().tolist())
            merch_opts = [{"label": m, "value": m} for m in opts]
        else:
            merch_opts = []

        s_idx = month_to_index(s, datactx.months_list)
        e_idx = month_to_index(e, datactx.months_list)
        return {"start": str(s), "end": str(e)}, merch_opts, str(s), str(e), [s_idx, e_idx]
