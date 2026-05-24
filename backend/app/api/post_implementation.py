from fastapi import APIRouter
from app.engines.post_implementation_review import (
    post_implementation_status,
    review,
    expected_vs_actual,
    lessons_learned,
    improvement_actions,
    post_implementation_memory,
)

router = APIRouter()

@router.get('/status')
async def get_status(): return post_implementation_status()

@router.post('/review')
async def post_review(body: dict): return review(body)

@router.post('/expected-vs-actual')
async def post_expected_vs_actual(body: dict): return expected_vs_actual(body)

@router.post('/lessons-learned')
async def post_lessons_learned(body: dict): return lessons_learned(body)

@router.post('/improvement-actions')
async def post_improvement_actions(body: dict): return improvement_actions(body)

@router.get('/memory')
async def get_memory(): return post_implementation_memory()
