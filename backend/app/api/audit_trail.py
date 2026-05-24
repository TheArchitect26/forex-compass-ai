from fastapi import APIRouter
from app.engines.institutional_audit_trail import (
    audit_trail_status,
    record_event,
    decision_provenance,
    trace,
    governance_lineage,
    audit_trail_memory,
)

router = APIRouter()

@router.get('/status')
async def get_status(): return audit_trail_status()

@router.post('/record')
async def post_record(body: dict): return record_event(body)

@router.post('/provenance')
async def post_provenance(body: dict): return decision_provenance(body)

@router.post('/trace')
async def post_trace(body: dict): return trace(body)

@router.post('/governance-lineage')
async def post_governance_lineage(body: dict): return governance_lineage(body)

@router.get('/memory')
async def get_memory(): return audit_trail_memory()
