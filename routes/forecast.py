from dotenv import load_dotenv, find_dotenv
from requests.exceptions import HTTPError
from flask_restful import Resource
from flask import jsonify, request
from dateutil.parser import parse
from datetime import datetime
import requests
import pytz
import os


class Forecast(Resource):
    """
    Object that handles the 'ping' endpoint
    """
    def get(self, city: str):
        """
        Check the weather forecast of a given city.
        :param city: a string object that represents the city to make a weather query about.
        :return: a JSON object that contains the weather information about the city.
        """
        # Make a call to the OpenWeatherMap API and check the units inserted at the query parameter.
        units = request.args.get('unit', '').casefold()
        weather_data, query_units = self.get_weather(city, units)
        temp = self.check_unit(query_units)

        # Get the date from the request if no date is provided use the current date.
        date_raw = request.args.get('at', )
        if date_raw:
            date = parse(date_raw).replace(tzinfo=pytz.UTC)
        else:
            date = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)

        # Based on the date check the index of the weather that corresponds with the date in the weather response.
        index = self.find_index(weather_data, date)

        # Prepare the error response.
        error = {
            'error': '',
            'error_code': ''
        }

        if date < datetime.utcnow().replace(tzinfo=pytz.UTC):
            error['error'] = f'{date}: is in the past'
            error['error_code'] = 'invalid_date'
            return jsonify(error), 400

        if type(weather_data) == dict:
            # Based on the date check the index of the weather that corresponds with the date in the weather response.
            index = self.find_index(weather_data, date)
            weather_dict = {
                f'{weather_data["list"][index]["weather"][0]["main"].lower()}':
                    f'{weather_data["list"][index]["weather"][0]["description"]}',
                'humidity': f'{weather_data["list"][index]["main"]["humidity"]}%',
                'pressure': f'{weather_data["list"][index]["main"]["pressure"]} hPa',
                'temperature': f'{str(weather_data["list"][index]["main"]["temp"]) + temp}',
            }
            return weather_dict, 200

        elif '404' in str(weather_data):
            error['error'] = f'cannot find the city"{city}"'
            error['error_code'] = 'city_not_found'
            return error, 404

        else:
            error['error'] = 'Something went wrong'
            error['error_code'] = 'internal_server_error'
            return error, 500

    @staticmethod
    def get_weather(city: str, units='standard'):
        """
        Make a call to the OpenWeatherMap api by retrieving the API_KEY and using the city.
        :param units: the unit type for the request. `standard` for Kelvin, `metric` for Celsius and `imperial` for
        Fahrenheit.
        :param city: a string object that represents the city to query weather data for.
        :return: a dictionary object containing the response from the OpenWeatherMap api.
        """
        load_dotenv(find_dotenv())
        api_key = os.environ.get('API_KEY')
        url = 'https://api.openweathermap.org/data/2.5/forecast?'

        try:
            response = requests.get(f'{url}q={city}&APPID={api_key}&units={units}')
            response.raise_for_status()
            return response.json(), units
        except HTTPError as error:
            return error, units

    @staticmethod
    def check_unit(unit: str):
        """
        Check value of the unit and return the correct unit notation for the temperature.
        :param unit: the unit type for the request. `standard` for Kelvin, `metric` for Celsius and `imperial` for
        Fahrenheit.
        :return: a string object that represents the unit of measure for the temperature.
        """
        if unit == 'metric':
            return 'C'
        elif unit == 'imperial':
            return 'F'
        else:
            return 'K'

    @staticmethod
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
