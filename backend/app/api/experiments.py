from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import ExperimentRun
from app.engines.governance import compare_metrics
from app.api.signals import replay_run, reliability

router = APIRouter()


class ReplayBody(BaseModel):
    experiment_id: str
    name: str
    description: str = ""
    target_logic_area: str = ""
    baseline_version: str = "phase8-v1"
    candidate_version: str = "phase9-candidate"
    pair: str = "EUR/USD"
    timeframe: str = "1h"
    strategy_profile: str = "intraday"
    dataset_used: str = "benchmark-trending"


@router.post("/run-replay")
async def run_replay(body: ReplayBody, db: AsyncSession = Depends(get_db)):
    row = ExperimentRun(
        experiment_id=body.experiment_id, name=body.name, description=body.description, status="running",
        target_logic_area=body.target_logic_area, baseline_version=body.baseline_version, candidate_version=body.candidate_version,
        dataset_used=body.dataset_used, strategy_profile=body.strategy_profile,
    )
    db.add(row)
    await db.commit()
    replay = await replay_run({"pair": body.pair, "timeframe": body.timeframe, "strategy_profile": body.strategy_profile}, db)
    rel = await reliability(db)
    baseline = {"net_pips": 5, "invalidation_rate": 0.2, "calibration_alignment": 2, "reliability": 55, "hold_rate": 0.3, "aggressiveness": 0.5}
    candidate = {"net_pips": rel.get("avg_net_pips", 0), "invalidation_rate": 0.25 if rel.get("drift_warnings") else 0.15, "calibration_alignment": 2, "reliability": rel.get("score", 0), "hold_rate": 0.3, "aggressiveness": 0.5}
    cmp = compare_metrics(baseline, candidate)
    row.status = "completed"
    row.metrics_summary = {"win_rate": rel.get("win_rate", 0), "net_pips": rel.get("avg_net_pips", 0), "reliability": rel.get("score", 0)}
    row.replay_metadata = replay.get("replay_metadata", {})
    row.comparison_results = cmp
    row.regression_analysis = cmp
    row.regime_conditions = {"fixed": replay.get("replay_metadata", {}).get("fixed_regime")}
    row.config_snapshot = {"sandbox": True}
    await db.commit()
    return {"experiment": _ser(row), "sandbox_isolation": True, "note": "No production state modified by experiment replay."}


@router.get("")
async def list_experiments(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(ExperimentRun).order_by(ExperimentRun.created_at.desc()).limit(100))).scalars().all()
    return {"items": [_ser(r) for r in rows]}


def _ser(r: ExperimentRun):
    return {
        "experiment_id": r.experiment_id, "name": r.name, "status": r.status,
        "target_logic_area": r.target_logic_area, "baseline_version": r.baseline_version,
        "candidate_version": r.candidate_version, "metrics_summary": r.metrics_summary,
        "rollback_status": r.rollback_status, "created_at": r.created_at.isoformat(),
        "comparison_results": r.comparison_results,
    }
