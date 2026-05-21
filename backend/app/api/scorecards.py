from fastapi import APIRouter
from app.engines.scorecard_governance import (
    scorecard_status,
    evaluate_scorecards,
    entity_scorecard,
    readiness_gates,
    improvement_plan,
    scorecard_memory,
)

router = APIRouter()

@router.get('/status')
async def get_scorecard_status(): return scorecard_status()

@router.post('/evaluate')
async def post_evaluate(body: dict): return evaluate_scorecards(body)

@router.post('/entity-scorecard')
async def post_entity_scorecard(body: dict): return entity_scorecard(body)

@router.post('/readiness-gates')
async def post_readiness_gates(body: dict): return readiness_gates(body)

@router.post('/improvement-plan')
async def post_improvement_plan(body: dict): return improvement_plan(body)

@router.get('/memory')
async def get_scorecard_memory(): return scorecard_memory()
