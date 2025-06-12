from flask import Flask, request
from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
symbol = os.getenv("SYMBOL")
quantity = float(os.getenv("QUANTITY"))

client = Client(api_key, api_secret)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    signal = data.get("message", "").lower()

    if signal == "buy":
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        print("✅ BUY EXECUTED:", order)
        return "Buy order sent", 200

    elif signal == "sell":
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
        print("✅ SELL EXECUTED:", order)
        return "Sell order sent", 200

    return "❌ Invalid signal", 400

if __name__ == '__main__':
    app.run(port=5000)
