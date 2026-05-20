from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import StrategicMemoryEvent, InstitutionalWorkflow, InstitutionalArchive, StrategicBriefing
from app.engines.cognitive_compression import compress_intelligence, generate_strategic_narratives, confidence_hierarchy, synthesize_recommendations

router = APIRouter()

@router.get('/history/summary')
async def history_summary(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StrategicMemoryEvent).order_by(StrategicMemoryEvent.created_at.desc()).limit(200))
    rows = q.scalars().all()
    return {
        "monthly_summaries": [r.details for r in rows[:12]],
        "regime_history_timeline": [r.anomaly_timeline for r in rows[:24]],
        "major_system_incidents": [r.title for r in rows if "incident" in r.event_type][:20],
        "count": len(rows),
    }

@router.get('/timeline')
async def strategic_timeline(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(StrategicMemoryEvent).order_by(StrategicMemoryEvent.created_at.desc()).limit(100))
    rows = q.scalars().all()
    return [{"event_type": r.event_type, "title": r.title, "details": r.details, "created_at": r.created_at.isoformat()} for r in rows]

@router.post('/compression/run')
async def run_compression(body: dict):
    return {"compression": compress_intelligence(body), "advisory_only": True}

@router.post('/narratives/generate')
async def narratives(body: dict):
    return {"narratives": generate_strategic_narratives(body), "reproducible": True}

@router.post('/recommendations/synthesize')
async def recommendation_synthesis(body: dict):
    return {"synthesis": synthesize_recommendations(body.get("recommendations", [])), "advisory_only": True, "auto_apply": False}

@router.post('/confidence/hierarchy')
async def hierarchy(body: dict):
    return {"confidence_hierarchy": confidence_hierarchy(body)}

@router.post('/workflows')
async def create_workflow(body: dict, db: AsyncSession = Depends(get_db)):
    wf = InstitutionalWorkflow(
        workflow_type=body.get("workflow_type", "anomaly_investigation"),
        owner_operator=body.get("owner_operator", "operator"),
        state=body.get("state", "open"),
        linked_findings=body.get("linked_findings", []),
        linked_evidence=body.get("linked_evidence", []),
        recommended_actions=body.get("recommended_actions", []),
        review_history=body.get("review_history", []),
    )
    db.add(wf); await db.commit(); await db.refresh(wf)
    return {"id": wf.id, "state": wf.state}

@router.get('/workflows')
async def list_workflows(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(InstitutionalWorkflow).order_by(InstitutionalWorkflow.updated_at.desc()).limit(100))
    rows = q.scalars().all()
    stale = [r.id for r in rows if r.state in {"open", "in_review"} and len(r.review_history or []) == 0]
    return {"workflows": [{"id": r.id, "type": r.workflow_type, "owner": r.owner_operator, "state": r.state, "recommended_actions": r.recommended_actions} for r in rows], "stale_investigations": stale}

@router.post('/archive')
async def create_archive(body: dict, db: AsyncSession = Depends(get_db)):
    row = InstitutionalArchive(
        archive_type=body.get("archive_type", "strategic_briefing"),
        title=body.get("title", "Untitled"),
        summary=body.get("summary", ""),
        tags=body.get("tags", []),
        evidence_refs=body.get("evidence_refs", []),
        confidence=float(body.get("confidence", 0.7)),
    )
    db.add(row); await db.commit(); await db.refresh(row)
    return {"id": row.id}

@router.get('/archive/search')
async def archive_search(q: str = Query(default=""), db: AsyncSession = Depends(get_db)):
    aq = await db.execute(select(InstitutionalArchive).order_by(InstitutionalArchive.created_at.desc()).limit(300))
    rows = aq.scalars().all()
    qn = q.lower().strip()
    out = [r for r in rows if (not qn) or (qn in (r.title or "").lower() or qn in (r.summary or "").lower())]
    return {"count": len(out), "results": [{"id": r.id, "type": r.archive_type, "title": r.title, "confidence": r.confidence} for r in out[:100]]}
