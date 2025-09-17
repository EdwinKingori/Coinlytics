import time
import django
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


def wait_for_db():
    db_conn = None
    while not db_conn:
        try:
            db_conn = connections['default']
            # Test the connection
            db_conn.cursor()
            print("Database available!")
            break
        except OperationalError as e:
            print(f'Database unavailable, waiting 2 seconds... ({e})')
            time.sleep(2)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Coinlytics.settings')
    django.setup()
    wait_for_db()
