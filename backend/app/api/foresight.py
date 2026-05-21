from fastapi import APIRouter
from app.engines.anticipatory_intelligence import foresight_scores, early_warnings, detect_trajectory, intervention_plan, foresight_memory

router = APIRouter()


@router.get('/status')
async def get_foresight_status():
    scores = foresight_scores({})
    trajectory = detect_trajectory({"trajectory_index": 0.25})
    return {"foresight_scores": scores, "trajectory_status": trajectory, "advisory_only": True}


@router.post('/scan')
async def post_foresight_scan(body: dict):
    return {
        "foresight_scores": foresight_scores(body),
        "trajectory_status": detect_trajectory(body),
        "warnings": early_warnings(body)["warnings"],
    }


@router.post('/early-warnings')
async def post_early_warnings(body: dict):
    return early_warnings(body)


@router.post('/intervention-plan')
async def post_intervention_plan(body: dict):
    return intervention_plan(body)


@router.get('/memory')
async def get_foresight_memory():
    return foresight_memory()
