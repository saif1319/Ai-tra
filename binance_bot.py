import requests
import time
from binance.client import Client

# 🔹 Replace with your actual Binance API credentials
BINANCE_API_KEY = "YOUR_API_KEY"
BINANCE_SECRET_KEY = "YOUR_SECRET_KEY"

# 🔹 Replace with your Telegram Bot Token & Chat ID
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# 🔹 Initialize Binance Client
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY, tld="us")

# 🔹 Function to send trade signals to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    return response.json()

# 🔹 Function to fetch all available trading pairs from Binance
def get_all_trading_pairs():
    try:
        exchange_info = client.get_exchange_info()
        pairs = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['status'] == 'TRADING']
        print(f"✅ Found {len(pairs)} trading pairs.")
        return pairs
    except Exception as e:
        print(f"❌ Error fetching trading pairs: {e}")
        return []

# 🔹 Function to check trade opportunity
def check_trade_opportunity(trading_pairs):
    for symbol in trading_pairs:
        try:
            price = float(client.get_symbol_ticker(symbol=symbol)["price"])

            # Example Trading Strategy (Modify as Needed)
            entry_price = price * 0.98  # Buy when price drops 2%
            stop_loss = price * 0.97    # Stop-loss at 3% drop
            take_profit = price * 1.05  # Take-profit at 5% increase

            # 🔹 Condition to trigger a trade alert
            if price <= entry_price:  # Buy condition (Modify as per strategy)
                trade_signal = f"""
                🔔 *New Trade Alert* 🔔
                ✅ Buy {symbol}
                💰 Entry Price: ${price}
                📉 Stop-Loss: ${stop_loss}
                📈 Take-Profit: ${take_profit}
                """
                send_telegram_message(trade_signal)
                print(f"✅ Trade opportunity detected for {symbol}! Alert sent.")
                return True  # ✅ Trade found

        except Exception as e:
            print(f"⚠️ Error fetching {symbol} price: {e}")

    return False  # ❌ No trade found

# 🔹 Fetch all trading pairs
trading_pairs = get_all_trading_pairs()

# 🔹 Continuous Monitoring
print("🚀 Bot started... Monitoring market for trade opportunities.")

while True:
    if check_trade_opportunity(trading_pairs):
        print("✅ Trade alert sent.")

    time.sleep(60)  # 🔹 Wait 60 seconds before checking again.
