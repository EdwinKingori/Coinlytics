import logging
from datetime import datetime
from django.utils import timezone
from django.apps import apps
from django.core.signals import request_started, request_finished
from django.db.backends.signals import connection_created

LOG_FILE = "coinlytics_system.log"


# Configuring root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Creating a file handler for app-wide logging
file_handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# ✅ Registering request lifecycle signals (logs every web and API requests)
def log_request_started(sender, environ, **kwargs):
    logger.info(" Request started: %s %s", environ.get(
        "REQUEST_METHOD"), environ.get("PATH_INFO"))


def log_request_completed(sender, **kwargs):
    logger.info("Request completed successfully")


request_started.connect(log_request_started)
request_finished.connect(log_request_completed)

# ✅ Logging database connection


def log_db_connection(sender, connection, **kwargs):
    logger.info("Database connected: %s", connection.settings_dict.get("NAME"))


connection_created.connect(log_db_connection)

logger.info("🟢 Logging system initialized at %s", timezone.now())
