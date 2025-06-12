from flask import Flask, request, jsonify
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException

app = Flask(__name__)

# Cargar las claves API desde variables de entorno (Railway)
API_KEY = "T5GJ0WAInrn3rm0imAeyyGOOCE5yUswNZiyFFBLKoiDtoC2hZuMtikBUjVYVee9F"
API_SECRET = "R38h1noXHOWI2xSujRezfD6CdFVTlWW4RkTnTjYKQZuRidp3Tkpg1ye9Eh33tZUs"

# Comprobar que las claves no están vacías
if not API_KEY or not API_SECRET:
    raise ValueError("API_KEY o API_SECRET no están definidas en las variables de entorno")

# Inicializar el cliente de Binance
client = Client(API_KEY, API_SECRET)

@app.route('/', methods=['GET'])
def home():
    return 'Bot de trading activo', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        action = data.get("action")

        if not action:
            return jsonify({"error": "No se proporcionó 'action' en el cuerpo del JSON"}), 400

        if action == "buy":
            order = client.create_order(
                symbol='EURUSDT',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=2  # <-- AJUSTA según tu saldo
            )
            return jsonify({"message": "Orden de compra ejecutada", "order": order}), 200

        elif action == "sell":
            order = client.create_order(
                symbol='EURUSDT',
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=2  # <-- AJUSTA según tu saldo
            )
            return jsonify({"message": "Orden de venta ejecutada", "order": order}), 200

        else:
            return jsonify({"error": f"Acción desconocida: {action}"}), 400

    except BinanceAPIException as e:
        return jsonify({"error": "Error con Binance API", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
