from fasthtml.common import *
from fasthtml.common import *
import json
from pathlib import Path
import hashlib
from hmac import compare_digest
import datetime
import requests
from dataclasses import dataclass
from functools import wraps
from weather import (
    get_weather, get_forecast, get_air_quality, get_aqi_description,
    prepare_chart_data, analyze_weather_trends
)

def weather_panel(weather_data, get_air_quality, get_aqi_description):
    if not weather_data:
        return Div("Weather data not available", cls="error-message")
    
    # 获取空气质量数据
    air_quality = get_air_quality(
        weather_data['coord']['lat'], 
        weather_data['coord']['lon']
    )
    
    # 处理空气质量数据
    aqi_info = None
    if air_quality and 'list' in air_quality and air_quality['list']:
        aqi = air_quality['list'][0]['main']['aqi']
        description, color = get_aqi_description(aqi)
        aqi_info = Div(
            H4("空气质量指数"),
            P(f"AQI: {aqi}", style=f"color: {color}; font-weight: bold;"),
            P(f"空气质量: {description}", style=f"color: {color};"),
            cls="aqi-info"
        )
    
    return Card(
        Div(
            H3(f"{weather_data['name']} 当前天气"),
            Grid(
                # 左侧天气信息
                Div(
                    P(f"温度: {weather_data['main']['temp']}°C"),
                    P(f"体感温度: {weather_data['main']['feels_like']}°C"),
                    P(f"天气: {weather_data['weather'][0]['description']}"),
                    P(f"湿度: {weather_data['main']['humidity']}%"),
                    P(f"风速: {weather_data['wind']['speed']}m/s"),
                    cls="weather-info"
                ),
                # 右侧空气质量信息
                aqi_info if aqi_info else None,
                cls="weather-grid"
            ),
            cls="weather-content"
        ),
        cls="weather-card"
    )

def forecast_panel(forecast_data, forecast_type='hourly'):
    """创建预报面板"""
    if not forecast_data:
        return Div("Forecast data not available", cls="error-message")
    
    if forecast_type == 'hourly':
        # 24小时预报
        forecasts = []
        for item in forecast_data['list'][:8]:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            forecasts.append(
                Card(
                    H4(dt.strftime('%H:%M')),
                    P(f"{item['main']['temp']}°C"),
                    P(item['weather'][0]['description']),
                    Img(src=f"http://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png"),
                    P(f"湿度: {item['main']['humidity']}%"),
                    P(f"风速: {item['wind']['speed']}m/s"),
                    P(f"降水概率: {int(item.get('pop', 0) * 100)}%"),
                    cls="forecast-card"
                )
            )
        title = "24小时预报"
    else:
        # 5天预报 - 修改温度计算逻辑
        daily_data = {}
        for item in forecast_data['list']:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            date = dt.strftime('%Y-%m-%d')
            
            if date not in daily_data:
                daily_data[date] = {
                    'temp_max': item['main']['temp_max'],  # 使用API提供的最高温
                    'temp_min': item['main']['temp_min'],  # 使用API提供的最低温
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'humidity': [],
                    'wind_speed': [],
                    'pop': 0
                }
            else:
                # 更新最高温和最低温
                daily_data[date]['temp_max'] = max(daily_data[date]['temp_max'], 
                                                 item['main']['temp_max'])
                daily_data[date]['temp_min'] = min(daily_data[date]['temp_min'], 
                                                 item['main']['temp_min'])
            
            # 收集其他数据
            daily_data[date]['humidity'].append(item['main']['humidity'])
            daily_data[date]['wind_speed'].append(item['wind']['speed'])
            daily_data[date]['pop'] = max(daily_data[date]['pop'], item.get('pop', 0))
        
        forecasts = []
        for date, data in list(daily_data.items())[:5]:
            dt = datetime.datetime.strptime(date, '%Y-%m-%d')
            # 计算平均值
            avg_humidity = sum(data['humidity']) / len(data['humidity'])
            avg_wind_speed = sum(data['wind_speed']) / len(data['wind_speed'])
            
            forecasts.append(
                Card(
                    H4(dt.strftime('%m-%d')),
                    P(f"最高温度: {data['temp_max']:.1f}°C"),
                    P(f"最低温度: {data['temp_min']:.1f}°C"),
                    P(data['description']),
                    Img(src=f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"),
                    P(f"湿度: {avg_humidity:.0f}%"),
                    P(f"风速: {avg_wind_speed:.1f}m/s"),
                    P(f"降水概率: {int(data['pop'] * 100)}%"),
                    cls="forecast-card"
                )
            )
        title = "5天预报"
    
    return Div(
        H3(title, style="text-align: center; margin: 20px 0;"),
        Div(*forecasts, cls="forecast-container"),
        cls="forecast-section"
    )
# Weather components
def weather_panel(weather_data):
    if not weather_data:
        return Div("Weather data not available", cls="error-message")
    
    # 获取空气质量数据
    air_quality = get_air_quality(
        weather_data['coord']['lat'], 
        weather_data['coord']['lon']
    )
    
    # 处理空气质量数据
    aqi_info = None
    if air_quality and 'list' in air_quality and air_quality['list']:
        aqi = air_quality['list'][0]['main']['aqi']
        description, color = get_aqi_description(aqi)
        aqi_info = Div(
            H4("空气质量指数"),
            P(f"AQI: {aqi}", style=f"color: {color}; font-weight: bold;"),
            P(f"空气质量: {description}", style=f"color: {color};"),
            cls="aqi-info"
        )
    
    return Card(
        Div(
            H3(f"{weather_data['name']} 当前天气"),
            Grid(
                # 左侧天气信息
                Div(
                    P(f"温度: {weather_data['main']['temp']}°C"),
                    P(f"体感温度: {weather_data['main']['feels_like']}°C"),
                    P(f"天气: {weather_data['weather'][0]['description']}"),
                    P(f"湿度: {weather_data['main']['humidity']}%"),
                    P(f"风速: {weather_data['wind']['speed']}m/s"),
                    cls="weather-info"
                ),
                # 右侧空气质量信息
                aqi_info if aqi_info else None,
                cls="weather-grid"
            ),
            cls="weather-content"
        ),
        cls="weather-card"
    )


