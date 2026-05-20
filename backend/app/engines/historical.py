from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from app.utils_time import utc_now

VALID_TF = {"1min":1,"5min":5,"15min":15,"30min":30,"1h":60,"4h":240,"1day":1440}


def normalize_pair(pair: str) -> str:
    p = pair.upper().replace("-", "/")
    if "/" not in p and len(p) == 6:
        p = f"{p[:3]}/{p[3:]}"
    return p


def normalize_timeframe(tf: str) -> str:
    return tf if tf in VALID_TF else "1h"


def malformed_ohlc(o,h,l,c) -> bool:
    return any(v is None for v in [o,h,l,c]) or h < max(o,c) or l > min(o,c) or l > h


def detect_gaps(timestamps: list[datetime], tf: str) -> int:
    if len(timestamps) < 2: return 0
    step = timedelta(minutes=VALID_TF.get(tf,60))
    gaps = 0
    for a,b in zip(timestamps[:-1], timestamps[1:]):
        if b - a > step * 1.5: gaps += 1
    return gaps


def integrity_score(total:int, dup:int, gaps:int, malformed:int, synthetic_ratio:float) -> int:
    score = 100
    score -= dup * 2
    score -= gaps * 3
    score -= malformed * 5
    score -= int(synthetic_ratio * 20)
    return max(0, score)
