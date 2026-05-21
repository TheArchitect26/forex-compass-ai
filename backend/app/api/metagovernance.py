from fastapi import APIRouter
from app.engines.meta_governance import metagovernance_status, policy_conflicts, safeguard_audit, harmonization_plan, doctrine_drift, metagovernance_memory

router = APIRouter()


@router.get('/status')
async def get_metagovernance_status():
    return metagovernance_status()


@router.post('/policy-conflicts')
async def post_policy_conflicts(body: dict):
    return policy_conflicts(body)


@router.post('/safeguard-audit')
async def post_safeguard_audit(body: dict):
    return safeguard_audit(body)


@router.post('/harmonization-plan')
async def post_harmonization_plan(body: dict):
    return harmonization_plan(body)


@router.post('/doctrine-drift')
async def post_doctrine_drift(body: dict):
    return doctrine_drift(body)


@router.get('/memory')
async def get_metagovernance_memory():
    return metagovernance_memory()
