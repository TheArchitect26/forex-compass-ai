"""Celery app + scheduled scanning."""
from celery import Celery
from celery.schedules import crontab
from app.config import settings

celery_app = Celery(
    "forex_ai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.jobs"],
)
celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule = {
    "scan-market-every-5min": {"task": "app.tasks.jobs.scan_market", "schedule": 300.0},
    "ingest-news-every-15min": {"task": "app.tasks.jobs.ingest_news", "schedule": 900.0},
    "retrain-daily": {"task": "app.tasks.jobs.retrain_ml", "schedule": crontab(hour=2, minute=0)},
}
