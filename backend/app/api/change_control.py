from fastapi import APIRouter
from app.engines.change_impact_analysis import (
    change_control_status,
    impact_analysis,
    review_requirements,
    rollback_readiness,
    approval_brief,
    change_control_memory,
)

router = APIRouter()

@router.get('/status')
async def get_status(): return change_control_status()

@router.post('/impact-analysis')
async def post_impact_analysis(body: dict): return impact_analysis(body)

@router.post('/review-requirements')
async def post_review_requirements(body: dict): return review_requirements(body)

@router.post('/rollback-readiness')
async def post_rollback_readiness(body: dict): return rollback_readiness(body)

@router.post('/approval-brief')
async def post_approval_brief(body: dict): return approval_brief(body)

@router.get('/memory')
async def get_memory(): return change_control_memory()
