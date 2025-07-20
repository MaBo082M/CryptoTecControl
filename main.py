import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "1349917110"))

app = Application.builder().token(TOKEN).build()

# /start Befehl mit Dashboard-Button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("🚫 Zugriff verweigert.")
        return

    keyboard = [[InlineKeyboardButton("📊 Forecast anzeigen", callback_data="forecast")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Wilkommen im CryptoTecControl Bot\n\nWähle eine Option:", reply_markup=reply_markup)

# Reaktion auf Button-Klicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "forecast":
        await query.edit_message_text("📈 Forecast-Modul:\nTagesziel: 100 EUR\nStatus: Noch nicht erreicht.")
    else:
        await query.edit_message_text("❓ Unbekannte Aktion")

# Handler registrieren
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# Bot starten
if __name__ == "__main__":
    app.run_polling()
