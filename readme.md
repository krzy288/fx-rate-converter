# 💱 FX Converter - FastAPI DevOps Demo Project

A simple backend service built with **FastAPI**, containerized with **Docker**, and designed to be CI/CD-ready with **GitHub Actions**.

---

## 🚀 Features

- Python + FastAPI backend
- Jinja2-rendered welcome page at `/`
- Swagger docs at `/docs`
- Dockerized app
- CI/CD pipeline via GitHub Actions
- Future: AWS deployment (App Runner / ECS)

---

## 🧪 Local Development

```bash
# Create and activate venv
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


Visit:

http://localhost:8000 → Welcome Page

http://localhost:8000/docs → Swagger UI


# Build image
docker build -t fx-converter .

# Run container
docker run -p 8000:8000 fx-converter
