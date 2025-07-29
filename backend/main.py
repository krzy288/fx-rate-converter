from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import requests
from sqlalchemy import create_engine, text
from contextlib import asynccontextmanager
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


def create_history_table():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS conversion_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                from_currency VARCHAR(3),
                to_currency VARCHAR(3),
                amount FLOAT,
                rate FLOAT,
                converted FLOAT,
                date VARCHAR(20)
            )
        """))


# --- LIFESPAN CONTEXT ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_history_table()  # when app started
    print("App started, history table created if not exists")
    yield
    # opcjonalnie: zamykanie zasobów


app = FastAPI(lifespan=lifespan)

if os.getenv("ENV") == "prod":
    app.add_middleware(HTTPSRedirectMiddleware)


templates = Jinja2Templates(directory="templates")
#mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


#Database configuration
# LOCAL DEV
#DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://fxuser:fxpass@localhost:13306/fxdb")
# PROD ENV
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://fxuser:fxpass@db:3306/fxdb")
engine = create_engine(DATABASE_URL)

print(f"🌍 ENV: {os.getenv('ENV')}")





#create_history_table()


@app.get("/convert")
def convert(from_currency: str = Query(... , min_length=3 , max_length=3), 
            to_currency: str = Query(..., min_length=3, max_length=3), 
            amount: float = Query(..., gt=0)):
    
    url = f"https://api.frankfurter.app/latest"
    params = {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")   

    print(data)

    converted = data["rates"][to_currency.upper()]
    rate = converted / amount

    # Save to DB
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO conversion_history (from_currency, to_currency, amount, rate, converted, date) VALUES (:from_currency, :to_currency, :amount, :rate, :converted, :date)"),
            {
                "from_currency": data["base"],
                "to_currency": to_currency.upper(),
                "amount": amount,
                "rate": round(rate, 4),
                "converted": converted,
                "date": data["date"]
            }
        )

    print("Saving to DB:", data)

    return {
        "from": data["base"],
        "to": to_currency.upper(),
        "amount": amount,
        "rate": round(rate, 4),
        "converted": converted,
        "date": data["date"]
    }


@app.get("/health")
def health_check():
    """Health check endpoint for Docker health checks"""
    return {"status": "healthy"}

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT count(*) FROM conversion_history"))
            print(result)
            row = result.mappings().fetchone()
            return {"status": "Database connection successful !", "result": row}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/history")
def get_history():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM conversion_history ORDER BY id DESC"))
        #rows = [dict(row) for row in result]
        rows = result.mappings().all()
        print(rows)
    return rows