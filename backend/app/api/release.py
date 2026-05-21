from fastapi import APIRouter
from app.engines.release_governance import release_status, release_readiness_check, build_risk, rollback_plan, post_release_review, release_memory

router = APIRouter()


@router.get('/status')
async def get_release_status():
    return release_status()


@router.post('/readiness-check')
async def post_release_readiness_check(body: dict):
    return release_readiness_check(body)


@router.post('/build-risk')
async def post_release_build_risk(body: dict):
    return build_risk(body)


@router.post('/rollback-plan')
async def post_release_rollback_plan(body: dict):
    return rollback_plan(body)


@router.post('/post-release-review')
async def post_post_release_review(body: dict):
    return post_release_review(body)


@router.get('/memory')
async def get_release_memory():
    return release_memory()
