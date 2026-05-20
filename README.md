# AI Forex Market Intelligence & Signal Assistant

Institutional-grade Forex analysis platform. The AI scans markets, generates high-probability signals with full reasoning, tracks outcomes, and learns over time. **It never auto-trades.** A human always executes.

> This repo is a production-grade scaffold: Next.js 14 frontend + Python FastAPI backend + PostgreSQL + Redis + Celery + ML stack, all containerised. It does **not** run inside the Lovable preview (Lovable runs Vite/React). Clone it and run `docker compose up`.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Next.js 14 (App Router) + TypeScript + Tailwind + shadcn    │
│  TradingView Lightweight Charts • Zustand • Framer Motion    │
└────────────────────────┬─────────────────────────────────────┘
                         │ REST + WebSocket
┌────────────────────────┴─────────────────────────────────────┐
│  FastAPI (async) — 16 modular engines                        │
│  ├─ Market Data        ├─ Technical Analysis                 │
│  ├─ Market Structure   ├─ Sentiment (FinBERT)                │
│  ├─ News & Macro       ├─ Signal Intelligence                │
│  ├─ ML (XGBoost/LSTM)  ├─ RL (Stable-Baselines3)             │
│  ├─ Backtesting (VBT)  ├─ Trade Journal                      │
│  ├─ Performance        ├─ Adaptive Learning                  │
│  ├─ Risk Management    ├─ Strategy Evolution                 │
│  └─ AI Explanation     └─ Dashboard API                      │
└──────┬────────────────────────────┬──────────────────────────┘
       │                            │
   PostgreSQL                  Redis + Celery
   (signals, journal,         (scanners, training,
    backtests, learning)       news ingestion)
```

## Quick start

```bash
cp .env.example .env       # add TWELVE_DATA_API_KEY, etc.
docker compose up --build
```

- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs

## Modules

See `backend/app/engines/` — each module has its own package with a clear interface. Adding a new indicator, ML model, or data provider is a single-file change.

## Disclaimer

This software is for research and education. It does not provide financial advice and never executes trades. Forex trading involves substantial risk of loss. All signals are probabilistic; always confirm with your own analysis and risk management.

## Phase 1 Run Guide

### 1) Install requirements

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Frontend:
```bash
cd frontend
npm install
```

### 2) Environment setup

```bash
cp .env.example .env
```

Required keys/settings:
- `TWELVE_DATA_API_KEY` (required for real live candles)
- `JWT_SECRET`
- `DATABASE_URL`
- `REDIS_URL`

If `TWELVE_DATA_API_KEY` is empty, the API returns synthetic demo candles and includes a warning in `/api/market/ohlcv`.

### 3) Run with Docker

```bash
docker compose up --build
```

Services:
- Frontend: `http://localhost:3000`
- Backend docs: `http://localhost:8000/docs`

### 4) Test key endpoints

```bash
bash backend/scripts/smoke_test.sh
```

Or manually:
- `GET /api/market/pairs`
- `GET /api/market/ohlcv?pair=EUR/USD&timeframe=1h&limit=100`
- `GET /api/analysis/EUR/USD`
- `GET /api/signals/scan`
- `GET /api/signals`

Health endpoint:
- `GET /api/health`

### 5) Common errors

- **422 on login/register email**: install backend deps (requires `email-validator`).
- **Synthetic data warning**: add `TWELVE_DATA_API_KEY` for real Twelve Data candles.
- **DB connection errors**: ensure `postgres` service is healthy and `DATABASE_URL` uses host `postgres` inside Docker.
- **Frontend cannot reach backend**: set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env`.

### 6) Verify real vs synthetic market data

- Check `GET /api/health`:
  - `market_data_mode: "real"` means Twelve Data is configured.
  - `market_data_mode: "synthetic"` means demo mode.
- Check `GET /api/market/ohlcv?...`:
  - `source: "twelve_data"` means live provider candles are active.
  - `warning` field is non-null when synthetic fallback is active or Twelve Data failed.

## Phase 2 Signal Trust Engine

Phase 2 improves trust and explainability of signals for the **personal Signal Assistant** (analysis only, no auto-execution).

- **Confidence (0–100)** is derived from multi-indicator confluence (trend, RSI, momentum, structure, and pattern alignment).
- **HOLD** appears when confirmations conflict or confluence is weak, instead of forcing BUY/SELL.
- **Risk level**:
  - `low/medium/high` is determined using volatility (ATR) and stop-loss distance sanity.
  - very low volatility weakens signal strength.
  - extreme volatility or oversized stop distance marks high risk.
- **Data source transparency**:
  - signals include `data_source: real|synthetic`.
  - synthetic mode adds warnings to reasoning.
- This remains a **personal signal assistant only** and **not financial advice**; it does not execute trades.

## Phase 3 Outcome Validation

Phase 3 adds candle-based post-signal validation so you can track whether signals were useful.

- Validation scans pending signals and compares post-signal candles against signal TP/SL/invalidation rules.
- Outcomes can be: `pending`, `win`, `loss`, `neutral`, `expired`.
- `pending` exists because enough future candles may not yet be available inside the timeframe expiry window.
- `HOLD` signals are validated to `neutral` after expiry and are excluded from win-rate calculations.
- Limitations: candle-level validation cannot know intra-candle execution ordering/spread/slippage; treat metrics as approximate signal-quality indicators, not broker-execution truth.
- This remains a personal **Signal Assistant** only and not financial advice.

## Phase 4 Automation and Discipline

- Scheduler: Celery beat runs automatic outcome validation every 10 minutes (`validate_outcomes`).
- Manual validation: call `POST /api/signals/validate-outcomes` any time.
- Validation run history is stored (`validation_runs`) and available via `GET /api/signals/validation-runs`.
- Quality gates:
  - minimum confidence threshold for BUY/SELL,
  - strong signals are downgraded when risk is high,
  - duplicate pair/timeframe signals are blocked within cooldown window,
  - synthetic BUY/SELL signals are blocked by default (`ALLOW_SYNTHETIC_SIGNALS=false`).
- Performance filtering supports pair/timeframe/risk/strength and synthetic include toggle.
- No trade execution is performed. This remains a personal Signal Assistant only.

## Phase 5 Calibration and Realistic Costs

- Timestamps now use timezone-aware UTC helpers to avoid deprecated naive UTC usage.
- Performance uses **net pips by default**:
  - `gross_result_pips` = raw movement
  - `estimated_cost_pips` = spread + slippage + optional commission assumption
  - `net_result_pips` = gross - estimated costs
- Pip model includes pair-aware assumptions:
  - normal FX: 0.0001
  - JPY pairs: 0.01
  - XAU/USD: configurable `XAU_PIP_SIZE`
- Calibration endpoint compares confidence buckets vs realized win rate to flag over/under-confidence.
- Reliability score summarizes sample size, net performance, win rate, and calibration alignment.
- Results are **estimates** from candle data + assumptions; broker execution reality may differ.
- No trade execution is performed. This remains a personal signal assistant only.

## Phase 6 Adaptive Intelligence

- Regime engine classifies market state (`trending`, `ranging`, `breakout`, `high volatility`, `low volatility`, `news-sensitive`, `unstable`) using explainable metrics (ATR, ADX, slope, compression, momentum consistency).
- Signal weighting adapts by regime in bounded and explainable ways (e.g., trend weighting up in trends, RSI weighting up in ranges).
- Strategy profiles (`scalping`, `intraday`, `swing`, `conservative`, `aggressive`) control confidence/risk/cooldown posture.
- Drift-aware reliability warnings trigger when invalidation frequency rises or reliability falls.
- Reliability history is persisted for trend charting and auditability.
- Adaptation is gradual/rule-bounded and explainable; no black-box-only decisions.
- This is still a personal signal assistant and does not execute trades.

## Phase 7 Stability and Safe Learning

- Strategy profile state is persisted in DB (`strategy_state`) so active profile survives restarts and remains authoritative across workers.
- Reliability snapshots are scheduler-driven (not endpoint-call-driven) to keep trend history cleaner and reproducible.
- Drift analytics include invalidation-frequency pressure and reliability degradation warnings.
- Explainability audit records persist adaptive decisions (before/after confidence, regime, profile, adaptive changes, reasons).
- Safety boundaries keep adaptation bounded and explainable (confidence clamped and profile-based thresholds).
- Regime/session performance analytics support observability by regime, profile, risk, and session.
- Session awareness uses UTC-safe classification (Asian, London, overlap, New York, off-hours).
- This remains a personal signal assistant only; no autonomous trade execution.
- Unrestricted self-learning is intentionally avoided to reduce overfitting and unstable behavior.

## Phase 8 Unified Infrastructure and Replayability

- A unified signal pipeline service now centralizes generation + discipline + persistence + audit behavior, reducing path drift between API and schedulers.
- Replay endpoint (`POST /api/signals/replay/run`) provides deterministic, explainable reruns using current engine versions and captured config context.
- Versioned reasoning metadata is embedded in config snapshots (`engine`, `weighting`, `discipline`, `profile` versions) for historical interpretability.
- Maintenance jobs run on schedule to clean orphaned records and keep reliability history/snapshots healthy.
- Strategy state is persisted in DB and serves as authoritative profile state across workers/restarts.
- Audit export endpoints provide reconstruction for signal and reliability decisions.
- Reproducibility and concurrency safety are prioritized; autonomous trading remains explicitly disabled.

## Phase 9 Governance and Safe Experimentation

- Experiments are tracked as first-class records with versions, datasets, replay metadata, and regression analysis.
- Sandbox replay mode (`/api/experiments/run-replay`) is isolated from production strategy state and does not overwrite production calibration/reliability baselines.
- Version governance APIs support activation/rollback/inspection (`/api/versions`).
- Data integrity endpoint (`/api/data/integrity`) surfaces contamination and malformed-data risk signals.
- Regression detection classifies candidate behavior as acceptable/warning/regression/critical regression.
- Governance prioritizes rollback readiness and explainable evidence over uncontrolled adaptation.
- Unrestricted self-modifying loops remain intentionally disabled.
- This remains a personal signal assistant only and does not execute trades.

## Phase 10 Historical Data and Replay Infrastructure

- Historical candles are now persisted in dedicated tables with source/integrity metadata to support deterministic replay and higher-integrity analytics.
- Ingestion supports backfill/incremental patterns through API-triggered ingestion and stores ingestion run statistics.
- Dataset integrity scoring now includes gap/duplicate/malformed/synthetic checks per dataset.
- Replay sessions support start/step/get patterns and preserve replay state for reproducibility.
- Replay realism remains estimate-based (spread/slippage/cooldown/session transitions handled at model level, not broker execution level).
- Versioned schema and config metadata are exposed to keep historical experiments interpretable.
- Maintenance philosophy emphasizes cleanup, retryability, and quarantine-ready integrity workflows.
- No execution is performed; this remains a personal signal assistant only.

## Phase 12 Research Orchestration and Coordinated Intelligence

Phase 12 adds a **research-first orchestration layer** that coordinates replay analysis, regime analysis, calibration review, drift monitoring, portfolio stress checks, reliability evaluation, experiment comparisons, and integrity checks into one explainable workflow.

### Philosophy
- Intelligence outputs are coordinated into unified conclusions rather than isolated metrics.
- Recommendations are always explainable, reproducible, and human-reviewed.
- This remains a personal signal/research assistant.
- **No autonomous trading and no order execution are implemented.**

### Human-controlled recommendations
The platform may recommend actions such as:
- reduce aggressive weighting,
- suspend a profile,
- re-run calibration,
- inspect integrity gaps,
- replay specific windows,
- downgrade confidence scaling.

Recommendations are advisory only and are **never auto-applied**.

### Research memory and governance boundaries
- Research tasks and findings are persisted for traceability and continuity.
- Timeline/evidence links preserve why conclusions changed over time.
- Governance boundaries preserve sandbox isolation, reproducibility, and auditability.
- The orchestration layer does not mutate production trading state automatically.

### API
- `GET /api/system/health` returns coordinated health scoring across data, calibration, replay integrity, portfolio reliability, adaptive stability, governance safety, and drift pressure.

### Remaining blockers for Phase 13
- Add richer evidence provenance from each engine with strict schema validation.
- Add UI drill-down linking findings to exact replay candles and experiment versions.
- Add async orchestration workers for large historical comparison jobs.
- Add role-based approval workflow for research recommendation promotion.

## Phase 13 Distributed Research Infrastructure and Operator Intelligence

Phase 13 extends the platform into a scalable quantitative research environment focused on distributed orchestration, indexed research memory, and operator visibility.

### Scalability philosophy
- Research workloads are queued and prioritized to handle replay batching, experiment batching, integrity scans, stress sweeps, and calibration/regime sweeps.
- Checkpoint/resume support makes long historical replay practical and restart-safe.

### Operator-control philosophy
- Operators can observe queue status, worker status, throughput, failure counts, and latency through dedicated system metrics and the Operator Center.
- All recommendations remain advisory and human-controlled.

### Indexing and research-memory philosophy
- Findings, tasks, experiments, and replay artifacts can be searched through a unified research index endpoint.
- Knowledge graph edges create institutional-style relationships between findings, experiments, regimes, and failures.

### Observability strategy
- `GET /api/system/metrics` aggregates scheduler/worker health, backlog, failed tasks, throughput, latency, incident counts, and database health.
- Operator Center visualizes system pressure indicators and reliability posture.

### Resource governance rationale
- Workload resource estimates, priority scoring, queue controls, and retry tracking reduce runaway analysis patterns.
- Distributed orchestration remains bounded and reproducible.

### No-execution disclaimer
- This platform remains a personal research and signal-intelligence system.
- It does **not** execute orders or run autonomous trading agents.

### Remaining blockers for Phase 14
- Add persistent per-worker heartbeats with historical uptime trend views.
- Add storage quota telemetry and automated archival jobs for old replay checkpoints.
- Add semantic/vector indexing for cross-artifact research retrieval.
- Add richer operator approval workflows for recommendation lifecycle transitions.

## Phase 14 Meta-Intelligence and Strategic Reasoning

Phase 14 introduces a strategic synthesis layer that converts cross-system telemetry into coherent, explainable operator guidance.

### Strategic reasoning philosophy
- Strategic synthesis combines regime, drift, integrity, reliability, replay, portfolio, governance, and workload signals.
- Conclusions are deterministic and evidence-linked to preserve reproducibility.

### Anomaly interpretation philosophy
- Anomalies are interpreted with likely causes, impact scope, confidence, and supporting evidence.
- Interpretation is meant to augment operator judgment, not replace it.

### Operator augmentation principles
- Strategic briefings and executive summaries provide high-level context and priority guidance.
- Recommendations are advisory-only and never auto-applied.

### Conflict-detection rationale
- Recommendation conflicts are explicitly flagged when systems produce opposing guidance.
- Conflicts require human arbitration before any policy changes are considered.

### Governance preservation
- Strategic status and briefings remain human-reviewable and traceable.
- No strategic pathway can self-authorize execution actions.

### No-execution disclaimer
- This platform remains personal research and signal intelligence tooling only.
- It does **not** place orders and does not run autonomous trading agents.

### Remaining blockers for Phase 15
- Add richer persisted anomaly lineage with artifact-level diff references.
- Add dependency graph drift-over-time visualization and alert thresholds.
- Add operator acknowledgment workflows and briefing lifecycle states.
- Add calibrated confidence backtesting for strategic recommendations.

## Phase 15 Cognitive Compression and Institutional Workflow

Phase 15 focuses on long-horizon operator clarity by compressing complex research streams into explainable strategic knowledge.

### Cognitive compression philosophy
- The platform condenses high-volume outputs into strategic themes, recurring instability patterns, successful conditions, unresolved anomalies, and critical risks.
- Compression is deterministic and reproducible to prevent narrative drift.

### Operator-centric intelligence philosophy
- Human-readable strategic context is prioritized over metric noise.
- Executive console additions emphasize trust, clarity, and actionable interpretation.

### Strategic narrative rationale
- Narrative generation links claims to explicit evidence references and confidence.
- Narratives are advisory interpretations, not self-authorizing decisions.

### Long-horizon memory principles
- Strategic memory aggregates monthly history, timeline events, and recurring incident patterns.
- Institutional workflow records preserve owner, state, evidence, and review history.

### Sustainability philosophy
- Stale investigation detection, unresolved issue surfacing, recommendation aging awareness, and concentration-risk flags help control complexity over time.
- Institutional archives keep strategic artifacts searchable and reusable.

### Governance preservation
- All recommendations remain explainable and advisory-only.
- No autonomous execution and no self-authorizing behavior are permitted.

### No-execution disclaimer
- This remains a personal research and signal intelligence platform only.
- It does **not** place trades or execute orders.

### Remaining blockers for Phase 16
- Add timeline-weighted confidence decay and recommendation aging policies.
- Add workflow SLA monitoring and escalation policies for abandoned reviews.
- Add semantic archive clustering and operator-specific brief curation.
- Add cross-phase narrative drift validation across long historical windows.

## Phase 16 Constitutional Intelligence and Trust Preservation

Phase 16 adds a constitutional governance layer to preserve trust, explainability, reproducibility, and operator confidence as system intelligence scales.

### Constitutional philosophy
- Explicit constitutional rules are persisted and queryable (`/api/governance/constitution`).
- Core rules include no autonomous execution, no silent adaptation, and operator approval requirements.

### Trust-preservation rationale
- Trust pressure tracks unresolved contradictions, confidence inflation, recommendation reversals, anomaly fatigue, governance overrides, and unresolved critical drift.
- Strategic guidance is flagged early when trustworthiness erosion signals appear.

### Explainability integrity philosophy
- Explainability integrity score tracks evidence completeness, reproducibility coverage, narrative consistency, recommendation traceability, audit completeness, and governance compliance.
- Consistency validation detects contradictory narratives, unstable recommendations, and confidence mismatches.

### Strategic continuity principles
- Long-term continuity summaries preserve yearly strategic summaries, regime eras, governance events, reliability eras, anomaly eras, and adaptation cycles.
- Confidence decay prevents stale certainty from becoming institutional dogma.

### Governance durability
- Recommendation lifecycle entries preserve changes, contradictions, evidence strength shifts, and governance concerns.
- Governance incidents track severity (`info`, `warning`, `critical`, `constitutional risk`) for institutional response discipline.

### No-execution guarantee
- This remains a personal research and signal intelligence platform only.
- It does **not** execute trades and does not self-authorize strategic actions.

### Remaining blockers for Phase 17
- Add policy-diff tooling for constitutional rule versioning and rollback.
- Add audit-signoff workflow for constitutional-risk incidents.
- Add decayed-confidence trend visualizations across archive timelines.
- Add governance simulation harness for rule stress testing before rollout.

## Phase 17 Epistemic Integrity and Institutional Resilience

Phase 17 introduces epistemic governance controls to keep long-horizon institutional knowledge coherent, reviewable, and trustworthy.

### Epistemic philosophy
- The system continuously evaluates evidence quality, freshness, contradiction density, stale assumptions, circular recommendation logic, and weak inference chains.
- Knowledge coherence is treated as a first-class safety boundary.

### Contradiction-management philosophy
- Contradictions are surfaced through explicit workflows (review, arbitration, deprecation, retirement consideration).
- No automatic deletion or self-authorized strategic retirement is allowed.

### Knowledge decay rationale
- Assumption confidence decays when validation is stale, replay coverage is weak, or contradictory evidence accumulates.
- This prevents frozen dogma and overconfidence from legacy conclusions.

### Institutional resilience principles
- Coherence scoring tracks epistemic integrity, contradiction pressure, institutional coherence, evidence freshness, fragmentation, and governance resilience.
- Archive stabilization detects duplicates, conflicts, and weakly grouped investigations.

### Governance continuity philosophy
- Human-review gates are mandatory for assumption updates, contradiction resolutions, and narrative transitions.
- Strategic changes remain explainable, reproducible, and operator-controlled.

### No-execution guarantee
- This remains a personal research and signal intelligence platform only.
- It does **not** execute trades and does not self-authorize strategic changes.

### Remaining blockers for Phase 18
- Add temporal contradiction heatmaps and era-based coherence drift analytics.
- Add operator consensus workflows for multi-step contradiction arbitration.
- Add replay-linked assumption validation schedulers with SLA tracking.
- Add archive-level reproducibility checksum verification for long-term integrity.

## Phase 18 Human Sovereignty and Anti-Complexity Architecture

Phase 18 reinforces explicit human authority and anti-complexity controls so long-horizon intelligence remains usable, explainable, and cognitively sustainable.

### Human sovereignty philosophy
- Operator override remains available at all times.
- No hidden adaptation, no silent escalation, no self-promoting conclusions, and no irreversible autonomous changes are permitted.
- Human approval is required for governance-sensitive operations.

### Anti-complexity philosophy
- Complexity pressure is measured across overload, saturation, backlog, alert density, governance burden, contradiction backlog, sprawl, and replay pressure.
- Simplification pipelines collapse redundant findings, deduplicate recommendations, suppress repetitive noise, and prioritize highest-impact investigations.

### Cognitive sustainability rationale
- Operator load scoring tracks cognitive load, fatigue, clarity, recommendation saturation, and governance burden.
- Human review pacing and focus-mode filtering reduce desensitization and alert fatigue.

### Strategic minimalism principles
- Focus modes (stability/calibration/replay/governance/anomaly/portfolio) intentionally suppress unrelated noise while preserving explainability depth.
- Layered explainability preserves reproducibility from executive summary to full audit chain.

### Governance simplicity philosophy
- Institutional minimalism safeguards identify low-value workflows, recommendation bloat, stale dashboards, and archive complexity growth.
- Strategic resets are operator-controlled, reversible, auditable, and never self-authorized.

### No-execution guarantee
- This remains a personal research and signal intelligence platform only.
- It does **not** execute trades and never self-authorizes strategic changes.

### Remaining blockers for Phase 19
- Add adaptive pacing policies based on operator interaction fatigue trends.
- Add longitudinal simplification efficacy scoring across quarters.
- Add policy-level reset approval chains with role segregation.
- Add archive entropy metrics and automated (human-approved) consolidation plans.

## Phase 19 Longevity and Strategic Survivability

Phase 19 establishes long-horizon survivability architecture to preserve institutional continuity across rewrites, migrations, and strategic evolution.

### Longevity philosophy
- Every major change carries lineage metadata: what changed, why, expected impact, affected assumptions, affected narratives, replay validity impact, and compatibility notes.
- Continuity is treated as an operational requirement, not optional documentation.

### Institutional continuity rationale
- Multi-era history (`/api/system/eras`) preserves reliability, governance, volatility, calibration, transition, crisis, and replay-migration context.
- Operator rationale remains central for future interpretability.

### Migration governance philosophy
- Migration planning is operator-approved, audit logged, reproducibility-preserving, and reversible where possible.
- No irreversible self-directed evolution is permitted.

### Replay compatibility philosophy
- Compatibility mode supports legacy replay interpretation with explicit integrity warnings and adapter requirements.
- Historical research remains interpretable even as engines evolve.

### Strategic lineage principles
- Deprecation workflows are explicit, auditable, and human-reviewed.
- No silent removals of assumptions, narratives, or strategic artifacts.

### Survivability engineering rationale
- Survivability scoring tracks architecture, migration safety, replay compatibility, governance durability, archive durability, institutional continuity, and operational resilience.
- Archive durability checks detect broken lineage and replay reference inconsistencies.

### No-execution guarantee
- This remains a personal research and signal intelligence platform only.
- It does **not** execute trades and does not self-authorize strategic evolution.

### Remaining blockers for Phase 20
- Add cross-era survivability trend analytics with drift-adjusted baselines.
- Add migration rehearsal simulator with rollback confidence scoring.
- Add durable lineage signatures for tamper-evident archival continuity.
- Add operator handoff packs for long absences and continuity restoration.

## Phase 20 Strategic Renewal and Controlled Evolution

Phase 20 introduces strategic-renewal architecture to keep the platform adaptive over multi-year horizons without compromising sovereignty, continuity, or explainability.

### Renewal philosophy
- Renewal mechanisms detect obsolete assumptions, stale governance structures, over-preserved workflows, outdated replay methods, strategic rigidity, archive stagnation, and institutional inertia.
- The goal is healthy evolution without strategic drift or institutional fossilization.

### Anti-rigidity rationale
- Adaptability scoring tracks governance, recommendations, workflows, replay, profiles, and calibration responsiveness.
- Inertia metrics make bottlenecks and adaptation paralysis visible before they become structural failures.

### Institutional adaptability philosophy
- Renewal workflows (assumption/governance/replay/archive/profile/methodology) are operator-reviewed, auditable, reproducible, and reversible where possible.
- Innovation experiments run in sandbox mode only and never auto-promote.

### Controlled evolution principles
- Evolution plans capture rationale, affected systems, compatibility impact, replay impact, governance impact, survivability impact, and rollback strategy.
- Major transitions remain explicit and human-approved.

### Identity-preservation philosophy
- The system tracks constitutional continuity, governance identity, explainability identity, sovereignty guarantees, and mission continuity so adaptation does not erase institutional identity.

### Long-horizon resilience rationale
- Evolution timelines and survivability metadata preserve institutional memory across eras, governance transitions, methodology shifts, and resilience recoveries.
- Anti-dogma scans continuously challenge stale assumptions and narrative lock-in.

### No-execution guarantee
- This remains a personal research and signal intelligence platform only.
- It does **not** execute trades and does not allow autonomous strategic authority.

### Remaining blockers for Phase 21
- Add quantitative renewal-success attribution per transition cycle.
- Add operator workload-aware scheduling for renewal proposals.
- Add cross-era identity drift thresholds with configurable alerts.
- Add policy-pack simulation for parallel controlled-evolution scenarios.

## Phase 21 Unified Meta-Operating System

Phase 21 introduces a unified meta-operating layer that coordinates governance, replay, research, continuity, survivability, observability, and renewal systems into one coherent institutional control plane.

### Meta-operating philosophy
- The platform now includes a dedicated meta-coordination layer to reduce subsystem fragmentation and improve long-horizon institutional manageability.
- Coordination remains recommendation-driven and operator-governed.

### Coordination rationale
- A global coordination graph links governance, replay, research, workflows, assumptions, migrations, renewals, incidents, and strategic narratives.
- Coordination pressure detection identifies divergence, duplicated logic, workflow fragmentation, synchronization failures, and overhead growth.

### Institutional cohesion principles
- Meta-resilience scoring tracks coordination resilience, synchronization integrity, institutional cohesion, subsystem alignment, continuity integrity, and governance coordination health.
- Cohesion is monitored as a first-class survivability dimension.

### Synchronization philosophy
- Synchronization checks flag unsynchronized eras, incompatible governance assumptions, replay/governance drift, and stale continuity mappings.
- Resolution remains operator-reviewed and non-destructive.

### Fragmentation-management rationale
- Institutional simplification recommendations identify overlapping workflows, duplicated narratives, redundant rules, stale links, and synchronization dead zones.
- The goal is lower coordination burden without hiding critical risk.

### No-execution guarantee
- This remains a personal research and signal intelligence platform only.
- It does **not** execute trades and does not permit autonomous irreversible coordination actions.

### Remaining blockers for Phase 22
- Add cross-layer policy conflict solver with human-approved reconciliation templates.
- Add live coordination graph drift monitoring with operator-tunable thresholds.
- Add longitudinal meta-memory anomaly clustering across multi-year timelines.
- Add explainability delta tracking for major coordination restructures.

## Phase 22 Semantic Stability and Strategic Orientation

Phase 22 hardens long-horizon meaning preservation so institutional concepts, narratives, and governance language remain coherent and interpretable over time.

### Semantic stability philosophy
- The platform actively monitors meaning consistency, narrative drift, governance terminology drift, replay interpretation drift, and recommendation semantic divergence.
- Conflicting definitions are surfaced early before semantic corruption compounds.

### Meaning-preservation rationale
- Concept lineage records preserve origin, revisions, contradictions, retired meanings, successor concepts, and confidence evolution.
- This ensures historical interpretation remains anchored even as systems evolve.

### Institutional orientation principles
- Orientation views continuously answer optimization target, constant principles, recent assumption shifts, dominant priorities, rising risks, and complexity hotspots.
- Orientation scoring tracks semantic coherence, clarity, comprehensibility, interpretability, and operator orientation stability.

### Glossary governance philosophy
- Canonical institutional glossary terms are persisted with deprecated markers, related concepts, historical meanings, replay relevance, and governance impact.
- Terminology governance reduces ambiguity across eras and teams.

### Anti-ambiguity rationale
- Meaning conflict detection flags contradictory terminology, duplicated concepts with different meanings, and interpretation conflicts.
- Narrative stabilization consolidates duplicates and identifies stale retirement candidates without irreversible deletion.

### Long-horizon interpretability principles
- Comprehension safeguards detect abstraction overload, terminology inflation, recursive governance complexity, and unreadable audit chains.
- Simplification guidance is generated to keep human comprehension central.

### No-execution guarantee
- This remains a personal research and signal intelligence platform only.
- It does **not** execute trades and does not permit autonomous strategic authority or recursive self-justifying governance.

### Remaining blockers for Phase 23
- Add semantic-drift trend analytics across eras with confidence-adjusted thresholds.
- Add glossary review cadences with operator signoff history and impact scoring.
- Add cross-model language consistency checks for generated narratives.
- Add semantic rollback tooling for concept-definition regressions.

## Phase 23 Mission Integrity and Existential Alignment

Phase 23 adds mission-integrity architecture to preserve foundational purpose, human-centered strategy, and existential alignment over extremely long institutional timelines.

### Mission-preservation philosophy
- The platform now maintains explicit mission structures: foundational mission, enduring objectives, strategic non-goals, constitutional commitments, sovereignty guarantees, anti-autonomy boundaries, and interpretability commitments.
- Mission intent remains an explicit governance artifact, not implicit tribal memory.

### Anti-optimization rationale
- Drift detection monitors mission, optimization, governance, complexity, purpose erosion, identity fragmentation, and recommendation-purpose divergence.
- Optimization without strategic value is treated as a first-class risk.

### Existential alignment principles
- Mission status scoring tracks mission alignment, existential coherence, strategic-purpose integrity, human-intent alignment, and institutional authenticity.
- Alignment warnings trigger simplification and purpose-recovery recommendations.

### Strategic humility philosophy
- Humility safeguards detect overconfidence inflation, self-importance drift, excessive abstraction, recursive governance complexity, false certainty, and recommendation absolutism.
- Guidance emphasizes uncertainty discipline and language simplification.

### Human-intent anchoring rationale
- Operator anchor notes preserve long-horizon intent, mission reaffirmations, reset intent, and anti-drift confirmations.
- Future evolution remains anchored to operator intent rather than internal optimization loops.

### Institutional authenticity philosophy
- Anti-hollowing protection flags purposeless subsystems, stale governance rituals, symbolic workflows, recommendation inflation, and archive accumulation without relevance.
- Retirement/simplification recommendations preserve meaningful institutional identity.

### No-execution guarantee
- This remains a personal research and signal intelligence platform only.
- It does **not** execute trades and does not allow autonomous institutional authority or self-generated mission drift.

### Remaining blockers for Phase 24
- Add mission-drift trend analytics with confidence-weighted decay over eras.
- Add operator reaffirmation cadence workflows with retention and review SLAs.
- Add cross-console mission-language consistency checks.
- Add mission-impact scoring for every major governance/replay/renewal proposal.

## Phase 25 Reality Anchoring and Practical Relevance

Phase 25 adds a reality-anchoring layer so the platform stays empirically grounded, strategically relevant, and human-centered. We explicitly resist internally self-validating governance loops, replay-only optimization, and complexity without practical value.

Guiding principles:
- Reality grounding over internal coherence alone
- Practical usefulness preservation over framework expansion
- External validity and operator utility as primary references
- Pragmatic intelligence over theoretical sophistication
- No-execution guarantee: this remains a research and signal intelligence platform only; it never executes trades

This phase introduces reality and relevance scoring, internal-loop detection, pragmatism warnings, replay-to-reality checks, usefulness anchors, and a dedicated Reality & Relevance Console.

## Phase 26 Personal Adaptation and Context-Aware Intelligence

Phase 26 introduces personal adaptation and context-aware intelligence so the platform stays aligned with evolving operator priorities, strategic needs, and cognitive capacity across long timelines.

Principles:
- Personal alignment over generic optimization
- Context awareness over static workflows
- Cognitive sustainability and anti-burnout protections
- Human-centered adaptability with operator intent as final authority
- No-execution guarantee: research/signal intelligence only; never autonomous trade execution

This phase adds context status and alignment scoring endpoints, adaptive workflow modes, overload safeguards, personal continuity memory, simplification guidance, and a dedicated Personal Alignment Console.

## Phase 27 Attention Architecture and Strategic Signal Extraction

Phase 27 adds attention architecture and priority intelligence to keep the platform focused on high-impact signal while suppressing low-value noise and urgency inflation.

Principles:
- Attention is a scarce strategic resource
- High-impact signal should remain visible; stale noise should fade
- Urgency must remain proportional and operator-governed
- Cognitive sustainability requires suppression, consolidation, and pruning
- No-execution guarantee: this remains a personal research and signal intelligence platform only

This phase introduces attention classification, strategic signal extraction, priority scoring, fatigue detection, focus-mode orchestration, relevance half-life tracking, anti-noise governance, and a dedicated Attention & Focus Console.

### Remaining blockers for Phase 28
- Persist attention-memory artifacts in durable DB tables with operator annotations.
- Add time-series trend analytics for alert-fatigue and signal-to-noise drift.
- Introduce operator-configurable suppression thresholds per focus mode.
- Add cross-console attention-impact scoring for every new workflow feature.

## Phase 28 Temporal Intelligence and Strategic Timing

Phase 28 adds temporal intelligence so the platform can distinguish short-term noise from longer-term strategic change, pace attention proportionally, and preserve operator agency over timing decisions.

Principles:
- Timing and urgency are related but not equivalent
- Rhythm awareness reduces reactive over-rotation
- Recurrence detection improves long-horizon judgment
- Strategic pacing should be proportionate and cognitively sustainable
- No-execution guarantee: temporal recommendations are advisory-only in a signal intelligence platform

This phase introduces temporal timing status, rhythm scanning, relevance decay, cycle detection, timing conflict detection, pacing recommendations, temporal memory, and a dedicated Temporal Intelligence Console.

## Phase 29 Strategic Synthesis and Central Nervous System

Phase 29 introduces a central strategic synthesis layer that condenses signals across attention, timing, reality, mission, governance, and operator load into one operator-first strategic view.

Principles:
- Cross-layer harmonization reduces dashboard fragmentation
- Conflict detection highlights disagreement between layers before action
- Synthesis is decision support, not decision replacement
- Human judgment remains final and sovereign
- No-execution guarantee: synthesis recommendations are advisory only

This phase adds a synthesis engine, conflict detection, strategic condensation (3 priorities / 3 ignore / 3 risks), synthesis API endpoints, persistence models, migration, tests, and the Strategic Synthesis Console.

## Phase 30 Anticipatory Intelligence and Strategic Foresight

Phase 30 introduces anticipatory intelligence to detect degradation pressure early, before reliability, attention, governance, replay quality, or strategic alignment materially decline.

Principles:
- Early warning over late reaction
- Foresight is probabilistic and limited, not deterministic
- Trajectory awareness helps prevent avoidable instability
- Prevention-over-reaction supports cognitive sustainability
- Human review is required for all interventions
- No-execution guarantee: all foresight output is advisory only

This phase adds early warning detection, foresight scoring, trajectory detection, intervention planning, foresight memory, dedicated APIs, persistence models/migration, tests, and a Foresight Console.

## Phase 31 Scenario Intelligence and Consequence Modeling

Phase 31 introduces scenario intelligence to explore plausible futures before decisions are made, with explicit consequence modeling and tradeoff visibility across governance, replay, attention, reality, and operator-load layers.

Principles:
- Scenarios are planning tools, not predictions
- Consequence modeling improves preparedness under uncertainty
- Tradeoff awareness prevents one-dimensional optimization
- Uncertainty discipline is mandatory for strategic simulation
- Human review is required for any scenario-guided policy change
- No-execution guarantee: all scenario output is advisory-only

This phase adds scenario execution, comparison, tradeoff summaries, consequence modeling, persistence models/migration, tests, and a Scenario Lab console.

## Phase 32 Adaptive Strategic Pathways

Phase 32 introduces adaptive strategic pathways so conditional responses can evolve with pressure, operator capacity, governance state, replay confidence, and data integrity while remaining operator-approved and reversible.

Principles:
- Adaptive pathways are planning structures, not autonomous actions
- Conditional responses improve consistency under changing constraints
- Reversibility is required for safe strategic adaptation
- Human approval remains mandatory before pathway adoption
- No-execution guarantee: pathway outputs are advisory only

This phase adds pathway evaluation/recommendation/comparison APIs, persistence models/migration, pathway memory, tests, and the Strategic Pathways Console.

## Phase 33 Causal Intelligence and Root-Cause Analysis

Phase 33 introduces causal intelligence to help explain why instability emerges, how subsystem dependencies propagate pressure, and which interventions may reduce recurrence risk under uncertainty.

Principles:
- Causal reasoning supports decisions; it does not prove certainty
- Correlation is not causation and must be treated carefully
- Intervention-effect estimates are bounded, probabilistic, and reversible
- Dependency propagation clarifies second-order risk pathways
- Human review remains mandatory for intervention decisions
- No-execution guarantee: causal recommendations are advisory-only

This phase adds causal analysis, graph snapshots, dependency propagation estimates, intervention-effect estimation, persistence models/migration, tests, and a Causal Intelligence Console.

## Phase 34 Institutional Learning Intelligence

Phase 34 introduces institutional learning intelligence to extract evidence-based lessons from interventions, forecasts, pathways, governance incidents, and operator feedback while preserving human authority over adoption.

Principles:
- Learning informs human decisions; it does not self-modify strategy automatically
- Correlation-derived lessons require caution and explicit confidence bounds
- Intervention review improves strategic accountability over time
- Forecast review enforces disciplined calibration of expectations
- Weak evidence must be flagged before adoption
- Human review is required before any institutional learning is operationalized
- No-execution guarantee: all learning outputs are advisory-only

This phase adds lesson extraction, intervention/forecast/assumption review APIs, persistence models/migration, tests, and the Institutional Learning Console.

## Phase 35 Ecosystem Intelligence and External Dependency Awareness

Phase 35 introduces ecosystem intelligence to map external dependencies and environmental pressures that influence platform reliability, research quality, and operator decision support.

Principles:
- External-awareness supports judgment; it does not automate decisions
- Dependency concentration increases systemic fragility and must be monitored
- Fallback planning should be explicit, reversible, and operator-reviewed
- Environmental pressure signals are uncertain and context-dependent
- Human review is required before fallback actions are adopted
- No-execution guarantee: ecosystem outputs are advisory-only

This phase adds dependency mapping, ecosystem risk scoring, fallback planning, environmental pressure detection, ecosystem memory, persistence models/migration, tests, and an Ecosystem Console.
