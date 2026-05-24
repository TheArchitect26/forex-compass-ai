from fastapi import APIRouter
from app.engines.runtime_observability import observability_status, runtime_scan, endpoint_health, regression_check, incident_summary, observability_memory

router = APIRouter()


@router.get('/status')
async def get_observability_status():
    return observability_status()


@router.post('/runtime-scan')
async def post_runtime_scan(body: dict):
    return runtime_scan(body)


@router.post('/endpoint-health')
async def post_endpoint_health(body: dict):
    return endpoint_health(body)


@router.post('/regression-check')
async def post_regression_check(body: dict):
    return regression_check(body)


@router.post('/incident-summary')
async def post_incident_summary(body: dict):
    return incident_summary(body)


@router.get('/memory')
async def get_observability_memory():
    return observability_memory()
