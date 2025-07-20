import os
import matplotlib.pyplot as plt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = os.getenv("BOT_TOKEN")
OWNER_IDS = list(map(int, os.getenv("OWNER_IDS", "1349917110").split(",")))
TARGET = float(os.getenv("TARGET_EUR", "100").replace(",", "."))
VIP_GROUP_LINK = os.getenv("VIP_GROUP_LINK", "https://t.me/+EXAMPLE")

app = Application.builder().token(TOKEN).build()
scheduler = BackgroundScheduler()
scheduler.start()

def generate_progress_chart(current, target):
    percent = min(100, current / target * 100)
    fig, ax = plt.subplots(figsize=(5, 1))
    ax.barh([""], [percent], color="#4CAF50")
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_facecolor("none")
    for spine in ax.spines.values():
        spine.set_visible(False)
    path = "/tmp/progress_chart.png"
    plt.savefig(path, bbox_inches='tight', transparent=True)
    plt.close()
    return path

# Forecast anzeigen
async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current = float(os.getenv("TOTAL_PROFIT", "0").replace(",", "."))
    snipes = int(os.getenv("SNIPES_TODAY", "0"))
    wins = int(os.getenv("WINS_TODAY", "0"))
    sniper_profit = float(os.getenv("SNIPER_PROFIT", "0").replace(",", "."))

    percent = min(100, int(current / TARGET * 100))
    blocks = int(percent / 10)
    bar = "█" * blocks + "░" * (10 - blocks)
    status = "✅ Ziel erreicht!" if current >= TARGET else "❌ Noch nicht erreicht"

    if user_id in OWNER_IDS:
        text = f"""📈 Forecast-Modul:
Tagesziel: {TARGET:.2f} €
Aktuell: {current:.2f} €
Fortschritt: [{bar}] {percent} %

📌 SniperBot heute:
Snipes: {snipes} | Treffer: {wins}
Gewinn: +{sniper_profit:.2f} €

Status: {status}"""

        keyboard = [[
            InlineKeyboardButton("🔄 Aktualisieren", callback_data="forecast")
        ], [
            InlineKeyboardButton("🤖 SniperBot-Status", callback_data="sniper")
        ], [
            InlineKeyboardButton("📅 Monats-Forecast", callback_data="monthly_forecast")
        ], [
            InlineKeyboardButton("📄 Forecast-PDF", callback_data="download_pdf")
        ], [
            InlineKeyboardButton("💰 HypoCoin", callback_data="hypocoin")
        ]]
    else:
        text = f"""📈 Öffentliche Vorschau:
Tagesziel: 100 €
Aktuell: {current:.2f} €
Fortschritt: [{bar}] {percent} %

💡 Hol dir den Vollzugang über crypto-tec.xyz"""
        keyboard = [[
            InlineKeyboardButton("🌐 Webseite öffnen", url="https://crypto-tec.xyz")
        ], [
            InlineKeyboardButton("🎟️ VIP-Zugang sichern", url=VIP_GROUP_LINK)
        ]]

    path = generate_progress_chart(current, TARGET)

    if update.callback_query:
        await update.callback_query.answer()
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(path, "rb"),
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# (Die restlichen Funktionen bleiben gleich, da forecast Buttons betroffen sind.)
