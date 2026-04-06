from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp, os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

TG_TOKEN   = os.getenv("TELEGRAM_TOKEN",   "8697142326:AAGXXMFO5hWjOyl0iTd1qULWDz1Qm8uiwt4")
TG_CHAT    = os.getenv("TELEGRAM_CHAT_ID", "6420734593")
FD_KEY     = os.getenv("FOOTBALL_DATA_KEY","bc6986fbad8d4a54af0e0f28b8022806")

class Msg(BaseModel):
    text: str

@app.get("/")
@app.head("/")
@app.get("/health")
@app.get("/ping")
async def health():
    return {"status": "ok", "telegram": bool(TG_TOKEN), "football": bool(FD_KEY)}

@app.post("/telegram")
async def telegram(msg: Msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(url, json={"chat_id": TG_CHAT, "text": msg.text, "parse_mode": "HTML"},
                              timeout=aiohttp.ClientTimeout(total=10)) as r:
                return await r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/football")
async def football(endpoint: str = "/matches?status=LIVE"):
    url = f"https://api.football-data.org/v4{endpoint}"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, headers={"X-Auth-Token": FD_KEY},
                             timeout=aiohttp.ClientTimeout(total=10)) as r:
                return await r.json()
    except Exception as e:
        return {"error": str(e)}

@app.get("/football/live")
async def live():
    return await football("/matches?status=LIVE")

@app.get("/football/today")
async def today():
    from datetime import date
    d = date.today().isoformat()
    return await football(f"/matches?dateFrom={d}&dateTo={d}")
