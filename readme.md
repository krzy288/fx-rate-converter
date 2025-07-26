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

� **Deployed on AWS EC2** (t3.micro instance)

> **Note:** Since we're not using an Elastic IP, the public IP address changes when the EC2 instance restarts. The current deployment URL needs to be manually updated in GitHub Actions after each instance restart.

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
- **Deployment Preparation**: The `scripts/prepare-deploy.sh` script optimizes the EC2 t3.micro instance:
  - Creates/configures 1GB swap file for memory management
  - Optimizes Docker configuration for production
  - Cleans up system resources and old Docker images
  - Applies memory optimizations for 1GB RAM constraint
  - Restarts services with production settings
- Deployment is fully automated, but requires manual hostname update in GitHub Actions after EC2 restart (no Elastic IP)

---

## 🖼️ Frontend

- All static assets (CSS, JS, images) are in `backend/static/`
- Main UI: `backend/templates/index.html`
- Modern, Playwright-friendly UI for testing and learning

---

## 📝 TODO

- [x] ~~Cleanup Docker volumes on EC2~~ ✅ Implemented in `prepare-deploy.sh`
- [x] ~~System optimization for t3.micro~~ ✅ Memory and swap optimizations added
- [ ] Add more Playwright tests
- [ ] Improve error handling and UX
- [ ] Consider Elastic IP for stable deployment URL
- [ ] (Optional) Add user authentication