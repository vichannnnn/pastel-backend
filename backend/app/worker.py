import os
from celery import Celery


celery_app = Celery(
    "tasks",
    include=["app.tasks.generate_pastel"],
)
celery_app.conf.timezone = "Asia/Singapore"

celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

celery_app.conf.beat_schedule = {
    "automated_generate_pastel_art_task": {
        "task": "automated_generate_pastel_art_task",
        "schedule": 90.0,
    },
}
