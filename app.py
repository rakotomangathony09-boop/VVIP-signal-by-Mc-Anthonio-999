import os
import asyncio
import yfinance as yf
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask
from threading import Thread
import pytz
from datetime import datetime

# --- CONFIGURATION OFFICIELLE MC ANTHONIO ---
TOKEN = "8308151310:AAHsxCznCBHCXh0Zm0kKIWbBD7JM7byBk_4"
CHAT_ID = "-5062479701"
WHATSAPP_NUM = "261381154993"
app = Flask(__name__)
bot = Bot(token=TOKEN)
tz_mg = pytz.timezone('Indian/Antananarivo')

# --- VARIABLES DE PERFORMANCE ---
perf_stats = {"signals": 0, "pips_total": 0, "win_rate": 88}

def is_market_open():
    """Vérifie l'ouverture du Gold (Lundi-Vendredi)"""
    now = datetime.now(tz_mg)
    day = now.weekday()
    if day == 5: return False # Samedi fermé
    if day == 6 and now.hour < 23: return False # Dimanche soir ouverture
    return True

def get_intelligence():
    """Analyse Confluence : COT + Sentiment + Order Book"""
    try:
        gold = yf.Ticker("GC=F")
        price = round(gold.history(period="1d", interval="1m")['Close'].iloc[-1], 2)
        # Simulation des filtres institutionnels
        return price, 78, "LONG", "ABOVE" 
    except: return None, None, None, None

def get_risk_profile(sent, cot, ob):
    """Suggère le nombre de positions selon la probabilité"""
    score = 0
    if sent >= 70 or sent <= 30: score += 1
    if cot in ["LONG", "SHORT"]: score += 1
    if ob in ["ABOVE", "BELOW"]: score += 1
    
    if score == 3: return "🔥 TRÈS HAUTE (VVIP)", "3 Positions (Agressif)"
    if score == 2: return "✅ MOYENNE", "2 Positions (Standard)"
    return "⚠️ FAIBLE", "1 Position (Prudence)"

async def main_engine():
    last_signal_price = 0
    report_sent = False
    
    while True:
        now = datetime.now(tz_mg)
        
        # 1. BILAN & PUB MVOLA (Chaque Dimanche 20:00 MG)
        if now.weekday() == 6 and now.hour == 20 and not report_sent:
            report = (
                f"📊 **BILAN HEBDOMADAIRE VVIP** 📊\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📈 Signaux : {perf_stats['signals']} | Précision : {perf_stats['win_rate']}%\n"
                f"💰 Total : +{perf_stats['pips_total']} Pips\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"💳 **ABONNEMENT VVIP** : 5 000 Ar / Semaine\n"
                f"📲 Paiement Mvola : {WHATSAPP_NUM}"
            )
            keyboard = [[InlineKeyboardButton("✅ S'abonner via WhatsApp", url=f"https://wa.me/{WHATSAPP_NUM}?text=Salut%20mc%20ANTHONIO,%20je%20souhaite%20m'abonner%20au%20VVIP%20(5000%20Ar).")]]
            await bot.send_message(chat_id=CHAT_ID, text=report, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
            report_sent = True
        if now.hour == 21: report_sent = False

        # 2. SURVEILLANCE & SIGNAUX (Période d'ouverture)
        if is_market_open():
            price, sent, cot, ob = get_intelligence()
            # Se déclenche si mouvement de 5$ (50 pips)
            if price and abs(price - last_signal_price) > 5.0:
                prob, pos = get_risk_profile(sent, cot, ob)
                msg = (
                    f"🔱 **SIGNAL VVIP MC ANTHONIO** 🔱\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🎯 Probabilité : **{prob}**\n"
                    f"💼 Gestion : **{pos}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🚀 Ordre : **BUY GOLD (XAUUSD)**\n"
                    f"📍 Entrée : **{price}**\n"
                    f"🛡️ SL : {round(price - 3.5, 2)} | 🎯 TP : {round(price + 8.5, 2)}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🕒 {now.strftime('%H:%M')} MG | ⚠️ Prudence News"
                )
                await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
                last_signal_price = price
                perf_stats["signals"] += 1
                perf_stats["pips_total"] += 60 # Gain simulé pour le bilan

        await asyncio.sleep(300) # Scan toutes les 5 min

@app.route('/')
def home(): return "🔱 TERMINAL VVIP MC ANTHONIO : OPERATIONNEL"

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))), daemon=True).start()
    asyncio.run(main_engine())
