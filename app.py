from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()
app = Flask(__name__)


def get_weather(city: str) -> dict:
    """
    Make a call to the OpenWeatherMap api by retrieving the API_KEY and using the city.
    :param city: a string object that represents the city to query weather data for.
    :return: a dictionary object containing the response from the OpenWeatherMap api.
    """
    api_key = os.environ.get('API_KEY')
    url = 'https://api.openweathermap.org/data/2.5/forecast?'
    response = requests.get(f'{url}q={city}&APPID={api_key}&units=metric')
    response.raise_for_status()
    print(response.json())
    return response.json()


@app.route('/ping')
def ping():
    """
    Endpoint to check if the service is working.
    :return: JSON object containing details about the API.
    """
    ping_dict = {
        "name": "weatherservice",
        "status": "ok",
        "version": "1.0.0"
    }
    return jsonify(ping_dict)


@app.route('/forecast/<city>')
def forecast(city: str):
    weather_data = get_weather(city)
    weather_dict = {
        f'{weather_data["list"][0]["weather"][0]["main"].lower()}': f'{weather_data["list"][0]["weather"][0]["description"]}',
        'humidity': f'{weather_data["list"][0]["main"]["humidity"]}%',
        'pressure': f'{weather_data["list"][0]["main"]["pressure"]} hPa',
        'temperature': f'{weather_data["list"][0]["main"]["temp"]}C',
    }
    return jsonify(weather_dict)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
