from fastapi import APIRouter
from app.engines.trust_calibration import trust_status, credibility_audit, recommendation_legitimacy, uncertainty_audit, overreach_scan, trust_memory

router = APIRouter()


@router.get('/status')
async def get_trust_status():
    return trust_status()


@router.post('/credibility-audit')
async def post_credibility_audit(body: dict):
    return credibility_audit(body)


@router.post('/recommendation-legitimacy')
async def post_recommendation_legitimacy(body: dict):
    return recommendation_legitimacy(body)


@router.post('/uncertainty-audit')
async def post_uncertainty_audit(body: dict):
    return uncertainty_audit(body)


@router.post('/overreach-scan')
async def post_overreach_scan(body: dict):
    return overreach_scan(body)


@router.get('/memory')
async def get_trust_memory():
    return trust_memory()
