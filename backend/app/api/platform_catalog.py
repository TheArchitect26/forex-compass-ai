from fastapi import APIRouter
from app.engines.platform_catalog import (
    platform_catalog_status,
    catalog_entities,
    ownership_audit,
    dependency_map,
    golden_paths,
    platform_catalog_memory,
)

router = APIRouter()


@router.get('/status')
async def get_platform_catalog_status(): return platform_catalog_status()


@router.post('/entities')
async def post_catalog_entities(body: dict): return catalog_entities(body)


@router.post('/ownership-audit')
async def post_ownership_audit(body: dict): return ownership_audit(body)


@router.post('/dependency-map')
async def post_dependency_map(body: dict): return dependency_map(body)


@router.post('/golden-paths')
async def post_golden_paths(body: dict): return golden_paths(body)


@router.get('/memory')
async def get_platform_catalog_memory(): return platform_catalog_memory()
