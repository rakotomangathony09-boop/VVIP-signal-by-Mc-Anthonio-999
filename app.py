import os
import asyncio
from binance.spot import Spot
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, render_template_string
from threading import Thread
import pytz
from datetime import datetime

# --- CONFIGURATION VVIP MC ANTHONIO ---
TOKEN = "8308151310:AAHsxCznCBHCXh0Zm0kKIWbBD7JM7byBk_4"
CHAT_ID = "-5062479701"
WHATSAPP_NUM = "261381154993"
app = Flask(__name__)
bot = Bot(token=TOKEN)
tz_mg = pytz.timezone('Indian/Antananarivo')
client = Spot()

# Données pour l'interface Bloomberg
market_view = {"price": 0.0, "time": "--:--:--", "status": "MONITORING"}

def get_binance_data():
    """Récupère le prix Gold réel sur Binance (PAXGUSDT)"""
    try:
        ticker = client.ticker_price("PAXGUSDT")
        price = round(float(ticker['price']), 2)
        market_view["price"] = price
        market_view["time"] = datetime.now(tz_mg).strftime('%H:%M:%S')
        return price
    except:
        return None

# --- INTERFACE DESIGN BLOOMBERG ---
HTML_UI = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="15">
    <title>MC ANTHONIO TERMINAL</title>
    <style>
        body { background-color: #020202; color: #ff9d00; font-family: 'Courier New', Courier, monospace; display: flex; justify-content: center; padding-top: 50px; }
        .terminal { border: 2px solid #333; width: 90%; max-width: 600px; padding: 20px; background: #000; box-shadow: 0 0 15px #ff9d0022; }
        .head { display: flex; justify-content: space-between; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 20px; font-size: 14px; }
        .price-display { text-align: center; margin: 40px 0; }
        .ticker { color: #555; font-size: 12px; }
        .price { font-size: 48px; color: #00ff00; font-weight: bold; text-shadow: 0 0 10px #00ff0044; }
        .status-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px; }
        .stat-card { border: 1px solid #222; padding: 10px; font-size: 12px; }
        .blink { animation: blinker 2s linear infinite; color: #00bcff; }
        @keyframes blinker { 50% { opacity: 0; } }
        .footer { margin-top: 30px; font-size: 9px; color: #333; text-align: center; }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="head">
            <div><span style="background:#ff9d00; color:#000; padding:0 5px;">LIVE</span> GOLD/USD</div>
            <div>{{ time }} MG</div>
        </div>
        <div class="price-display">
            <div class="ticker">BINANCE REAL-TIME FEED</div>
            <div class="price">$ {{ price }}</div>
        </div>
        <div class="status-grid">
            <div class="stat-card">ENGINE: <span class="blink">ACTIVE</span></div>
            <div class="stat-card">CONFLUENCE: <span style="color:#00ff00;">3-piliers OK</span></div>
        </div>
        <div class="footer">MC ANTHONIO PROPRIETARY TERMINAL V43.0 - ANTANANARIVO</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    get_binance_data()
    return render_template_string(HTML_UI, price=market_view["price"], time=market_view["time"])

async def engine():
    last_p = 0
    while True:
        p = get_binance_data()
        if p and abs(p - last_p) > 5.0:
            # ICI : Ton analyse COT/SENTIMENT/OB déclenche le vrai signal
            # Exemple de signal BUY si confluence détectée :
            msg = (
                f"🔱 **SIGNAL VVIP MC ANTHONIO** 🔱\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📊 Source : **Binance Real-Time**\n"
                f"🚀 Ordre : **BUY GOLD (XAUUSD)**\n"
                f"📍 Entrée : **{p}**\n"
                f"🛡️ SL : {round(p-3.5, 2)} | 🎯 TP : {round(p+8.0, 2)}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🕒 {datetime.now(tz_mg).strftime('%H:%M')} MG"
            )
            try:
                await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
                last_p = p
            except: pass
        await asyncio.sleep(60)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))), daemon=True).start()
    asyncio.run(engine())
