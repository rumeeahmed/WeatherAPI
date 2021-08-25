import unittest
import requests
from requests import Response


class ForecastTest(unittest.TestCase):
    """
    Object that tests the forecast endpoint.
    """
    @staticmethod
    def get(city: str, units: str = None, date: str = None,) -> Response:
        """
        Perform a Get request on the `forecast` endpoint.
        :param city: a string object that represents the city to query the weather for.
        :param units: a string object that represents the units the weather data should return.
        :param date: a string object that represents the date to get weather from.
        :return: a Response object.
        """
        return requests.get(f'http://127.0.0.1:5005/forecast/{city}?units={units}&at={date}')

    def test_weather(self):
        response = self.get('London', 'metric')
        print(response.json())
