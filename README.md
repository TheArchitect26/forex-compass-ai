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
