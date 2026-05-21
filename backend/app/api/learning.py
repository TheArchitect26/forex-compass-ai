from fastapi import APIRouter
from app.engines.institutional_learning import learning_status, extract_lessons, intervention_review, forecast_review, assumption_review, learning_memory

router = APIRouter()


@router.get('/status')
async def get_learning_status():
    return learning_status()


@router.post('/extract-lessons')
async def post_extract_lessons(body: dict):
    return extract_lessons(body)


@router.post('/intervention-review')
async def post_intervention_review(body: dict):
    return intervention_review(body)


@router.post('/forecast-review')
async def post_forecast_review(body: dict):
    return forecast_review(body)


@router.post('/assumption-review')
async def post_assumption_review(body: dict):
    return assumption_review(body)


@router.get('/memory')
async def get_learning_memory():
    return learning_memory()
