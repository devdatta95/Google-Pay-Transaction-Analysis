import numpy as np

def _indian_group(n: int) -> str:
    s = f"{n:d}"
    if len(s) <= 3: return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head: parts.insert(0, head)
    return ",".join(parts + [tail])

def indian_number(x: float | int) -> str:
    if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
        return "—"
    neg = x < 0
    n = abs(int(round(x)))
    s = _indian_group(n)
    return ("-" if neg else "") + s

def fmt_currency_indian(x) -> str:
    if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
        return "—"
    return f"₹{indian_number(x)}"
