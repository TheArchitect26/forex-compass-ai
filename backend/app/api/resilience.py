from fastapi import APIRouter
from app.engines.existential_resilience import resilience_status, crisis_scan, continuity_plan, black_swan_review, recovery_readiness, resilience_memory

router = APIRouter()


@router.get('/status')
async def get_resilience_status():
    return resilience_status()


@router.post('/crisis-scan')
async def post_crisis_scan(body: dict):
    return crisis_scan(body)


@router.post('/continuity-plan')
async def post_continuity_plan(body: dict):
    return continuity_plan(body)


@router.post('/black-swan-review')
async def post_black_swan_review(body: dict):
    return black_swan_review(body)


@router.post('/recovery-readiness')
async def post_recovery_readiness(body: dict):
    return recovery_readiness(body)


@router.get('/memory')
async def get_resilience_memory():
    return resilience_memory()
