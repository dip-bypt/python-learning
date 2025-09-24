
import requests
import json

"""
Day 3: Dynamic Weather Data Fetcher

This script allows you to enter any city name, fetches its latitude and longitude using a geocoding API, then retrieves and displays the current temperature and humidity for that location using the Open-Meteo API.

Key Concepts:
- User input for dynamic location
- Geocoding (city name to coordinates)
- API requests and JSON handling
- Error handling and file operations
"""

def get_coordinates(city):
    """Get latitude and longitude for a city using Nominatim geocoding API."""
    geo_url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"
    try:
        resp = requests.get(geo_url, headers={"User-Agent": "python-learning-script"})
        resp.raise_for_status()
        data = resp.json()
        if not data:
            print(f"No coordinates found for '{city}'.")
            return None, None
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    except Exception as e:
        print("Error fetching coordinates:", e)
        return None, None

def get_weather(lat, lon):
    """Fetch weather data for given latitude and longitude from Open-Meteo API."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error fetching weather data:", e)
        return None

def main():
    city = input("Enter a city name: ").strip()
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        print("Cannot proceed without valid coordinates.")
        return
    weather_data = get_weather(lat, lon)
    if not weather_data or 'current' not in weather_data:
        print("No weather data available.")
        return
    # Save to JSON file
    with open("weather.json", "w") as f:
        json.dump(weather_data, f, indent=4)
    print("Weather data saved to weather.json ✅")
    # Extract and print temperature and humidity
    temp = weather_data["current"].get("temperature_2m", "N/A")
    humidity = weather_data["current"].get("relative_humidity_2m", "N/A")
    print(f"Temperature: {temp}°C")
    print(f"Humidity: {humidity}%")

if __name__ == "__main__":
    main()
