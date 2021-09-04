from tests.base import BaseTest


class TestForecast(BaseTest):
    """
    Object that handles the `unit` tests for the Forecast Resource.
    """
    def test_metric_unit(self) -> None:
        """
        Test the `check_unit` method in the Forecast Resource.
        :return: None
        """
        unit = self.resource.check_unit('metric')
        self.assertEqual('C', unit, f'Expected the unit to be `C`, got {unit} instead')

    def test_imperial_unit(self) -> None:
        """
        Test the `check_unit` method in the Forecast Resource.
        :return: None
        """
        unit = self.resource.check_unit('imperial')
        self.assertEqual('F', unit, f'Expected the unit to be `F`, got {unit} instead')

    def test_default_unit(self) -> None:
        """
        Test the `check_unit` method in the Forecast Resource.
        :return: None
        """
        unit = self.resource.check_unit('unit')
        self.assertEqual('K', unit, f'Expected the unit to be `K`, got {unit} instead')
