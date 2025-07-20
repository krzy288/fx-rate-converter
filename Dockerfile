#dockerfile

from python:3.10-slim

workdir /app

copy backend/requirements.txt .

run pip install --no-cache-dir -r requirements.txt

copy backend/ .

expose 8000

cmd ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]