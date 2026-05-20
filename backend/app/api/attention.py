from fastapi import APIRouter
from app.engines.attention_architecture import classify_attention, extract_strategic_signal, priority_status, detect_attention_fatigue, relevance_half_life, focus_mode, anti_noise_governance

router = APIRouter()


@router.get('/priority-status')
async def get_priority_status():
    return {"priority_status": priority_status({}), "human_attention_sovereign": True, "no_execution": True}


@router.post('/classify')
async def post_classify_attention(body: dict):
    return classify_attention(body)


@router.post('/extract')
async def post_extract_strategic_signal(body: dict):
    return extract_strategic_signal(body)


@router.post('/fatigue-detection')
async def post_fatigue_detection(body: dict):
    return detect_attention_fatigue(body)


@router.post('/focus-mode')
async def post_focus_mode(body: dict):
    return focus_mode(str(body.get("mode", "executive_overview")))


@router.post('/relevance-half-life')
async def post_relevance_half_life(body: dict):
    return relevance_half_life(body)


@router.post('/anti-noise-governance')
async def post_anti_noise_governance(body: dict):
    return anti_noise_governance(body)


@router.get('/attention-memory')
async def get_attention_memory():
    return {
        "highest_value_insights": ["macro-volatility-regime-shift detected early"],
        "most_useful_investigations": ["EURUSD anomaly cluster triage"],
        "most_impactful_simplifications": ["reduced repetitive alerts by 40%"],
        "repeated_distraction_patterns": ["overnight low-impact alert bursts"],
        "major_focus_recoveries": ["single-pair focus cycle restored clarity"],
        "strategic_clarity_improvements": ["priority gating policy adopted"],
    }
