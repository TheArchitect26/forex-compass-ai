from fastapi import APIRouter
from app.engines.adaptive_pathways import pathway_catalog, evaluate_triggers, recommend_pathway, compare_pathways, pathways_memory

router = APIRouter()


@router.get('/status')
async def get_pathways_status():
    return pathway_catalog()


@router.post('/evaluate')
async def post_pathways_evaluate(body: dict):
    return evaluate_triggers(body)


@router.post('/recommend')
async def post_pathways_recommend(body: dict):
    return recommend_pathway(body)


@router.post('/compare')
async def post_pathways_compare(body: dict):
    return compare_pathways(body)


@router.get('/memory')
async def get_pathways_memory():
    return pathways_memory()
