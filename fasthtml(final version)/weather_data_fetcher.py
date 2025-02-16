"""
Module: weather_data_fetcher.py
Description: A module for fetching weather data from the OpenWeatherMap API.

This module provides a simple interface to retrieve current weather data, 5-day forecasts, and air quality information
using the OpenWeatherMap API. It handles API requests and basic error handling, making it easy to integrate weather data into your application.

Note:
    - You need a valid OpenWeatherMap API key to use this module.
    - The API key should be kept secure to avoid unauthorized access.
    - If you encounter issues with API requests, check the API key, city name, latitude, and longitude for accuracy.
    - Network issues may affect API requests; ensure your network connection is stable.
    - If the API requests fail, it might be due to network problems or invalid API links. Please check the links and try again later.

See Also:
    weather_data_processor.py: A module for processing and analyzing weather data.
"""
import requests

class WeatherDataFetcher:
    """
    A utility class for fetching weather data from the OpenWeatherMap API.

    This class provides static methods to retrieve current weather data, 5-day forecasts, and air quality information.
    It handles API requests and basic error handling.

    Attributes:
        API_KEY (str): The API key for accessing the OpenWeatherMap API.
    """
    API_KEY = "ffbd62ce8de707d8aef093dca5dce999"

    @staticmethod
    def get_weather(city):
        """
        Obtain current weather data for a given city.

        Args:
            city (str): The name of the city.

        Returns:
            dict or None: A dictionary containing the current weather data, or None if the request fails.

        Raises:
            requests.RequestException: If the API request fails.
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WeatherDataFetcher.API_KEY}&units=metric&lang=zh_cn"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_forecast(city):
        """
        Obtain 5-day forecast data for a given city.

        Args:
            city (str): The name of the city.

        Returns:
            dict or None: A dictionary containing the 5-day forecast data, or None if the request fails.

        Raises:
            requests.RequestException: If the API request fails.
        """
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WeatherDataFetcher.API_KEY}&units=metric&lang=zh_cn"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_air_quality(lat,lon):
        """
        Obtain air quality data for a given latitude and longitude.

        Args:
            lat (float): The latitude.
            lon (float): The longitude.

        Returns:
            dict or None: A dictionary containing the air quality data, or None if the request fails.

        Raises:
            ValueError: If latitude or longitude is not provided.
            requests.RequestException: If the API request fails.
        """
        if not lat or not lon:
            raise ValueError("Latitude and longitude are required for air quality data")
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WeatherDataFetcher.API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None