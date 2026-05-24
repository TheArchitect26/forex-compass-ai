from fastapi import APIRouter
from app.engines.memory_retrieval import memory_status, memory_search, contextual_recall, related_items, staleness_review, memory_index

router = APIRouter()


@router.get('/status')
async def get_memory_status():
    return memory_status()


@router.post('/search')
async def post_memory_search(body: dict):
    return memory_search(body)


@router.post('/contextual-recall')
async def post_contextual_recall(body: dict):
    return contextual_recall(body)


@router.post('/related-items')
async def post_related_items(body: dict):
    return related_items(body)


@router.post('/staleness-review')
async def post_staleness_review(body: dict):
    return staleness_review(body)


@router.get('/index')
async def get_memory_index():
    return memory_index()
