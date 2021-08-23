from flask import Flask, jsonify, request
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from datetime import datetime
import requests
import os

load_dotenv()
app = Flask(__name__)


def get_weather(city: str, units='standard'):
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
        return error, units


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


def find_index(weather_data: dict, date: datetime) -> int:
    """
    Find the index position of where the datetime is in the weather data, if no time information is provided in the
    query parameters then return an index of 0.
    :param weather_data: the json response from the OpenWeatherMap API.
    :param date: the date entered in the query parameter.
    :return: an integer value representing the index of where the weather query for a particular time.
    """
    weather_list = weather_data['list']
    for index, weather in enumerate(weather_list):
        print(index)
        if weather['dt_txt'] == date.strftime('%Y-%m-%d %H:%M:%S'):
            return index
        else:
            return 0


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
    units = request.args.get('unit', '').casefold()

    date_raw = request.args.get('at')
    if date_raw:
        date = datetime.strptime(date_raw, '%Y-%m-%d')
    else:
        date = datetime.utcnow()

    weather_data, query_units = get_weather(city, units)
    temp = check_unit(query_units)

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
        error['error'] = f'cannot find the city"{city}"'
        error['error_code'] = 'city_not_found'
        return jsonify(error), 404

    else:
        error['error'] = 'Something went wrong'
        error['error_code'] = 'internal_server_error'
        return jsonify(error), 500


if __name__ == '__main__':
    app.run(debug=True, port=5002)
