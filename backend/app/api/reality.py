from fastapi import APIRouter
from app.engines.reality_anchoring import reality_status, relevance_score, detect_internal_loops, pragmatism_safeguards, reality_workflows
from app.engines.wisdom_architecture import wisdom_status, uncertainty_integrity, anti_maximalism

router = APIRouter()


@router.get('/reality-status')
async def get_reality_status():
    payload = {
        "practical_utility": 0.77,
        "empirical_grounding": 0.74,
        "real_world_relevance": 0.73,
        "recommendation_applicability": 0.72,
        "operator_utility": 0.78,
        "replay_to_reality_consistency": 0.69,
        "strategic_usefulness_decay": 0.24,
    }
    return {
        "reality_status": reality_status(payload),
        "external_grounding": {
            "real_world_outcome_alignment": 0.71,
            "actionable_value_density": 0.74,
            "governance_usefulness": 0.7,
            "operator_impact_quality": 0.76,
        },
        "no_execution": True,
    }


@router.get('/relevance-score')
async def get_relevance_score():
    return {"relevance_score": relevance_score({}), "advisory_only": True}


@router.post('/internal-loop-detection')
async def post_internal_loop_detection(body: dict):
    return detect_internal_loops(body)


@router.post('/pragmatism-safeguards')
async def post_pragmatism_safeguards(body: dict):
    return pragmatism_safeguards(body)


@router.post('/reality-workflows')
async def post_reality_workflows(body: dict):
    return reality_workflows(body)


@router.get('/wisdom-grounding')
async def get_wisdom_grounding():
    return {
        "wisdom": wisdom_status({}),
        "uncertainty_integrity": uncertainty_integrity({}),
        "anti_maximalism": anti_maximalism({}),
        "reality_connected": True,
    }
