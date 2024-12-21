from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import scrape_listings
import os

# Initialize Flask app and configure CORS
app = Flask(__name__)
CORS(app)  # For development; restrict origins in production

def parse_price(price_str):
    """Parse the price string into a numeric value."""
    if not price_str:
        return 0
    try:
        price_str = price_str.replace("PKR\n", "").strip()
        if "Crore" in price_str:
            return float(price_str.replace("Crore", "").strip()) * 10_000_000
        elif "Lakh" in price_str:
            return float(price_str.replace("Lakh", "").strip()) * 100_000
        else:
            return float(price_str)
    except (ValueError, AttributeError):
        return 0

@app.route("/api/listings", methods=["GET"])
def get_listings():
    """Fetch and filter real estate listings."""
    try:
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Bind to 0.0.0.0 and use dynamic port for deployment
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)
