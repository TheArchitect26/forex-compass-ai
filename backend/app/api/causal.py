from fastapi import APIRouter
from app.engines.causal_intelligence import causal_status, analyze_root_cause, causal_graph, propagation_estimate, intervention_effect, causal_memory

router = APIRouter()


@router.get('/status')
async def get_causal_status():
    return causal_status()


@router.post('/analyze')
async def post_causal_analyze(body: dict):
    return analyze_root_cause(body)


@router.post('/graph')
async def post_causal_graph(body: dict):
    return causal_graph(body)


@router.post('/propagation')
async def post_causal_propagation(body: dict):
    return propagation_estimate(body)


@router.post('/intervention-effect')
async def post_causal_intervention_effect(body: dict):
    return intervention_effect(body)


@router.get('/memory')
async def get_causal_memory():
    return causal_memory()
