"""
ProTrader Suite v5 — Backend Render.com
Telegram alertes instantanées + Football-Data proxy + keepalive
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ProTrader Suite Backend")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN",   "8697142326:AAGXXMFO5hWjOyl0iTd1qULWDz1Qm8uiwt4")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "6420734593")
FOOTBALL_KEY     = os.getenv("FOOTBALL_DATA_KEY","bc6986fbad8d4a54af0e0f28b8022806")

class Msg(BaseModel):
    text: str

@app.get("/")
@app.head("/")
async def root():
    return {"status": "ok", "service": "ProTrader Suite v5"}

@app.get("/health")
@app.get("/ping")
async def health():
    return {"status": "ok", "telegram": bool(TELEGRAM_TOKEN), "football": bool(FOOTBALL_KEY)}

@app.post("/telegram")
async def send_telegram(msg: Msg):
    if not TELEGRAM_TOKEN:
        return {"ok": False, "error": "No token"}
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg.text, "parse_mode": "HTML"},
                              timeout=aiohttp.ClientTimeout(total=10)) as r:
                return await r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/football")
async def football(endpoint: str = "/matches?status=LIVE"):
    url = f"https://api.football-data.org/v4{endpoint}"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, headers={"X-Auth-Token": FOOTBALL_KEY},
                             timeout=aiohttp.ClientTimeout(total=10)) as r:
                return await r.json()
    except Exception as e:
        return {"error": str(e)}

@app.get("/football/live")
async def football_live():
    return await football("/matches?status=LIVE")

@app.get("/football/today")
async def football_today():
    from datetime import date
    d = date.today().isoformat()
    return await football(f"/matches?dateFrom={d}&dateTo={d}")

