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
    replay_metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
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


class OperationalReview(Base):
    __tablename__ = "operational_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    review_type: Mapped[str] = mapped_column(String(120), index=True)
    review_window: Mapped[str] = mapped_column(String(80), default="this week")
    urgency: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class DeferredAction(Base):
    __tablename__ = "deferred_actions"
    id: Mapped[int] = mapped_column(primary_key=True)
    reason_deferred: Mapped[str] = mapped_column(Text, default="")
    review_date: Mapped[str] = mapped_column(String(80), default="in 7 days")
    risk_of_delay: Mapped[float] = mapped_column(Float, default=0.0)
    dependencies: Mapped[list] = mapped_column(JSON, default=list)
    escalation_trigger: Mapped[str] = mapped_column(Text, default="")
    retirement_eligibility: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class MaintenanceCycle(Base):
    __tablename__ = "maintenance_cycles"
    id: Mapped[int] = mapped_column(primary_key=True)
    maintenance_plan: Mapped[list] = mapped_column(JSON, default=list)
    overdue_work: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ArchitectureAudit(Base):
    __tablename__ = "architecture_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    audit_label: Mapped[str] = mapped_column(String(120), default="phase37_baseline_audit", index=True)
    subsystem_coherence: Mapped[float] = mapped_column(Float, default=0.0)
    api_clarity: Mapped[float] = mapped_column(Float, default=0.0)
    model_uniqueness: Mapped[float] = mapped_column(Float, default=0.0)
    terminology_consistency: Mapped[float] = mapped_column(Float, default=0.0)
    frontend_navigation_clarity: Mapped[float] = mapped_column(Float, default=0.0)
    architectural_simplicity: Mapped[float] = mapped_column(Float, default=0.0)
    maintenance_burden: Mapped[float] = mapped_column(Float, default=0.0)
    consolidation_opportunity: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class SubsystemOverlap(Base):
    __tablename__ = "subsystem_overlaps"
    id: Mapped[int] = mapped_column(primary_key=True)
    duplicated_engine_responsibilities: Mapped[list] = mapped_column(JSON, default=list)
    overlapping_apis: Mapped[list] = mapped_column(JSON, default=list)
    repeated_governance_logic: Mapped[list] = mapped_column(JSON, default=list)
    similar_scoring_systems: Mapped[list] = mapped_column(JSON, default=list)
    stale_consoles: Mapped[list] = mapped_column(JSON, default=list)
    unused_workflows: Mapped[list] = mapped_column(JSON, default=list)
    fragmented_terminology: Mapped[list] = mapped_column(JSON, default=list)
    model_table_overlap: Mapped[list] = mapped_column(JSON, default=list)
    redundant_memory_systems: Mapped[list] = mapped_column(JSON, default=list)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ConsolidationProposal(Base):
    __tablename__ = "consolidation_proposals"
    id: Mapped[int] = mapped_column(primary_key=True)
    benefits: Mapped[list] = mapped_column(JSON, default=list)
    risks: Mapped[list] = mapped_column(JSON, default=list)
    migration_needs: Mapped[list] = mapped_column(JSON, default=list)
    reversibility: Mapped[str] = mapped_column(String(80), default="high with phased rollout")
    affected_files: Mapped[list] = mapped_column(JSON, default=list)
    proposals: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)

class EntropyAudit(Base):
    __tablename__ = "entropy_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    entropy_score: Mapped[float] = mapped_column(Float, default=0.0)
    coupling_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    maintainability_score: Mapped[float] = mapped_column(Float, default=0.0)
    refactor_priority_score: Mapped[float] = mapped_column(Float, default=0.0)
    subsystem_drift_score: Mapped[float] = mapped_column(Float, default=0.0)
    architectural_recovery_score: Mapped[float] = mapped_column(Float, default=0.0)
    simplification_opportunity_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class RefactorRecommendation(Base):
    __tablename__ = "refactor_recommendations"
    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(160), index=True)
    expected_benefit: Mapped[str] = mapped_column(Text, default="")
    risk_level: Mapped[str] = mapped_column(String(24), default="medium")
    reversibility: Mapped[str] = mapped_column(String(80), default="high")
    estimated_complexity: Mapped[str] = mapped_column(String(24), default="medium")
    affected_subsystems: Mapped[list] = mapped_column(JSON, default=list)
    migration_guidance: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ArchitecturalRecoveryPlan(Base):
    __tablename__ = "architectural_recovery_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    facade_candidates: Mapped[list] = mapped_column(JSON, default=list)
    consolidation_targets: Mapped[list] = mapped_column(JSON, default=list)
    layering_inconsistencies: Mapped[list] = mapped_column(JSON, default=list)
    unclear_boundaries: Mapped[list] = mapped_column(JSON, default=list)
    maintenance_hotspots: Mapped[list] = mapped_column(JSON, default=list)
    simplification_opportunities: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class EvolutionTransitionAssessment(Base):
    __tablename__ = "evolution_transition_assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    transition_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    continuity_preservation_score: Mapped[float] = mapped_column(Float, default=0.0)
    migration_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    rollback_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    institutional_memory_safety_score: Mapped[float] = mapped_column(Float, default=0.0)
    operator_disruption_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    mission_continuity_score: Mapped[float] = mapped_column(Float, default=0.0)
    explainability_preservation_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ContinuityPreservationPlan(Base):
    __tablename__ = "continuity_preservation_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    continuity_risks: Mapped[list] = mapped_column(JSON, default=list)
    preservation_actions: Mapped[list] = mapped_column(JSON, default=list)
    validation_checks: Mapped[list] = mapped_column(JSON, default=list)
    rollback_notes: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class RollbackReadinessPlan(Base):
    __tablename__ = "rollback_readiness_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    rollback_feasibility: Mapped[str] = mapped_column(String(64), default="moderate_to_high")
    reversible_changes: Mapped[list] = mapped_column(JSON, default=list)
    irreversible_changes: Mapped[list] = mapped_column(JSON, default=list)
    migration_checkpoints: Mapped[list] = mapped_column(JSON, default=list)
    backup_requirements: Mapped[list] = mapped_column(JSON, default=list)
    compatibility_risks: Mapped[list] = mapped_column(JSON, default=list)
    data_loss_risks: Mapped[list] = mapped_column(JSON, default=list)
    operator_review_gates: Mapped[list] = mapped_column(JSON, default=list)
    rollback_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class GovernancePolicyAudit(Base):
    __tablename__ = "governance_policy_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    governance_alignment_score: Mapped[float] = mapped_column(Float, default=0.0)
    safeguard_consistency_score: Mapped[float] = mapped_column(Float, default=0.0)
    policy_clarity_score: Mapped[float] = mapped_column(Float, default=0.0)
    escalation_coherence_score: Mapped[float] = mapped_column(Float, default=0.0)
    human_review_consistency_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_boundary_integrity_score: Mapped[float] = mapped_column(Float, default=0.0)
    auditability_score: Mapped[float] = mapped_column(Float, default=0.0)
    doctrine_drift_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class PolicyConflict(Base):
    __tablename__ = "policy_conflicts"
    id: Mapped[int] = mapped_column(primary_key=True)
    conflict_source: Mapped[str] = mapped_column(String(200), index=True)
    contradiction: Mapped[str] = mapped_column(Text, default="")
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    risk_if_unresolved: Mapped[str] = mapped_column(Text, default="")
    escalation_level: Mapped[str] = mapped_column(String(32), default="medium")
    operator_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class SafeguardHarmonizationPlan(Base):
    __tablename__ = "safeguard_harmonization_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    conflict_source: Mapped[str] = mapped_column(String(200), default="")
    proposed_resolution: Mapped[str] = mapped_column(Text, default="")
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    risk_if_unresolved: Mapped[str] = mapped_column(Text, default="")
    reversibility: Mapped[str] = mapped_column(String(64), default="high")
    operator_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class TrustCalibrationAudit(Base):
    __tablename__ = "trust_calibration_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    institutional_credibility_score: Mapped[float] = mapped_column(Float, default=0.0)
    recommendation_legitimacy_score: Mapped[float] = mapped_column(Float, default=0.0)
    uncertainty_transparency_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_calibration_score: Mapped[float] = mapped_column(Float, default=0.0)
    usefulness_credibility_score: Mapped[float] = mapped_column(Float, default=0.0)
    overreach_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    operator_trust_pressure_score: Mapped[float] = mapped_column(Float, default=0.0)
    humility_integrity_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class RecommendationLegitimacyReview(Base):
    __tablename__ = "recommendation_legitimacy_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    evidence_strength: Mapped[str] = mapped_column(String(40), default="moderate")
    uncertainty_clarity: Mapped[str] = mapped_column(String(80), default="clear")
    actionability: Mapped[str] = mapped_column(String(40), default="medium")
    proportionality: Mapped[str] = mapped_column(String(40), default="medium")
    reversibility: Mapped[str] = mapped_column(String(40), default="high")
    historical_usefulness: Mapped[str] = mapped_column(String(80), default="mixed")
    operator_burden: Mapped[str] = mapped_column(String(40), default="medium")
    risk_of_overreach: Mapped[str] = mapped_column(String(40), default="medium")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class CredibilityIncident(Base):
    __tablename__ = "credibility_incidents"
    id: Mapped[int] = mapped_column(primary_key=True)
    incident_type: Mapped[str] = mapped_column(String(120), index=True)
    severity: Mapped[str] = mapped_column(String(24), default="medium")
    description: Mapped[str] = mapped_column(Text, default="")
    affected_recommendation_area: Mapped[str] = mapped_column(String(120), default="")
    corrective_guidance: Mapped[str] = mapped_column(Text, default="")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class PurposeCoherenceAudit(Base):
    __tablename__ = "purpose_coherence_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    purpose_coherence_score: Mapped[float] = mapped_column(Float, default=0.0)
    mission_alignment_score: Mapped[float] = mapped_column(Float, default=0.0)
    meaning_preservation_score: Mapped[float] = mapped_column(Float, default=0.0)
    anti_hollowing_score: Mapped[float] = mapped_column(Float, default=0.0)
    usefulness_to_complexity_score: Mapped[float] = mapped_column(Float, default=0.0)
    operator_purpose_alignment_score: Mapped[float] = mapped_column(Float, default=0.0)
    doctrine_embodiment_score: Mapped[float] = mapped_column(Float, default=0.0)
    strategic_authenticity_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class MeaningDriftSignal(Base):
    __tablename__ = "meaning_drift_signals"
    id: Mapped[int] = mapped_column(primary_key=True)
    signal_type: Mapped[str] = mapped_column(String(120), index=True)
    signal_description: Mapped[str] = mapped_column(Text, default="")
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    drift_severity: Mapped[str] = mapped_column(String(24), default="medium")
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class MissionAlignmentReview(Base):
    __tablename__ = "mission_alignment_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    stated_doctrine: Mapped[list] = mapped_column(JSON, default=list)
    actual_recommendations: Mapped[list] = mapped_column(JSON, default=list)
    frontend_console_behavior: Mapped[list] = mapped_column(JSON, default=list)
    api_safeguards: Mapped[list] = mapped_column(JSON, default=list)
    readme_claims: Mapped[list] = mapped_column(JSON, default=list)
    tests_safeguards: Mapped[list] = mapped_column(JSON, default=list)
    doctrine_embodiment_check: Mapped[list] = mapped_column(JSON, default=list)
    mission_alignment_score: Mapped[float] = mapped_column(Float, default=0.0)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class WisdomAudit(Base):
    __tablename__ = "wisdom_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    wisdom_score: Mapped[float] = mapped_column(Float, default=0.0)
    prudence_score: Mapped[float] = mapped_column(Float, default=0.0)
    restraint_score: Mapped[float] = mapped_column(Float, default=0.0)
    ambiguity_tolerance_score: Mapped[float] = mapped_column(Float, default=0.0)
    uncertainty_integrity_score: Mapped[float] = mapped_column(Float, default=0.0)
    long_term_judgment_score: Mapped[float] = mapped_column(Float, default=0.0)
    overreaction_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    strategic_patience_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class AmbiguityReview(Base):
    __tablename__ = "ambiguity_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    knowns: Mapped[list] = mapped_column(JSON, default=list)
    uncertain: Mapped[list] = mapped_column(JSON, default=list)
    assumed: Mapped[list] = mapped_column(JSON, default=list)
    needs_review: Mapped[list] = mapped_column(JSON, default=list)
    what_not_to_conclude_yet: Mapped[list] = mapped_column(JSON, default=list)
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class JudgmentDisciplineReview(Base):
    __tablename__ = "judgment_discipline_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    reflective_reasoning: Mapped[str] = mapped_column(Text, default="")
    historical_experience: Mapped[str] = mapped_column(Text, default="")
    long_term_well_being: Mapped[str] = mapped_column(Text, default="")
    moderation: Mapped[str] = mapped_column(String(40), default="moderate")
    reversibility: Mapped[str] = mapped_column(String(40), default="high")
    proportionality: Mapped[str] = mapped_column(String(40), default="medium")
    operator_burden: Mapped[str] = mapped_column(String(40), default="medium")
    mission_alignment: Mapped[str] = mapped_column(Text, default="")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class CrisisResilienceAudit(Base):
    __tablename__ = "crisis_resilience_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    existential_resilience_score: Mapped[float] = mapped_column(Float, default=0.0)
    crisis_continuity_score: Mapped[float] = mapped_column(Float, default=0.0)
    shock_absorption_score: Mapped[float] = mapped_column(Float, default=0.0)
    mission_survival_score: Mapped[float] = mapped_column(Float, default=0.0)
    governance_continuity_score: Mapped[float] = mapped_column(Float, default=0.0)
    operator_sustainability_score: Mapped[float] = mapped_column(Float, default=0.0)
    data_survivability_score: Mapped[float] = mapped_column(Float, default=0.0)
    recovery_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ContinuityCrisisPlan(Base):
    __tablename__ = "continuity_crisis_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    crisis_type: Mapped[str] = mapped_column(String(120), default="")
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    critical_systems_to_preserve: Mapped[list] = mapped_column(JSON, default=list)
    systems_to_pause: Mapped[list] = mapped_column(JSON, default=list)
    minimum_viable_operating_mode: Mapped[list] = mapped_column(JSON, default=list)
    recovery_sequence: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class BlackSwanReview(Base):
    __tablename__ = "black_swan_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    assumptions_invalidated_by_shock: Mapped[list] = mapped_column(JSON, default=list)
    overreliance_on_normal_conditions: Mapped[list] = mapped_column(JSON, default=list)
    false_certainty_under_extreme_uncertainty: Mapped[list] = mapped_column(JSON, default=list)
    fragile_dependencies: Mapped[list] = mapped_column(JSON, default=list)
    crisis_time_governance_contradictions: Mapped[list] = mapped_column(JSON, default=list)
    crisis_alert_overload: Mapped[list] = mapped_column(JSON, default=list)
    loss_of_operator_clarity: Mapped[list] = mapped_column(JSON, default=list)
    risk_of_overreaction: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class TechnicalDebtAudit(Base):
    __tablename__ = "technical_debt_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    technical_debt_score: Mapped[float] = mapped_column(Float, default=0.0)
    maintainability_score: Mapped[float] = mapped_column(Float, default=0.0)
    build_fragility_score: Mapped[float] = mapped_column(Float, default=0.0)
    dependency_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    migration_burden_score: Mapped[float] = mapped_column(Float, default=0.0)
    test_confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    refactor_urgency_score: Mapped[float] = mapped_column(Float, default=0.0)
    debt_paydown_priority_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class DebtItem(Base):
    __tablename__ = "debt_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(40), index=True)
    severity: Mapped[str] = mapped_column(String(24), default="medium")
    affected_files: Mapped[list] = mapped_column(JSON, default=list)
    impact: Mapped[str] = mapped_column(Text, default="")
    estimated_effort: Mapped[str] = mapped_column(String(24), default="medium")
    risk_if_ignored: Mapped[str] = mapped_column(Text, default="")
    recommended_owner_action: Mapped[str] = mapped_column(Text, default="")
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class DebtPaydownPlan(Base):
    __tablename__ = "debt_paydown_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    paydown_actions: Mapped[list] = mapped_column(JSON, default=list)
    recommended_timeline: Mapped[list] = mapped_column(JSON, default=list)
    owners: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ReleaseReadinessAudit(Base):
    __tablename__ = "release_readiness_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    release_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    build_confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    deployment_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    rollback_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    migration_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    environment_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    post_release_monitoring_score: Mapped[float] = mapped_column(Float, default=0.0)
    production_suitability_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class DeploymentRiskAssessment(Base):
    __tablename__ = "deployment_risk_assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    unresolved_dependency_versions: Mapped[list] = mapped_column(JSON, default=list)
    deprecated_nextjs_warnings: Mapped[list] = mapped_column(JSON, default=list)
    frontend_backend_api_mismatch: Mapped[list] = mapped_column(JSON, default=list)
    migration_drift: Mapped[list] = mapped_column(JSON, default=list)
    missing_production_env_vars: Mapped[list] = mapped_column(JSON, default=list)
    unsafe_fallback_assumptions: Mapped[list] = mapped_column(JSON, default=list)
    test_gaps_new_routers: Mapped[list] = mapped_column(JSON, default=list)
    deployment_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class RollbackPlanReview(Base):
    __tablename__ = "rollback_plan_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    rollback_steps: Mapped[list] = mapped_column(JSON, default=list)
    database_rollback_warning: Mapped[str] = mapped_column(Text, default="")
    migration_caution: Mapped[str] = mapped_column(Text, default="")
    post_rollback_validation: Mapped[list] = mapped_column(JSON, default=list)
    rollback_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class RuntimeHealthAudit(Base):
    __tablename__ = "runtime_health_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    runtime_health_score: Mapped[float] = mapped_column(Float, default=0.0)
    endpoint_reliability_score: Mapped[float] = mapped_column(Float, default=0.0)
    latency_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    frontend_backend_compatibility_score: Mapped[float] = mapped_column(Float, default=0.0)
    error_pressure_score: Mapped[float] = mapped_column(Float, default=0.0)
    deployment_regression_score: Mapped[float] = mapped_column(Float, default=0.0)
    monitoring_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    recovery_visibility_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class EndpointHealthObservation(Base):
    __tablename__ = "endpoint_health_observations"
    id: Mapped[int] = mapped_column(primary_key=True)
    endpoint_path: Mapped[str] = mapped_column(String(255), index=True)
    method: Mapped[str] = mapped_column(String(12), default="GET")
    expected_status: Mapped[int] = mapped_column(Integer, default=200)
    observed_status: Mapped[int] = mapped_column(Integer, default=200)
    latency_estimate_ms: Mapped[float] = mapped_column(Float, default=0.0)
    error_pattern: Mapped[str] = mapped_column(Text, default="")
    affected_subsystem: Mapped[str] = mapped_column(String(80), default="")
    severity: Mapped[str] = mapped_column(String(24), default="low")
    recommended_human_review: Mapped[bool] = mapped_column(Boolean, default=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class DeploymentRegressionSignal(Base):
    __tablename__ = "deployment_regression_signals"
    id: Mapped[int] = mapped_column(primary_key=True)
    routes_failing_after_release: Mapped[list] = mapped_column(JSON, default=list)
    api_base_url_mismatch: Mapped[list] = mapped_column(JSON, default=list)
    vercel_backend_route_mismatch: Mapped[list] = mapped_column(JSON, default=list)
    static_frontend_page_mismatch: Mapped[list] = mapped_column(JSON, default=list)
    missing_env_var_runtime_errors: Mapped[list] = mapped_column(JSON, default=list)
    dependency_runtime_import_failures: Mapped[list] = mapped_column(JSON, default=list)
    slow_endpoints: Mapped[list] = mapped_column(JSON, default=list)
    repeated_500_or_404_patterns: Mapped[list] = mapped_column(JSON, default=list)
    deployment_regression_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ControlPlaneSnapshot(Base):
    __tablename__ = "control_plane_snapshots"
    id: Mapped[int] = mapped_column(primary_key=True)
    operator_clarity_score: Mapped[float] = mapped_column(Float, default=0.0)
    dashboard_sprawl_score: Mapped[float] = mapped_column(Float, default=0.0)
    cognitive_load_score: Mapped[float] = mapped_column(Float, default=0.0)
    institutional_health_score: Mapped[float] = mapped_column(Float, default=0.0)
    actionability_score: Mapped[float] = mapped_column(Float, default=0.0)
    signal_to_noise_score: Mapped[float] = mapped_column(Float, default=0.0)
    navigation_burden_score: Mapped[float] = mapped_column(Float, default=0.0)
    consolidation_opportunity_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class OperatorFocusSummary(Base):
    __tablename__ = "operator_focus_summaries"
    id: Mapped[int] = mapped_column(primary_key=True)
    focus_view: Mapped[str] = mapped_column(String(64), index=True)
    top_institutional_priorities: Mapped[list] = mapped_column(JSON, default=list)
    top_ignore_or_defer: Mapped[list] = mapped_column(JSON, default=list)
    critical_warnings: Mapped[list] = mapped_column(JSON, default=list)
    next_best_human_reviewed_action: Mapped[str] = mapped_column(Text, default="")
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ConsoleSprawlAudit(Base):
    __tablename__ = "console_sprawl_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    too_many_sidebar_items: Mapped[bool] = mapped_column(Boolean, default=False)
    overlapping_frontend_pages: Mapped[list] = mapped_column(JSON, default=list)
    low_value_consoles: Mapped[list] = mapped_column(JSON, default=list)
    duplicated_summaries: Mapped[list] = mapped_column(JSON, default=list)
    navigation_confusion: Mapped[list] = mapped_column(JSON, default=list)
    excessive_context_switching: Mapped[list] = mapped_column(JSON, default=list)
    dashboards_to_group: Mapped[list] = mapped_column(JSON, default=list)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class OperatorExperienceAudit(Base):
    __tablename__ = "operator_experience_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    operator_experience_score: Mapped[float] = mapped_column(Float, default=0.0)
    usability_clarity_score: Mapped[float] = mapped_column(Float, default=0.0)
    navigation_simplicity_score: Mapped[float] = mapped_column(Float, default=0.0)
    readability_score: Mapped[float] = mapped_column(Float, default=0.0)
    actionability_score: Mapped[float] = mapped_column(Float, default=0.0)
    warning_fatigue_score: Mapped[float] = mapped_column(Float, default=0.0)
    mobile_usability_score: Mapped[float] = mapped_column(Float, default=0.0)
    interface_coherence_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class UsabilityIssue(Base):
    __tablename__ = "usability_issues"
    id: Mapped[int] = mapped_column(primary_key=True)
    issue_category: Mapped[str] = mapped_column(String(80), index=True)
    severity: Mapped[str] = mapped_column(String(24), default="medium")
    affected_surfaces: Mapped[list] = mapped_column(JSON, default=list)
    issue_description: Mapped[str] = mapped_column(Text, default="")
    recommended_fix: Mapped[str] = mapped_column(Text, default="")
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InterfaceSimplificationPlan(Base):
    __tablename__ = "interface_simplification_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)
    daily_use_pathway: Mapped[list] = mapped_column(JSON, default=list)
    maintenance_view_outline: Mapped[list] = mapped_column(JSON, default=list)
    crisis_view_outline: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class MemoryIndexEntry(Base):
    __tablename__ = "memory_index_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    entry_key: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    category: Mapped[str] = mapped_column(String(40), index=True)
    title: Mapped[str] = mapped_column(String(255), default="")
    tags: Mapped[list] = mapped_column(JSON, default=list)
    summary: Mapped[str] = mapped_column(Text, default="")
    source_module: Mapped[str] = mapped_column(String(120), default="")
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class MemoryRetrievalQuery(Base):
    __tablename__ = "memory_retrieval_queries"
    id: Mapped[int] = mapped_column(primary_key=True)
    query_text: Mapped[str] = mapped_column(Text, default="")
    context: Mapped[str] = mapped_column(Text, default="")
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    usefulness_score: Mapped[float] = mapped_column(Float, default=0.0)
    staleness_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ContextualRecallResult(Base):
    __tablename__ = "contextual_recall_results"
    id: Mapped[int] = mapped_column(primary_key=True)
    query_ref: Mapped[str] = mapped_column(String(120), default="")
    related_lessons: Mapped[list] = mapped_column(JSON, default=list)
    related_decisions: Mapped[list] = mapped_column(JSON, default=list)
    related_incidents: Mapped[list] = mapped_column(JSON, default=list)
    related_assumptions: Mapped[list] = mapped_column(JSON, default=list)
    related_warnings: Mapped[list] = mapped_column(JSON, default=list)
    related_phases: Mapped[list] = mapped_column(JSON, default=list)
    stale_knowledge_risks: Mapped[list] = mapped_column(JSON, default=list)
    recommended_human_review: Mapped[str] = mapped_column(Text, default="")
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class DistilledInsight(Base):
    __tablename__ = "distilled_insights"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), default="")
    insight_type: Mapped[str] = mapped_column(String(64), index=True)
    summary: Mapped[str] = mapped_column(Text, default="")
    strategic_retention_score: Mapped[float] = mapped_column(Float, default=0.0)
    knowledge_durability_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class StrategicHeuristic(Base):
    __tablename__ = "strategic_heuristics"
    id: Mapped[int] = mapped_column(primary_key=True)
    heuristic: Mapped[str] = mapped_column(Text, default="")
    domain: Mapped[str] = mapped_column(String(64), default="general")
    usefulness_score: Mapped[float] = mapped_column(Float, default=0.0)
    actionability_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InstitutionalAntiPattern(Base):
    __tablename__ = "institutional_anti_patterns"
    id: Mapped[int] = mapped_column(primary_key=True)
    anti_pattern: Mapped[str] = mapped_column(String(120), index=True)
    recurring_context: Mapped[str] = mapped_column(Text, default="")
    severity: Mapped[str] = mapped_column(String(24), default="medium")
    cognitive_cost_score: Mapped[float] = mapped_column(Float, default=0.0)
    recurrence_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class InstitutionalEvaluation(Base):
    __tablename__ = "institutional_evaluations"
    id: Mapped[int] = mapped_column(primary_key=True)
    institutional_maturity_score: Mapped[float] = mapped_column(Float, default=0.0)
    usability_maturity_score: Mapped[float] = mapped_column(Float, default=0.0)
    release_maturity_score: Mapped[float] = mapped_column(Float, default=0.0)
    runtime_maturity_score: Mapped[float] = mapped_column(Float, default=0.0)
    governance_maturity_score: Mapped[float] = mapped_column(Float, default=0.0)
    memory_maturity_score: Mapped[float] = mapped_column(Float, default=0.0)
    strategic_usefulness_score: Mapped[float] = mapped_column(Float, default=0.0)
    maintainability_maturity_score: Mapped[float] = mapped_column(Float, default=0.0)
    operator_clarity_score: Mapped[float] = mapped_column(Float, default=0.0)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class MaturityBenchmark(Base):
    __tablename__ = "maturity_benchmarks"
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    current_score: Mapped[float] = mapped_column(Float, default=0.0)
    target_score: Mapped[float] = mapped_column(Float, default=0.0)
    evidence: Mapped[list] = mapped_column(JSON, default=list)
    trend: Mapped[str] = mapped_column(String(24), default="stable")
    maturity_level: Mapped[str] = mapped_column(String(24), default="developing")
    recommended_improvement: Mapped[str] = mapped_column(Text, default="")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ImprovementPlan(Base):
    __tablename__ = "improvement_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    plan_items: Mapped[list] = mapped_column(JSON, default=list)
    priority_order: Mapped[list] = mapped_column(JSON, default=list)
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class CapabilityLifecycleAudit(Base):
    __tablename__ = "capability_lifecycle_audits"
    id: Mapped[int] = mapped_column(primary_key=True)
    capability: Mapped[str] = mapped_column(String(120), index=True)
    lifecycle_state: Mapped[str] = mapped_column(String(40), index=True)
    value_evidence: Mapped[str] = mapped_column(Text, default="")
    maintenance_burden: Mapped[str] = mapped_column(String(24), default="medium")
    overlap_risk: Mapped[str] = mapped_column(String(24), default="medium")
    maturity_level: Mapped[str] = mapped_column(String(24), default="active")
    recommendation: Mapped[str] = mapped_column(Text, default="")
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class CapabilityRetirementCandidate(Base):
    __tablename__ = "capability_retirement_candidates"
    id: Mapped[int] = mapped_column(primary_key=True)
    capability: Mapped[str] = mapped_column(String(120), index=True)
    reason: Mapped[str] = mapped_column(Text, default="")
    burden_without_clarity: Mapped[bool] = mapped_column(Boolean, default=False)
    grouped_under_control_plane: Mapped[bool] = mapped_column(Boolean, default=False)
    retire_later: Mapped[bool] = mapped_column(Boolean, default=True)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ControlledEvolutionPlan(Base):
    __tablename__ = "controlled_evolution_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    what_to_evolve_next: Mapped[list] = mapped_column(JSON, default=list)
    what_to_freeze: Mapped[list] = mapped_column(JSON, default=list)
    what_to_consolidate: Mapped[list] = mapped_column(JSON, default=list)
    what_to_monitor: Mapped[list] = mapped_column(JSON, default=list)
    what_to_retire_later: Mapped[list] = mapped_column(JSON, default=list)
    what_not_to_touch: Mapped[list] = mapped_column(JSON, default=list)
    risk_notes: Mapped[list] = mapped_column(JSON, default=list)
    reversibility_notes: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class PlatformCatalogEntity(Base):
    __tablename__ = "platform_catalog_entities"
    id: Mapped[int] = mapped_column(primary_key=True)
    entity_name: Mapped[str] = mapped_column(String(128), index=True)
    entity_type: Mapped[str] = mapped_column(String(32), index=True)
    lifecycle_state: Mapped[str] = mapped_column(String(32), index=True)
    owner: Mapped[str] = mapped_column(String(128), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    related_phase: Mapped[str] = mapped_column(String(32), default="")
    related_files: Mapped[list] = mapped_column(JSON, default=list)
    related_apis: Mapped[list] = mapped_column(JSON, default=list)
    related_frontend_page: Mapped[str] = mapped_column(String(128), default="")
    dependencies: Mapped[list] = mapped_column(JSON, default=list)
    operational_importance: Mapped[str] = mapped_column(String(32), default="medium")
    documentation_status: Mapped[str] = mapped_column(String(32), default="partial")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class CapabilityOwnershipRecord(Base):
    __tablename__ = "capability_ownership_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    capability_name: Mapped[str] = mapped_column(String(128), index=True)
    owner: Mapped[str] = mapped_column(String(128), default="")
    lifecycle_state: Mapped[str] = mapped_column(String(32), default="active")
    ownership_status: Mapped[str] = mapped_column(String(32), default="clear")
    notes: Mapped[str] = mapped_column(Text, default="")
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class GoldenPathDefinition(Base):
    __tablename__ = "golden_path_definitions"
    id: Mapped[int] = mapped_column(primary_key=True)
    path_name: Mapped[str] = mapped_column(String(128), index=True)
    required_files: Mapped[list] = mapped_column(JSON, default=list)
    required_tests: Mapped[list] = mapped_column(JSON, default=list)
    required_readme_update: Mapped[bool] = mapped_column(Boolean, default=True)
    required_router_registration: Mapped[bool] = mapped_column(Boolean, default=False)
    required_migration_when_applicable: Mapped[bool] = mapped_column(Boolean, default=True)
    validation_commands: Mapped[list] = mapped_column(JSON, default=list)
    rollback_notes: Mapped[str] = mapped_column(Text, default="")
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class CapabilityScorecard(Base):
    __tablename__ = "capability_scorecards"
    id: Mapped[int] = mapped_column(primary_key=True)
    capability_name: Mapped[str] = mapped_column(String(128), index=True)
    entity_type: Mapped[str] = mapped_column(String(32), default="engine")
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    category_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    pass_fail_status: Mapped[str] = mapped_column(String(32), default="conditional_pass")
    readiness_level: Mapped[str] = mapped_column(String(32), default="developing")
    evidence_strength: Mapped[str] = mapped_column(String(32), default="moderate")
    gap_severity: Mapped[str] = mapped_column(String(32), default="moderate")
    improvement_priority: Mapped[str] = mapped_column(String(32), default="high")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ScorecardFinding(Base):
    __tablename__ = "scorecard_findings"
    id: Mapped[int] = mapped_column(primary_key=True)
    capability_name: Mapped[str] = mapped_column(String(128), index=True)
    finding_type: Mapped[str] = mapped_column(String(64), index=True)
    severity: Mapped[str] = mapped_column(String(32), default="moderate")
    evidence: Mapped[str] = mapped_column(Text, default="")
    recommended_action: Mapped[str] = mapped_column(Text, default="")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ReadinessGateReview(Base):
    __tablename__ = "readiness_gate_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    capability_name: Mapped[str] = mapped_column(String(128), index=True)
    gate_results: Mapped[dict] = mapped_column(JSON, default=dict)
    validation_commands: Mapped[list] = mapped_column(JSON, default=list)
    review_summary: Mapped[str] = mapped_column(Text, default="")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class GoldenPathWorkflow(Base):
    __tablename__ = "golden_path_workflows"
    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_name: Mapped[str] = mapped_column(String(128), index=True)
    workflow_type: Mapped[str] = mapped_column(String(64), index=True)
    guided_steps: Mapped[list] = mapped_column(JSON, default=list)
    workflow_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class GoldenPathChecklist(Base):
    __tablename__ = "golden_path_checklists"
    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_name: Mapped[str] = mapped_column(String(128), index=True)
    required_files: Mapped[list] = mapped_column(JSON, default=list)
    required_tests: Mapped[list] = mapped_column(JSON, default=list)
    validation_commands: Mapped[list] = mapped_column(JSON, default=list)
    rollback_notes: Mapped[str] = mapped_column(Text, default="")
    scorecard_checks: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class GoldenPathDeviationReview(Base):
    __tablename__ = "golden_path_deviation_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_name: Mapped[str] = mapped_column(String(128), index=True)
    deviation_reason: Mapped[str] = mapped_column(Text, default="")
    risk_introduced: Mapped[str] = mapped_column(String(32), default="moderate")
    affected_standards: Mapped[list] = mapped_column(JSON, default=list)
    compensating_controls: Mapped[list] = mapped_column(JSON, default=list)
    rollback_recovery_notes: Mapped[str] = mapped_column(Text, default="")
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ChangeImpactAssessment(Base):
    __tablename__ = "change_impact_assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    change_type: Mapped[str] = mapped_column(String(64), index=True)
    change_summary: Mapped[str] = mapped_column(Text, default="")
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    affected_files: Mapped[list] = mapped_column(JSON, default=list)
    risk_level: Mapped[str] = mapped_column(String(32), default="moderate")
    scores: Mapped[dict] = mapped_column(JSON, default=dict)
    required_human_reviewers: Mapped[list] = mapped_column(JSON, default=list)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ChangeReviewRequirement(Base):
    __tablename__ = "change_review_requirements"
    id: Mapped[int] = mapped_column(primary_key=True)
    change_type: Mapped[str] = mapped_column(String(64), index=True)
    review_flags: Mapped[dict] = mapped_column(JSON, default=dict)
    rationale: Mapped[str] = mapped_column(Text, default="")
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ChangeApprovalBrief(Base):
    __tablename__ = "change_approval_briefs"
    id: Mapped[int] = mapped_column(primary_key=True)
    change_summary: Mapped[str] = mapped_column(Text, default="")
    reason_for_change: Mapped[str] = mapped_column(Text, default="")
    expected_benefit: Mapped[str] = mapped_column(Text, default="")
    risk_if_approved: Mapped[str] = mapped_column(Text, default="")
    risk_if_rejected: Mapped[str] = mapped_column(Text, default="")
    validation_plan: Mapped[list] = mapped_column(JSON, default=list)
    rollback_plan: Mapped[list] = mapped_column(JSON, default=list)
    open_questions: Mapped[list] = mapped_column(JSON, default=list)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class PostImplementationReview(Base):
    __tablename__ = "post_implementation_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    change_summary: Mapped[str] = mapped_column(Text, default="")
    planned_outcome: Mapped[str] = mapped_column(Text, default="")
    actual_outcome: Mapped[str] = mapped_column(Text, default="")
    deviations: Mapped[list] = mapped_column(JSON, default=list)
    what_worked: Mapped[list] = mapped_column(JSON, default=list)
    what_failed: Mapped[list] = mapped_column(JSON, default=list)
    unexpected_impacts: Mapped[list] = mapped_column(JSON, default=list)
    affected_systems: Mapped[list] = mapped_column(JSON, default=list)
    rollback_status: Mapped[str] = mapped_column(String(32), default="not_required")
    operator_impact: Mapped[str] = mapped_column(String(32), default="low")
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ChangeLessonLearned(Base):
    __tablename__ = "change_lessons_learned"
    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_category: Mapped[str] = mapped_column(String(64), index=True)
    lesson_text: Mapped[str] = mapped_column(Text, default="")
    reusable_heuristic: Mapped[str] = mapped_column(Text, default="")
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ChangeImprovementAction(Base):
    __tablename__ = "change_improvement_actions"
    id: Mapped[int] = mapped_column(primary_key=True)
    action_text: Mapped[str] = mapped_column(Text, default="")
    priority: Mapped[str] = mapped_column(String(32), default="medium")
    status: Mapped[str] = mapped_column(String(32), default="open")
    owner: Mapped[str] = mapped_column(String(128), default="")
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class InstitutionalPolicy(Base):
    __tablename__ = "institutional_policies"
    id: Mapped[int] = mapped_column(primary_key=True)
    policy_name: Mapped[str] = mapped_column(String(128), index=True)
    policy_category: Mapped[str] = mapped_column(String(64), index=True)
    doctrine_text: Mapped[str] = mapped_column(Text, default="")
    non_negotiable: Mapped[bool] = mapped_column(Boolean, default=True)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class GovernanceDoctrine(Base):
    __tablename__ = "governance_doctrines"
    id: Mapped[int] = mapped_column(primary_key=True)
    doctrine_name: Mapped[str] = mapped_column(String(128), index=True)
    principle_summary: Mapped[str] = mapped_column(Text, default="")
    review_obligations: Mapped[list] = mapped_column(JSON, default=list)
    anti_automation_protections: Mapped[list] = mapped_column(JSON, default=list)
    continuity_principles: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class PolicyComplianceReview(Base):
    __tablename__ = "policy_compliance_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(128), index=True)
    subject_type: Mapped[str] = mapped_column(String(64), index=True)
    compliance_flags: Mapped[dict] = mapped_column(JSON, default=dict)
    conflict_summary: Mapped[str] = mapped_column(Text, default="")
    risk_severity: Mapped[str] = mapped_column(String(32), default="moderate")
    recommended_resolution_path: Mapped[list] = mapped_column(JSON, default=list)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class InstitutionalAuditEvent(Base):
    __tablename__ = "institutional_audit_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    what_decided_or_recommended: Mapped[str] = mapped_column(Text, default="")
    why_produced: Mapped[str] = mapped_column(Text, default="")
    source_systems: Mapped[list] = mapped_column(JSON, default=list)
    evidence_used: Mapped[list] = mapped_column(JSON, default=list)
    assumptions: Mapped[list] = mapped_column(JSON, default=list)
    policy_references: Mapped[list] = mapped_column(JSON, default=list)
    related_phase: Mapped[str] = mapped_column(String(32), default="")
    affected_capability: Mapped[str] = mapped_column(String(128), default="")
    human_reviewer_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class DecisionProvenanceRecord(Base):
    __tablename__ = "decision_provenance_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    decision_id: Mapped[str] = mapped_column(String(128), index=True)
    recommendation_source: Mapped[list] = mapped_column(JSON, default=list)
    review_inputs: Mapped[list] = mapped_column(JSON, default=list)
    scorecard_evidence: Mapped[list] = mapped_column(JSON, default=list)
    change_control_rationale: Mapped[str] = mapped_column(Text, default="")
    post_implementation_lessons: Mapped[list] = mapped_column(JSON, default=list)
    approval_assumptions: Mapped[list] = mapped_column(JSON, default=list)
    governance_conflicts: Mapped[list] = mapped_column(JSON, default=list)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class GovernanceLineageRecord(Base):
    __tablename__ = "governance_lineage_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    lineage_summary: Mapped[str] = mapped_column(Text, default="")
    policy_references: Mapped[list] = mapped_column(JSON, default=list)
    related_reviews: Mapped[list] = mapped_column(JSON, default=list)
    conflict_visibility: Mapped[str] = mapped_column(String(32), default="visible")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class EvidenceRecord(Base):
    __tablename__ = "evidence_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    evidence_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    evidence_type: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(255), default="")
    source_system: Mapped[str] = mapped_column(String(128), default="")
    source_file_or_endpoint: Mapped[str] = mapped_column(String(255), default="")
    related_policy: Mapped[str] = mapped_column(String(128), default="")
    related_control: Mapped[str] = mapped_column(String(128), default="")
    related_phase: Mapped[str] = mapped_column(String(32), default="")
    related_change: Mapped[str] = mapped_column(String(128), default="")
    related_audit_event: Mapped[str] = mapped_column(String(128), default="")
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    owner: Mapped[str] = mapped_column(String(128), default="")
    evidence_summary: Mapped[str] = mapped_column(Text, default="")
    confidence: Mapped[str] = mapped_column(String(32), default="moderate")
    freshness_status: Mapped[str] = mapped_column(String(32), default="fresh")
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ControlMapping(Base):
    __tablename__ = "control_mappings"
    id: Mapped[int] = mapped_column(primary_key=True)
    risk_to_control: Mapped[list] = mapped_column(JSON, default=list)
    control_to_evidence: Mapped[list] = mapped_column(JSON, default=list)
    evidence_to_policy: Mapped[list] = mapped_column(JSON, default=list)
    policy_to_audit_event: Mapped[list] = mapped_column(JSON, default=list)
    change_to_validation_evidence: Mapped[list] = mapped_column(JSON, default=list)
    release_to_runtime_evidence: Mapped[list] = mapped_column(JSON, default=list)
    pir_to_lesson_evidence: Mapped[list] = mapped_column(JSON, default=list)
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class EvidenceChainOfCustody(Base):
    __tablename__ = "evidence_chain_of_custody"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_origin: Mapped[str] = mapped_column(Text, default="")
    evidence_path: Mapped[list] = mapped_column(JSON, default=list)
    linked_decisions: Mapped[list] = mapped_column(JSON, default=list)
    linked_policies: Mapped[list] = mapped_column(JSON, default=list)
    linked_controls: Mapped[list] = mapped_column(JSON, default=list)
    linked_reviews: Mapped[list] = mapped_column(JSON, default=list)
    timestamp_trail: Mapped[list] = mapped_column(JSON, default=list)
    gaps: Mapped[list] = mapped_column(JSON, default=list)
    weak_links: Mapped[list] = mapped_column(JSON, default=list)
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    advisory_only: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
