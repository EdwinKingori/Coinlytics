from django.apps import AppConfig
import logging

# ✅ Hooking the startup and shutdown logging events
logger = logging.getLogger(__name__)


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        logger.info("🚀 API application started successfully.")
