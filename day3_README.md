# Day 3: File Handling & API Requests

## Overview
This project demonstrates file handling, JSON operations, API requests, and error handling. It involves calling the OpenWeather API for a city, saving the weather data to a JSON file, and reading it back to print temperature and humidity.

## Files Included
- `day3.py`: The main Python script that handles API requests and file operations.
- `day3_README.md`: This guideline file.

## Prerequisites
- Python 3.x installed on your system.
- Install required libraries: `pip install requests`.

## Step-by-Step Guide

### 1. Setup
- Ensure you are in the project directory: `/Users/bypti703/Documents/GENERAL_DETAILS/Python_Learning`.
- The file `day3.py` should be present.

### 2. Running the Script
- Open a terminal in VSCode or your system.
- Navigate to the project directory.
- Run the script using uvicorn:
  ```
  uvicorn day3:app --reload
  ```
- The script will fetch the weather data, save it to `weather.json`, and print the temperature and humidity.
- Expected Output:
  ```
  Data saved to weather.json
  Temperature: 15.5°C
  Humidity: 72%
  ```

### 3. Code Explanation
- **Import Statements**: `import requests` and `import json` - For making API requests and handling JSON data.
- **API Key and URL**: Uses the provided API key and constructs the URL for the OpenWeather API.
- **get_weather_data()**: Fetches data from the API with error handling.
- **save_to_json()**: Saves the data to a JSON file.
- **read_and_print_data()**: Reads the JSON file and prints temperature and humidity.
- **Class Day3**: The class with `__call__` method that runs the logic on initialization.
- **Error Handling**: Uses try-except blocks to handle potential errors.

### 4. Customization
- **Change City**: Modify the `CITY` variable in `day3.py` to your desired city.
- **Change File Name**: Modify the `filename` parameter in the functions.

### 5. Troubleshooting
- **API Key Error**: Ensure the API key is correct and has not expired.
- **Network Error**: Check your internet connection.
- **JSON Error**: Ensure the JSON file is not corrupted.

## Learning Outcomes
- Learned how to make API requests using the `requests` module.
- Practiced file handling with `open()` for reading and writing.
- Used the `json` module for JSON operations.
- Implemented error handling with try-except.

## Next Steps
- Experiment with other APIs or add more weather data fields.
- Explore more advanced error handling techniques.
