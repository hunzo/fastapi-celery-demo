import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "Asia/Bangkok")

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks"],
)

# ค่าพื้นฐานที่ดีต่อ production เบื้องต้น
celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone=CELERY_TIMEZONE,
    enable_utc=True,
    task_track_started=True,
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# ตัวอย่าง periodic tasks (ต้องมี celery-beat)
celery.conf.beat_schedule = {
    "ping-every-30s": {
        "task": "app.tasks.ping",
        "schedule": 30.0,
        "args": (),
    },
}
