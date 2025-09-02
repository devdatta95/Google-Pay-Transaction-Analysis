from pathlib import Path

# data file (you can override by passing a Path to create_app)
DATA_DIR  = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "Gpay_Transaction_Data.csv"

# -------------- Styling ---------------
EXTERNAL_STYLESHEETS = [
    "https://www.w3schools.com/w3css/4/w3.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
]



# Graph sizing
FIG_H = 360
FIG_H_TALL = FIG_H * 2   # for extra-tall charts like Merchant Pareto

# GRAPH_STYLE = {"height": f"{FIG_H}px"}


# Treemap / category exclusions
EXCLUDE_CATS = {"unrecognized", "uncategorized", "unknown", "misc", "others", "other"}

# Completed status tokens (normalized)
COMPLETED_TOKENS = {"completed", "success", "succeeded", "successful"}

# Base figure height (already in your file)
FIG_H = 360  # or whatever you have

# NEW: treemap height = +40%
TREEMAP_H = int(FIG_H * 1.4)


# ---- Clustering defaults ----
# Feature names must exist in the engineered feature frame inside analysis/clustering.py
CLUSTER_FEATURES = [
    "amount_inr",
    "hour",
    "dow_num",
    "is_weekend",
    "day",
    "month",
    "merchant_txn_count_norm",
    "merchant_outflow_share",
]
DEFAULT_K_CLUSTERS = 5
MAX_TSNE_POINTS = 3000   # sampling cap for responsiveness

# gpay_insights/config.py

# # --------- Plot sizing ----------
FIG_H = 360
# FIG_H_TALL = 720   # used for tall charts like Pareto

# Base Plotly config for all graphs
GRAPH_CONFIG = {
    "displayModeBar": "hover",
    "responsive": True,
    "scrollZoom": False,
}

# Let each Graph fill its card by default
GRAPH_STYLE = {
    "height": "100%"
}




THEME_PRESETS = {
    "Light":   {"plotly_template": "plotly_white", "card_bg": "#ffffff", "font_color": "#111111", "gridcolor": "#e5e7eb"},
    "Dark":    {"plotly_template": "plotly_dark",  "card_bg": "#161a23", "font_color": "#e8e8e8", "gridcolor": "#2a2f3a"},
    "ggplot2": {"plotly_template": "ggplot2",      "card_bg": "#ffffff", "font_color": "#222222", "gridcolor": "#e5e7eb"},
    "seaborn": {"plotly_template": "seaborn",      "card_bg": "#ffffff", "font_color": "#1f2937", "gridcolor": "#e5e7eb"},
}
DEFAULT_THEME_KEY = "Light"

CARD_STYLE = {
    "padding": "12px 16px",
    "borderRadius": "14px",
    "boxShadow": "0 4px 16px rgba(0,0,0,0.08)",
    "background": "var(--card-bg)",
    "border": "1px solid var(--card-border)",
}
# GRAPH_STYLE = {"height": "420px"}   # keep your heights
# GRAPH_CONFIG = {"displayModeBar": "hover"}
# FIG_H_TALL = 650
FIG_H_NORMAL = 420
