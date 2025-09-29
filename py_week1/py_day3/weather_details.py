import json
import requests

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
BASE_URL2 = 'https://api.weatherapi.com/v1/current.json?'
BASE_URL_GOOGLE = 'https://weather.googleapis.com/v1/currentConditions:lookup?'
API_KEY = '52a17d91b3ed0697b05a7dd6fdc708c4'
API_KEY2 = 'bc8fb57064f546fd81854950252509'
API_KEY_GOOGLE = 'AIzaSyC_BwJelYMeVngnawYX-7M2r5SKH7GX6j4'
CITY = 'Ahmedabad'

URL = BASE_URL + 'appid=' + API_KEY + '&q=' + CITY
URL2 = BASE_URL2 + 'q=' + CITY + '&key=' + API_KEY2
URL_GOOGLE = BASE_URL_GOOGLE + 'key=' + API_KEY_GOOGLE + '&locations=' + CITY

def main():
    response = requests.get(URL2) # request to the API
    print(response.json()) # convert the response to JSON format
    if response.status_code == 200:
        try: # handle try and exception for error handling
            data = response.json()
            open('weather_details.json', 'w').write(json.dumps(data)) # write the data to a json file
            read_data = open('weather_details.json', 'r') # read the data from the json file
            jsonLoaded = json.load(read_data) # load the data from the json file
            weatherData = jsonLoaded['current']
            temperature = weatherData['temp_c']
            humidity = weatherData['humidity']
            pressure = weatherData['pressure_mb']
            wind = weatherData['wind_kph']
            time = weatherData['last_updated']
            report = weatherData['condition']['text']
            print(f"{CITY:-^30}")
            print(f"Time: {time} UTC")
            print(f"Temperature: {temperature} C")
            print(f"Wind: {wind} Km/h")
            print(f"Humidity: {humidity} %")
            print(f"Pressure: {pressure} mb")
            print(f"Weather Report: {report}")
        except  KeyError:
            print("Error: Key not found in the response data")
    else:
        print("Error in the HTTP request")

if __name__ == "__main__":
    main()
