from flask import Flask, jsonify, request
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from requests.exceptions import HTTPError
import requests
import os


load_dotenv()
app = Flask(__name__)


def get_weather(city: str, units: str):
    """
    Make a call to the OpenWeatherMap api by retrieving the API_KEY and using the city.
    :param units: the unit type for the request. `standard` for Kelvin, `metric` for Celsius and `imperial` for
    Fahrenheit.
    :param city: a string object that represents the city to query weather data for.
    :return: a dictionary object containing the response from the OpenWeatherMap api.
    """

    api_key = os.environ.get('API_KEY')
    url = 'https://api.openweathermap.org/data/2.5/forecast?'

    try:
        response = requests.get(f'{url}q={city}&APPID={api_key}&units={units}')
        response.raise_for_status()
        return response.json(), units
    except HTTPError as error:
        return error


def check_unit(unit: str):
    """
    Check value of the unit and return the correct unit notation for the temperature.
    :param unit: the unit type for the request. `standard` for Kelvin, `metric` for Celsius and `imperial` for
    Fahrenheit.
    :return: a string object.
    """
    if unit == 'metric':
        return 'C'
    elif unit == 'imperial':
        return 'F'
    else:
        return 'K'


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

    try:
        units = request.args['unit']
    except KeyError:
        units = None

    weather_data, query_units = get_weather(city, units)
    temp = check_unit(units)

    error = {
        'error': '',
        'error_code': ''
    }

    if type(weather_data) == dict:
        weather_dict = {
            f'{weather_data["list"][0]["weather"][0]["main"].lower()}':
                f'{weather_data["list"][0]["weather"][0]["description"]}',
            'humidity': f'{weather_data["list"][0]["main"]["humidity"]}%',
            'pressure': f'{weather_data["list"][0]["main"]["pressure"]} hPa',
            'temperature': f'{str(weather_data["list"][0]["main"]["temp"]) + temp}',
        }
        return jsonify(weather_dict)

    elif '404' in str(weather_data):
        error = {
            "error": f"cannot find the city'{city}'",
            "error_code": "country_not_found"
        }
        return jsonify(error)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
