from fastapi import APIRouter
from app.engines.operator_experience import ux_status, usability_audit, navigation_audit, readability_review, simplification_plan, ux_memory

router = APIRouter()


@router.get('/status')
async def get_ux_status():
    return ux_status()


@router.post('/usability-audit')
async def post_usability_audit(body: dict):
    return usability_audit(body)


@router.post('/navigation-audit')
async def post_navigation_audit(body: dict):
    return navigation_audit(body)


@router.post('/readability-review')
async def post_readability_review(body: dict):
    return readability_review(body)


@router.post('/simplification-plan')
async def post_simplification_plan(body: dict):
    return simplification_plan(body)


@router.get('/memory')
async def get_ux_memory():
    return ux_memory()
