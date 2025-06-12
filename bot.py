from flask import Flask, request, jsonify
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
import json

app = Flask(__name__)

# === API KEYS ===
API_KEY = "T5GJ0WAInrn3rm0imAeyyGOOCE5yUswNZiyFFBLKoiDtoC2hZuMtikBUjVYVee9F"
API_SECRET = "R38h1noXHOWI2xSujRezfD6CdFVTlWW4RkTnTjYKQZuRidp3Tkpg1ye9Eh33tZUs"

if not API_KEY or not API_SECRET:
    raise ValueError("API_KEY o API_SECRET no están definidas")

client = Client(API_KEY, API_SECRET)

# === ESTADO ===
STATE_FILE = "trade_state.json"

def get_last_action():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            return state.get("last_action")
    return None

def set_last_action(action):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_action": action}, f)

# === ENDPOINTS ===
@app.route('/', methods=['GET'])
def home():
    return 'Bot de trading activo (modo Spot)', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        action = data.get("action")

        if not action:
            return jsonify({"error": "No se proporcionó 'action'"}), 400

        last_action = get_last_action()

        # === COMPRA ===
        if action == "buy":
            if last_action == "buy":
                return jsonify({"message": "Ya hay una compra activa. Ignorado."}), 200
            
            order = client.create_order(
                symbol='EURUSDT',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=45
            )
            set_last_action("buy")
            return jsonify({"message": "Orden de compra ejecutada", "order": order}), 200

        # === VENTA ===
        elif action == "sell":
            if last_action != "buy":
                return jsonify({"message": "No hay compra previa. Venta ignorada."}), 200

            order = client.create_order(
                symbol='EURUSDT',
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=45
            )
            set_last_action("sell")
            return jsonify({"message": "Orden de venta ejecutada", "order": order}), 200

        else:
            return jsonify({"error": f"Acción desconocida: {action}"}), 400

    except BinanceAPIException as e:
        return jsonify({"error": "Error Binance API", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
