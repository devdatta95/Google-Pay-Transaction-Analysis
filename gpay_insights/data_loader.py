from dataclasses import dataclass
from datetime import date as _date
from pathlib import Path
from typing import Optional, List
import numpy as np
import pandas as pd

from . import config

@dataclass
class DataContext:
    df: pd.DataFrame
    date_col: str
    amt_col: str
    cat_col: Optional[str]
    status_col: Optional[str]
    instr_col: Optional[str]
    merchant_col: Optional[str]
    tx_col: Optional[str]
    months_list: list[_date]
    months_index: pd.DatetimeIndex
    min_date: _date
    max_date: _date

def _read_csv_robust(path: Path) -> pd.DataFrame:
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            continue
    raise ValueError(f"Could not read CSV: {path}")

def first_match(cols: List[str], needles: List[str]):
    for n in needles:
        for c in cols:
            if n in c:
                return c
    return None

def load_data_context(csv_path: Path) -> DataContext:
    df = _read_csv_robust(csv_path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    date_col   = first_match(df.columns, ["date"])
    amt_col    = first_match(df.columns, ["amount", "amt", "value"])
    cat_col    = first_match(df.columns, ["category"])
    status_col = first_match(df.columns, ["status"])
    instr_col  = first_match(df.columns, ["method", "instrument", "mode", "channel"])

    merchant_like = [
        "merchant","merchant_name","to_from","party","counterparty",
        "name","label","note","description","details","beneficiary"
    ]
    merchant_col = next((c for c in merchant_like if c in df.columns and df[c].nunique(dropna=True) > 1), None)

    if date_col is None: raise ValueError("No date-like column found.")
    if amt_col  is None: raise ValueError("No amount/amt/value column found.")

    # parse date to IST
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce", utc=True)
    df[date_col] = df[date_col].dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
    df = df[df[date_col].notna()].copy()

    # normalize amount
    df[amt_col] = (df[amt_col].astype(str).str.replace(",", "", regex=False).str.replace("₹", "", regex=False))
    df[amt_col] = pd.to_numeric(df[amt_col], errors="coerce")
    df = df[df[amt_col].notna()].copy()

    # flow mapping (best-effort)
    tx_candidates = [c for c in df.columns if "type" in c or "direction" in c or ("transaction" in c and "type" in c)]
    tx_col = tx_candidates[0] if tx_candidates else None
    outflow_aliases = {"paid", "sent", "debit", "payment", "purchase", "bill", "charge"}
    inflow_aliases  = {"received", "credit", "refund", "cashback"}

    def flow_direction(x: str) -> str:
        s = str(x).lower()
        if any(a in s for a in outflow_aliases): return "Outflow"
        if any(a in s for a in inflow_aliases):  return "Inflow"
        return "Unknown"
    df["_flow"] = df[tx_col].map(flow_direction) if tx_col else "Unknown"

    # helpers
    df["_month"] = df[date_col].dt.to_period("M").dt.to_timestamp()
    df["_dow"]   = df[date_col].dt.day_name()
    df["_hour"]  = df[date_col].dt.hour
    df["_date_only"] = df[date_col].dt.date

    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()

    months_index = pd.date_range(min_date, max_date, freq="MS")
    months_list  = [d.date() for d in months_index]

    return DataContext(
        df=df,
        date_col=date_col, amt_col=amt_col, cat_col=cat_col, status_col=status_col,
        instr_col=instr_col, merchant_col=merchant_col, tx_col=tx_col,
        months_list=months_list, months_index=months_index,
        min_date=min_date, max_date=max_date
    )
