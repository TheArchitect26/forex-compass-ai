from fastapi import APIRouter
from app.engines.architectural_coherence import coherence_status, overlap_scan, consolidation_plan, simplification_risk, architecture_memory

router = APIRouter()


@router.get('/status')
async def get_architecture_status():
    return coherence_status()


@router.post('/overlap-scan')
async def post_overlap_scan(body: dict):
    return overlap_scan(body)


@router.post('/consolidation-plan')
async def post_consolidation_plan(body: dict):
    return consolidation_plan(body)


@router.post('/simplification-risk')
async def post_simplification_risk(body: dict):
    return simplification_risk(body)


@router.get('/memory')
async def get_architecture_memory():
    return architecture_memory()
