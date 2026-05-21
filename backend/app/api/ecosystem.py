from fastapi import APIRouter
from app.engines.ecosystem_intelligence import ecosystem_status, dependency_map, risk_scan, fallback_plan, environmental_pressure, ecosystem_memory

router = APIRouter()


@router.get('/status')
async def get_ecosystem_status():
    return ecosystem_status()


@router.post('/dependency-map')
async def post_dependency_map(body: dict):
    return dependency_map(body)


@router.post('/risk-scan')
async def post_risk_scan(body: dict):
    return risk_scan(body)


@router.post('/fallback-plan')
async def post_fallback_plan(body: dict):
    return fallback_plan(body)


@router.post('/environmental-pressure')
async def post_environmental_pressure(body: dict):
    return environmental_pressure(body)


@router.get('/memory')
async def get_ecosystem_memory():
    return ecosystem_memory()
