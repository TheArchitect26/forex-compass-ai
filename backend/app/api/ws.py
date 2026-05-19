"""WebSocket — live price ticks for charts."""
import asyncio, json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.engines.market_data import market_data

router = APIRouter()


@router.websocket("/ws/prices")
async def prices(ws: WebSocket):
    await ws.accept()
    pair = ws.query_params.get("pair", "EUR/USD")
    try:
        while True:
            df = await market_data.ohlcv(pair, "1min", 2)
            last = df.iloc[-1]
            await ws.send_text(json.dumps({
                "pair": pair, "time": int(last.datetime.timestamp()),
                "price": float(last.close),
            }))
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        return
