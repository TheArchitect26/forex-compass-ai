from fastapi import APIRouter
from app.engines.controlled_evolution import evolution_control_status, capability_audit, lifecycle_review, retirement_candidates, evolution_plan, evolution_control_memory

router = APIRouter()

@router.get('/status')
async def get_evolution_control_status(): return evolution_control_status()

@router.post('/capability-audit')
async def post_capability_audit(body: dict): return capability_audit(body)

@router.post('/lifecycle-review')
async def post_lifecycle_review(body: dict): return lifecycle_review(body)

@router.post('/retirement-candidates')
async def post_retirement_candidates(body: dict): return retirement_candidates(body)

@router.post('/evolution-plan')
async def post_evolution_plan(body: dict): return evolution_plan(body)

@router.get('/memory')
async def get_evolution_control_memory(): return evolution_control_memory()
