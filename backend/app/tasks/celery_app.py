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
    "auto-training-due-check-every-minute": {"task": "app.tasks.jobs.auto_train_signals", "schedule": 60.0},
    "validate-outcomes-every-10min": {"task": "app.tasks.jobs.validate_outcomes", "schedule": 600.0},
    "reliability-snapshot-every-30min": {"task": "app.tasks.jobs.snapshot_reliability", "schedule": 1800.0},
    "maintenance-every-hour": {"task": "app.tasks.jobs.run_maintenance", "schedule": 3600.0},
    "ingest-news-every-15min": {"task": "app.tasks.jobs.ingest_news", "schedule": 900.0},
    "retrain-daily": {"task": "app.tasks.jobs.retrain_ml", "schedule": crontab(hour=2, minute=0)},
}
