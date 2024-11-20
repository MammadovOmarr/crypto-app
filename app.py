from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import os
from urllib.parse import quote as url_quote


port = int(os.environ.get("PORT",5000))

app = Flask(__name__)

last_prices = {"bitcoin": None, "ethereum": None, "solana": None}

# Helper function to fetch price
def fetch_price(crypto):
    global last_prices
    if crypto == 'bitcoin':
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    elif crypto == 'ethereum':
        url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD"
    elif crypto == 'solana':
        url = "https://min-api.cryptocompare.com/data/price?fsym=SOL&tsyms=USD"
    else:
        None


    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if crypto == 'bitcoin':
        price_usd = data["bpi"]["USD"]["rate_float"]
    elif crypto == 'ethereum':
        price_usd = data["USD"] 
    elif crypto == 'solana':
        price_usd = data["USD"]
    

    last_price = last_prices[crypto]
    if last_price is None:
        percentage_change = 0
    else:
        percentage_change = ((price_usd - last_price) / last_price) * 100

    # Update the last price
    last_prices[crypto] = price_usd

    return price_usd, percentage_change
    



# Endpoint for fetching cryptocurrency price
@app.route("/api/price/<crypto>")
def crypto_price(crypto):
    price_usd, percentage_change = fetch_price(crypto)
    if price_usd is None:
        return jsonify(error=f"Failed to fetch {crypto} price"), 500
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    return jsonify(price_usd=price_usd, timestamp=timestamp, percentage_change=percentage_change)

# Main route for serving the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route for the crypto price page
@app.route("/crypto_price")
def crypto_price_page():
    return render_template("crypto_price.html")

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=port)
