import os
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

# Holt den Token aus den Railway-Umgebungsvariablen
TOKEN = os.getenv("BOT_TOKEN")

# Erstelle die Telegram-Bot-Anwendung
app = Application.builder().token(TOKEN).build()

# /start-Befehl
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Wilkommen im CryptoTecControl Bot")

# Befehl registrieren
app.add_handler(CommandHandler("start", start))

# Bot starten
if __name__ == "__main__":
    app.run_polling()
