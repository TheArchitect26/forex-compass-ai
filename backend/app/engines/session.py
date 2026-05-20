from datetime import datetime, timezone

def classify_session(dt: datetime) -> str:
    h = dt.astimezone(timezone.utc).hour
    if 0 <= h < 7:
        return "Asian"
    if 7 <= h < 12:
        return "London"
    if 12 <= h < 16:
        return "London-NewYork overlap"
    if 16 <= h < 21:
        return "NewYork"
    return "off-hours"
