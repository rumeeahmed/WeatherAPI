import unittest
import requests
from requests import Response
from datetime import datetime


class ForecastTest(unittest.TestCase):
    """
    Object that tests the forecast endpoint.
    """
    @staticmethod
    def get(city: str, units: str = None, date: str = None) -> Response:
        """
        Perform a Get request on the `forecast` endpoint.
        :param city: a string object that represents the city to query the weather for.
        :param units: a string object that represents the units the weather data should return.
        :param date: a string object that represents the date to get weather from.
        :return: a Response object.
        """
        url = 'http://127.0.0.1:5005/forecast'
        if not date and not units:
            return requests.get(f'{url}/{city}')
        elif units and not date:
            return requests.get(f'{url}/{city}?unit={units}')
        elif date and not units:
            return requests.get(f'{url}/{city}?at={date}')
        else:
            return requests.get(f'{url}/{city}?unit={units}&at={date}')

    def test_city(self):
        """
        Test the forecast with just the City parameter.
        :return: None
        """
        response = self.get('London')
        self.assertEqual(response.status_code, 200)

    def test_false_city(self):
        """
        Test the forecast with a city that does not exist.
        :return: None
        """
        response = self.get('Winterfell')
        self.assertEqual(response.status_code, 404)

    def test_celsius_unit(self):
        """
        Test the response when the unit is set to metric, the temperature should be in Celsius.
        :return: None
        """
        response = self.get('London', 'metric')
        data = response.json()
        temperature = data['temperature']
        self.assertEqual(temperature[-1], 'C')

    def test_fahrenheit_unit(self):
        """
        Test the response when the unit is set to imperial, the temperature should be in Fahrenheit.
        :return: None
        """
        response = self.get('London', 'imperial')
        data = response.json()
        temperature = data['temperature']
        self.assertEqual(temperature[-1], 'F')

    def test_kelvin_unit(self):
        """
        Test the response when the unit is set to nothing, the temperature should be in Kelvin.
        :return: None
        """
        response = self.get('London')
        data = response.json()
        temperature = data['temperature']
        self.assertEqual(temperature[-1], 'K')

    def test_date(self):
        """
        Test a response with a date.
        :return: None
        """
        date = datetime.now().strftime('%Y-%m-%d')
        response = self.get('London', date=date)
        self.assertEqual(response.status_code, 200)
