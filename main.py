import os
import matplotlib.pyplot as plt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
OWNER_IDS = list(map(int, os.getenv("OWNER_IDS", "1349917110").split(",")))
TARGET = float(os.getenv("TARGET_EUR", "100"))

app = Application.builder().token(TOKEN).build()

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
    current = float(os.getenv("TOTAL_PROFIT", "0"))
    percent = min(100, int(current / TARGET * 100))
    blocks = int(percent / 10)
    bar = "█" * blocks + "░" * (10 - blocks)
    status = "✅ Ziel erreicht!" if current >= TARGET else "❌ Noch nicht erreicht"

    if user_id in OWNER_IDS:
        text = f"""📈 Forecast-Modul:
Tagesziel: {TARGET:.2f} €
Aktuell: {current:.2f} €
Fortschritt: [{bar}] {percent} %

Status: {status}"""

        keyboard = [[
            InlineKeyboardButton("🔄 Aktualisieren", callback_data="forecast"),
            InlineKeyboardButton("🤖 SniperBot-Status", callback_data="sniper"),
            InlineKeyboardButton("📅 Monats-Forecast", callback_data="monthly_forecast"),
            InlineKeyboardButton("📄 Forecast-PDF", callback_data="download_pdf")
        ]]
    else:
        text = f"""📈 Öffentliche Vorschau:
Tagesziel: 100 €
Aktuell: {current:.2f} €
Fortschritt: [{bar}] {percent} %

💡 Hol dir den Vollzugang über crypto-tec.xyz"""
        keyboard = [[
            InlineKeyboardButton("🌐 Webseite öffnen", url="https://crypto-tec.xyz")
        ]]

    path = generate_progress_chart(current, TARGET)
    await update.callback_query.answer()
    await context.bot.send_photo(
       chat_id=update.effective_chat.id,
       photo=open(path, "rb"),
       caption=text,
       reply_markup=InlineKeyboardMarkup(keyboard)
    )

# SniperBot Status anzeigen
async def sniper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in OWNER_IDS:
        await update.callback_query.answer("🚫 Kein Zugriff", show_alert=True)
        return

    snipes = int(os.getenv("SNIPES_TODAY", "0"))
    wins = int(os.getenv("WINS_TODAY", "0"))
    profit = float(os.getenv("TOTAL_PROFIT", "0"))
    quote = round((wins / snipes) * 100, 1) if snipes > 0 else 0.0

    text = f"""🤖 SniperBot-Ergebnisse:
Snipes: {snipes}
Treffer: {wins}
Erfolgsquote: {quote:.1f} %
Einnahmen: +{profit:.2f} €"""
    keyboard = [[
        InlineKeyboardButton("📊 Forecast anzeigen", callback_data="forecast"),
        InlineKeyboardButton("🔄 Aktualisieren", callback_data="sniper")
    ]]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

# Monats-Forecast
async def monthly_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in OWNER_IDS:
        await update.callback_query.answer("🚫 Kein Zugriff", show_alert=True)
        return

    today = float(os.getenv("TOTAL_PROFIT", "0"))
    days_30 = today * 30
    days_60 = today * 60
    days_90 = today * 90

    text = f"""📅 Monats-Forecast (basierend auf aktuellem Tageswert):

📆 30 Tage: {days_30:.2f} €
📆 60 Tage: {days_60:.2f} €
📆 90 Tage: {days_90:.2f} €"""
    keyboard = [[
        InlineKeyboardButton("🔙 Zurück", callback_data="forecast")
    ]]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

# Forecast-PDF Download
async def download_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.callback_query.answer()
    if user_id in OWNER_IDS:
        await update.callback_query.message.reply_document(
            document="https://crypto-tec.xyz/assets/Forecast_Owner.pdf",
            filename="Forecast_Owner.pdf",
            caption="📄 Hier ist dein aktueller Forecast als PDF."
        )
    else:
        await update.callback_query.message.reply_document(
            document="https://crypto-tec.xyz/assets/Forecast_Investor.pdf",
            filename="Forecast_Investor.pdf",
            caption="📄 Vorschau-Forecast für Gäste. Für Vollzugang: crypto-tec.xyz"
        )

# Start mit Button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in OWNER_IDS:
        keyboard = [[InlineKeyboardButton("🌐 Website öffnen", url="https://crypto-tec.xyz")]]
        await update.effective_chat.send_message("🚫 Zugriff verweigert. Nur mit Einladung nutzbar.", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    keyboard = [[
        InlineKeyboardButton("📊 Forecast anzeigen", callback_data="forecast"),
        InlineKeyboardButton("🤖 SniperBot-Status", callback_data="sniper")
    ]]
    await update.effective_chat.send_message("👋 Willkommen im CryptoTecControl Bot\n\nWähle eine Option:", reply_markup=InlineKeyboardMarkup(keyboard))

# Handler
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(forecast, pattern="^forecast$"))
app.add_handler(CallbackQueryHandler(sniper, pattern="^sniper$"))
app.add_handler(CallbackQueryHandler(monthly_forecast, pattern="^monthly_forecast$"))
app.add_handler(CallbackQueryHandler(download_pdf, pattern="^download_pdf$"))

# Start Polling
if __name__ == "__main__":
    app.run_polling()
