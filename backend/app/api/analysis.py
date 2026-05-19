from fastapi import APIRouter
from app.engines.signal_intelligence import analyze_pair

router = APIRouter()


@router.get("/{pair_base}/{pair_quote}")
async def analyze(pair_base: str, pair_quote: str):
    return await analyze_pair(f"{pair_base.upper()}/{pair_quote.upper()}")
