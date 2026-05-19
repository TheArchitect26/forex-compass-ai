from fastapi import APIRouter
from app.engines import news as news_engine, sentiment

router = APIRouter()


@router.get("")
async def overall(currency: str | None = None):
    heads = await news_engine.headlines()
    return sentiment.aggregate(heads, currency=currency)
