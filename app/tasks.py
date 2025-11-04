import time
from celery import states
from celery.exceptions import Ignore
from app.celery_app import celery


@celery.task(name="app.tasks.add")
def add(x: int, y: int) -> int:
    return x + y


@celery.task(bind=True, name="app.tasks.long_task", autoretry_for=(RuntimeError,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def long_task(self, seconds: int = 10) -> str:
    """งานยาว พร้อม auto-retry แบบ exponential backoff เมื่อเจอ RuntimeError"""
    if seconds < 0:
        # invalid input -> fail hard, ไม่ retry
        self.update_state(state=states.FAILURE, meta={
                          "reason": "seconds must be >= 0"})
        raise Ignore()
    # ตัวอย่างสุ่ม error รอบแรกๆ เพื่อเดโม retry
    if seconds > 5 and self.request.retries == 0:
        raise RuntimeError("Simulated transient failure")
    for i in range(seconds):
        time.sleep(1)
        self.update_state(state="PROGRESS", meta={
                          "elapsed": i + 1, "total": seconds})
    return f"slept {seconds}s"


@celery.task(name="app.tasks.ping")
def ping() -> str:
    return "pong"
