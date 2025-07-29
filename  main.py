from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import time
import hmac
import hashlib
import base64

app = FastAPI()

SECRET = "super-secret-token"  # podés cambiarlo por una variable de entorno

def generate_token(id_farm: str, expiry_hours: int = 12) -> str:
    expiry_time = int(time.time()) + expiry_hours * 3600
    message = f"{id_farm}:{expiry_time}"
    signature = hmac.new(SECRET.encode(), message.encode(), hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(f"{message}:{signature.hex()}".encode()).decode()
    return token

@app.get("/generate-url")
def generate_url(id_farm: str = Query(...)):
    token = generate_token(id_farm)
    full_url = f"https://www.forms.example.com/{id_farm}/decla1?token={token}"
    return JSONResponse({"url": full_url})
