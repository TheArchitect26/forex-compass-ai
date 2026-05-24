from fastapi import APIRouter
from app.engines.feature_flag_governance import feature_flags_status, feature_flag_audit, stale_review, cleanup_plan, rollout_safety, feature_flags_memory

router = APIRouter()

@router.get('/status')
async def get_feature_flags_status(): return feature_flags_status()

@router.post('/audit')
async def post_feature_flags_audit(body: dict): return feature_flag_audit(body)

@router.post('/stale-review')
async def post_stale_review(body: dict): return stale_review(body)

@router.post('/cleanup-plan')
async def post_cleanup_plan(body: dict): return cleanup_plan(body)

@router.post('/rollout-safety')
async def post_rollout_safety(body: dict): return rollout_safety(body)

@router.get('/memory')
async def get_feature_flags_memory(): return feature_flags_memory()
