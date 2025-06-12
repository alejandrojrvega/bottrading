# bot.py
from flask import Flask, request
from binance.client import Client
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    action = data.get("action")

    if action == "buy":
        print("Ejecutar orden de compra")
        # client.create_order(...)  # Simulación
    elif action == "sell":
        print("Ejecutar orden de venta")
        # client.create_order(...)  # Simulación
    else:
        return {"status": "error", "message": "Acción no reconocida"}, 400

    return {"status": "success"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)