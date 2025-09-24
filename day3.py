#!/usr/bin/env python3

import requests
import json

API_KEY = '7baa13496932eb02c0efa3ffb2def7ed'
CITY = 'London'
URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

def get_weather_data():
    """
    Fetches weather data from OpenWeather API.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_json(data, filename='day3_weather.json'):
    """
    Saves the weather data to a JSON file.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

def read_and_print_data(filename='weather.json'):
    """
    Reads the JSON file and prints temperature and humidity.
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
    except Exception as e:
        print(f"Error reading data: {e}")

class Day3:
    def __call__(self):
        data = get_weather_data()
        if data:
            save_to_json(data)
            read_and_print_data()

# Create an instance of the Day2 class
app = Day3()
