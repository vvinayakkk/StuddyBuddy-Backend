# StuddyBuddy Backend

[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)](https://opensource.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Stack](https://img.shields.io/badge/Stack-Django%20%7C%20Celery%20%7C%20Postgres%20%7C%20Redis%20%7C%20MinIO%20%7C%20Prometheus-blue)]()

---

## 📚 Project Overview
StuddyBuddy is a scalable, production-ready, fully open source backend for a collaborative study platform. It provides robust APIs for user management, notes, test series, todo lists, resources, chat, and analytics, all built with Django and Django REST Framework.

---

## 🚀 Features
- **User Authentication & Roles**: JWT-based, student/senior roles, profile management
- **Notes**: CRUD, sharing, rich text, drawing, search, pagination
- **Test Series**: Test creation, analytics, sharing, search, pagination
- **Todo List**: Assignments, self-study, CRUD, search, pagination
- **Resources**: List, search, pagination, filtering
- **PDF Chatbot**: PDF upload, Q&A, chat
- **Connections**: Friend requests, friends list, video call, chat
- **Admin/Analytics**: User stats, deactivation/reactivation, GDPR export
- **Health Checks**: Global and per-app
- **OpenAPI/Swagger Docs**: Auto-generated API documentation
- **Background Jobs**: Celery with Redis
- **Object Storage**: MinIO (S3-compatible)
- **Metrics & Monitoring**: Prometheus metrics endpoint
- **Dockerized**: One-command setup for all services
- **100% Free & Open Source**: No paid dependencies

---

## 🛠️ Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **Object Storage**: MinIO (S3-compatible)
- **Background Jobs**: Celery
- **API Docs**: drf-yasg (Swagger/OpenAPI)
- **Metrics**: Prometheus, prometheus-django
- **Containerization**: Docker, docker-compose
- **Process Management**: Supervisor
- **Testing**: pytest, Django test runner

---

## 📦 Setup & Installation

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd suddy-buddu/StuddyBuddy-Backend/server/studybuddy
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your secrets/config:
```sh
cp .env.example .env
# Edit .env with your preferred editor and set all required values
```

### 3. Build & Run All Services (Docker Compose)
```sh
docker-compose up --build
```
This will start:
- Django API (Gunicorn)
- Celery worker & beat
- PostgreSQL
- Redis
- MinIO (S3-compatible object storage)
- Prometheus (metrics)

### 4. Access Services
- **API**: http://localhost:8000/
- **Swagger Docs**: http://localhost:8000/swagger/
- **Prometheus Metrics**: http://localhost:8000/metrics/
- **Prometheus UI**: http://localhost:9090/
- **MinIO Console**: http://localhost:9001/ (user/pass: minioadmin)

---

## ⚙️ Environment Variables
See `.env.example` for all required variables. Key settings:
- **Database**: `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`, `DJANGO_DB_HOST`, `DJANGO_DB_PORT`
- **MinIO**: `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET_NAME`, `MINIO_USE_SSL`
- **Celery**: `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- **Prometheus**: `PROMETHEUS_METRICS_EXPORT_PORT`
- **Email**: SMTP settings for password reset/verification
- **CORS**: `DJANGO_CORS_ALLOWED_ORIGINS`

---

## 🗂️ Project Structure
```
StuddyBuddy-Backend/
  server/
    studybuddy/
      ├── authentication/   # User, auth, admin endpoints
      ├── connections/      # Friends, chat, video call
      ├── notes/            # Notes CRUD, sharing
      ├── pdfchatbot/       # PDF Q&A
      ├── resources/        # Resource listing
      ├── testseries/       # Test series, analytics
      ├── todolist/         # Assignments, self-study
      ├── models/           # ML models (if any)
      ├── faiss_index/      # Vector index (if any)
      ├── manage.py
      ├── requirements.txt
      ├── Dockerfile
      ├── docker-compose.yml
      ├── supervisord.conf
      ├── prometheus.yml
      ├── .env.example
      └── README.md
```

---

## 🐳 Docker & Process Management
- **Docker Compose**: Orchestrates all services
- **Supervisor**: Runs Gunicorn, Celery worker, and Celery beat in one container
- **Volumes**: Static/media, DB, MinIO data are persisted

---

## ☁️ Object Storage (MinIO)
- MinIO is used for all static/media file storage
- Access MinIO console at http://localhost:9001/ (minioadmin/minioadmin)
- Configure Django to use MinIO via `.env` and `django-storages`

---

## 🏃 Background Jobs (Celery)
- Celery is auto-configured with Redis as broker and backend
- Add your background tasks in any app's `tasks.py`
- Celery worker and beat are managed by Supervisor

---

## 📊 Monitoring & Metrics (Prometheus)
- Prometheus scrapes Django metrics at `/metrics/`
- Prometheus UI at http://localhost:9090/
- Add custom metrics using `prometheus-django` if needed

---

## 📖 API Documentation
- **Swagger UI**: http://localhost:8000/swagger/
- **Redoc**: http://localhost:8000/redoc/
- All endpoints are versioned under `/api/v1/`

---

## 🧪 Testing
- Run tests with:
```sh
docker-compose exec web pytest
```
- Test skeletons are provided for all major apps

---

## 👩‍💻 Development
- Use Docker for local development
- Add new apps or endpoints as needed
- Use Celery for async/background jobs
- Use MinIO for all file uploads
- Use Prometheus for monitoring

---

## 🤝 Contributing
1. Fork the repo
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

---

## 📝 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 💬 Contact
For questions, issues, or contributions, open an issue or contact the maintainer. 