from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import requests
from sqlalchemy import create_engine

app = FastAPI()

templates = Jinja2Templates(directory="templates")

#mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


#Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://fxuser:fxpass@db:3306/fxdb")
engine = create_engine(DATABASE_URL)


def create_history_table():
    with engine.connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversion_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                from_currency VARCHAR(3),
                to_currency VARCHAR(3),
                amount FLOAT,
                rate FLOAT,
                converted FLOAT,
                date VARCHAR(20)
            )
        """)
create_history_table()


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
    with engine.connect() as conn:
        conn.execute(
            "INSERT INTO conversion_history (from_currency, to_currency, amount, rate, converted, date) VALUES (%s, %s, %s, %s, %s, %s)",
            (data["base"], to_currency.upper(), amount, round(rate, 4), converted, data["date"])
        )

    return {
        "from": data["base"],
        "to": to_currency.upper(),
        "amount": amount,
        "rate": round(rate, 4),
        "converted": converted,
        "date": data["date"]
    }


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return {"status": "Database connection successful", "result": result.fetchone()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/history")
def get_history():
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM conversion_history ORDER BY id DESC LIMIT 10")
        rows = [dict(row) for row in result]
    return rows