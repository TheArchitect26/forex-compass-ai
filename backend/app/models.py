from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, Boolean, JSON, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from app.utils_time import utc_now


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class Signal(Base):
    __tablename__ = "signals"
    id: Mapped[int] = mapped_column(primary_key=True)
    pair: Mapped[str] = mapped_column(String(16), index=True)
    direction: Mapped[str] = mapped_column(String(8))  # BUY / SELL / HOLD
    timeframe: Mapped[str] = mapped_column(String(8))
    entry: Mapped[float] = mapped_column(Float)
    stop_loss: Mapped[float] = mapped_column(Float)
    take_profit: Mapped[float] = mapped_column(Float)
    risk_reward: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)
    strength: Mapped[str] = mapped_column(String(16), default="weak")
    risk_level: Mapped[str] = mapped_column(String(16), default="medium")
    reason_summary: Mapped[str] = mapped_column(Text, default="")
    indicators_used: Mapped[list] = mapped_column(JSON, default=list)
    invalidation_price: Mapped[float] = mapped_column(Float, default=0.0)
    data_source: Mapped[str] = mapped_column(String(16), default="synthetic")
    market_regime: Mapped[str] = mapped_column(String(32))
    reasoning: Mapped[dict] = mapped_column(JSON)  # technical/news/sentiment breakdown
    explanation: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16), default="open")  # open|win|loss|expired
    pnl_pips: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    signal_id: Mapped[int | None] = mapped_column(ForeignKey("signals.id"), nullable=True)
    pair: Mapped[str] = mapped_column(String(16))
    direction: Mapped[str] = mapped_column(String(8))
    entry: Mapped[float] = mapped_column(Float)
    exit: Mapped[float | None] = mapped_column(Float, nullable=True)
    size: Mapped[float] = mapped_column(Float, default=0.0)
    pnl: Mapped[float | None] = mapped_column(Float, nullable=True)
    result: Mapped[str | None] = mapped_column(String(8), nullable=True)  # win/loss/be
    notes: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class BacktestRun(Base):
    __tablename__ = "backtest_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    strategy: Mapped[str] = mapped_column(String(64))
    pair: Mapped[str] = mapped_column(String(16))
    timeframe: Mapped[str] = mapped_column(String(8))
    start: Mapped[datetime] = mapped_column(DateTime)
    end: Mapped[datetime] = mapped_column(DateTime)
    params: Mapped[dict] = mapped_column(JSON)
    metrics: Mapped[dict] = mapped_column(JSON)  # sharpe, winrate, dd, expectancy...
    equity_curve: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class LearningRecord(Base):
    """Adaptive learning memory — what conditions led to wins/losses."""
    __tablename__ = "learning_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    pattern_key: Mapped[str] = mapped_column(String(128), index=True)
    regime: Mapped[str] = mapped_column(String(32))
    pair: Mapped[str] = mapped_column(String(16))
    wins: Mapped[int] = mapped_column(Integer, default=0)
    losses: Mapped[int] = mapped_column(Integer, default=0)
    avg_rr: Mapped[float] = mapped_column(Float, default=0.0)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class SignalOutcome(Base):
    __tablename__ = "signal_outcomes"
    id: Mapped[int] = mapped_column(primary_key=True)
    signal_id: Mapped[int] = mapped_column(ForeignKey("signals.id"), unique=True, index=True)
    pair: Mapped[str] = mapped_column(String(16), index=True)
    timeframe: Mapped[str] = mapped_column(String(8), index=True)
    direction: Mapped[str] = mapped_column(String(8))
    entry_price: Mapped[float] = mapped_column(Float)
    stop_loss: Mapped[float] = mapped_column(Float)
    take_profit: Mapped[float] = mapped_column(Float)
    invalidation_price: Mapped[float] = mapped_column(Float)
    outcome: Mapped[str] = mapped_column(String(16), default="pending", index=True)  # pending|win|loss|neutral|expired|invalidated
    max_favorable_move: Mapped[float] = mapped_column(Float, default=0.0)
    max_adverse_move: Mapped[float] = mapped_column(Float, default=0.0)
    result_pips: Mapped[float] = mapped_column(Float, default=0.0)
    gross_result_pips: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_cost_pips: Mapped[float] = mapped_column(Float, default=0.0)
    net_result_pips: Mapped[float] = mapped_column(Float, default=0.0)
    checked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ValidationRun(Base):
    __tablename__ = "validation_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="running", index=True)  # running|completed|failed
    signals_checked: Mapped[int] = mapped_column(Integer, default=0)
    outcomes_updated: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)


class ReliabilityHistory(Base):
    __tablename__ = "reliability_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[float] = mapped_column(Float)
    label: Mapped[str] = mapped_column(String(16))
    sample_size: Mapped[int] = mapped_column(Integer, default=0)
    win_rate: Mapped[float] = mapped_column(Float, default=0.0)
    avg_net_pips: Mapped[float] = mapped_column(Float, default=0.0)
    drift_warning: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class StrategyState(Base):
    __tablename__ = "strategy_state"
    id: Mapped[int] = mapped_column(primary_key=True)
    active_profile: Mapped[str] = mapped_column(String(32), default="intraday", unique=True)
    source: Mapped[str] = mapped_column(String(16), default="default")  # manual|adaptive|default
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ExplainabilityAudit(Base):
    __tablename__ = "explainability_audit"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    pair: Mapped[str] = mapped_column(String(16), index=True)
    timeframe: Mapped[str] = mapped_column(String(8), index=True)
    regime: Mapped[str] = mapped_column(String(32))
    strategy_profile: Mapped[str] = mapped_column(String(32))
    signal_decision: Mapped[str] = mapped_column(String(8))
    confidence_before: Mapped[float] = mapped_column(Float)
    confidence_after: Mapped[float] = mapped_column(Float)
    adaptive_changes: Mapped[dict] = mapped_column(JSON, default=dict)
    drift_warnings: Mapped[list] = mapped_column(JSON, default=list)
    reasons: Mapped[str] = mapped_column(Text, default="")


class MaintenanceRun(Base):
    __tablename__ = "maintenance_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_type: Mapped[str] = mapped_column(String(64), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="running")
    rows_cleaned: Mapped[int] = mapped_column(Integer, default=0)
    warnings_errors: Mapped[str | None] = mapped_column(Text, nullable=True)


class VersionRegistry(Base):
    __tablename__ = "version_registry"
    id: Mapped[int] = mapped_column(primary_key=True)
    engine_version: Mapped[str] = mapped_column(String(32), default="phase8-v1")
    weighting_version: Mapped[str] = mapped_column(String(32), default="rw-1")
    calibration_version: Mapped[str] = mapped_column(String(32), default="cal-1")
    adaptation_version: Mapped[str] = mapped_column(String(32), default="adapt-1")
    discipline_version: Mapped[str] = mapped_column(String(32), default="disc-1")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ExperimentRun(Base):
    __tablename__ = "experiment_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(16), default="draft")  # draft/running/completed/archived
    target_logic_area: Mapped[str] = mapped_column(String(64), default="")
    baseline_version: Mapped[str] = mapped_column(String(64), default="")
    candidate_version: Mapped[str] = mapped_column(String(64), default="")
    metrics_summary: Mapped[dict] = mapped_column(JSON, default=dict)
    rollback_status: Mapped[str] = mapped_column(String(32), default="none")
    dataset_used: Mapped[str] = mapped_column(String(64), default="")
    config_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    strategy_profile: Mapped[str] = mapped_column(String(32), default="")
    regime_conditions: Mapped[dict] = mapped_column(JSON, default=dict)
    replay_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    comparison_results: Mapped[dict] = mapped_column(JSON, default=dict)
    regression_analysis: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class HistoricalCandle(Base):
    __tablename__ = "historical_candles"
    id: Mapped[int] = mapped_column(primary_key=True)
    pair: Mapped[str] = mapped_column(String(16), index=True)
    timeframe: Mapped[str] = mapped_column(String(8), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float, default=0.0)
    source: Mapped[str] = mapped_column(String(32), default="twelve_data")
    integrity_flags: Mapped[dict] = mapped_column(JSON, default=dict)
    dataset_version: Mapped[str] = mapped_column(String(32), default="ds-v1")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    pair: Mapped[str] = mapped_column(String(16), index=True)
    timeframe: Mapped[str] = mapped_column(String(8), index=True)
    source: Mapped[str] = mapped_column(String(32), default="twelve_data")
    candles_fetched: Mapped[int] = mapped_column(Integer, default=0)
    candles_inserted: Mapped[int] = mapped_column(Integer, default=0)
    gaps_detected: Mapped[int] = mapped_column(Integer, default=0)
    malformed_rows: Mapped[int] = mapped_column(Integer, default=0)
    retries: Mapped[int] = mapped_column(Integer, default=0)
    source_reliability: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(16), default="completed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ReplaySession(Base):
    __tablename__ = "replay_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    pair: Mapped[str] = mapped_column(String(16), index=True)
    timeframe: Mapped[str] = mapped_column(String(8), index=True)
    strategy_profile: Mapped[str] = mapped_column(String(32), default="intraday")
    start_ts: Mapped[datetime] = mapped_column(DateTime)
    end_ts: Mapped[datetime] = mapped_column(DateTime)
    cursor_ts: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    steps: Mapped[int] = mapped_column(Integer, default=0)
    state: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(16), default="running")
    dataset_snapshot: Mapped[str] = mapped_column(String(64), default="ds-v1")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class PortfolioReplaySession(Base):
    __tablename__ = "portfolio_replay_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), default="portfolio-lab")
    pair: Mapped[str] = mapped_column(String(16), index=True)
    timeframe: Mapped[str] = mapped_column(String(8), index=True)
    strategy_profile: Mapped[str] = mapped_column(String(32), default="intraday")
    sizing_mode: Mapped[str] = mapped_column(String(32), default="fixed_risk")
    balance: Mapped[float] = mapped_column(Float, default=10000.0)
    equity_curve: Mapped[list] = mapped_column(JSON, default=list)
    open_positions: Mapped[list] = mapped_column(JSON, default=list)
    closed_positions: Mapped[list] = mapped_column(JSON, default=list)
    exposure_state: Mapped[dict] = mapped_column(JSON, default=dict)
    risk_state: Mapped[dict] = mapped_column(JSON, default=dict)
    replay_session_id: Mapped[int | None] = mapped_column(ForeignKey("replay_sessions.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="running")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ResearchTask(Base):
    __tablename__ = "research_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_type: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(16), default="pending", index=True)
    priority: Mapped[str] = mapped_column(String(16), default="normal", index=True)
    triggered_by: Mapped[str] = mapped_column(String(64), default="manual")
    linked_datasets: Mapped[list] = mapped_column(JSON, default=list)
    linked_experiments: Mapped[list] = mapped_column(JSON, default=list)
    linked_replay_sessions: Mapped[list] = mapped_column(JSON, default=list)
    findings_summary: Mapped[str] = mapped_column(Text, default="")
    warnings: Mapped[list] = mapped_column(JSON, default=list)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ResearchFinding(Base):
    __tablename__ = "research_findings"
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    affected_regimes: Mapped[list] = mapped_column(JSON, default=list)
    affected_profiles: Mapped[list] = mapped_column(JSON, default=list)
    evidence_refs: Mapped[list] = mapped_column(JSON, default=list)
    reproducible: Mapped[bool] = mapped_column(Boolean, default=True)
    triggered_by_task_id: Mapped[int | None] = mapped_column(ForeignKey("research_tasks.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ResearchWorkload(Base):
    __tablename__ = "research_workloads"
    id: Mapped[int] = mapped_column(primary_key=True)
    workload_type: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(16), default="queued", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=50, index=True)
    retries: Mapped[int] = mapped_column(Integer, default=0)
    execution_duration_ms: Mapped[float] = mapped_column(Float, default=0.0)
    queue_name: Mapped[str] = mapped_column(String(32), default="research")
    worker_id: Mapped[str] = mapped_column(String(64), default="unassigned")
    resource_estimate: Mapped[dict] = mapped_column(JSON, default=dict)
    checkpoint: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ResearchGraphEdge(Base):
    __tablename__ = "research_graph_edges"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_type: Mapped[str] = mapped_column(String(32), index=True)
    source_id: Mapped[str] = mapped_column(String(64), index=True)
    target_type: Mapped[str] = mapped_column(String(32), index=True)
    target_id: Mapped[str] = mapped_column(String(64), index=True)
    relation: Mapped[str] = mapped_column(String(64), default="related_to")
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)




class FeatureFlagCleanupPlan(Base):
    __tablename__ = "feature_flag_cleanup_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    flag_key: Mapped[str] = mapped_column(String(80), index=True)
    current_state: Mapped[str] = mapped_column(String(32), default="active")
    deprecation_stage: Mapped[str] = mapped_column(String(32), default="planned")
    affected_components: Mapped[list] = mapped_column(JSON, default=list)
    rollback_strategy: Mapped[str] = mapped_column(Text, default="")
    operator_approved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)

class StrategicBriefing(Base):
    __tablename__ = "strategic_briefings"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(160), index=True)
    severity: Mapped[str] = mapped_column(String(16), default="normal", index=True)
    summary: Mapped[str] = mapped_column(Text, default="")
    supporting_evidence: Mapped[list] = mapped_column(JSON, default=list)
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    recommended_actions: Mapped[list] = mapped_column(JSON, default=list)
    reproducibility_refs: Mapped[list] = mapped_column(JSON, default=list)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class StrategicMemoryEvent(Base):
    __tablename__ = "strategic_memory_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(160))
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    anomaly_timeline: Mapped[list] = mapped_column(JSON, default=list)
    repeated_pattern_key: Mapped[str] = mapped_column(String(128), default="", index=True)
    successful_mitigation: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InstitutionalWorkflow(Base):
    __tablename__ = "institutional_workflows"
    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_type: Mapped[str] = mapped_column(String(64), index=True)
    owner_operator: Mapped[str] = mapped_column(String(128), default="operator")
    state: Mapped[str] = mapped_column(String(32), default="open", index=True)
    linked_findings: Mapped[list] = mapped_column(JSON, default=list)
    linked_evidence: Mapped[list] = mapped_column(JSON, default=list)
    recommended_actions: Mapped[list] = mapped_column(JSON, default=list)
    review_history: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InstitutionalArchive(Base):
    __tablename__ = "institutional_archives"
    id: Mapped[int] = mapped_column(primary_key=True)
    archive_type: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(180), index=True)
    summary: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[list] = mapped_column(JSON, default=list)
    evidence_refs: Mapped[list] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ConstitutionalRule(Base):
    __tablename__ = "constitutional_rules"
    id: Mapped[int] = mapped_column(primary_key=True)
    rule_key: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    rule_text: Mapped[str] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class GovernanceIncident(Base):
    __tablename__ = "governance_incidents"
    id: Mapped[int] = mapped_column(primary_key=True)
    incident_type: Mapped[str] = mapped_column(String(80), index=True)
    severity: Mapped[str] = mapped_column(String(32), index=True)  # info|warning|critical|constitutional_risk
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class RecommendationLifecycle(Base):
    __tablename__ = "recommendation_lifecycle"
    id: Mapped[int] = mapped_column(primary_key=True)
    recommendation_key: Mapped[str] = mapped_column(String(120), index=True)
    state: Mapped[str] = mapped_column(String(32), default="active", index=True)
    evidence_strength: Mapped[float] = mapped_column(Float, default=0.7)
    contradicted: Mapped[bool] = mapped_column(Boolean, default=False)
    governance_concern: Mapped[bool] = mapped_column(Boolean, default=False)
    changes: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class StrategicAssumption(Base):
    __tablename__ = "strategic_assumptions"
    id: Mapped[int] = mapped_column(primary_key=True)
    assumption_text: Mapped[str] = mapped_column(Text)
    supporting_evidence: Mapped[list] = mapped_column(JSON, default=list)
    contradictory_evidence: Mapped[list] = mapped_column(JSON, default=list)
    historical_confidence: Mapped[float] = mapped_column(Float, default=0.7)
    last_validation_date: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    replay_coverage: Mapped[float] = mapped_column(Float, default=0.5)
    regimes_affected: Mapped[list] = mapped_column(JSON, default=list)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ContradictionWorkflow(Base):
    __tablename__ = "contradiction_workflows"
    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_kind: Mapped[str] = mapped_column(String(64), default="contradiction_review", index=True)
    state: Mapped[str] = mapped_column(String(32), default="open", index=True)
    linked_assumption_id: Mapped[int | None] = mapped_column(ForeignKey("strategic_assumptions.id"), nullable=True)
    evidence_arbitration_notes: Mapped[str] = mapped_column(Text, default="")
    recommendation_deprecation_candidates: Mapped[list] = mapped_column(JSON, default=list)
    stale_strategy_retirement_candidates: Mapped[list] = mapped_column(JSON, default=list)
    review_history: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class EvolutionLineage(Base):
    __tablename__ = "evolution_lineage"
    id: Mapped[int] = mapped_column(primary_key=True)
    changed_component: Mapped[str] = mapped_column(String(120), index=True)
    why: Mapped[str] = mapped_column(Text, default="")
    expected_impact: Mapped[str] = mapped_column(Text, default="")
    affected_assumptions: Mapped[list] = mapped_column(JSON, default=list)
    affected_narratives: Mapped[list] = mapped_column(JSON, default=list)
    affected_replay_validity: Mapped[list] = mapped_column(JSON, default=list)
    compatibility_notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InstitutionalMigration(Base):
    __tablename__ = "institutional_migrations"
    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[str] = mapped_column(String(80), index=True)
    plan: Mapped[dict] = mapped_column(JSON, default=dict)
    reversible: Mapped[bool] = mapped_column(Boolean, default=True)
    operator_approved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending_approval", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class EvolutionPlan(Base):
    __tablename__ = "evolution_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    proposed_evolution: Mapped[str] = mapped_column(String(180), index=True)
    rationale: Mapped[str] = mapped_column(Text, default="")
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    compatibility_impact: Mapped[str] = mapped_column(String(32), default="low")
    replay_impact: Mapped[str] = mapped_column(String(32), default="low")
    governance_impact: Mapped[str] = mapped_column(String(32), default="medium")
    survivability_impact: Mapped[str] = mapped_column(String(32), default="medium")
    rollback_strategy: Mapped[str] = mapped_column(Text, default="")
    operator_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class RenewalWorkflow(Base):
    __tablename__ = "renewal_workflows"
    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_type: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending_review", index=True)
    operator_reviewed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    auditable: Mapped[bool] = mapped_column(Boolean, default=True)
    reproducible: Mapped[bool] = mapped_column(Boolean, default=True)
    reversible: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class MetaCoordinationEvent(Base):
    __tablename__ = "meta_coordination_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    severity: Mapped[str] = mapped_column(String(32), default="info", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class GlossaryTerm(Base):
    __tablename__ = "glossary_terms"
    id: Mapped[int] = mapped_column(primary_key=True)
    term: Mapped[str] = mapped_column(String(120), index=True)
    canonical_definition: Mapped[str] = mapped_column(Text, default="")
    deprecated: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    related_concepts: Mapped[list] = mapped_column(JSON, default=list)
    historical_meanings: Mapped[list] = mapped_column(JSON, default=list)
    replay_version_relevance: Mapped[list] = mapped_column(JSON, default=list)
    governance_impact: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ConceptLineage(Base):
    __tablename__ = "concept_lineage"
    id: Mapped[int] = mapped_column(primary_key=True)
    concept: Mapped[str] = mapped_column(String(140), index=True)
    origin: Mapped[str] = mapped_column(Text, default="")
    revisions: Mapped[list] = mapped_column(JSON, default=list)
    contradictions: Mapped[list] = mapped_column(JSON, default=list)
    retired_meanings: Mapped[list] = mapped_column(JSON, default=list)
    successor_concepts: Mapped[list] = mapped_column(JSON, default=list)
    confidence_evolution: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class MissionAnchor(Base):
    __tablename__ = "mission_anchors"
    id: Mapped[int] = mapped_column(primary_key=True)
    operator_note: Mapped[str] = mapped_column(Text, default="")
    mission_reaffirmation: Mapped[str] = mapped_column(Text, default="")
    long_horizon_intent: Mapped[str] = mapped_column(Text, default="")
    reset_intent: Mapped[str] = mapped_column(Text, default="")
    anti_drift_confirmation: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class MissionTimelineEvent(Base):
    __tablename__ = "mission_timeline_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    severity: Mapped[str] = mapped_column(String(32), default="info", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class TemporalEvent(Base):
    __tablename__ = "temporal_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    timing_classification: Mapped[str] = mapped_column(String(24), index=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class RhythmObservation(Base):
    __tablename__ = "rhythm_observations"
    id: Mapped[int] = mapped_column(primary_key=True)
    rhythm_state: Mapped[str] = mapped_column(String(32), index=True)
    domain: Mapped[str] = mapped_column(String(80), index=True)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class TimingDecision(Base):
    __tablename__ = "timing_decisions"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(180), index=True)
    recommendation: Mapped[str] = mapped_column(String(32), index=True)
    rationale: Mapped[str] = mapped_column(Text, default="")
    operator_approved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class SynthesisSnapshot(Base):
    __tablename__ = "synthesis_snapshots"
    id: Mapped[int] = mapped_column(primary_key=True)
    summary: Mapped[dict] = mapped_column(JSON, default=dict)
    top_priorities: Mapped[list] = mapped_column(JSON, default=list)
    suppressed_noise: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class SynthesisConflict(Base):
    __tablename__ = "synthesis_conflicts"
    id: Mapped[int] = mapped_column(primary_key=True)
    conflict_type: Mapped[str] = mapped_column(String(120), index=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    severity: Mapped[str] = mapped_column(String(32), default="warning", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class StrategicFocusDecision(Base):
    __tablename__ = "strategic_focus_decisions"
    id: Mapped[int] = mapped_column(primary_key=True)
    focus_mode: Mapped[str] = mapped_column(String(80), index=True)
    review_window: Mapped[str] = mapped_column(String(80), default="within 24 hours")
    rationale: Mapped[str] = mapped_column(Text, default="")
    operator_approved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ForesightWarning(Base):
    __tablename__ = "foresight_warnings"
    id: Mapped[int] = mapped_column(primary_key=True)
    warning_type: Mapped[str] = mapped_column(String(120), index=True)
    classification: Mapped[str] = mapped_column(String(24), index=True)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class StrategicForecast(Base):
    __tablename__ = "strategic_forecasts"
    id: Mapped[int] = mapped_column(primary_key=True)
    trajectory: Mapped[str] = mapped_column(String(32), index=True)
    instability_probability: Mapped[float] = mapped_column(Float, default=0.0)
    time_to_risk_estimate_days: Mapped[int] = mapped_column(Integer, default=14)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InterventionPlan(Base):
    __tablename__ = "intervention_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    plan: Mapped[list] = mapped_column(JSON, default=list)
    urgency: Mapped[float] = mapped_column(Float, default=0.0)
    operator_review_required: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ScenarioRun(Base):
    __tablename__ = "scenario_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_name: Mapped[str] = mapped_column(String(120), index=True)
    assumptions: Mapped[list] = mapped_column(JSON, default=list)
    result: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ScenarioComparison(Base):
    __tablename__ = "scenario_comparisons"
    id: Mapped[int] = mapped_column(primary_key=True)
    left_option: Mapped[str] = mapped_column(String(120), index=True)
    right_option: Mapped[str] = mapped_column(String(120), index=True)
    preferred_option: Mapped[str] = mapped_column(String(120), index=True)
    reasoning: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ConsequenceAssessment(Base):
    __tablename__ = "consequence_assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_name: Mapped[str] = mapped_column(String(120), index=True)
    primary_effects: Mapped[list] = mapped_column(JSON, default=list)
    second_order_effects: Mapped[list] = mapped_column(JSON, default=list)
    risks_introduced: Mapped[list] = mapped_column(JSON, default=list)
    risks_reduced: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class AdaptivePathway(Base):
    __tablename__ = "adaptive_pathways"
    id: Mapped[int] = mapped_column(primary_key=True)
    pathway_name: Mapped[str] = mapped_column(String(120), index=True)
    trigger_conditions: Mapped[dict] = mapped_column(JSON, default=dict)
    entry_criteria: Mapped[list] = mapped_column(JSON, default=list)
    exit_criteria: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class PathwayEvaluation(Base):
    __tablename__ = "pathway_evaluations"
    id: Mapped[int] = mapped_column(primary_key=True)
    pathway_name: Mapped[str] = mapped_column(String(120), index=True)
    evaluation: Mapped[dict] = mapped_column(JSON, default=dict)
    escalation_needed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class PathwayDecision(Base):
    __tablename__ = "pathway_decisions"
    id: Mapped[int] = mapped_column(primary_key=True)
    recommended_pathway: Mapped[str] = mapped_column(String(120), index=True)
    approved_by_operator: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    reversibility_notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class CausalAnalysis(Base):
    __tablename__ = "causal_analyses"
    id: Mapped[int] = mapped_column(primary_key=True)
    incident_type: Mapped[str] = mapped_column(String(120), index=True)
    root_causes: Mapped[list] = mapped_column(JSON, default=list)
    confidence_level: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class CausalGraphSnapshot(Base):
    __tablename__ = "causal_graph_snapshots"
    id: Mapped[int] = mapped_column(primary_key=True)
    nodes: Mapped[list] = mapped_column(JSON, default=list)
    edges: Mapped[list] = mapped_column(JSON, default=list)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InterventionEffectEstimate(Base):
    __tablename__ = "intervention_effect_estimates"
    id: Mapped[int] = mapped_column(primary_key=True)
    intervention: Mapped[str] = mapped_column(String(180), index=True)
    likely_benefit: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    time_horizon: Mapped[str] = mapped_column(String(80), default="1-3 weeks")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InstitutionalLesson(Base):
    __tablename__ = "institutional_lessons"
    id: Mapped[int] = mapped_column(primary_key=True)
    lesson: Mapped[str] = mapped_column(Text, default="")
    evidence: Mapped[list] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    limitations: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InterventionReview(Base):
    __tablename__ = "intervention_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    intervention: Mapped[str] = mapped_column(String(180), index=True)
    effectiveness_score: Mapped[float] = mapped_column(Float, default=0.0)
    operator_burden: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_in_lesson: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ForecastReview(Base):
    __tablename__ = "forecast_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    predicted: Mapped[str] = mapped_column(Text, default="")
    actual: Mapped[str] = mapped_column(Text, default="")
    accuracy_score: Mapped[float] = mapped_column(Float, default=0.0)
    miss_reason: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class AssumptionLearningReview(Base):
    __tablename__ = "assumption_learning_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    assumption: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(24), default="review")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    evidence: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class EcosystemDependency(Base):
    __tablename__ = "ecosystem_dependencies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    dependency_type: Mapped[str] = mapped_column(String(80), index=True)
    criticality: Mapped[str] = mapped_column(String(24), default="medium")
    current_health: Mapped[str] = mapped_column(String(24), default="unknown")
    fallback_availability: Mapped[str] = mapped_column(String(24), default="unknown")
    concentration_risk: Mapped[str] = mapped_column(String(24), default="medium")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class EcosystemRiskAssessment(Base):
    __tablename__ = "ecosystem_risk_assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    scores: Mapped[dict] = mapped_column(JSON, default=dict)
    uncertainty_notes: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class FallbackPlan(Base):
    __tablename__ = "fallback_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    outage_type: Mapped[str] = mapped_column(String(120), index=True)
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    temporary_workaround: Mapped[str] = mapped_column(Text, default="")
    operator_action_required: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
