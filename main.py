import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("🚫 Zugriff verweigert.")
        return

    keyboard = [[InlineKeyboardButton("📊 Forecast", callback_data="forecast")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Willkommen im CryptoTecControl Bot ⚙️", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "forecast":
        await query.edit_message_text(text="📈 Forecast:
Tagesziel 100 € Netto
Status: 🔄 Noch nicht erreicht")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    logger.info("Bot läuft...")
    app.run_polling()
