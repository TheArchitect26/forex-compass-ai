from fastapi import APIRouter
from app.engines.evidence_registry import (
    evidence_status,
    register_evidence,
    control_map,
    chain_of_custody,
    readiness_review,
    evidence_memory,
)

router = APIRouter()

@router.get('/status')
async def get_status(): return evidence_status()

@router.post('/register')
async def post_register(body: dict): return register_evidence(body)

@router.post('/control-map')
async def post_control_map(body: dict): return control_map(body)

@router.post('/chain-of-custody')
async def post_chain_of_custody(body: dict): return chain_of_custody(body)

@router.post('/readiness-review')
async def post_readiness_review(body: dict): return readiness_review(body)

@router.get('/memory')
async def get_memory(): return evidence_memory()
