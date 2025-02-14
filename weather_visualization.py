from typing import Dict, Any, Optional
import datetime

class WeatherVisualizer:
    @staticmethod
    def prepare_chart_data(forecast_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
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
        
        # 收集短期数据
        for item in forecast_data['list'][:8]:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            short_term['times'].append(dt.strftime('%H:%M'))
            short_term['temperatures'].append(item['main']['temp'])
            short_term['humidity'].append(item['main']['humidity'])
            short_term['windSpeed'].append(item['wind']['speed'])
            short_term['precipitation'].append(item.get('pop', 0) * 100)
        
        # 处理5天预报数据
        daily_data = WeatherVisualizer._process_daily_data(forecast_data['list'])
        
        # 整理长期预报数据
        for date, data in list(daily_data.items())[:5]:
            long_term['dates'].append(date)
            long_term['max_temps'].append(data['max_temp'])
            long_term['min_temps'].append(data['min_temp'])
            long_term['humidity'].append(
                sum(data['humidity']) / len(data['humidity']))
            long_term['windSpeed'].append(
                sum(data['wind_speed']) / len(data['wind_speed']))
            long_term['precipitation'].append(data['pop'] * 100)
        
        return {
            'short_term': short_term,
            'long_term': long_term
        }

    @staticmethod
    def _process_daily_data(forecast_list: list) -> Dict[str, Any]:
        daily_data = {}
        
        for item in forecast_list:
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
            
            data = daily_data[date]
            data['max_temp'] = max(data['max_temp'], item['main']['temp_max'])
            data['min_temp'] = min(data['min_temp'], item['main']['temp_min'])
            data['humidity'].append(item['main']['humidity'])
            data['wind_speed'].append(item['wind']['speed'])
            data['pop'] = max(data['pop'], item.get('pop', 0))
            
        return daily_data 