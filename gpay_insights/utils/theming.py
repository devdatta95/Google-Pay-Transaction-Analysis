# gpay_insights/utils/theming.py
from __future__ import annotations
import plotly.graph_objects as go
from .. import config

def _normalize_key(k: str) -> str:
    return (k or config.DEFAULT_THEME_KEY).strip()

def get_theme(key: str):
    k = _normalize_key(key)
    return config.THEME_PRESETS.get(k, config.THEME_PRESETS[config.DEFAULT_THEME_KEY])

def apply_theme(fig: go.Figure, theme_key: str) -> go.Figure:
    th = get_theme(theme_key)
    fig.update_layout(
        template=th["plotly_template"],
        paper_bgcolor=th["card_bg"],
        plot_bgcolor=th["card_bg"],
        font=dict(color=th["font_color"]),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=th["gridcolor"], linecolor=th["gridcolor"], zerolinecolor=th["gridcolor"])
    fig.update_yaxes(gridcolor=th["gridcolor"], linecolor=th["gridcolor"], zerolinecolor=th["gridcolor"])
    return fig

def themed_text_color(theme_key: str) -> str:
    dark = (theme_key or "").lower().startswith("dark")
    return "#e8e8e8" if dark else "#111111"
