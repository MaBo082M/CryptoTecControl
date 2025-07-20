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
    sniper_profit = float(os.getenv("SNIPER_PROFIT", "0").replace(",", "."))
    current = sniper_profit
    snipes = int(os.getenv("SNIPES_TODAY", "0"))
    wins = int(os.getenv("WINS_TODAY", "0"))

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

        keyboard = [
            [InlineKeyboardButton("🔄 Aktualisieren", callback_data="forecast")],
            [InlineKeyboardButton("🤖 SniperBot-Status", callback_data="sniper")],
            [InlineKeyboardButton("📅 Monats-Forecast", callback_data="monthly_forecast")],
            [InlineKeyboardButton("📄 Forecast-PDF", callback_data="download_pdf")],
            [InlineKeyboardButton("💰 HypoCoin", callback_data="hypocoin")]
        ]
    else:
        text = f"""📈 Öffentliche Vorschau:
Tagesziel: 100 €
Aktuell: {current:.2f} €
Fortschritt: [{bar}] {percent} %

💡 Hol dir den Vollzugang über crypto-tec.xyz"""
        keyboard = [
            [InlineKeyboardButton("🌐 Webseite öffnen", url="https://crypto-tec.xyz")],
            [InlineKeyboardButton("🎟️ VIP-Zugang sichern", url=VIP_GROUP_LINK)]
        ]

    path = generate_progress_chart(current, TARGET)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_media(
            media=InputMediaPhoto(media=open(path, "rb"), caption=text),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open(path, "rb"),
            caption=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# /start Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"/start aufgerufen von {update.effective_user.id}")
    await update.message.reply_text(
        "Willkommen im CryptoTecControl Bot!\nWähle eine Option:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📈 Forecast anzeigen", callback_data="forecast")]
        ])
    )

# Button Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat.id

    await query.answer()
    print(f"Button gedrückt: {data} von Chat-ID: {chat_id}")

    if data == "forecast":
        await forecast(update, context)
    elif data == "sniper":
        sniper_status = os.getenv("SNIPER_STATUS", "BETA")
        await context.bot.send_message(chat_id=chat_id, text=f"🤖 SniperBot ist aktiv. Modul-Status: {sniper_status}.")
    elif data == "monthly_forecast":
        await context.bot.send_message(chat_id=chat_id, text="📅 Monatsprognose: Dynamische Prognose wird geladen… (Platzhalter)")
    elif data == "download_pdf":
        await context.bot.send_message(chat_id=chat_id, text="📄 Forecast-PDF: Link folgt demnächst auf crypto-tec.xyz")
    elif data == "hypocoin":
        await context.bot.send_message(chat_id=chat_id, text="💰 HypoCoin-Modul wird geladen… Bald verfügbar für VIPs.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Unbekannter Befehl.")

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    app.run_polling()
