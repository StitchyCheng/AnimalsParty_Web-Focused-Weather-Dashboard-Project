"""
weather_data_processor.py

This module provides a utility class, WeatherDataProcessor, for processing and analyzing weather data.
It includes methods for obtaining AQI descriptions, preparing chart data, and analyzing weather trends.

Classes:
    WeatherDataProcessor: A utility class for processing weather data.

Methods:
    get_aqi_description(aqi): Obtain an air quality description based on AQI value.
    prepare_chart_data(forecast_data): Prepare data for short-term (24 hours) and long-term (5 days) weather charts.
    analyze_weather_trends(forecast_data): Analyze weather trends and provide insights, alerts, and suggestions.
"""

import datetime

class WeatherDataProcessor:
    """
    A utility class for processing and analyzing weather data.

    This class provides methods for obtaining AQI descriptions, preparing chart data, and analyzing weather trends.
    It is designed to work with weather data from APIs like OpenWeatherMap.
    """
    @staticmethod
    def get_aqi_description(aqi):
        """
        Obtain an air quality description based on the AQI value.

        Args:
            aqi (int): The Air Quality Index value.

        Returns:
            tuple: A tuple containing the air quality description and a corresponding color code.

        Example:
            >>> description, color = WeatherDataProcessor.get_aqi_description(75)
            >>> print(description, color)
            good #f0ad4e
        """
        if aqi <= 50:
            return "Excellent", "green"
        elif aqi <= 100:
            return "good", "#f0ad4e"
        elif aqi <= 150:
            return "Light pollution", "orange"
        elif aqi <= 200:
            return "Moderate pollution", "red"
        elif aqi <= 300:
            return "Heavy pollution", "purple"
        else:
            return "Severe pollution", "maroon"

    @staticmethod
    def prepare_chart_data(forecast_data):
        """
        Prepare data for short-term (24 hours) and long-term (5 days) weather charts.

        Args:
            forecast_data (dict): A dictionary containing forecast data.
                Expected keys:
                    - 'list': List of forecast items with keys 'dt', 'main', 'weather', 'wind', and 'pop'.

        Returns:
            dict: A dictionary containing prepared data for short-term and long-term charts.
                Keys:
                    - 'short_term': Data for the next 24 hours.
                    - 'long_term': Data for the next 5 days.

        Example:
            >>> chart_data = WeatherDataProcessor.prepare_chart_data(forecast_data)
            >>> print(chart_data)
        """
        if not forecast_data:
            return None
        
        # Short Term Forecast (24 hours)
        short_term = {
            'times': [],
            'temperatures': [],
            'humidity': [],
            'windSpeed': [],
            'precipitation': []
        }
        
        # Long term Forecast (5 days)
        long_term = {
            'dates': [],
            'max_temps': [],
            'min_temps': [],
            'humidity': [],
            'windSpeed': [],
            'precipitation': []
        }
        
        # collect data
        for item in forecast_data['list'][:8]:  # Analyze 24-hour data
            dt = datetime.datetime.fromtimestamp(item['dt'])
            short_term['times'].append(dt.strftime('%H:%M'))
            short_term['temperatures'].append(item['main']['temp'])
            short_term['humidity'].append(item['main']['humidity'])
            short_term['windSpeed'].append(item['wind']['speed'])
            short_term['precipitation'].append(item.get('pop', 0) * 100)
        
        # processing 5-day forecast data
        daily_data = {}
        for item in forecast_data['list']:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            date = dt.strftime('%Y-%m-%d')
            
            if date not in daily_data:
                daily_data[date] = {
                    'max_temp': float('-inf'),
                    'min_temp': float('inf'),
                    'humidity': [],
                    'wind_speed': [],
                    'pop': 0
                }
            
            daily_data[date]['max_temp'] = max(daily_data[date]['max_temp'], item['main']['temp_max'])
            daily_data[date]['min_temp'] = min(daily_data[date]['min_temp'], item['main']['temp_min'])
            daily_data[date]['humidity'].append(item['main']['humidity'])
            daily_data[date]['wind_speed'].append(item['wind']['speed'])
            daily_data[date]['pop'] = max(daily_data[date]['pop'], item.get('pop', 0))
        
        # Organize 5-day forecast data
        for date, data in list(daily_data.items())[:5]:
            long_term['dates'].append(date)
            long_term['max_temps'].append(data['max_temp'])
            long_term['min_temps'].append(data['min_temp'])
            long_term['humidity'].append(sum(data['humidity']) / len(data['humidity']))
            long_term['windSpeed'].append(sum(data['wind_speed']) / len(data['wind_speed']))
            long_term['precipitation'].append(data['pop'] * 100)
        
        return {
            'short_term': short_term,
            'long_term': long_term
        }

    @staticmethod
    def analyze_weather_trends(forecast_data):
        """
        Analyze weather trends and provide insights, alerts, and suggestions.

        Args:
            forecast_data (dict): A dictionary containing forecast data.
                Expected keys:
                    - 'list': List of forecast items with keys 'dt', 'main', 'weather', 'wind', and 'pop'.

        Returns:
            dict: A dictionary containing the analysis results, including:
                - 'temperature_trend': Temperature trend information.
                - 'comfort_analysis': Comfort level analysis for each time point.
                - 'weather_alerts': Weather alerts (e.g., high temperature, strong wind).
                - 'outdoor_suggestions': Suggestions for outdoor activities.
                - 'trend_description': A summary description of the weather trends.
            """
        if not forecast_data:
            return None
        
        analysis = {
            'temperature_trend': {},
            'comfort_analysis': {},
            'weather_alerts': [],
            'outdoor_suggestions': [],
            'trend_description': ''
        }
        
        temps = []
        humidity = []
        wind_speeds = []
        weather_conditions = []
        timestamps = []  # Add timestamp list
        
        # Collecting data
        for item in forecast_data['list'][:8]:  # Analyze 24-hour data
            dt = datetime.datetime.fromtimestamp(item['dt'])
            temp = item['main']['temp']
            humid = item['main']['humidity']
            wind = item['wind']['speed']
            condition = item['weather'][0]['main']
            
            temps.append(temp)
            humidity.append(humid)
            wind_speeds.append(wind)
            weather_conditions.append(condition)
            timestamps.append(dt)
        
        # Temperature trend analysis
        temp_min, temp_max = min(temps), max(temps)
        temp_change = temps[-1] - temps[0]
        min_temp_time = timestamps[temps.index(temp_min)].strftime('%H:%M')
        max_temp_time = timestamps[temps.index(temp_max)].strftime('%H:%M')
        
        analysis['temperature_trend'] = {
            'min': temp_min,
            'min_time': min_temp_time,
            'max': temp_max,
            'max_time': max_temp_time,
            'change': temp_change,
            'trend': 'rising' if temp_change > 2 else 'falling' if temp_change < -2 else 'stable'
        }
        
        # Comfort analysis
        for temp, humid, wind, dt in zip(temps, humidity, wind_speeds, timestamps):
            time_str = dt.strftime('%H:%M')
            # Calculate the perceived temperature
            feels_like = temp - 0.4 * (temp - 10) * (1 - humid/100)
            # Calculate the wind chill index
            wind_chill = 13.12 + 0.6215 * temp - 11.37 * (wind ** 0.16) + 0.3965 * temp * (wind ** 0.16)
            
            comfort_level = 'comfortable'
            if feels_like < 10:
                comfort_level = 'cold'
            elif feels_like > 28:
                comfort_level = 'hot'
            
            analysis['comfort_analysis'][time_str] = {
                'temp': round(temp, 1),
                'feels_like': round(feels_like, 1),
                'wind_chill': round(wind_chill, 1),
                'comfort_level': comfort_level
            }
        
        # Weather warning
        if max(temps) > 35:
            analysis['weather_alerts'].append({
                'type': 'high_temperature',
                'message': 'High temperature warning: Pay attention to heat and avoid prolonged outdoor activities.'
            })
        if max(wind_speeds) > 10.8:  # Strong wind (above 5级)
            analysis['weather_alerts'].append({
                'type': 'strong_wind',
                'message': 'High wind warning: Pay attention to the wind, outdoor activities need to be cautious'
            })
        if any(h > 85 for h in humidity):
            analysis['weather_alerts'].append({
                'type': 'high_humidity',
                'message': 'High humidity: pay attention to moisture, outdoor exercise may be uncomfortable'
            })
        
        # Outdoor activity suggestions
        weather_score = 100
        if 'Rain' in weather_conditions or 'Snow' in weather_conditions:
            weather_score -= 30
            analysis['outdoor_suggestions'].append('It is recommended to bring an umbrella and take precautions against rain/snow.')
        if max(wind_speeds) > 5:
            weather_score -= 20
            analysis['outdoor_suggestions'].append('The wind is strong. Pay attention to keeping warm during outdoor activities.')
        if max(temps) > 30 or min(temps) < 10:
            weather_score -= 20
            analysis['outdoor_suggestions'].append('The temperature is not ideal. It is recommended to adjust the timing of outdoor activities accordingly.')
        
        analysis['outdoor_activity_score'] = max(0, weather_score)
        
        # Generate trend description
        trend_desc = []
        if analysis['temperature_trend']['trend'] == 'rising':
            trend_desc.append('The temperature shows a upward trend.')
        elif analysis['temperature_trend']['trend'] == 'falling':
            trend_desc.append('The temperature shows a downward trend.')
        else:
            trend_desc.append('Temperature relative stability')
        
        if 'Rain' in weather_conditions:
            trend_desc.append('There is rain.')
        if max(wind_speeds) > 5:
            trend_desc.append('Wind is strong.')
        
        analysis['trend_description'] = ', '.join(trend_desc) + '.'
        
        return analysis