from fastapi import APIRouter
from app.engines.scenario_intelligence import scenario_status, run_scenario, compare_scenarios, scenario_memory

router = APIRouter()


@router.get('/status')
async def get_scenario_status():
    return scenario_status()


@router.post('/run')
async def post_scenario_run(body: dict):
    return run_scenario(body)


@router.post('/compare')
async def post_scenario_compare(body: dict):
    return compare_scenarios(body)


@router.post('/tradeoffs')
async def post_scenario_tradeoffs(body: dict):
    return compare_scenarios(body)


@router.get('/memory')
async def get_scenario_memory():
    return scenario_memory()
