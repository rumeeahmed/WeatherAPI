from system_base import SystemBase
from datetime import datetime, timedelta


class ForecastTest(SystemBase):
    """
    Object that performs system tests the `forecast` endpoint.
    """
    @staticmethod
    def get_current_time() -> datetime:
        """
        Get the current time with the current timezone information.
        :return: a timezone aware datetime object.
        """
        timezone = datetime.now().astimezone().tzinfo
        now = datetime.now(tz=timezone)
        return now

    def test_city(self) -> None:
        """
        Test the forecast with just the `city` parameter.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/forecast/London')
            self.assertEqual(
                200, response.status_code,
                f'Expected the response status code to be 200, got {response.status_code} instead.'
            )

    def test_false_city(self) -> None:
        """
        Test the forecast with a `city` that does not exist.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/forecast/Winterfell')
            self.assertEqual(
                404, response.status_code,
                f'Expected the response status code to be 200, got {response.status_code} instead.'
            )

    def test_celsius_unit(self) -> None:
        """
        Test the response when the `unit` is set to metric, the temperature should be in Celsius.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/forecast/London?unit=metric')
            data = response.json
            temperature = data['temperature']
            self.assertEqual(
                'C', temperature[-1],
                f'Expected the temperature units in `C`, got {temperature[-1]} instead'
            )

    def test_fahrenheit_unit(self) -> None:
        """
        Test the response when the unit is set to imperial, the temperature should be in Fahrenheit.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/forecast/London?unit=imperial')
            data = response.json
            temperature = data['temperature']
            self.assertEqual(
                'F', temperature[-1],
                f'Expected the temperature units in `F`, got {temperature[-1]} instead'
            )

    def test_kelvin_unit(self) -> None:
        """
        Test the response when the unit is set to `Kelvin`.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/forecast/London?unit=kelvin')
            data = response.json
            temperature = data['temperature']
            self.assertEqual(
                'K', temperature[-1],
                f'Expected the temperature units in `K`, got {temperature[-1]} instead'
            )

    def test_no_unit_specified(self) -> None:
        """
        Test the response when the unit is set to nothing, the temperature should be in Kelvin.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/forecast/London')
            data = response.json
            temperature = data['temperature']
            self.assertEqual(
                'K', temperature[-1],
                f'Expected the temperature units in `K`, got {temperature[-1]} instead'
            )

    def test_date(self) -> None:
        """
        Test a response with a date.
        :return: None
        """
        date = datetime.now().strftime('%Y-%m-%d')
        with self.test_client() as test_client:
            response = test_client.get(f'/forecast/London?units=metric&at={date}')
            self.assertEqual(
                200, response.status_code,
                f'Expected the response status code to be 200, got {response.status_code} instead.'
            )

    def test_date_time(self) -> None:
        """
        Test the response when a datetime string is given.
        :return: None
        """
        now = self.get_current_time()

        # Add 10 minutes to the current date to ensure that that time is slightly in the future so the previous date
        # error is not triggered.
        minutes = timedelta(minutes=10)
        now += minutes

        # Get the string representation of the date to use to make the request.
        date = now.strftime('%Y-%m-%dT%H:%M:%S%z')

        with self.test_client() as test_client:
            response = test_client.get(f'/forecast/London?units=metric&at={date}')
            self.assertEqual(
                200, response.status_code,
                f'Expected the response status code to be 200, got {response.status_code} instead.'
            )

    def test_previous_date(self) -> None:
        """
        Test the response when an old date is given.
        :return: None
        """
        now = self.get_current_time()
        day = timedelta(days=1)
        now -= day
        # Get the string representation of the date to use to make the request.
        date = now.strftime('%Y-%m-%dT%H:%M:%S%z')
        with self.test_client() as test_client:
            response = test_client.get(f'/forecast/London?units=metric&at={date}').json

        self.assertEqual(
            'invalid_date', response['error_code'],
            f'Expected the the JSON to return `invalid_date`, got {response["error_code"]} instead'
        )

    def test_server_error(self) -> None:
        """
        Test the response for a internal server error by sending an invalid datetime string.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/forecast/London?units=metric&at=2021-08-25T19:33:0x0+00:00')

        self.assertEqual(
            500, response.status_code,
            f'Expected the response status code to be 500, got {response.status_code} instead.'
        )
