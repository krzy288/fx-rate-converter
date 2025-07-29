FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required for Chromium and Firefox
RUN apt-get update && apt-get install -y \
    curl \
    libglib2.0-0 \
    libnspr4 \
    libnss3 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libexpat1 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libasound2 \
    libatspi2.0-0 \
    libxcb-shm0 \
    libx11-xcb1 \
    libxcursor1 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libcairo-gobject2 \
    libfreetype6 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

#install dependencies
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install additional packages for HTTP testing
RUN pip install requests

# Install Chromium and Firefox browsers
RUN pip install playwright && playwright install chromium firefox

COPY ./tests ./tests
COPY conftest.py .
COPY pytest.ini .

ENV BASE_URL=http://localhost:8000
ENV ENV=dev

ENTRYPOINT ["sh", "-c", "sleep 100 && pytest -vv tests/e2e/ --html=playwright-report/report.html --self-contained-html"]
