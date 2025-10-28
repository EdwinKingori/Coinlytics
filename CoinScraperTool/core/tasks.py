import os
from datetime import datetime, timedelta
from django.utils import timezone
from celery import shared_task

LOG_FILE = "coinlytics_system.log"


# ✅ Deleting log enteries older than 5 days
@shared_task
def clean_old_logs():
    if not os.path.exists(LOG_FILE):
        return "No log file found."

    cutoff = timezone.now() - timedelta(days=5)
    new_lines = []

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                timestamp = datetime.strptime(line.split("]")[
                                              0].strip("["), "%Y-%m-%d %H:%M:%S")
                if timestamp > cutoff:
                    new_lines.append(line)
            except Exception:
                new_lines.append(line)

    with open(LOG_FILE, "w") as f:
        f.writelines(new_lines)

    return f"🧹 Logs older than 5 days deleted. Remaining entries: {len(new_lines)}"
