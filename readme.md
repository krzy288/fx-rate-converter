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
- external api for rates

---


## 🚀 Deployment Info
The FX Rate Converter app is currently deployed on an AWS EC2 instance:

!!! If not working - then EC2 is turned off due to cost reduction !!!

👉 Live App URL

http://13.49.14.187:8000/

📄 Swagger/OpenAPI documentation available at:
http://13.49.14.187:8000/docs

The backend is powered by FastAPI and runs inside a Docker container. Deployment is fully automated via GitHub Actions and runs on a t3.micro EC2 instance under the AWS Free Tier.




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


#todo
- add db mysql 
- docker compose
- new apis