import requests
import datetime

# API配置
API_KEY = "ffbd62ce8de707d8aef093dca5dce999"

def get_weather(city):
    """获取当前天气数据"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_cn"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_forecast(city):
    """获取5天预报数据"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=zh_cn"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_air_quality(lat, lon):
    """获取空气质量数据"""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_aqi_description(aqi):
    """获取空气质量描述"""
    if aqi <= 50:
        return "优", "green"
    elif aqi <= 100:
        return "良", "#f0ad4e"
    elif aqi <= 150:
        return "轻度污染", "orange"
    elif aqi <= 200:
        return "中度污染", "red"
    elif aqi <= 300:
        return "重度污染", "purple"
    else:
        return "严重污染", "maroon"

def prepare_chart_data(forecast_data):
    """准备图表数据"""
    if not forecast_data:
        return None
    
    # 短期预报（24小时）
    short_term = {
        'times': [],
        'temperatures': [],
        'humidity': [],
        'windSpeed': [],
        'precipitation': []
    }
    
    # 长期预报（5天）
    long_term = {
        'dates': [],
        'max_temps': [],
        'min_temps': [],
        'humidity': [],
        'windSpeed': [],
        'precipitation': []
    }
    
    # 收集数据
    for item in forecast_data['list'][:8]:  # 分析24小时数据
        dt = datetime.datetime.fromtimestamp(item['dt'])
        short_term['times'].append(dt.strftime('%H:%M'))
        short_term['temperatures'].append(item['main']['temp'])
        short_term['humidity'].append(item['main']['humidity'])
        short_term['windSpeed'].append(item['wind']['speed'])
        short_term['precipitation'].append(item.get('pop', 0) * 100)
    
    # 处理5天预报数据
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
    
    # 整理5天预报数据
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

def analyze_weather_trends(forecast_data):
    """分析天气趋势和提供建议"""
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
    timestamps = []  # 添加时间戳列表
    
    # 收集数据
    for item in forecast_data['list'][:8]:  # 分析24小时数据
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
    
    # 温度趋势分析
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
    
    # 舒适度分析
    for temp, humid, wind, dt in zip(temps, humidity, wind_speeds, timestamps):
        time_str = dt.strftime('%H:%M')
        # 计算体感温度
        feels_like = temp - 0.4 * (temp - 10) * (1 - humid/100)
        # 计算风寒指数
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
    
    # 天气预警
    if max(temps) > 35:
        analysis['weather_alerts'].append({
            'type': 'high_temperature',
            'message': '高温预警：注意防暑降温，避免长时间户外活动'
        })
    if max(wind_speeds) > 10.8:  # 5级以上大风
        analysis['weather_alerts'].append({
            'type': 'strong_wind',
            'message': '大风预警：注意防风，户外活动需谨慎'
        })
    if any(h > 85 for h in humidity):
        analysis['weather_alerts'].append({
            'type': 'high_humidity',
            'message': '湿度较大：注意防潮，户外运动可能不适'
        })
    
    # 户外活动建议
    weather_score = 100
    if 'Rain' in weather_conditions or 'Snow' in weather_conditions:
        weather_score -= 30
        analysis['outdoor_suggestions'].append('建议带伞，注意防雨/防雪')
    if max(wind_speeds) > 5:
        weather_score -= 20
        analysis['outdoor_suggestions'].append('风力较大，户外活动注意保暖')
    if max(temps) > 30 or min(temps) < 10:
        weather_score -= 20
        analysis['outdoor_suggestions'].append('温度不适，建议适当调整户外活动时间')
    
    analysis['outdoor_activity_score'] = max(0, weather_score)
    
    # 生成趋势描述
    trend_desc = []
    if analysis['temperature_trend']['trend'] == 'rising':
        trend_desc.append('温度呈上升趋势')
    elif analysis['temperature_trend']['trend'] == 'falling':
        trend_desc.append('温度呈下降趋势')
    else:
        trend_desc.append('温度相对稳定')
    
    if 'Rain' in weather_conditions:
        trend_desc.append('有降雨')
    if max(wind_speeds) > 5:
        trend_desc.append('风力较大')
    
    analysis['trend_description'] = '，'.join(trend_desc) + '。'
    
    return analysis 