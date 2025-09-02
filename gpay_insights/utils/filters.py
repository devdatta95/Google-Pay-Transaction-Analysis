from datetime import date as _date
import numpy as np
import pandas as pd
from .. import config

def month_start(d: _date) -> _date:
    return _date(d.year, d.month, 1)

def month_to_index(d: _date, months_list: list[_date]) -> int:
    ms = month_start(d)
    try:
        return months_list.index(ms)
    except ValueError:
        if ms <= months_list[0]: return 0
        return len(months_list) - 1

def apply_filters(df: pd.DataFrame, date_col: str, start: _date, end: _date) -> pd.DataFrame:
    return df[(df[date_col] >= pd.to_datetime(start)) &
              (df[date_col] <= (pd.to_datetime(end) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)))].copy()

def is_completed_series(s: pd.Series) -> pd.Series:
    if s is None: return pd.Series([True]*len(s))
    ss = s.astype(str).str.lower().str.strip()
    return ss.isin(config.COMPLETED_TOKENS)

def apply_completed_only(df: pd.DataFrame, status_col: str | None) -> pd.DataFrame:
    if status_col and status_col in df.columns:
        return df[is_completed_series(df[status_col])].copy()
    return df.copy()

def resolve_dates_by_trigger(trigger_id, date_start: str, date_end: str, year_val, slider_range, ctx):
    s = _date.fromisoformat(date_start) if date_start else ctx.min_date
    e = _date.fromisoformat(date_end) if date_end else ctx.max_date

    if trigger_id in ("date-start", "date-end"):
        pass
    elif trigger_id == "year-dropdown" and year_val not in (None, "All"):
        y = int(year_val)
        s = _date(y, 1, 1); e = _date(y, 12, 31)
    elif trigger_id == "month-slider" and isinstance(slider_range, (list, tuple)) and len(slider_range) == 2:
        i0, i1 = int(slider_range[0]), int(slider_range[1])
        i0 = max(0, min(i0, len(ctx.months_list)-1))
        i1 = max(0, min(i1, len(ctx.months_list)-1))
        s = ctx.months_list[min(i0, i1)]
        e = (ctx.months_index[max(i0, i1)] + pd.offsets.MonthEnd(0)).date()

    if s < ctx.min_date: s = ctx.min_date
    if e > ctx.max_date: e = ctx.max_date
    if e < s: e = s
    return s, e
