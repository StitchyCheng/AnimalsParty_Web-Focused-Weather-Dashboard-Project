import pytest
import requests
from weather_data_fetcher import WeatherDataFetcher
from weather_data_processor import WeatherDataProcessor

"""
Module: test_weather.py
Description: This module contains unit tests for the weather data fetching and processing functionality.
"""

class TestWeatherDataFetching:
    """
    A test class for verifying the functionality of weather data fetching methods.
    """

    @staticmethod
    def test_get_weather():
        """
        Test retrieving current weather data.

        This test verifies that the get_weather method of WeatherDataFetcher can successfully fetch
        current weather data for a given city. It checks if the response is not None, the request was
        successful (cod == 200), and the data contains main weather information.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        weather_data = WeatherDataFetcher.get_weather("Berlin")
        assert weather_data is not None
        assert weather_data.get('cod') == 200  # Ensure the request was successful
        assert 'main' in weather_data  # Ensure the data contains main weather information

    @staticmethod
    def test_get_forecast():
        """
        Test retrieving forecast data.

        This test verifies that the get_forecast method of WeatherDataFetcher can successfully fetch
        forecast data for a given city. It checks if the response is not None, the request was
        successful (cod == 200), and the data contains forecast information.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        forecast_data = WeatherDataFetcher.get_forecast("Berlin")
        assert forecast_data is not None
        assert forecast_data.get('cod') == '200'  # Ensure the request was successful
        assert 'list' in forecast_data  # Ensure the data contains forecast information

    @staticmethod
    def test_get_air_quality():
        """
        Test retrieving air quality data.

        This test verifies that the get_air_quality method of WeatherDataFetcher can successfully fetch
        air quality data for a given latitude and longitude. It checks if the response is not None and
        the data contains air quality information.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        air_quality_data = WeatherDataFetcher.get_air_quality(52.52, 13.405)
        assert air_quality_data is not None
        assert len(air_quality_data.get('list', [])) > 0  # Ensure the data contains air quality information


class TestWeatherDataProcessing:
    """
    A test class for verifying the functionality of weather data processing methods.
    """

    @staticmethod
    def test_prepare_chart_data():
        """
        Test data processing for chart preparation.

        This test verifies that the prepare_chart_data method of WeatherDataProcessor can successfully
        process forecast data and prepare chart data. It checks if the processed data is not None and
        contains both short-term and long-term forecast information.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        forecast_data = WeatherDataFetcher.get_forecast("Berlin")
        chart_data = WeatherDataProcessor.prepare_chart_data(forecast_data)
        assert chart_data is not None
        assert 'short_term' in chart_data
        assert 'long_term' in chart_data

    @staticmethod
    def test_get_aqi_description():
        """
        Test air quality index description.

        This test verifies that the get_aqi_description method of WeatherDataProcessor can successfully
        provide an air quality description and color for a given AQI value. It checks if the description
        and color match the expected values.

        Args:
            None

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        description, color = WeatherDataProcessor.get_aqi_description(50)
        assert description == "Excellent"
        assert color == "green"