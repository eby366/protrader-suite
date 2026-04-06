from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aiohttp, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

@app.get("/")
def root():
    return {"status": "ProTrader Suite Backend OK"}

@app.get("/health")
def health():
    return {"status": "ok", "telegram": bool(TELEGRAM_TOKEN)}

@app.post("/telegram")
async def send_telegram(msg: dict):
    if not TELEGRAM_TOKEN:
        return {"ok": False, "error": "No token"}
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg.get("text", ""),
        "parse_mode": "HTML"
    }
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=payload) as r:
            data = await r.json()
            return data

@app.get("/football")
async def football_proxy(endpoint: str = "/matches?status=LIVE"):
    key = "bc6986fbad8d4a54af0e0f28b8022806"
    url = f"https://api.football-data.org/v4{endpoint}"
    async with aiohttp.ClientSession() as s:
        async with s.get(url, headers={"X-Auth-Token": key}) as r:
            return await r.json()
