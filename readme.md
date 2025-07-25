# 💱 FX Converter - FastAPI DevOps Demo Project

A simple currency converter web app built with **FastAPI** and **Jinja2**, featuring a modern frontend, persistent MySQL storage, and full CI/CD automation with **Docker** and **GitHub Actions**.

---

## 🚀 Features

- Python + FastAPI backend
- Modern, responsive frontend (HTML + CSS + JS, all static assets in `/static`)
- Currency conversion via [Frankfurter API](https://www.frankfurter.app/)
- Conversion history stored in MySQL (Dockerized)
- Swagger docs at `/docs`
- Dockerized app (multi-environment ready)
- CI/CD pipeline via GitHub Actions (see `.github/workflows/ci.yml`)
- Automated deployment to AWS EC2

---

## 🌐 Live Demo

👉 [Live App URL](http://13.49.14.187:8000/)  
📄 [Swagger/OpenAPI docs](http://13.49.14.187:8000/docs)

> If the app is not working, the EC2 instance may be turned off for cost reasons.

---

## 🧑‍💻 Local Development

```bash
# 1. Clone the repo and enter the backend directory
git clone https://github.com/krzy288/fx-rate-converter.git
cd fx-rate-converter/backend

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app (default: local MySQL, see main.py for DB config)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Visit:
#   http://localhost:8000         (Frontend UI)
#   http://localhost:8000/docs    (Swagger UI)
```

---

## 🐳 Docker Usage

```bash
# Build the image
docker build -t fx-converter .

# Run the app (ensure MySQL is running and accessible)
docker run -p 8000:8000 fx-converter

# Or use Docker Compose for full stack (backend + db)
docker compose -f docker-compose.yaml up --build
```

---

## ⚙️ CI/CD & Deployment

- All pushes to `master` trigger the GitHub Actions pipeline:
  - Lint & run unit tests
  - Build & integration test with Docker Compose
  - Deploy to AWS EC2 (via SSH, see `.github/workflows/ci.yml`)
- Deployment is fully automated. See workflow file for details.

---

## 🖼️ Frontend

- All static assets (CSS, JS, images) are in `backend/static/`
- Main UI: `backend/templates/index.html`
- Modern, Playwright-friendly UI for testing and learning

---

## 📝 TODO

- [ ] Cleanup Docker volumes on EC2
- [ ] Add more Playwright tests
- [ ] Improve error handling and UX
- [ ] (Optional) Add user authentication