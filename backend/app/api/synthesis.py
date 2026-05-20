from fastapi import APIRouter
from app.engines.strategic_synthesis import run_synthesis, detect_cross_layer_conflicts, condensed_brief, synthesis_memory

router = APIRouter()


@router.get('/status')
async def get_synthesis_status():
    sample = {
        "priorities": [{"label": "stability risk", "score": 0.92}, {"label": "reliability drift", "score": 0.83}, {"label": "operator overload", "score": 0.78}],
        "noise": [{"label": "duplicate alert class", "noise_score": 0.95}, {"label": "stale narrative", "noise_score": 0.82}, {"label": "low-impact metric", "noise_score": 0.8}],
        "risks": [{"label": "regime instability", "score": 0.88}, {"label": "governance incident", "score": 0.74}, {"label": "calibration decay", "score": 0.7}],
    }
    return {"status": run_synthesis(sample)}


@router.post('/run')
async def post_synthesis_run(body: dict):
    return run_synthesis(body)


@router.post('/conflicts')
async def post_synthesis_conflicts(body: dict):
    return {"conflicts": detect_cross_layer_conflicts(body)}


@router.get('/brief')
async def get_synthesis_brief():
    sample = {
        "priorities": [{"label": "mission-safe simplification", "score": 0.89}, {"label": "replay realism", "score": 0.84}, {"label": "alert suppression", "score": 0.8}],
        "noise": [{"label": "redundant dashboard widget", "noise_score": 0.9}, {"label": "stale anomaly thread", "noise_score": 0.86}, {"label": "legacy report", "noise_score": 0.77}],
        "risks": [{"label": "operator fatigue", "score": 0.81}, {"label": "timing conflict", "score": 0.75}, {"label": "false urgency", "score": 0.72}],
    }
    return condensed_brief(sample)


@router.get('/memory')
async def get_synthesis_memory():
    return synthesis_memory()
