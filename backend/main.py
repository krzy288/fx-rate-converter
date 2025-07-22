from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import requests


app = FastAPI()

templates = Jinja2Templates(directory="templates")

#mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

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