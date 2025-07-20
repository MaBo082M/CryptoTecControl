import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "1349917110"))
TARGET = 100  # Tagesziel in EUR

app = Application.builder().token(TOKEN).build()

# Forecast anzeigen
async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = float(os.getenv("TODAY_EARNINGS", "0"))
    percent = min(100, int(current / TARGET * 100))
    blocks = int(percent / 10)
    bar = "█" * blocks + "░" * (10 - blocks)
    status = "✅ Ziel erreicht!" if current >= TARGET else "❌ Noch nicht erreicht"

    text = f"""📈 Forecast-Modul:
Tagesziel: {TARGET:.2f} €
Aktuell: {current:.2f} €
Fortschritt: [{bar}] {percent} %

Status: {status}"""
    keyboard = [[InlineKeyboardButton("🔄 Aktualisieren", callback_data="forecast")]]
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

# Start mit Button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("🚫 Zugriff verweigert.")
        return
    keyboard = [[InlineKeyboardButton("📊 Forecast anzeigen", callback_data="forecast")]]
    await update.message.reply_text("👋 Willkommen im CryptoTecControl Bot\n\nWähle eine Option:", reply_markup=InlineKeyboardMarkup(keyboard))

# Handler
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(forecast, pattern="^forecast$"))

# Start Polling
if __name__ == "__main__":
    app.run_polling()
