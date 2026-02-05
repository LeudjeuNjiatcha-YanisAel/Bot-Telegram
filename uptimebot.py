import os
import requests
from flask import Flask
import threading
import time

# FLASK (uptime)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Telegram actif 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    def ping_loop():
        while True:
            try:
                url = os.environ.get(
                    "RENDER_EXTERNAL_URL",
                    "https://bot-telegram-krsa.onrender.com"
                )
                requests.get(url, timeout=10)
                print("🏓 Ping Render OK")
            except Exception as e:
                print(f"❌ Ping échoué : {e}")
            time.sleep(600)  # toutes les 10 minutes

    t = threading.Thread(target=ping_loop)
    t.daemon = True
    t.start()