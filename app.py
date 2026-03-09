import os
import asyncio
from binance.spot import Spot
from telegram import Bot
from flask import Flask, render_template_string
from threading import Thread
import pytz
from datetime import datetime

# --- CONFIGURATION VVIP MC ANTHONIO ---
TOKEN = "8308151310:AAHsxCznCBHCXh0Zm0kKIWbBD7JM7byBk_4"
CHAT_ID = "-5062479701"
app = Flask(__name__)
bot = Bot(token=TOKEN)
tz_mg = pytz.timezone('Indian/Antananarivo')
client = Spot()

# Initialisation des données
market_view = {
    "price": "0.00",
    "cot": "BULLISH",
    "sentiment": "78% SHORT",
    "ob": "LIQ ABOVE",
    "score": "🔥 TRÈS HAUTE"
}

def get_market_data():
    try:
        ticker = client.ticker_price("PAXGUSDT")
        price = float(ticker['price'])
        market_view["price"] = f"{price:,.2f}"
        return price
    except: return 0.0

def get_sessions():
    now = datetime.now(tz_mg)
    sessions = [
        {"name": "LONDON", "open": 11, "close": 19},
        {"name": "NEW YORK", "open": 16, "close": 23}
    ]
    results = []
    for s in sessions:
        o = now.replace(hour=s['open'], minute=0, second=0)
        c = now.replace(hour=s['close'], minute=0, second=0)
        if o <= now < c:
            diff = c - now
            results.append({"name": s['name'], "status": f"OUVERT (Ferme dans {str(diff).split('.')[0]})", "color": "#00ff00"})
        else:
            status = "FERMÉ"
            if now < o:
                wait = o - now
                status = f"FERMÉ (Ouvre dans {str(wait).split('.')[0]})"
            results.append({"name": s['name'], "status": status, "color": "#ff3b3b"})
    return results

UI_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="5">
    <title>MC ANTHONIO TERMINAL</title>
    <style>
        body { background: #000; color: #fff; font-family: 'Courier New', monospace; padding: 20px; margin: 0; }
        .container { border: 2px solid #333; max-width: 800px; margin: auto; background: #050505; padding: 30px; }
        .header { color: #ff9d00; display: flex; justify-content: space-between; border-bottom: 1px solid #222; padding-bottom: 10px; }
        .price-hero { text-align: center; padding: 50px 0; }
        .price-val { font-size: 80px; color: #00ff00; font-weight: bold; text-shadow: 0 0 20px #00ff0044; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
        .card { border: 1px solid #222; padding: 15px; background: #000; }
        .label { font-size: 10px; color: #555; text-transform: uppercase; margin-bottom: 5px; }
        .val { font-size: 14px; font-weight: bold; }
        .blink { animation: blinker 1.5s linear infinite; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>🔱 MC ANTHONIO V43.0</div>
            <div>{{ time }} MG</div>
        </div>
        <div class="price-hero">
            <div class="label">XAU/USD BINANCE LIVE</div>
            <div class="price-val">$ {{ data.price }}</div>
        </div>
        <div class="grid">
            {% for s in sessions %}
            <div class="card">
                <div class="label">SESSION {{ s.name }}</div>
                <div class="val" style="color:{{ s.color }};">{{ s.status }}</div>
            </div>
            {% endfor %}
        </div>
        <div class="grid" style="grid-template-columns: 1fr 1fr 1fr;">
            <div class="card"><div class="label">1. COT</div><div class="val" style="color:#00ff00;">{{ data.cot }}</div></div>
            <div class="card"><div class="label">2. SENTIMENT</div><div class="val" style="color:#ff3b3b;">{{ data.sentiment }}</div></div>
            <div class="card"><div class="label">3. ORDER BOOK</div><div class="val" style="color:#00bcff;">{{ data.ob }}</div></div>
        </div>
        <div style="text-align:center; margin-top:30px; border-top: 1px solid #222; padding-top:20px;">
            <div class="label">CONFLUENCE SCORE</div>
            <div style="font-size:28px; color:#ff9d00;" class="blink">{{ data.score }}</div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    get_market_data()
    t = datetime.now(tz_mg).strftime('%H:%M:%S')
    return render_template_string(UI_TEMPLATE, data=market_view, sessions=get_sessions(), time=t)

async def main_bot():
    last_p = 0
    while True:
        p = get_market_data()
        # Logique de signal réel : Supprimé le test, attend la confluence
        await asyncio.sleep(60)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()
    asyncio.run(main_bot())
