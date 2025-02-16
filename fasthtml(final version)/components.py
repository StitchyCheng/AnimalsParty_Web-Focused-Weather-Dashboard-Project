"""
components.py

This module contains functions to generate HTML components for displaying weather data.
It provides reusable components for creating weather panels and forecast panels.

Functions:
    weather_panel(weather_data, get_air_quality=False, get_aqi_description=None):
        Generate a weather panel with current weather information and air quality data.
    forecast_panel(forecast_data, forecast_type='hourly'):
        Generate a forecast panel with hourly or daily forecast data.
"""
from fasthtml.common import *
import json
from pathlib import Path
import hashlib
from hmac import compare_digest
import datetime
import requests
from dataclasses import dataclass
from functools import wraps
from weather_data_fetcher import WeatherDataFetcher
from weather_data_processor import WeatherDataProcessor

def weather_panel(weather_data, get_air_quality, get_aqi_description):
    if not weather_data:
        return Div("Weather data not available", cls="error-message")
    """
    Generate a weather panel with current weather information and air quality data.

    Args:
        weather_data (dict): A dictionary containing current weather data.
        get_air_quality (bool, optional): Whether to retrieve air quality data. Defaults to False.
        get_aqi_description (function, optional): A function to get AQI description. Defaults to None.

    Returns:
        Card: A weather panel card containing weather information and air quality data.

    Raises:
        None
    """
    # Retrieve air quality data
    air_quality = WeatherDataFetcher.get_air_quality(
        weather_data['coord']['lat'], 
        weather_data['coord']['lon']
    )
    
    # Process air quality data
    aqi_info = None
    if air_quality and 'list' in air_quality and air_quality['list']:
        aqi = air_quality['list'][0]['main']['aqi']
        description, color = WeatherDataProcessor.get_aqi_description(aqi)
        aqi_info = Div(
            H4("Air Quality Index"),
            P(f"AQI: {aqi}", style=f"color: {color}; font-weight: bold;"),
            P(f"Air Quality: {description}", style=f"color: {color};"),
            cls="aqi-info"
        )
    
    return Card(
        Div(
            H3(f"{weather_data['name']} Current Weather"),
            Grid(
                # Left weather information
                Div(
                    P(f"Temperature: {weather_data['main']['temp']}°C"),
                    P(f"Perceived Temperature: {weather_data['main']['feels_like']}°C"),
                    P(f"Weather: {weather_data['weather'][0]['description']}"),
                    P(f"Humidity: {weather_data['main']['humidity']}%"),
                    P(f"Wind Speed: {weather_data['wind']['speed']}m/s"),
                    cls="weather-info"
                ),
                # Right air quality information
                aqi_info if aqi_info else None,
                cls="weather-grid"
            ),
            cls="weather-content"
        ),
        cls="weather-card"
    )

def forecast_panel(forecast_data, forecast_type='hourly'):
    """
    Generate a forecast panel with hourly or daily forecast data.

    Args:
        forecast_data (dict): A dictionary containing forecast data.
        forecast_type (str, optional): Type of forecast to display. Defaults to 'hourly'.

    Returns:
        Div: A forecast panel containing hourly or daily forecast information.

    Raises:
        None
    """
    if not forecast_data:
        return Div("Forecast data not available", cls="error-message")
    
    if forecast_type == 'hourly':
        # 24-hour forecast
        forecasts = []
        for item in forecast_data['list'][:8]:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            forecasts.append(
                Card(
                    H4(dt.strftime('%H:%M')),
                    P(f"{item['main']['temp']}°C"),
                    P(item['weather'][0]['description']),
                    Img(src=f"http://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png"),
                    P(f"Humidity: {item['main']['humidity']}%"),
                    P(f"Wind Speed: {item['wind']['speed']}m/s"),
                    P(f"Precipitation probability: {int(item.get('pop', 0) * 100)}%"),
                    cls="forecast-card"
                )
            )
        title = "24-hour Forecast"
    else:
        # 5-day forecast
        daily_data = {}
        for item in forecast_data['list']:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            date = dt.strftime('%Y-%m-%d')
            
            if date not in daily_data:
                daily_data[date] = {
                    'temp_max': item['main']['temp_max'],  # Use the highest temperature provided by the API
                    'temp_min': item['main']['temp_min'],  # Use the lowest temperature provided by the API
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'humidity': [],
                    'wind_speed': [],
                    'pop': 0
                }
            else:
                # Update the highest and lowest temperatures
                daily_data[date]['temp_max'] = max(daily_data[date]['temp_max'], 
                                                 item['main']['temp_max'])
                daily_data[date]['temp_min'] = min(daily_data[date]['temp_min'], 
                                                 item['main']['temp_min'])
            
            # Collect other data
            daily_data[date]['humidity'].append(item['main']['humidity'])
            daily_data[date]['wind_speed'].append(item['wind']['speed'])
            daily_data[date]['pop'] = max(daily_data[date]['pop'], item.get('pop', 0))
        
        forecasts = []
        for date, data in list(daily_data.items())[:5]:
            dt = datetime.datetime.strptime(date, '%Y-%m-%d')
            # Calculate average values
            avg_humidity = sum(data['humidity']) / len(data['humidity'])
            avg_wind_speed = sum(data['wind_speed']) / len(data['wind_speed'])
            
            forecasts.append(
                Card(
                    H4(dt.strftime('%m-%d')),
                    P(f"Max Temperature: {data['temp_max']:.1f}°C"),
                    P(f"Min Temperature: {data['temp_min']:.1f}°C"),
                    P(data['description']),
                    Img(src=f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"),
                    P(f"Humidity: {avg_humidity:.0f}%"),
                    P(f"Wind Speed: {avg_wind_speed:.1f}m/s"),
                    P(f"Precipitation probability: {int(data['pop'] * 100)}%"),
                    cls="forecast-card"
                )
            )
        title = "Weather Forecast in 5 days"
    
    return Div(
        H3(title, style="text-align: center; margin: 20px 0;"),
        Div(*forecasts, cls="forecast-container"),
        cls="forecast-section"
    )

# Weather components
def weather_panel(weather_data):
    if not weather_data:
        return Div("Weather data not available", cls="error-message")
    
    # Retrieve air quality data
    air_quality = WeatherDataFetcher.get_air_quality(
        weather_data['coord']['lat'], 
        weather_data['coord']['lon']
    )
    
    # Process air quality data
    aqi_info = None
    if air_quality and 'list' in air_quality and air_quality['list']:
        aqi = air_quality['list'][0]['main']['aqi']
        description, color = WeatherDataProcessor.get_aqi_description(aqi)
        aqi_info = Div(
            H4("Air Quality Index"),
            P(f"AQI: {aqi}", style=f"color: {color}; font-weight: bold;"),
            P(f"Air Quality: {description}", style=f"color: {color};"),
            cls="aqi-info"
        )
    
    return Card(
        Div(
            H3(f"{weather_data['name']} Current Weather"),
            Grid(
                # Left weather information
                Div(
                    P(f"Temperature: {weather_data['main']['temp']}°C"),
                    P(f"Perceived Temperature: {weather_data['main']['feels_like']}°C"),
                    P(f"Weather: {weather_data['weather'][0]['description']}"),
                    P(f"Humidity: {weather_data['main']['humidity']}%"),
                    P(f"Wind Speed: {weather_data['wind']['speed']}m/s"),
                    cls="weather-info"
                ),
                # Right air quality information
                aqi_info if aqi_info else None,
                cls="weather-grid"
            ),
            cls="weather-content"
        ),
        cls="weather-card"
    )