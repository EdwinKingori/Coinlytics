from django.apps import AppConfig
import logging


# ✅ Hooking the startup and shutdown logging events
logger = logging.getLogger(__name__)


class ScraperAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraper_app'

    def ready(self):
        logger.info("🌍 Scraper Web app started successfully.")
