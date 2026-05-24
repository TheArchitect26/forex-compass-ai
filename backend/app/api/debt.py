from fastapi import APIRouter
from app.engines.technical_debt_observatory import debt_status, debt_scan, prioritize_debt, paydown_plan, dependency_risk, debt_memory

router = APIRouter()


@router.get('/status')
async def get_debt_status():
    return debt_status()


@router.post('/scan')
async def post_debt_scan(body: dict):
    return debt_scan(body)


@router.post('/prioritize')
async def post_prioritize_debt(body: dict):
    return prioritize_debt(body)


@router.post('/paydown-plan')
async def post_paydown_plan(body: dict):
    return paydown_plan(body)


@router.post('/dependency-risk')
async def post_dependency_risk(body: dict):
    return dependency_risk(body)


@router.get('/memory')
async def get_debt_memory():
    return debt_memory()
