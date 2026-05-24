from fastapi import APIRouter
from app.engines.operational_orchestration import operational_status, review_plan, deferred_action, maintenance_cycle, cadence_check, operations_memory

router = APIRouter()


@router.get('/status')
async def get_operations_status():
    return operational_status()


@router.post('/review-plan')
async def post_review_plan(body: dict):
    return review_plan(body)


@router.post('/deferred-action')
async def post_deferred_action(body: dict):
    return deferred_action(body)


@router.post('/maintenance-cycle')
async def post_maintenance_cycle(body: dict):
    return maintenance_cycle(body)


@router.post('/cadence-check')
async def post_cadence_check(body: dict):
    return cadence_check(body)


@router.get('/memory')
async def get_operations_memory():
    return operations_memory()
