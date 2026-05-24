from fastapi import APIRouter
from app.engines.golden_path_workflows import (
    golden_paths_status,
    workflow,
    checklist,
    validate_plan,
    deviation_review,
    golden_paths_memory,
)

router = APIRouter()

@router.get('/status')
async def get_status(): return golden_paths_status()

@router.post('/workflow')
async def post_workflow(body: dict): return workflow(body)

@router.post('/checklist')
async def post_checklist(body: dict): return checklist(body)

@router.post('/validate-plan')
async def post_validate_plan(body: dict): return validate_plan(body)

@router.post('/deviation-review')
async def post_deviation_review(body: dict): return deviation_review(body)

@router.get('/memory')
async def get_memory(): return golden_paths_memory()
