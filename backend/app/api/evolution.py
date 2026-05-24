from fastapi import APIRouter
from app.engines.evolutionary_resilience import evolution_status, transition_assessment, migration_readiness, continuity_plan, rollback_plan, evolution_memory

router = APIRouter()


@router.get('/status')
async def get_evolution_status():
    return evolution_status()


@router.post('/transition-assessment')
async def post_transition_assessment(body: dict):
    return transition_assessment(body)


@router.post('/migration-readiness')
async def post_migration_readiness(body: dict):
    return migration_readiness(body)


@router.post('/continuity-plan')
async def post_continuity_plan(body: dict):
    return continuity_plan(body)


@router.post('/rollback-plan')
async def post_rollback_plan(body: dict):
    return rollback_plan(body)


@router.get('/memory')
async def get_evolution_memory():
    return evolution_memory()
