#==================================
# Real-time Weather Info (Open-Meteo)
# Search weather for ANY place!
#==================================
import requests
from datetime import datetime

WEATHER_CODES = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail"
}

def geocode_place(place_name):
    """Convert a place name into latitude, longitude, and display name."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": place_name,
        "count": 5,
        "language": "en",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, timeout=6)
        r.raise_for_status()
        results = r.json().get("results", [])

        if not results:
            print(f'  No location found for "{place_name}".')
            return None

        # If multiple results, let user pick one
        if len(results) > 1:
            print(f"\n  Multiple places found for '{place_name}':")
            for i, res in enumerate(results, 1):
                country  = res.get("country", "")
                admin    = res.get("admin1", "")
                label    = f"{res['name']}, {admin}, {country}".strip(", ")
                print(f"  {i}. {label}")

            while True:
                choice = input(f"\n  Pick a number (1-{len(results)}): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(results):
                    chosen = results[int(choice) - 1]
                    break
                print("  Invalid choice. Try again.")
        else:
            chosen = results[0]

        display = (
            f"{chosen['name']}, "
            f"{chosen.get('admin1', '')}, "
            f"{chosen.get('country', '')}"
        ).strip(", ")

        return {
            "lat":     chosen["latitude"],
            "lon":     chosen["longitude"],
            "name":    display,
            "timezone": chosen.get("timezone", "auto")
        }

    except Exception as e:
        print(f"  Geocoding error: {e}")
        return None


def get_weather(lat, lon, timezone):
    """Fetch current weather for given coordinates."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":  lat,
        "longitude": lon,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone":     timezone,
        "forecast_days": 1
    }
    try:
        r = requests.get(url, params=params, timeout=6)
        r.raise_for_status()
        data = r.json()["current"]

        code = data.get("weather_code", 0)
        desc = WEATHER_CODES.get(code, "Unknown")

        return {
            "time":       data["time"],
            "temp":       data["temperature_2m"],
            "feels_like": data["apparent_temperature"],
            "humidity":   data["relative_humidity_2m"],
            "wind":       data["wind_speed_10m"],
            "precip":     data["precipitation"],
            "desc":       desc
        }

    except Exception as e:
        print(f"  Weather fetch error: {e}")
        return None


def show_weather(place_name):
    """Geocode a place, then display its weather."""
    print(f'\n  Looking up "{place_name}"...')
    location = geocode_place(place_name)
    if not location:
        return

    print(f"  Fetching weather for {location['name']}...")
    w = get_weather(location["lat"], location["lon"], location["timezone"])
    if not w:
        print("  Could not fetch weather data.")
        return

    # Format time nicely
    try:
        dt = datetime.fromisoformat(w["time"])
        time_str = dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        time_str = w["time"][:16]

    # Display result
    print()
    print("=" * 55)
    print(f"  {location['name']}")
    print(f"  {time_str}")
    print("=" * 55)
    print(f"  Condition     :  {w['desc']}")
    print(f"  Temperature   :  {w['temp']} °C  (feels like {w['feels_like']} °C)")
    print(f"  Humidity      :  {w['humidity']}%")
    print(f"  Wind Speed    :  {w['wind']} km/h")
    print(f"  Precipitation :  {w['precip']} mm")
    print("=" * 55)


def main():
    print("\n" + "#" * 55)
    print("#   Real-time Weather — Powered by Open-Meteo   #")
    print("#" * 55)

    while True:
        print("\n  1. Check weather for a place")
        print("  2. Exit")
        ch = input("\n  Choose (1 or 2): ").strip()

        if ch == "1":
            place = input("  Enter place name (e.g. Tokyo, London, Dhaka): ").strip()
            if place:
                show_weather(place)
            else:
                print("  Please enter a place name.")

        elif ch == "2":
            print("\n  Goodbye! Stay dry ☂\n")
            break

        else:
            print("  Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()