from fastapi import FastAPI

app = FastAPI()

@app.get("/convert")
def convert(from_currency: str = "EUR", to_currency: str = "USD", amount: float = 1.0):
    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "rate": 1.12,
        "converted": round(amount * 1.12 ,2)
    }