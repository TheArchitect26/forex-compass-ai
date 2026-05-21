from fastapi import APIRouter
from app.engines.temporal_intelligence import timing_status, classify_timing, rhythm_scan, relevance_decay, detect_cycles, timing_conflicts, pacing_recommendation

router = APIRouter()


@router.get('/timing-status')
async def get_timing_status():
    base = timing_status({})
    return {"timing_status": base, "strategic_pacing": pacing_recommendation({})}


@router.post('/classify')
async def post_classify(body: dict):
    return classify_timing(body)


@router.post('/rhythm-scan')
async def post_rhythm_scan(body: dict):
    return rhythm_scan(body)


@router.post('/relevance-decay')
async def post_relevance_decay(body: dict):
    return relevance_decay(body)


@router.post('/cycle-detection')
async def post_cycle_detection(body: dict):
    return detect_cycles(body)


@router.post('/timing-conflicts')
async def post_timing_conflicts(body: dict):
    return timing_conflicts(body)


@router.get('/memory')
async def get_temporal_memory():
    return {
        "recurring_cycles": ["weekly alert burst"],
        "timing_decisions": ["defer low-impact governance review"],
        "delayed_reviews": ["monthly replay deep-dive"],
        "deferred_items": ["low priority dashboard cleanup"],
        "archived_stale_items": ["obsolete anomaly narrative"],
        "major_timing_corrections": ["urgency policy normalized"],
        "rhythm_disruptions": ["high volatility week with operator overload"],
    }
