from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.db import get_db
from app.models import ReplaySession, HistoricalCandle, PortfolioReplaySession
from app.engines.session import classify_session
from app.engines.portfolio import estimate_position_size, compute_metrics, correlation_bucket

router = APIRouter()

class StartBody(BaseModel):
    pair: str
    timeframe: str
    start: str
    end: str
    strategy_profile: str = "intraday"

@router.post('/session/start')
async def start_session(body: StartBody, db: AsyncSession = Depends(get_db)):
    from datetime import datetime
    start = datetime.fromisoformat(body.start)
    end = datetime.fromisoformat(body.end)
    sess = ReplaySession(pair=body.pair, timeframe=body.timeframe, strategy_profile=body.strategy_profile, start_ts=start, end_ts=end, cursor_ts=start, steps=0, state={"reliability":50, "regime":"unknown"}, status="running")
    db.add(sess); await db.commit(); await db.refresh(sess)
    return {"session_id": sess.id, "status": sess.status}

@router.post('/session/step')
async def step_session(body: dict, db: AsyncSession = Depends(get_db)):
    sid = int(body.get('session_id'))
    sess = await db.get(ReplaySession, sid)
    if not sess: raise HTTPException(404, 'session not found')
    if sess.status != 'running': return {"session_id": sid, "status": sess.status}
    q = await db.execute(select(HistoricalCandle).where(HistoricalCandle.pair==sess.pair, HistoricalCandle.timeframe==sess.timeframe, HistoricalCandle.timestamp>=sess.cursor_ts, HistoricalCandle.timestamp<=sess.end_ts).order_by(HistoricalCandle.timestamp.asc()).limit(1))
    c = q.scalars().first()
    if not c:
        sess.status = 'completed'; await db.commit(); return {"session_id": sid, "status": sess.status}
    sess.cursor_ts = c.timestamp
    sess.steps += 1
    sess.state = {**(sess.state or {}), "last_price": c.close, "session": classify_session(c.timestamp)}
    await db.commit()
    return {"session_id": sid, "status": sess.status, "step": sess.steps, "cursor": sess.cursor_ts.isoformat(), "state": sess.state}

@router.get('/session/{sid}')
async def get_session(sid: int, db: AsyncSession = Depends(get_db)):
    sess = await db.get(ReplaySession, sid)
    if not sess: raise HTTPException(404, 'session not found')
    return {"id": sess.id, "pair": sess.pair, "timeframe": sess.timeframe, "strategy_profile": sess.strategy_profile, "start": sess.start_ts.isoformat(), "end": sess.end_ts.isoformat(), "cursor": sess.cursor_ts.isoformat() if sess.cursor_ts else None, "steps": sess.steps, "status": sess.status, "state": sess.state}

@router.post('/portfolio/start')
async def portfolio_start(body: dict, db: AsyncSession = Depends(get_db)):
    from datetime import datetime
    start = datetime.fromisoformat(body.get('start'))
    end = datetime.fromisoformat(body.get('end'))
    sess = ReplaySession(pair=body.get('pair','EUR/USD'), timeframe=body.get('timeframe','1h'), strategy_profile=body.get('strategy_profile','intraday'), start_ts=start, end_ts=end, cursor_ts=start, steps=0, state={"reliability":50}, status='running')
    db.add(sess); await db.flush()
    p = PortfolioReplaySession(name=body.get('name','portfolio-lab'), pair=sess.pair, timeframe=sess.timeframe, strategy_profile=sess.strategy_profile, sizing_mode=body.get('sizing_mode','fixed_risk'), balance=float(body.get('initial_balance',10000)), equity_curve=[float(body.get('initial_balance',10000))], replay_session_id=sess.id, status='running', exposure_state={"max_concurrent": int(body.get('max_concurrent',3))}, risk_state={"max_exposure": float(body.get('max_exposure',0.3))})
    db.add(p); await db.commit(); await db.refresh(p)
    return {"portfolio_session_id": p.id, "replay_session_id": sess.id, "status": p.status}

@router.post('/portfolio/step')
async def portfolio_step(body: dict, db: AsyncSession = Depends(get_db)):
    pid = int(body.get('portfolio_session_id'))
    p = await db.get(PortfolioReplaySession, pid)
    if not p: raise HTTPException(404, 'portfolio session not found')
    if p.status != 'running': return {"portfolio_session_id": pid, "status": p.status}
    # step underlying replay
    out = await step_session({"session_id": p.replay_session_id}, db)
    if out.get('status') == 'completed':
        p.status = 'completed'
        await db.commit()
        return {"portfolio_session_id": pid, "status": p.status, "analytics": compute_metrics(p.equity_curve)}
    last_price = out.get('state', {}).get('last_price')
    confidence = float(body.get('confidence', 65))
    atr_pct = float(body.get('atr_pct', 0.005))
    size = estimate_position_size(p.sizing_mode, p.balance, confidence, atr_pct)
    action = body.get('action', 'accept')
    open_positions = list(p.open_positions or [])
    closed_positions = list(p.closed_positions or [])
    # delayed confirmation / partial fill / slippage curve approx
    fill_ratio = 0.7 if body.get('low_liquidity') else 1.0
    slippage_penalty = 0.0002 if body.get('high_volatility') else 0.00005
    if action == 'accept' and len(open_positions) < p.exposure_state.get('max_concurrent',3):
        open_positions.append({"entry": last_price + slippage_penalty, "size": size*fill_ratio, "session": out.get('state',{}).get('session')})
    # simple close rule every 3 steps
    if out.get('step',0) % 3 == 0 and open_positions:
        pos = open_positions.pop(0)
        pnl = (last_price - pos['entry']) * 10000 * pos['size']
        closed_positions.append({**pos, "exit": last_price, "pnl": pnl})
        p.balance += pnl
    p.open_positions = open_positions
    p.closed_positions = closed_positions
    eq = list(p.equity_curve or [])
    eq.append(p.balance + sum((last_price - x['entry']) * 10000 * x['size'] for x in open_positions))
    p.equity_curve = eq
    # exposure/correlation warnings
    corr_warn = None
    if len(open_positions) >= 2:
        corr_warn = correlation_bucket(p.pair, p.pair)
    p.risk_state = {**(p.risk_state or {}), "correlation_warning": corr_warn, "session_exposure": out.get('state',{}).get('session')}
    await db.commit()
    analytics = compute_metrics(eq)
    return {"portfolio_session_id": pid, "status": p.status, "balance": p.balance, "open_positions": len(open_positions), "closed_positions": len(closed_positions), "analytics": analytics, "risk_state": p.risk_state}

@router.get('/portfolio/{pid}')
async def portfolio_get(pid: int, db: AsyncSession = Depends(get_db)):
    p = await db.get(PortfolioReplaySession, pid)
    if not p: raise HTTPException(404, 'portfolio session not found')
    return {"id": p.id, "name": p.name, "pair": p.pair, "timeframe": p.timeframe, "profile": p.strategy_profile, "sizing_mode": p.sizing_mode, "status": p.status, "balance": p.balance, "equity_curve": p.equity_curve, "open_positions": p.open_positions, "closed_positions": p.closed_positions, "exposure_state": p.exposure_state, "risk_state": p.risk_state, "analytics": compute_metrics(p.equity_curve)}

@router.post('/stress-test')
async def stress_test(body: dict, db: AsyncSession = Depends(get_db)):
    # reproducible deterministic stress multipliers
    base = float(body.get('base_score', 60))
    factors = {
        "flash_volatility": -12,
        "spread_spike": -8,
        "missing_candles": -10,
        "delayed_confirmations": -6,
        "bad_data": -15,
        "regime_shift": -9,
        "low_liquidity": -7,
    }
    active = body.get('scenarios', list(factors.keys()))
    delta = sum(factors.get(x, 0) for x in active)
    score = max(0, base + delta)
    return {"stress_score": score, "scenarios": active, "details": {k: factors[k] for k in active}, "reproducible": True}
