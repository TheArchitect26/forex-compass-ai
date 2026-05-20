from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import Signal, HistoricalCandle, IngestionRun
from app.engines.historical import malformed_ohlc, detect_gaps, integrity_score, normalize_pair, normalize_timeframe
from app.engines.market_data import market_data

router = APIRouter()

@router.get('/integrity')
async def integrity(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Signal))).scalars().all()
    malformed = [r.id for r in rows if '/' not in r.pair or r.timeframe not in {"1min","5min","15min","30min","1h","4h","1day"}]
    synthetic = sum(1 for r in rows if r.data_source == 'synthetic')
    dup_pairs = {}
    for r in rows:
        k=(r.pair,r.timeframe,r.created_at.replace(second=0,microsecond=0)); dup_pairs[k]=dup_pairs.get(k,0)+1
    duplicate_est = sum(1 for v in dup_pairs.values() if v>1)
    score = max(0,100-len(malformed)*5-duplicate_est*2-(20 if synthetic>0 else 0))
    return {"source_checks":{"synthetic_count":synthetic},"duplicate_candle_detection":{"estimated_duplicates":duplicate_est},"malformed_ohlc_detection":{"malformed_signal_refs":malformed},"synthetic_contamination_checks":{"synthetic_ratio":round(synthetic/max(1,len(rows)),3)},"replay_dataset_integrity_score":score}

@router.get('/integrity/datasets')
async def integrity_datasets(db: AsyncSession = Depends(get_db)):
    candles = (await db.execute(select(HistoricalCandle).order_by(HistoricalCandle.timestamp.asc()))).scalars().all()
    by = {}
    for c in candles:
        by.setdefault((c.pair,c.timeframe), []).append(c)
    items=[]
    for (pair,tf),cs in by.items():
        ts=[c.timestamp for c in cs]
        dup=len(cs)-len({t.isoformat() for t in ts})
        gaps=detect_gaps(ts, tf)
        mal=sum(1 for c in cs if malformed_ohlc(c.open,c.high,c.low,c.close))
        synth=sum(1 for c in cs if c.source=='synthetic')
        score=integrity_score(len(cs),dup,gaps,mal,synth/max(1,len(cs)))
        items.append({"pair":pair,"timeframe":tf,"rows":len(cs),"duplicates":dup,"gaps":gaps,"malformed":mal,"synthetic_ratio":round(synth/max(1,len(cs)),3),"integrity_score":score})
    return {"datasets": items}

@router.post('/ingest')
async def ingest(body: dict, db: AsyncSession = Depends(get_db)):
    pair = normalize_pair(body.get('pair','EUR/USD')); tf = normalize_timeframe(body.get('timeframe','1h')); limit=int(body.get('limit',500))
    df = await market_data.ohlcv(pair, tf, limit)
    fetched=len(df); inserted=0; malformed=0
    for r in df.itertuples():
        if malformed_ohlc(r.open,r.high,r.low,r.close):
            malformed += 1; continue
        exists=(await db.execute(select(HistoricalCandle).where(HistoricalCandle.pair==pair, HistoricalCandle.timeframe==tf, HistoricalCandle.timestamp==r.datetime))).scalars().first()
        if exists: continue
        db.add(HistoricalCandle(pair=pair,timeframe=tf,timestamp=r.datetime,open=float(r.open),high=float(r.high),low=float(r.low),close=float(r.close),volume=float(r.volume),source=market_data.source_info(pair,tf,limit).get('source','synthetic')))
        inserted += 1
    run = IngestionRun(pair=pair,timeframe=tf,source=market_data.source_info(pair,tf,limit).get('source','synthetic'),candles_fetched=fetched,candles_inserted=inserted,gaps_detected=0,malformed_rows=malformed,retries=0,source_reliability=round(inserted/max(1,fetched),3),status='completed')
    db.add(run); await db.commit()
    return {"pair":pair,"timeframe":tf,"candles_fetched":fetched,"candles_inserted":inserted,"malformed_rows":malformed}
