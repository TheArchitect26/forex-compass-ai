from fastapi import APIRouter
from app.engines.institutional_policy import (
    policy_status,
    policies_list,
    evaluate_compliance,
    conflict_review,
    doctrine_summary,
    policy_memory,
)

router = APIRouter()

@router.get('/status')
async def get_status(): return policy_status()

@router.post('/list')
async def post_list(body: dict): return policies_list(body)

@router.post('/evaluate-compliance')
async def post_evaluate_compliance(body: dict): return evaluate_compliance(body)

@router.post('/conflict-review')
async def post_conflict_review(body: dict): return conflict_review(body)

@router.post('/doctrine-summary')
async def post_doctrine_summary(body: dict): return doctrine_summary(body)

@router.get('/memory')
async def get_memory(): return policy_memory()
