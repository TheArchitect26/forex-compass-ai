from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import ResearchFinding, ResearchTask, ExperimentRun, ReplaySession, ResearchWorkload, ResearchGraphEdge
from app.engines.research_index import index_search
from app.engines.distributed_research import estimate_resources, queue_priority, replay_checkpoint, restore_checkpoint
from app.engines.recommendation_priority import prioritize_recommendation

router = APIRouter()

@router.get('/search')
async def search_research(
    q: str = Query(default=""),
    severity: str | None = Query(default=None),
    regime: str | None = Query(default=None),
    profile: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    fq = await db.execute(select(ResearchFinding).limit(200))
    findings = [{"id": f"finding:{x.id}", "kind": "finding", "message": x.message, "severity": "elevated", "regimes": x.affected_regimes, "profiles": x.affected_profiles} for x in fq.scalars().all()]
    tq = await db.execute(select(ResearchTask).limit(200))
    tasks = [{"id": f"task:{x.id}", "kind": "task", "summary": x.findings_summary, "severity": x.priority, "regimes": [], "profiles": []} for x in tq.scalars().all()]
    eq = await db.execute(select(ExperimentRun).limit(200))
    exps = [{"id": f"experiment:{x.id}", "kind": "experiment", "summary": x.name, "severity": "normal", "regimes": [], "profiles": [x.strategy_profile]} for x in eq.scalars().all()]
    rq = await db.execute(select(ReplaySession).limit(200))
    replays = [{"id": f"replay:{x.id}", "kind": "replay", "summary": f"{x.pair} {x.timeframe}", "severity": "normal", "regimes": [x.state.get('regime', 'unknown')] if x.state else [], "profiles": [x.strategy_profile]} for x in rq.scalars().all()]
    rows = findings + tasks + exps + replays
    results = index_search(rows, q=q, filters={"severity": severity, "regime": regime, "profile": profile})
    return {"count": len(results), "results": results[:100]}

@router.post('/workload/queue')
async def queue_workload(body: dict, db: AsyncSession = Depends(get_db)):
    w = ResearchWorkload(
        workload_type=body.get("type", "replay_batch"),
        priority=queue_priority(body),
        status="queued",
        resource_estimate=estimate_resources(body.get("type", "replay_batch"), int(body.get("batch_size", 1))),
    )
    db.add(w); await db.commit(); await db.refresh(w)
    return {"id": w.id, "status": w.status, "priority": w.priority, "resource_estimate": w.resource_estimate}

@router.post('/workload/{wid}/checkpoint')
async def set_checkpoint(wid: int, body: dict, db: AsyncSession = Depends(get_db)):
    w = await db.get(ResearchWorkload, wid)
    if not w:
        return {"error": "workload not found"}
    w.checkpoint = replay_checkpoint(body.get("cursor"), int(body.get("steps", 0)), body.get("state", {}))
    await db.commit()
    return {"workload_id": w.id, "checkpoint": w.checkpoint}

@router.get('/workload/{wid}/resume')
async def resume_checkpoint(wid: int, db: AsyncSession = Depends(get_db)):
    w = await db.get(ResearchWorkload, wid)
    if not w:
        return {"error": "workload not found"}
    return {"workload_id": w.id, "resume": restore_checkpoint(w.checkpoint or {})}

@router.post('/graph/edge')
async def create_graph_edge(body: dict, db: AsyncSession = Depends(get_db)):
    edge = ResearchGraphEdge(
        source_type=body.get("source_type", "finding"),
        source_id=str(body.get("source_id", "0")),
        target_type=body.get("target_type", "experiment"),
        target_id=str(body.get("target_id", "0")),
        relation=body.get("relation", "related_to"),
        weight=float(body.get("weight", 1.0)),
        metadata=body.get("metadata", {}),
    )
    db.add(edge); await db.commit(); await db.refresh(edge)
    return {"id": edge.id}

@router.post('/recommendation/prioritize')
async def prioritize(body: dict):
    return {"recommendation": prioritize_recommendation(body), "advisory_only": True, "auto_apply": False}
