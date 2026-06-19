#====================
# Currency Converter
#====================
import json
import os
import time
import requests
from datetime import datetime

HISTORY_FILE = "conversion_history.json"
CACHE_FILE = "rates_cache.json"
API_BASE_URL = "https://open.er-api.com/v6/latest"

def load_history():
    """Load conversion history. Returns empty list if file missing or corrupted."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_history(record):
    """Append new conversion and keep only last 50 entries."""
    history = load_history()
    history.append(record)
    if len(history) > 50:
        history = history[-50:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def load_cache():
    """Load cached rates if file exists."""
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

def save_cache(data):
    """Save fresh rates from API."""
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def fetch_rates(base: str):
    """Fetch fresh rates from the API."""
    url = f"{API_BASE_URL}/{base.upper()}"
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()  # ✅ parentheses added

        if data.get("result") != "success":
            raise ValueError(f"API returned error: {data.get('error-type')}")

        save_cache(data)
        print(f"Fresh rates loaded for {base} (next update: {data.get('time_next_update_utc')})")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Network/API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def get_rates(base: str = "USD"):
    """Smart caching layer."""
    cache = load_cache()

    if (cache and cache.get("base_code") == base.upper()
            and time.time() < cache.get("time_next_update_unix", 0)):
        return cache

    fresh = fetch_rates(base)
    if fresh:
        return fresh

    if cache:
        print("Using cached rates (may be outdated or for different base)")
        return cache
    return None

def list_supported_currencies():
    rates_data = get_rates("USD")
    if not rates_data:
        print("Cannot fetch currency list right now")
        return

    currencies = sorted(rates_data["rates"].keys())
    print(f"\n=== Supported Currencies ({len(currencies)} total) ===")

    for i in range(0, len(currencies), 10):
        row = currencies[i:i+10]
        print(" ".join(f"{code}" for code in row))  # ✅ dot added

    print("\nTip: Any of these can be used as From or To currency")  # ✅ outside loop

def convert_currency():
    """Main conversion logic with full validation and error recovery."""
    print("\nReal-time Currency Converter (any pair supported)")

    from_cur = input("From currency code (e.g. USD): ").strip().upper()  # ✅ fixed
    if not from_cur:
        from_cur = "USD"

    to_cur = input("To currency code (e.g. EUR): ").strip().upper()
    if not to_cur:
        print("To currency is required.")
        return

    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    rates_data = get_rates(from_cur)
    if not rates_data:
        print("No rates available (API down and no cache).")  # ✅ fixed quotes
        return

    rates = rates_data["rates"]

    if to_cur not in rates:
        print(f"{to_cur} is not supported.")
        return

    result = amount * rates[to_cur]

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "from": from_cur,
        "to": to_cur,
        "amount": round(amount, 4),
        "result": round(result, 4),  # ✅ comma added
        "rate": round(rates[to_cur], 6)
    }
    save_history(record)

    print("\n" + "="*50)
    print(f"{amount:,.4f} {from_cur} → {result:,.4f} {to_cur}")
    print(f"Exchange rate: 1 {from_cur} = {rates[to_cur]:.6f} {to_cur}")
    print("="*50)  # ✅ fixed indentation

def view_history():  # ✅ moved to top level
    """Display last 10 conversions."""
    history = load_history()
    if not history:
        print("No conversions saved yet.")
        return

    print("\n=== Last 10 Conversions ===")
    for entry in reversed(history[-10:]):
        print(f"{entry['timestamp']} | "
              f"{entry['amount']} {entry['from']} → "
              f"{entry['result']} {entry['to']} "
              f"(rate: {entry['rate']})")

def refresh_rates():  # ✅ moved to top level
    """Force fresh rates download."""
    print("Forcing fresh rates from API...")
    fresh = fetch_rates("USD")
    if fresh:
        print("Rates refreshed successfully!")

def main():
    print("Robust Currency Converter (with caching & fallback)")
    print("Using official free API → no key required\n")

    while True:
        print("\n" + "-"*40)
        print("1. Convert Currency")
        print("2. View History")       # ✅ was "1"
        print("3. List Supported Currencies")
        print("4. Refresh Rates Now")
        print("5. Exit")
        print("-"*40)

        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            convert_currency()
        elif choice == "2":
            view_history()
        elif choice == "3":
            list_supported_currencies()
        elif choice == "4":
            refresh_rates()
        elif choice == "5":
            print("Goodbye! Your history is saved.")
            break

if __name__ == "__main__":  # ✅ double underscores
    if not load_cache():
        print("Loading initial rates...")
        get_rates("USD")
    main()