from tests.base import BaseTest
from datetime import datetime


class TestForecast(BaseTest):
    """
    Object that handles the `integration` test for the `Forecast` route.
    """
    def test_get_weather_success_response(self) -> None:
        """
        Test the response of a successful call of the `get_weather` method in the Forecast Resource object.
        :return: None
        """
        response = self.resource.get_weather('London', 'metric')
        data, unit = response

        self.assertIsInstance(
            response, tuple, f'Expected to the response to be a tuple object but is instead {type(response)}.'
        )
        self.assertEqual(
            200, int(data['cod'])
            , f'Expected the code inside the data returned to be 200, got {int(data["cod"])} instead.'
        )
        self.assertEqual(
            'metric', unit, f'Expected the units to be metric, got {unit} instead.'
        )

    def test_get_weather_failed_response(self) -> None:
        """
        Test the response of a failed call of the `get_weather` method in the Forecast Resource object.
        :return: None
        """
        response = self.resource.get_weather('Winterfell', 'metric')
        data, unit = response

        self.assertIsInstance(
            response, tuple, f'Expected to the response to be a tuple object but is instead {type(response)}.'
        )
        self.assertEqual(
            404, data.response.status_code
            , f'Expected the code inside the data returned to be 200, got {data.response.status_code} instead.'
        )
        self.assertEqual(
            'metric', unit, f'Expected the units to be metric, got {unit} instead.'
        )

    def test_find_true_index(self) -> None:
        """
        Test the `find_index` method in the Forecast Resource object but with a datetime that does match the
        response data from the OpenWeatherMapAPI, the expected index should be 1.
        :return: None
        """
        data, _ = self.resource.get_weather('London')
        date_raw = data['list'][1]['dt_txt']
        date = datetime.strptime(date_raw, '%Y-%m-%d %H:%M:%S')
        index = self.resource.find_index(data, date)
        self.assertEqual(1, index, f'Expected the index to be 1, got {index} instead.')

    def test_find_false_index(self) -> None:
        """
        Test the `find_index` method in the Forecast Resource object but with a datetime that does not match the
        response data from the OpenWeatherMapAPI, the expected index should be 0.
        :return: None
        """
        data, _ = self.resource.get_weather('London')
        now = datetime.now()
        index = self.resource.find_index(data, now)
        self.assertEqual(0, index, f'Expected the index to be 0, got {index} instead.')
