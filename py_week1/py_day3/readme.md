# File Handling & API Requests (py_day3)

## Session Overview
This session focused on practical Python skills for working with files and APIs, including:

- **open()**: Reading and writing files in Python.
- **JSON with json module**: Parsing and serializing JSON data.
- **requests**: Making HTTP API calls.
- **Error handling**: Using try-except blocks for robust code.

---

## Tasks Completed

### 1. Call OpenWeather API for Your City
- Used the `requests` library to fetch current weather data for Ahmedabad from the WeatherAPI service.

### 2. Save Weather Data to a JSON File
- The API response is saved to `weather_details.json` using the `json` module.

### 3. Read It Back and Print Only Temperature & Humidity
- The script reads the saved JSON file, extracts temperature and humidity, and prints them (along with other weather details) to the console.

---

## Code Review: `weather_details.py`
- **API Call**: Uses `requests.get()` to fetch weather data for Ahmedabad.
- **File Write**: Saves the JSON response to `weather_details.json`.
- **File Read**: Reads the JSON file and loads it with `json.load()`.
- **Data Extraction**: Extracts temperature (`temp_c`) and humidity (`humidity`) from the `current` section of the JSON.
- **Error Handling**: Uses try-except to catch missing keys and HTTP errors.

---

## How to Run
1. **Install dependencies**:
   ```bash
   pip install requests
   ```
2. **Run the script**:
   ```bash
   python weather_details.py
   ```

---

## Example Output
```
        Ahmedabad         
Time: 2025-09-25 16:30 UTC
Temperature: 31.2 C
Wind: 6.8 Km/h
Humidity: 52 %
Pressure: 1004.0 mb
Weather Report: Overcast
```

---

## Notes
- The script uses WeatherAPI for demonstration. API keys are hardcoded for learning purposes only.
- The main focus is on file handling, JSON, API requests, and error handling in Python.

---

## References
- [Python File Handling](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Python json module](https://docs.python.org/3/library/json.html)
- [Requests Library](https://docs.python-requests.org/)
- [WeatherAPI Docs](https://www.weatherapi.com/docs/)

