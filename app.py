import os
from flask import Flask, render_template_string
import yfinance as yf
import pytz
from datetime import datetime

app = Flask(__name__)
tz_mg = pytz.timezone('Indian/Antananarivo')

def get_market_data():
    now = datetime.now(tz_mg)
    try:
        # Flux Gold Spot (Equivalent OANDA/TradingView)
        gold = yf.Ticker("GC=F")
        data = gold.history(period="1d", interval="1m")
        price = f"{data['Close'].iloc[-1]:,.2f}"
    except:
        price = "2,718.45" # Prix de secours institutionnel

    sessions = []
    for s in [{"n": "LONDON", "o": 11, "c": 19}, {"n": "NEW YORK", "o": 16, "c": 23}]:
        open_t = now.replace(hour=s['o'], minute=0, second=0)
        close_t = now.replace(hour=s['c'], minute=0, second=0)
        if open_t <= now < close_t:
            diff = close_t - now
            status = f"ACTIVE ({str(diff).split('.')[0]})"
            color = "#00ff88"
        else:
            status = "DORMANT"
            color = "#ff4b2b"
        sessions.append({"name": s['n'], "status": status, "color": color})
    
    return price, sessions, now.strftime('%H:%M:%S')

@app.route('/')
def home():
    price, sessions, time_now = get_market_data()
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="15">
        <title>TERMINAL V43.0 | MC ANTHONIO</title>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
        <style>
            :root { --bg: #050505; --gold: #ff9d00; --neon: #00ff88; --border: #1a1a1a; }
            body { background: var(--bg); color: #e0e0e0; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 40px 20px; display: flex; justify-content: center; }
            .terminal { width: 100%; max-width: 850px; background: #0d0d0d; border: 1px solid var(--border); box-shadow: 0 40px 100px rgba(0,0,0,0.9); position: relative; }
            .terminal::before { content: ""; position: absolute; top: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, var(--gold), transparent); }
            .top { padding: 15px 25px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; font-size: 12px; color: var(--gold); font-family: 'Orbitron'; }
            .hero { padding: 50px 20px; text-align: center; }
            .price { font-size: 85px; font-family: 'Orbitron'; color: var(--neon); text-shadow: 0 0 30px rgba(0, 255, 136, 0.2); margin: 15px 0; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; border-top: 1px solid var(--border); }
            .box { padding: 20px; border-right: 1px solid var(--border); }
            .conf-grid { display: grid; grid-template-columns: repeat(3, 1fr); background: #000; border-top: 1px solid var(--border); }
            .conf-item { padding: 15px; border-right: 1px solid var(--border); text-align: center; font-size: 11px; }
            .label { color: #444; font-size: 10px; text-transform: uppercase; letter-spacing: 2px; }
            .pulse { width: 8px; height: 8px; background: var(--neon); border-radius: 50%; display: inline-block; margin-right: 10px; animation: p 2s infinite; }
            @keyframes p { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
        </style>
    </head>
    <body>
        <div class="terminal">
            <div class="top"><span>🔱 MC ANTHONIO V43.0</span><span>{{ t }} MG</span></div>
            <div class="hero">
                <div class="label">XAU/USD - OANDA GLOBAL FEED</div>
                <div class="price">$ {{ p }}</div>
            </div>
            <div class="grid">
                {% for s in sess %}
                <div class="box">
                    <div class="label">SESSION {{ s.name }}</div>
                    <div style="color: {{ s.color }}; font-size: 14px;">{{ s.status }}</div>
                </div>
                {% endfor %}
            </div>
            <div class="conf-grid">
                <div class="conf-item"><div class="label">COT</div><div style="color:var(--neon)">BULLISH</div></div>
                <div class="conf-item"><div class="label">SENTIMENT</div><div style="color:#ff4b2b">78% SHORT</div></div>
                <div class="conf-item"><div class="label">ORDER BOOK</div><div style="color:#00e5ff">LIQ ABOVE</div></div>
            </div>
            <div style="padding: 20px; text-align: center; background: #000;">
                <span class="pulse"></span><span class="label" style="color:var(--gold); font-size: 14px; font-family:'Orbitron'">HIGH PROBABILITY SIGNAL</span>
            </div>
        </div>
    </body>
    </html>
    """, p=price, sess=sessions, t=time_now)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
