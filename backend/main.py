from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

#mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/convert")
def convert(from_currency: str = "EUR", to_currency: str = "USD", amount: float = 1.0):
    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "rate": 1.12,
        "converted": round(amount * 1.12 ,2)
    }


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})