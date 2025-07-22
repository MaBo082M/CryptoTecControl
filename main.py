import asyncio
import requests
import time

# Telegram-Konfiguration
BOT_TOKEN = "8178722863:AAErLZ-PtVVVN7Fqn6_UPAzGs8iMWWDuIA4"
OWNER_ID = 1349917110

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": OWNER_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        print("Telegram Response:", response.status_code, response.text)
    except Exception as e:
        print("Telegram send_alert() error:", e)

# Beispielhafte SniperBot Loop (simuliert)
async def sniper_loop():
    while True:
        print("SniperBot läuft... (Loop aktiv)")
        await asyncio.sleep(10)  # simuliert Arbeit
        # Optional: send_alert("🔔 Neuer Scan abgeschlossen") bei realem Trigger

# Hauptfunktion
async def main():
    send_alert("✅ SniperBot gestartet! Telegram-Verbindung steht.")
    await sniper_loop()

# Async starten
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Fehler in main():", e)