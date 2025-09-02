from dash import Input, Output, dcc
from ..figures.forecast import forecast_figure

def register_download_callbacks(app, datactx):
    @app.callback(
        Output("dl-forecast", "data", allow_duplicate=True),
        Input("btn-dl-forecast", "n_clicks"),
        prevent_initial_call=True
    )
    def download_forecast(n):
        _, fdf = forecast_figure(datactx.df, datactx.date_col, datactx.amt_col)
        if fdf.empty: return None
        return dcc.send_data_frame(fdf.to_csv, "GPay_Monthly_Completed_Amount_Forecast_12M_Positive.csv", index=False)
