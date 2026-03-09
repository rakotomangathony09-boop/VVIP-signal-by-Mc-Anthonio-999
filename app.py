import os
from flask import Flask, render_template_string
from binance.spot import Spot
import pytz
from datetime import datetime

app = Flask(__name__)
tz_mg = pytz.timezone('Indian/Antananarivo')
# Flux Binance Public
client = Spot()

def get_market_data():
    now = datetime.now(tz_mg)
    try:
        # Récupération directe du prix Or sur Binance
        ticker = client.ticker_price("PAXGUSDT")
        price = f"{float(ticker['price']):,.2f}"
    except:
        price = "SYNCHRONISATION..."

    # Calcul des sessions avec compte à rebours
    sessions = []
    for s in [{"n": "LONDON", "o": 11, "c": 19}, {"n": "NEW YORK", "o": 16, "c": 23}]:
        open_t = now.replace(hour=s['o'], minute=0, second=0)
        close_t = now.replace(hour=s['c'], minute=0, second=0)
        
        if open_t <= now < close_t:
            diff = close_t - now
            status = f"OUVERT (Ferme dans {str(diff).split('.')[0]})"
            color = "#00ff00"
        else:
            if now < open_t:
                diff = open_t - now
                status = f"FERMÉ (Ouvre dans {str(diff).split('.')[0]})"
            else:
                status = "FERMÉ"
            color = "#ff3b3b"
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
        <meta http-equiv="refresh" content="10">
        <title>TERMINAL VVIP MC ANTHONIO</title>
        <style>
            body { background: #000; color: #fff; font-family: 'Courier New', monospace; padding: 20px; text-align: center; }
            .box { border: 1px solid #333; max-width: 750px; margin: auto; background: #050505; padding: 30px; box-shadow: 0 0 30px rgba(0,255,0,0.1); }
            .price { font-size: 80px; color: #00ff00; font-weight: bold; margin: 20px 0; text-shadow: 0 0 20px rgba(0,255,0,0.3); }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 25px; }
            .card { border: 1px solid #222; padding: 15px; background: #000; }
            .label { font-size: 10px; color: #555; text-transform: uppercase; margin-bottom: 5px; }
            .blink { animation: b 1.5s infinite; color: #ff9d00; font-size: 26px; font-weight: bold; }
            @keyframes b { 50% { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="box">
            <div style="color:#ff9d00; display:flex; justify-content:space-between; font-weight:bold;">
                <span>🔱 MC ANTHONIO V43.0</span><span>{{ t }} MG</span>
            </div>
            
            <div style="margin-top:40px; color:#555; font-size:10px; letter-spacing:2px;">XAU/USD BINANCE LIVE FEED (PAXG)</div>
            <div class="price">$ {{ p }}</div>
            
            <div class="grid">
                {% for s in sess %}
                <div class="card">
                    <div class="label">SESSION {{ s.name }}</div>
                    <div style="color:{{ s.color }}; font-size:13px; font-weight:bold;">{{ s.status }}</div>
                </div>
                {% endfor %}
            </div>
            
            <div class="grid" style="grid-template-columns: 1fr 1fr 1fr;">
                <div class="card"><div class="label">COT</div><div style="color:#0f0; font-weight:bold;">BULLISH</div></div>
                <div class="card"><div class="label">SENTIMENT</div><div style="color:#f33; font-weight:bold;">78% SHORT</div></div>
                <div class="card"><div class="label">ORDER BOOK</div><div style="color:#00bcff; font-weight:bold;">LIQ ABOVE</div></div>
            </div>
            
            <div style="margin-top:40px; border-top: 1px solid #222; padding-top:20px;">
                <div class="label" style="margin-bottom:10px;">CONFLUENCE SCORE</div>
                <div class="blink">🔥 TRÈS HAUTE</div>
            </div>
            
            <div style="margin-top:30px; font-size:9px; color:#222;">PROPRIETARY TRADING TERMINAL - ANTANANARIVO</div>
        </div>
    </body>
    </html>
    """, p=price, sess=sessions, t=time_now)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
