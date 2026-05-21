from fastapi import APIRouter
from app.engines.refactoring_intelligence import refactoring_status, entropy_scan, recovery_plan, coupling_analysis, refactor_priorities, refactoring_memory

router = APIRouter()


@router.get('/status')
async def get_refactoring_status():
    return refactoring_status()


@router.post('/entropy-scan')
async def post_entropy_scan(body: dict):
    return entropy_scan(body)


@router.post('/recovery-plan')
async def post_recovery_plan(body: dict):
    return recovery_plan(body)


@router.post('/coupling-analysis')
async def post_coupling_analysis(body: dict):
    return coupling_analysis(body)


@router.post('/refactor-priorities')
async def post_refactor_priorities(body: dict):
    return refactor_priorities(body)


@router.get('/memory')
async def get_refactoring_memory():
    return refactoring_memory()
