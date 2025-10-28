from celery import Celery
import os

# ✅ Setting the default django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Coinlytics.settings')


# ✅ Creating the celery app
app = Celery('Coinlytics')


# ✅ Loading settings with the celery_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')


# ✅ enbaling discover tasks in all installed apps
app.autodiscover_tasks()
