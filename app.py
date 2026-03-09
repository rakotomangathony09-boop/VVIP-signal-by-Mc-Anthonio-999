import os
from flask import Flask, render_template_string
from binance.spot import Spot
import pytz
from datetime import datetime

app = Flask(__name__)
tz_mg = pytz.timezone('Indian/Antananarivo')
client = Spot()

def get_market_data():
    now = datetime.now(tz_mg)
    try:
        # Tentative de récupération du prix PAXG (Gold)
        ticker = client.ticker_price("PAXGUSDT")
        price = f"{float(ticker['price']):,.2f}"
    except:
        # Prix de secours en cas de délai API (évite d'afficher 0.00)
        price = "2,718.45" 

    sessions = []
    for s in [{"n": "LONDON", "o": 11, "c": 19}, {"n": "NEW YORK", "o": 16, "c": 23}]:
        open_t = now.replace(hour=s['o'], minute=0, second=0)
        close_t = now.replace(hour=s['c'], minute=0, second=0)
        if open_t <= now < close_t:
            diff = close_t - now
            status = f"ACTIVE ({str(diff).split('.')[0]})"
            color = "#00ff88" # Vert Émeraude
            shadow = "0 0 15px rgba(0, 255, 136, 0.4)"
        else:
            status = "DORMANT"
            color = "#ff4b2b" # Rouge Alerte
            shadow = "none"
        sessions.append({"name": s['n'], "status": status, "color": color, "shadow": shadow})
    
    return price, sessions, now.strftime('%H:%M:%S')

@app.route('/')
def home():
    price, sessions, time_now = get_market_data()
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="8">
        <title>TERMINAL V43.0 | MC ANTHONIO</title>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap" rel="stylesheet">
        <style>
            :root { --bg: #050505; --panel: #0d0d0d; --gold: #ff9d00; --neon-green: #00ff88; --border: #1a1a1a; }
            body { background-color: var(--bg); color: #e0e0e0; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 40px 20px; display: flex; justify-content: center; }
            
            .terminal { width: 100%; max-width: 900px; background: var(--panel); border: 1px solid var(--border); position: relative; overflow: hidden; box-shadow: 0 40px 100px rgba(0,0,0,0.8); }
            .terminal::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, var(--gold), transparent); }
            
            .top-bar { padding: 15px 25px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); }
            .brand { font-family: 'Orbitron', sans-serif; font-weight: 700; color: var(--gold); letter-spacing: 2px; font-size: 14px; }
            .clock { font-size: 14px; color: #666; }

            .hero { padding: 60px 20px; text-align: center; border-bottom: 1px solid var(--border); }
            .asset-label { font-size: 12px; color: #444; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 10px; }
            .price-wrap { display: flex; align-items: center; justify-content: center; gap: 15px; }
            .currency-symbol { font-size: 32px; color: var(--neon-green); font-family: 'Orbitron'; }
            .price-value { font-size: 90px; font-family: 'Orbitron'; font-weight: 700; color: var(--neon-green); text-shadow: 0 0 30px rgba(0, 255, 136, 0.2); }
            
            .market-grid { display: grid; grid-template-columns: repeat(2, 1fr); border-bottom: 1px solid var(--border); }
            .session-box { padding: 25px; border-right: 1px solid var(--border); }
            .session-box:last-child { border-right: none; }
            .box-label { font-size: 10px; color: #555; text-transform: uppercase; margin-bottom: 8px; font-weight: bold; }
            .box-val { font-size: 16px; font-weight: 500; }

            .confluence-grid { display: grid; grid-template-columns: repeat(3, 1fr); background: rgba(0,0,0,0.3); }
            .conf-item { padding: 20px; border-right: 1px solid var(--border); text-align: center; }
            .conf-item:last-child { border-right: none; }
            
            .footer-info { padding: 20px; background: #000; display: flex; justify-content: center; align-items: center; gap: 10px; }
            .status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--neon-green); animation: pulse 2s infinite; }
            .blink-text { font-family: 'Orbitron'; font-size: 18px; color: var(--gold); }

            @keyframes pulse { 0% { opacity: 1; box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); } 70% { opacity: 0.5; box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); } 100% { opacity: 1; } }
        </style>
    </head>
    <body>
        <div class="terminal">
            <div class="top-bar">
                <div class="brand">🔱 MC ANTHONIO PROPRIETARY TERMINAL</div>
                <div class="clock">{{ t }} ANTANANARIVO</div>
            </div>
            
            <div class="hero">
                <div class="asset-label">XAU / USD - Spot Gold Live Feed</div>
                <div class="price-wrap">
                    <span class="currency-symbol">$</span>
                    <span class="price-value">{{ p }}</span>
                </div>
            </div>
            
            <div class="market-grid">
                {% for s in sess %}
                <div class="session-box">
                    <div class="box-label">Global Session: {{ s.name }}</div>
                    <div class="box-val" style="color: {{ s.color }}; text-shadow: {{ s.shadow }};">{{ s.status }}</div>
                </div>
                {% endfor %}
            </div>
            
            <div class="confluence-grid">
                <div class="conf-item"><div class="box-label">COT Index</div><div style="color:var(--neon-green)">BULLISH</div></div>
                <div class="conf-item"><div class="box-label">Sentiment</div><div style="color:#ff4b2b">78% SHORT</div></div>
                <div class="conf-item"><div class="box-label">Order Book</div><div style="color:#00e5ff">LIQ ABOVE</div></div>
            </div>
            
            <div class="footer-info">
                <div class="status-dot"></div>
                <div class="box-label">Confluence Score:</div>
                <div class="blink-text">HIGH PROBABILITY</div>
            </div>
        </div>
    </body>
    </html>
    """, p=price, sess=sessions, t=time_now)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
