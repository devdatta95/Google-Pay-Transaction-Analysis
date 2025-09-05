# gpay_insights/config.py

from pathlib import Path

# data file (you can override by passing a Path to create_app)
DATA_DIR  = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "Gpay_Transaction_Data.csv"

# -------------- Styling ---------------
EXTERNAL_STYLESHEETS = [
    "https://www.w3schools.com/w3css/4/w3.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
]



# Base figure height (already in your file)
FIG_H = 380
FIG_H_TALL = FIG_H    # for extra-tall charts like Merchant Pareto

# GRAPH_STYLE = {"height": f"{FIG_H}px"}

# Treemap / category exclusions
EXCLUDE_CATS = {"unrecognized", "uncategorized", "unknown", "misc", "others", "other"}

# Completed status tokens (normalized)
COMPLETED_TOKENS = {"completed", "success", "succeeded", "successful"}

# NEW: treemap height = +40%
TREEMAP_H = int(FIG_H * 1.4)




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



CARD_STYLE = {
    "padding": "12px 16px",
    "borderRadius": "14px",
    "boxShadow": "0 4px 16px rgba(0,0,0,0.08)",
    "background": "var(--card-bg)",
    "border": "1px solid var(--card-border)",
}

FIG_H_NORMAL = 420
