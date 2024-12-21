from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import scrape_listings
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)
    
app = Flask(__name__)
CORS(app)  # Allow all origins

def parse_price(price_str):
    try:
        price_str = price_str.replace("PKR\n", "").strip()
        if "Crore" in price_str:
            return float(price_str.replace("Crore", "").strip()) * 10_000_000
        elif "Lakh" in price_str:
            return float(price_str.replace("Lakh", "").strip()) * 100_000
        else:
            return float(price_str)
    except ValueError:
        return 0

@app.route("/api/listings", methods=["GET"])
def get_listings():
    city = request.args.get("city", "lahore")
    max_pages = int(request.args.get("max_pages", 5))
    min_price = int(request.args.get("min_price", 0))
    max_price = int(request.args.get("max_price", 1_000_000_000))  # Large default max price

    listings = scrape_listings(city, max_pages)

    filtered_listings = [
        listing for listing in listings
        if min_price <= parse_price(listing["title"]) <= max_price
    ]

    return jsonify({"listings": filtered_listings})

if __name__ == "__main__":
    app.run(debug=True)
