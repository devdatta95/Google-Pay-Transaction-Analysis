# gpay_insights/layouts/dashboard.py
from dash import dcc, html, dash_table
from .. import config


def build_layout(ctx):
    # A convenient, slightly taller height for charts that need room
    FIG_H_STD = getattr(config, "FIG_H", 360)
    FIG_H_TALL = getattr(config, "FIG_H_TALL", int(FIG_H_STD * 1.6))

    return html.Div([
        # ---------------- Stores ----------------
        dcc.Store(id="filters-store", data={"start": str(ctx.min_date), "end": str(ctx.max_date)}),

        # ---------------- Date controls ----------------
        html.Div([
            html.Div(className="date-group", children=[
                html.Label("Start date"),
                html.Div([
                    html.I(className="fa fa-calendar", style={"marginRight": "6px"}),
                    dcc.Input(
                        id="date-start",
                        type="date",
                        value=str(ctx.min_date),
                        className="date-input",
                        debounce=True,
                    ),
                ]),
            ]),
            html.Div(className="date-group", children=[
                html.Label("End date"),
                html.Div([
                    html.I(className="fa fa-calendar", style={"marginRight": "6px"}),
                    dcc.Input(
                        id="date-end",
                        type="date",
                        value=str(ctx.max_date),
                        className="date-input",
                        debounce=True,
                    ),
                ]),
            ]),
            html.Div(className="date-group", children=[
                html.Label("Year"),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[{"label": "All", "value": "All"}] + [
                        {"label": str(y), "value": int(y)}
                        for y in sorted(ctx.df[ctx.date_col].dt.year.unique())
                    ],
                    value="All",
                    clearable=False,
                    style={"minWidth": "140px"},
                ),
            ]),
        ], className="date-controls"),

        html.Div([
            html.Label("Select Timeline"),
            dcc.RangeSlider(
                id="month-slider",
                min=0, max=len(ctx.months_list) - 1, step=1,
                value=[0, len(ctx.months_list) - 1],
                marks={
                    0: ctx.months_index[0].strftime("%b %Y"),
                    (len(ctx.months_list) - 1): ctx.months_index[-1].strftime("%b %Y"),
                },
                tooltip={"always_visible": False},
            ),
        ], style={"margin": "2px 12px 8px"}),

        # ---------------- KPI Row ----------------
        html.Div(
            id="kpi-row",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))",
                "gap": "12px",
                "margin": "12px",
            },
        ),

        # ---------------- Overview ----------------
        html.Div(id="overview", children=[
            html.Div([
                html.Div(
                    dcc.Graph(
                        id="fig_ts",
                        config=config.GRAPH_CONFIG,
                        style={**config.GRAPH_STYLE, "height": f"{FIG_H_TALL}px"},
                    ),
                    style=config.CARD_STYLE,
                ),
                html.Div(
                    dcc.Graph(
                        id="fig_cum",
                        config=config.GRAPH_CONFIG,
                        style={**config.GRAPH_STYLE, "height": f"{FIG_H_TALL}px"},
                    ),
                    style=config.CARD_STYLE,
                ),
            ], style={"display": "grid", "gridTemplateColumns": "1.5fr 1fr", "gap": "12px", "margin": "12px"}),
        ], style={"scrollMarginTop": "64px"}),

        # ---------------- Categories & Merchants ----------------
        html.Div(id="cats_merch", children=[

            # ROW 1: Top Categories (left) + Paid/Sent/Received Pie (right)
            html.Div([
                html.Div(
                    dcc.Graph(
                        id="fig_cat",
                        config=config.GRAPH_CONFIG,
                        # give a little extra height so x-tick labels never collide with next row
                        style={**config.GRAPH_STYLE, "height": f"{FIG_H_TALL}px"},
                    ),
                    style=config.CARD_STYLE,
                ),
                html.Div([
                    html.Div([
                        html.Span("Pie Chart Metric:",
                                  style={"fontSize": "12px", "color": "#444", "marginRight": "8px"}),
                        dcc.RadioItems(
                            id="flow-pie-metric",
                            options=[
                                {"label": " Amount (₹)  ", "value": "amount"},
                                {"label": " Count", "value": "count"},
                            ],
                            value="amount",
                            inline=True,
                        ),
                    ], style={"marginBottom": "6px"}),
                    dcc.Graph(
                        id="fig_flow_pie",
                        config=config.GRAPH_CONFIG,
                        style={**config.GRAPH_STYLE, "height": f"{FIG_H_TALL}px"},
                    ),
                ], style=config.CARD_STYLE),
            ], style={"display": "grid", "gridTemplateColumns": "1.3fr 1fr", "gap": "12px", "margin": "12px"}),

            # ROW 2: Monthly Transaction Count (full width)
            html.Div([
                html.Div(
                    dcc.Graph(
                        id="fig_txn_count",
                        config=config.GRAPH_CONFIG,
                        style={**config.GRAPH_STYLE, "height": f"{FIG_H_TALL}px"},
                    ),
                    style=config.CARD_STYLE,
                ),
            ], style={"display": "grid", "gridTemplateColumns": "1fr", "gap": "12px", "margin": "0 12px 12px"}),

            # ROW 3: Instruments Donut (30%) + Heatmap (70%)
            html.Div([
                # Left: donut
                html.Div(
                    dcc.Graph(
                        id="fig_instr_donut",
                        config=config.GRAPH_CONFIG,
                        style={**config.GRAPH_STYLE, "height": f"{FIG_H_TALL}px"},
                    ),
                    style=config.CARD_STYLE,
                ),

                # Right: heatmap with local metric switch
                html.Div([
                    html.Div([
                        html.Span("Heatmap metric:",
                                  style={"fontSize": "12px", "color": "#444", "marginRight": "8px"}),
                        dcc.RadioItems(
                            id="heatmap-metric-local",
                            options=[
                                {"label": " Amount (₹)", "value": "amount"},
                                {"label": " Count", "value": "count"},
                            ],
                            value="count",
                            inline=True,
                        ),
                    ], style={"marginBottom": "6px"}),
                    dcc.Graph(
                        id="fig_cal",
                        config=config.GRAPH_CONFIG,
                        style={**config.GRAPH_STYLE, "height": f"{FIG_H_TALL}px"},
                    ),
                ], style=config.CARD_STYLE),
            ], style={"display": "grid", "gridTemplateColumns": "3fr 7fr", "gap": "12px", "margin": "12px"}),

            # ROW 4: Merchant Pareto (full width, Top-N slider in header)
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Top-N merchants:",
                                  style={"fontSize": "12px", "color": "#444", "marginRight": "8px"}),
                        dcc.Slider(
                            id="opt-topn-local",
                            min=10, max=50, step=5, value=25, marks=None,
                            tooltip={"always_visible": False},
                        ),
                    ], style={"marginBottom": "6px"}),
                    dcc.Graph(
                        id="fig_merch_pareto",
                        config=config.GRAPH_CONFIG,
                        style={"height": f"{int(FIG_H_TALL * 2.5)}px"},  # nice, tall pareto
                    ),
                ], style=config.CARD_STYLE),
            ], style={"display": "grid", "gridTemplateColumns": "1fr", "gap": "12px", "margin": "12px"}),

            # ROW 5: Treemap (70%) + Status (30%)
            html.Div([
                html.Div([
                    html.Div("Category → Merchant", style={"fontWeight": 600, "marginBottom": "4px"}),
                    html.Div(id="treemap-total",
                             style={"fontSize": "12px", "color": "#555", "marginBottom": "6px"}),
                    dcc.Graph(
                        id="fig_treemap",
                        config={**config.GRAPH_CONFIG, "responsive": True},
                        style={"height": f"{int(FIG_H_TALL)}px"},
                    ),
                ],
                    style={**config.CARD_STYLE, "height": "52vh", "minHeight": "420px"},
                    className="card-flex"
                ),

                html.Div(
                    dcc.Graph(
                        id="fig_status_bar",
                        config={**config.GRAPH_CONFIG, "responsive": True},
                        style={"height": f"{int(FIG_H_TALL)}px"},
                    ),
                    style={**config.CARD_STYLE, "height": "52vh", "minHeight": "420px"},
                    className="card-flex",
                ),
            ], style={"display": "grid", "gridTemplateColumns": "7fr 3fr", "gap": "12px", "margin": "12px"}),

        ], style={"scrollMarginTop": "64px"}),

        # ---------------- Forecast ----------------
        html.Div(id="forecast", children=[
            html.Div([
                html.Div("12-Month Forecast (Completed Outflow)",
                         style={"fontWeight": 600, "marginBottom": "6px"}),
                html.Button(
                    "Download forecast CSV",
                    id="btn-dl-forecast",
                    n_clicks=0,
                    style={
                        "padding": "8px 12px",
                        "borderRadius": "10px",
                        "border": "1px solid #ddd",
                        "background": "#f2fbff",
                        "cursor": "pointer",
                        "marginBottom": "8px",
                    },
                ),
                dcc.Download(id="dl-forecast"),
                dcc.Graph(
                    id="fig_forecast",
                    config=config.GRAPH_CONFIG,
                    style={**config.GRAPH_STYLE, "height": f"{FIG_H_TALL}px"},
                ),
            ], style=config.CARD_STYLE),
        ], style={"margin": "12px", "scrollMarginTop": "64px"}),

        # ---------------- RFM ----------------
        html.Div(id="rfm", children=[
            html.Div([
                html.Div("RFM Scores by Merchant (current filter)",
                         style={"fontWeight": 600, "marginBottom": "6px"}),
                dash_table.DataTable(
                    id="tbl_rfm",
                    page_size=12,
                    sort_action="native",
                    filter_action="native",
                    style_table={"overflowX": "auto", "maxHeight": "420px", "overflowY": "auto"},
                    style_cell={
                        "fontFamily": "Inter, system-ui, -apple-system, Segoe UI, Roboto",
                        "fontSize": "12px",
                        "padding": "6px",
                    },
                ),
            ], style={**config.CARD_STYLE, "margin": "12px"}),
        ], style={"scrollMarginTop": "64px"}),

        # ---------------- Merchant Explorer ----------------
        html.Div(id="merchant_explorer", children=[
            html.Div([
                html.Div("Merchant Explorer", style={"fontWeight": 600, "marginBottom": "6px"}),
                dcc.Dropdown(id="merchant-search", placeholder="Type to search merchant…", clearable=True),
                html.Div(
                    id="merchant-rfm-cards",
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(120px, 1fr))",
                        "gap": "8px",
                        "marginTop": "8px",
                    },
                ),
                dash_table.DataTable(
                    id="tbl_merchant_tx",
                    page_size=12,
                    sort_action="native",
                    filter_action="native",
                    style_table={"maxHeight": "440px", "overflowY": "auto"},
                    style_cell={
                        "fontFamily": "Inter, system-ui, -apple-system, Segoe UI, Roboto",
                        "fontSize": "12px",
                        "padding": "6px",
                        "whiteSpace": "nowrap",
                        "textOverflow": "ellipsis",
                        "maxWidth": 260,
                    },
                ),
            ], style=config.CARD_STYLE),
        ], style={"margin": "12px", "scrollMarginTop": "64px"}),


    ])
