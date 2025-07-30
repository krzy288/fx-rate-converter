# 💱 FX Converter - FastAPI DevOps Demo Project

A simple currency converter web app built with **FastAPI** and **Jinja2🐳 Job 2: Docker Compose Integration Test (needs: setup)
    ├── 📥 Checkout code
    ├── 🏗️ Build and run with Docker Compose (app + db + tests)
    ├── ⏳ Wait for app to start (5 attempts, 10s each)
    ├── 🧪 Test if app is live (curl /docs)
    ├── 💨 Run Smoke Tests
    │   ├── curl http://localhost:8000/
    │   ├── curl http://localhost:8000/db-check
    │   └── curl http://localhost:8000/history
    └── 🛑 Stop Docker containersing a modern frontend, persistent MySQL storage, and full CI/CD automation with **Docker** and **GitHub Actions**.

---

## 🚀 Features

- Python + FastAPI backend
- Modern, responsive frontend (HTML + CSS + JS, all static assets in `/static`)
- Currency conversion via [Frankfurter API](https://www.frankfurter.app/)
- Conversion history stored in MySQL (Dockerized)
- Swagger docs at `/docs`
- Dockerized app (multi-environment ready)
- **End-to-end testing with Playwright** (Firefox browser in Docker)
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

### Single Container
```bash
# Build the image
docker build -t fx-converter .

# Run the app (ensure MySQL is running and accessible)
docker run -p 8000:8000 fx-converter
```

### Full Stack with Docker Compose (Recommended)
```bash
# Start all services: app + database + tests
docker compose up --build -d

# Check container status
docker compose ps

# View test results (tests run automatically after 60s delay)
docker compose logs tests

# Run tests manually
docker compose exec tests pytest tests/e2e/ -v

# Stop all services
docker compose down
```

**Services in Docker Compose:**
- **app**: FastAPI backend (port 8000)
- **db**: MySQL database (port 13306)
- **tests**: Playwright e2e tests with Firefox browser

---

## ⚙️ CI/CD & Deployment

- All pushes to `master` trigger the GitHub Actions pipeline:
  - Lint & run unit tests
  - Build & integration test with Docker Compose (app + db + tests)
  - Deploy to AWS EC2 (via SSH, see `.github/workflows/ci.yml`)
- **Testing Strategy**: 
  - Unit tests run in GitHub Actions
  - Playwright e2e tests run in Docker with Firefox browser
  - Switched from Chromium to Firefox due to SSL protocol issues in containerized environment
- **Deployment Preparation**: The `scripts/prepare-deploy.sh` script optimizes the EC2 t3.micro instance:
  - Creates/configures 1GB swap file for memory management
  - Optimizes Docker configuration for production
  - Cleans up system resources and old Docker images
  - Applies memory optimizations for 1GB RAM constraint
  - Restarts services with production settings
- Deployment is fully automated, but requires manual hostname update in GitHub Actions after EC2 restart (no Elastic IP)

### 📋 CI/CD Flow Schema

```
📝 Code Push to `master` (or PR)
    ↓
🔍 GitHub Actions Trigger (.github/workflows/ci.yml)
    ↓
⚙️ Job 1: Environment Setup & Dependencies & Unit Tests
    ├── � Checkout code
    ├── 🐍 Set up Python 3.10
    ├── 📦 Install dependencies (backend/requirements.txt)
    └── � Run unit tests (pytest tests/unit --verbose)
        ↓
🐳 Job 2: Docker Compose Integration Test (needs: setup)
    ├── 📥 Checkout code
    ├── 🏗️ Build and run with Docker Compose
    ├── ⏳ Wait for app to start (5 attempts, 10s each)
    ├── � Test if app is live (curl /docs)
    ├── 💨 Run Smoke Tests
    │   ├── curl http://localhost:8000/
    │   ├── curl http://localhost:8000/db-check
    │   └── curl http://localhost:8000/history
    └── 🛑 Stop Docker containers
        ↓
� Job 3: Deploy to EC2 (needs: docker-build)
    ├── 📥 Checkout repo
    ├── � Set up SSH (keys, known_hosts)
    ├── � SSH to EC2 and Deploy:
    │   ├── 📦 git pull origin master
    │   ├── �️ Run optimize-and-cleanup.sh
    │   ├── 🛑 docker compose down
    │   ├── 🏗️ docker compose up --build -d
    │   └── ⏳ Wait 10s for containers
    └── 💨 Run EC2 Smoke Checks:
        ├── 🔄 5 attempts to reach localhost:8000
        ├── ✅ Test root endpoint
        ├── ✅ Test /db-check
        └── ✅ Test /history (optional)
            ↓
🎯 Live Application Running on EC2
    ├── 🌐 FastAPI Backend (Port 8000)
    ├── 🗄️ MySQL Database (Dockerized)
    ├── 🧪 Playwright Tests (Firefox, Dockerized)
    └── ✅ Smoke tests passed
```

**Manual Steps Required:**
- 🔧 Update EC2 hostname in GitHub Actions secrets after instance restart
- 🛠️ Run `prepare-deploy.sh` for system optimization (optional but recommended)

---

## 🖼️ Frontend & Testing

- All static assets (CSS, JS, images) are in `backend/static/`
- Main UI: `backend/templates/index.html`
- Modern, Playwright-friendly UI for automated testing
- **E2E Testing**: Comprehensive Playwright tests with Firefox browser
  - Homepage structure and functionality tests
  - Currency conversion workflow tests
  - Form validation and interaction tests
  - Test reports generated in `playwright-report/` directory

---

## 📝 TODO

- [x] ~~Cleanup Docker volumes on EC2~~ ✅ Implemented in `prepare-deploy.sh`
- [x] ~~System optimization for t3.micro~~ ✅ Memory and swap optimizations added
- [x] ~~Integrate Playwright tests into CI and CD~~ ✅ Docker Compose with Firefox browser
- [ ] Add Playwright tests to CI/CD pipeline (currently only in Docker Compose)
- [ ] Add more comprehensive Playwright test scenarios
- [ ] Improve error handling and UX
- [ ] Consider Elastic IP for stable deployment URL
- [ ] **Architecture Enhancement**: Add dedicated container for FX API service
  - Currently: Direct API calls to Frankfurter API from FastAPI backend
  - Future: Separate microservice container for currency conversion logic
  - Benefits: Better separation of concerns, independent scaling, API rate limiting
  - Implementation: 4th container (app + db + tests + fx-api-service)
- [ ] (Optional) Add user authentication

---

## 🧠 Brainstorming - Future Roadmap & Learning Opportunities

### 🚀 **Phase 1: Kubernetes Migration (Next Major Step)**
**Goal**: Transform from Docker Compose to production-ready Kubernetes cluster

**Learning Opportunities:**
- **Local Development**: 
  - Migrate to `minikube` or `kind` for local K8s development
  - Learn `kubectl`, Kubernetes manifests (YAML), and Helm charts
  - Implement ConfigMaps, Secrets, and persistent volumes
- **Container Orchestration**:
  - Create Deployments, Services, and Ingress controllers
  - Implement horizontal pod autoscaling (HPA)
  - Set up health checks, readiness/liveness probes
- **Service Mesh** (Advanced):
  - Integrate Istio for traffic management and observability
  - Implement circuit breakers and retry policies

### ☁️ **Phase 2: AWS Cloud-Native Architecture**
**Goal**: Leverage managed AWS services for scalability and reliability

**AWS Learning Path:**
- **Container Services**:
  - **EKS (Elastic Kubernetes Service)**: Managed Kubernetes cluster
  - **ECR (Elastic Container Registry)**: Private Docker image repository
  - **Fargate**: Serverless containers (alternative to EC2 nodes)
- **Database & Storage**:
  - **RDS**: Managed MySQL with automated backups, read replicas
  - **ElastiCache**: Redis for session storage and caching
  - **S3**: Static asset storage (CSS, JS, images)
- **Networking & Security**:
  - **ALB (Application Load Balancer)**: Traffic distribution with SSL termination
  - **Route 53**: DNS management and health checks
  - **VPC**: Secure network isolation with public/private subnets
  - **IAM**: Fine-grained access control and service roles

### 📊 **Phase 3: Observability & Monitoring Stack**
**Goal**: Production-grade monitoring, logging, and alerting

**Modern DevOps Tools:**
- **Metrics & Monitoring**:
  - **Prometheus**: Metrics collection and storage
  - **Grafana**: Dashboards and visualization
  - **CloudWatch**: AWS-native monitoring (logs, metrics, alarms)
- **Logging**:
  - **ELK Stack** (Elasticsearch, Logstash, Kibana) or **EFK** (Fluentd)
  - **AWS CloudWatch Logs**: Centralized log aggregation
- **Distributed Tracing**:
  - **Jaeger** or **AWS X-Ray**: Request tracing across microservices
- **Alerting**:
  - **AlertManager** (Prometheus) or **SNS** (AWS Simple Notification Service)

### 🔄 **Phase 4: Advanced CI/CD & GitOps**
**Goal**: Implement modern deployment strategies and automation

**CI/CD Evolution:**
- **GitOps Workflow**:
  - **ArgoCD** or **Flux**: Kubernetes-native GitOps deployment
  - **GitHub Actions** → **ECR** → **EKS** pipeline
- **Advanced Deployment Strategies**:
  - Blue-Green deployments
  - Canary releases with traffic splitting
  - Rolling updates with zero downtime
- **Security & Compliance**:
  - **Container scanning**: Trivy, Snyk, or AWS ECR vulnerability scanning
  - **SAST/DAST**: Static and dynamic security testing
  - **Policy as Code**: Open Policy Agent (OPA) for Kubernetes policies

### 🏗️ **Phase 5: Microservices Architecture**
**Goal**: Break monolith into independently scalable services

**Service Decomposition:**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway    │    │  Auth Service   │
│   (React/Vue)   │◄──►│   (Kong/Envoy)   │◄──►│   (OAuth2/JWT)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │ FX Service  │ │User Service │ │History Svc  │
            │  (Rates)    │ │(Profiles)   │ │(Analytics)  │
            └─────────────┘ └─────────────┘ └─────────────┘
```

### 🎯 **Phase 6: Advanced AWS & Cost Optimization**
**Goal**: Enterprise-grade architecture with cost efficiency

**Advanced AWS Services:**
- **Serverless Components**:
  - **Lambda**: Event-driven functions (webhooks, data processing)
  - **API Gateway**: Managed API with throttling and caching
  - **DynamoDB**: NoSQL for high-performance user sessions
- **Cost Optimization**:
  - **Spot Instances**: 70% cost reduction for non-critical workloads
  - **Reserved Instances**: Predictable workload cost savings
  - **AWS Cost Explorer**: Budget monitoring and optimization recommendations
- **Multi-Region Setup**:
  - **Cross-region replication**: Disaster recovery and global performance
  - **CloudFront CDN**: Global content distribution

### 💡 **Bonus Learning Tracks**

**Infrastructure as Code (IaC):**
- **Terraform**: Multi-cloud infrastructure provisioning
- **AWS CDK**: Type-safe infrastructure with Python/TypeScript
- **Pulumi**: Modern IaC with familiar programming languages

**Security & Compliance:**
- **AWS Security Hub**: Centralized security findings
- **AWS Config**: Resource compliance monitoring
- **Secrets management**: AWS Secrets Manager, HashiCorp Vault

**Performance & Scalability:**
- **Load testing**: k6, Artillery, or AWS Load Testing
- **Chaos engineering**: Chaos Monkey, Gremlin
- **Performance profiling**: Application Performance Monitoring (APM)

---

**🎓 Learning Value**: This roadmap covers the entire modern DevOps ecosystem from containerization to cloud-native architecture, providing hands-on experience with industry-standard tools and practices used by major tech companies.