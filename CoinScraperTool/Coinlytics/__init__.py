import logging
from datetime import datetime
from django.core.signals import request_finished
from django.apps import apps
from .celery import app as celery_app

# ✅ Loading Celery app on django startup
__all__ = ['celery_app']


logger = logging.getLogger(__name__)


def on_startup():
    logger.info(
        "🟢 Django application (Coinlytics) startup complete at %s", datetime.utcnow())


def on_shutdown(**kwargs):
    logger.info("🔴 Django application shutdown detected at %s",
                datetime.utcnow())


on_startup()
request_finished.connect(on_shutdown)
