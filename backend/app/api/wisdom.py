from fastapi import APIRouter
from app.engines.institutional_wisdom import wisdom_status, ambiguity_review, judgment_audit, restraint_check, prudence_review, wisdom_memory

router = APIRouter()


@router.get('/status')
async def get_wisdom_status():
    return wisdom_status()


@router.post('/ambiguity-review')
async def post_ambiguity_review(body: dict):
    return ambiguity_review(body)


@router.post('/judgment-audit')
async def post_judgment_audit(body: dict):
    return judgment_audit(body)


@router.post('/restraint-check')
async def post_restraint_check(body: dict):
    return restraint_check(body)


@router.post('/prudence-review')
async def post_prudence_review(body: dict):
    return prudence_review(body)


@router.get('/memory')
async def get_wisdom_memory():
    return wisdom_memory()
