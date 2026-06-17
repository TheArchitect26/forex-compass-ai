from fastapi import APIRouter
from app.engines import news as news_engine

router = APIRouter()


@router.get("/calendar")
async def calendar():
    return await news_engine.upcoming_events()


@router.get("/headlines")
async def headlines():
    return await news_engine.headlines()


@router.get("/status")
async def status():
    return news_engine.provider_status()
