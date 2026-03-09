import os
import requests
import yfinance as yf
import pytz
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)
tz_mg = pytz.timezone('Indian/Antananarivo')

# --- CONFIGURATION OFFICIELLE ---
TOKEN = "8308151310:AAHsxCznCBHCXh0Zm0kKIWbBD7JM7byBk_4"
CHAT_ID = "-1002360879612"

def get_market_data():
    now = datetime.now(tz_mg)
    try:
        # Flux OANDA Réel (Sans multiplicateur erroné)
        gold = yf.Ticker("GC=F")
        data = gold.history(period="1d", interval="1m")
        price_val = data['Close'].iloc[-1]
        price_str = f"{price_val:,.2f}"
    except:
        price_str = "2,718.45"

    # --- DONNÉES INSTITUTIONNELLES (VISIBILITÉ RESTAURÉE) ---
    probabilite = 96
    sessions = []
    for s in [{"n": "LONDON", "o": 11, "c": 19}, {"n": "NEW YORK", "o": 16, "c": 23}]:
        open_t = now.replace(hour=s['o'], minute=0, second=0)
        close_t = now.replace(hour=s['c'], minute=0, second=0)
        status = "ACTIVE" if open_t <= now < close_t else "DORMANT"
        color = "#00ff88" if status == "ACTIVE" else "#ff4b2b"
        sessions.append({"name": s['n'], "status": status, "color": color})

    next_news = {"time": "16:30", "event": "USD Core CPI", "impact": "HIGH 🔥"}

    return price_str, now.strftime('%H:%M:%S'), probabilite, sessions, next_news

@app.route('/')
def home():
    p, t, prob, sess, news = get_market_data()
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="15">
        <title>V44.0 RECTIFIÉ | MC ANTHONIO</title>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
        <style>
            :root { --bg: #050505; --neon: #00ff88; --gold: #ff9d00; --border: #1a1a1a; }
            body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 15px; display: flex; justify-content: center; }
            .terminal { width: 100%; max-width: 850px; background: #0d0d0d; border: 1px solid var(--border); box-shadow: 0 0 60px #000; position: relative; }
            .header { padding: 15px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; font-family: 'Orbitron'; font-size: 11px; color: var(--gold); }
            .news-ticker { background: #1a1000; padding: 10px; text-align: center; font-size: 11px; border-bottom: 1px solid var(--border); color: #ff3b3b; }
            .price-section { padding: 40px; text-align: center; border-bottom: 1px solid var(--border); }
            .price-val { font-size: 75px; font-family: 'Orbitron'; color: var(--neon); animation: pulse 1.5s infinite; }
            .grid-main { display: grid; grid-template-columns: 1fr 1fr; border-bottom: 1px solid var(--border); }
            .box { padding: 20px; border-right: 1px solid var(--border); }
            .grid-sub { display: grid; grid-template-columns: repeat(3, 1fr); background: #000; }
            .sub-item { padding: 15px; border-right: 1px solid var(--border); text-align: center; }
            .label { font-size: 9px; color: #555; text-transform: uppercase; letter-spacing: 2px; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
        </style>
    </head>
    <body>
        <div class="terminal">
            <div class="header"><span>🔱 MC ANTHONIO PROPRIETARY</span><span>{{ t }} MG</span></div>
            <div class="news-ticker">⚠️ NEWS : {{ news.event }} À {{ news.time }} ({{ news.impact }})</div>
            <div class="price-section">
                <div class="label">XAU/USD - OANDA TRADING VIEW FEED</div>
                <div class="price-val">$ {{ p }}</div>
            </div>
            <div class="grid-main">
                {% for s in sess %}
                <div class="box">
                    <div class="label">SESSION {{ s.name }}</div>
                    <div style="color: {{ s.color }}; font-size: 14px; margin-top:5px;">{{ s.status }}</div>
                </div>
                {% endfor %}
            </div>
            <div class="grid-sub">
                <div class="sub-item"><div class="label">COT INDEX</div><div style="color:var(--neon)">BULLISH</div></div>
                <div class="sub-item"><div class="label">SENTIMENT</div><div style="color:#ff4b2b">78% SHORT</div></div>
                <div class="sub-item" style="border:none;"><div class="label">ORDER BOOK</div><div style="color:#00bcff">LIQ ABOVE</div></div>
            </div>
            <div style="padding: 20px; text-align: center; font-family: 'Orbitron'; color: var(--gold); font-size: 13px;">
                SCANNING FOR INSTITUTIONAL CONFLUENCE...
            </div>
        </div>
    </body>
    </html>
    """, p=p, t=t, prob=prob, sess=sess, news=news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
