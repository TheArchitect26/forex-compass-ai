from fastapi import APIRouter
from app.engines.knowledge_compression import compression_status, distill, strategic_lessons, anti_patterns, heuristics, compression_memory

router = APIRouter()


@router.get('/status')
async def get_compression_status():
    return compression_status()


@router.post('/distill')
async def post_distill(body: dict):
    return distill(body)


@router.post('/strategic-lessons')
async def post_strategic_lessons(body: dict):
    return strategic_lessons(body)


@router.post('/anti-patterns')
async def post_anti_patterns(body: dict):
    return anti_patterns(body)


@router.post('/heuristics')
async def post_heuristics(body: dict):
    return heuristics(body)


@router.get('/memory')
async def get_compression_memory():
    return compression_memory()
