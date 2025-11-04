# 🚀 FastAPI + Celery + Redis Example

ตัวอย่างโปรเจกต์สาธิตการใช้งาน **FastAPI** ร่วมกับ **Celery** เพื่อรันงานแบบ asynchronous และ background task โดยใช้ **Redis** เป็น broker และ result backend พร้อม **Flower** สำหรับดูสถานะงาน

---

## 🧱 โครงสร้างโปรเจกต์

```
fastapi-celery/
├─ app/
│  ├─ main.py            # FastAPI endpoints
│  ├─ celery_app.py      # Celery instance and configuration
│  └─ tasks.py           # Celery tasks definition
├─ requirements.txt
├─ docker-compose.yml
├─ .env.example
└─ README.md
```

---

## ⚙️ การติดตั้งและใช้งาน

### 1. Clone โปรเจกต์

```bash
git clone https://github.com/your-org/fastapi-celery.git
cd fastapi-celery
```

### 2. ตั้งค่า Environment

คัดลอกไฟล์ตัวอย่าง `.env`

```bash
cp .env.example .env
```

ไฟล์ `.env`

```env
REDIS_URL=redis://redis:6379/0
CELERY_TIMEZONE=Asia/Bangkok
```

### 3. รันด้วย Docker Compose

```bash
docker compose up -d
```

ระบบจะเปิด:

- **FastAPI API** → [http://localhost:8000](http://localhost:8000)
- **Flower Dashboard** → [http://localhost:5555](http://localhost:5555)
- **Redis** → port 6379

---

## 🧩 การทดสอบ API

### ✅ ตรวจสอบสถานะระบบ

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

### ➕ สร้างงานบวกเลข

```bash
curl -sX POST http://localhost:8000/tasks/add \
     -H 'Content-Type: application/json' \
     -d '{"x": 10, "y": 5}'
# {"task_id": "<task-id>"}
```

### ⏳ สร้างงานที่ใช้เวลานาน

```bash
curl -sX POST http://localhost:8000/tasks/long \
     -H 'Content-Type: application/json' \
     -d '{"seconds": 10}'
# {"task_id": "<task-id>"}
```

### 🔍 ตรวจสอบสถานะของงาน

```bash
curl -s http://localhost:8000/tasks/<task-id>
```

### 📦 ดึงผลลัพธ์ของงาน

```bash
curl -s http://localhost:8000/tasks/<task-id>/result
```

---

## 🧠 ตัวอย่าง Periodic Task

ใน `app/celery_app.py` ได้ตั้งค่า periodic task ตัวอย่าง:

```python
celery.conf.beat_schedule = {
    "ping-every-30s": {
        "task": "app.tasks.ping",
        "schedule": 30.0,
    },
}
```

Celery Beat จะรันทุก 30 วินาที ส่งค่า `"pong"` เพื่อทดสอบระบบ

---

## 🧰 Flower Dashboard

Flower คือเครื่องมือดูสถานะงานของ Celery

เปิดได้ที่:
👉 [http://localhost:5555](http://localhost:5555)

จะแสดงข้อมูล:

- รายการ task ทั้งหมด
- Task progress/status
- Worker/Queue
- Retry count และ error logs

---

## 🛡️ ข้อควรพิจารณาใน Production

- ใช้ **RabbitMQ** เป็น broker สำหรับงานที่มีปริมาณมาก
- เปิดใช้ **acks_late** และ **retry** สำหรับงานที่อาจล้มเหลว
- ตั้งค่า **result_expires** เพื่อลดการใช้หน่วยความจำ Redis
- ใช้ **supervisor หรือ systemd** เพื่อดูแล worker processes
- เก็บ log ด้วย **structlog หรือ Prometheus exporter**

---

## 🧾 License

MIT License © 2025

---

ต้องการให้เพิ่มตัวอย่าง deployment บน **Kubernetes (Helm / manifest)** หรือ **ใช้ RabbitMQ แทน Redis** ไหม?
จะได้จัด README พร้อมไฟล์ให้ครบเซต.
