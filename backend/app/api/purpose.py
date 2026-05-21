from fastapi import APIRouter
from app.engines.purpose_coherence import purpose_status, coherence_audit, meaning_drift, anti_hollowing, mission_alignment, purpose_memory

router = APIRouter()


@router.get('/status')
async def get_purpose_status():
    return purpose_status()


@router.post('/coherence-audit')
async def post_coherence_audit(body: dict):
    return coherence_audit(body)


@router.post('/meaning-drift')
async def post_meaning_drift(body: dict):
    return meaning_drift(body)


@router.post('/anti-hollowing')
async def post_anti_hollowing(body: dict):
    return anti_hollowing(body)


@router.post('/mission-alignment')
async def post_mission_alignment(body: dict):
    return mission_alignment(body)


@router.get('/memory')
async def get_purpose_memory():
    return purpose_memory()
