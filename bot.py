import os
from flask import Flask, request, jsonify
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot de trading activo'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data or 'action' not in data:
        return jsonify({'error': 'Payload inválido'}), 400

    action = data['action']

    if action == 'buy':
        # Ejemplo con cantidad fija. Reemplaza con tu lógica de cálculo.
        client.create_order(
            symbol='BTCUSDT',
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=0.001
        )
    elif action == 'sell':
        client.create_order(
            symbol='BTCUSDT',
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=0.001
        )
    else:
        return jsonify({'error': 'Acción no reconocida'}), 400

    return jsonify({'message': f'Orden {action} ejecutada'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
