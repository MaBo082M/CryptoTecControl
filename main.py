import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("🚫 Zugriff verweigert. Nur Owner erlaubt.")
        return

    keyboard = [[InlineKeyboardButton("📊 Forecast", callback_data="forecast")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Willkommen im CryptoTecControl-Bot ⚙️", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "forecast":
        await query.edit_message_text("📈 Ziel: 100 € Netto/Tag
Status: 🔄 Noch nicht erreicht")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
