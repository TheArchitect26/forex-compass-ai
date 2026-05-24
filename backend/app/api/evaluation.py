from fastapi import APIRouter
from app.engines.institutional_evaluation import evaluation_status, maturity_assessment, benchmark, improvement_plan, regression_review, evaluation_memory

router = APIRouter()

@router.get('/status')
async def get_evaluation_status(): return evaluation_status()

@router.post('/maturity-assessment')
async def post_maturity_assessment(body: dict): return maturity_assessment(body)

@router.post('/benchmark')
async def post_benchmark(body: dict): return benchmark(body)

@router.post('/improvement-plan')
async def post_improvement_plan(body: dict): return improvement_plan(body)

@router.post('/regression-review')
async def post_regression_review(body: dict): return regression_review(body)

@router.get('/memory')
async def get_evaluation_memory(): return evaluation_memory()
