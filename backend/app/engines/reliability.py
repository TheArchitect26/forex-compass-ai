from __future__ import annotations

def classify_alignment(bucket_mid: float, win_rate: float) -> str:
    if abs(win_rate - bucket_mid) <= 10:
        return "aligned"
    return "overconfident" if win_rate < bucket_mid else "underconfident"


def reliability_score(sample_size: int, win_rate: float, avg_net_pips: float, aligned_buckets: int) -> tuple[float, str]:
    score = min(100, max(0, (min(sample_size, 200) / 2) + win_rate * 0.4 + max(0, avg_net_pips) * 2 + aligned_buckets * 4))
    label = "unproven" if score < 25 else "weak" if score < 45 else "improving" if score < 65 else "reliable" if score < 80 else "strong"
    return round(score, 1), label
