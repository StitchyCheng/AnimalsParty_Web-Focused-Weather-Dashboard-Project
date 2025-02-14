import unittest
from main import analyze_weather_trends, prepare_chart_data
import datetime
from typing import Dict, Any, Optional

class TestWeatherAnalysis(unittest.TestCase):
    def setUp(self):
        # 创建模拟的天气预报数据
        self.mock_forecast_data = {
            'list': [
                {
                    'dt': int(datetime.datetime.now().timestamp()),
                    'main': {
                        'temp': 25,
                        'temp_min': 20,
                        'temp_max': 30,
                        'humidity': 60,
                        'feels_like': 26
                    },
                    'weather': [{'main': 'Clear', 'description': 'clear sky'}],
                    'wind': {'speed': 3.5}
                }
            ] * 8  # 复制8次模拟24小时数据
        }

    def test_analyze_weather_trends(self):
        analysis = analyze_weather_trends(self.mock_forecast_data)
        
        # 验证分析结果的结构
        self.assertIsNotNone(analysis)
        self.assertIn('temperature_trend', analysis)
        self.assertIn('comfort_analysis', analysis)
        self.assertIn('weather_alerts', analysis)
        self.assertIn('outdoor_suggestions', analysis)
        self.assertIn('trend_description', analysis)
        
        # 验证温度趋势数据
        temp_trend = analysis['temperature_trend']
        self.assertIn('min', temp_trend)
        self.assertIn('max', temp_trend)
        self.assertIn('trend', temp_trend)
        
        # 验证舒适度分析
        self.assertTrue(len(analysis['comfort_analysis']) > 0)
        
    def test_prepare_chart_data(self):
        chart_data = prepare_chart_data(self.mock_forecast_data)
        
        # 验证图表数据结构
        self.assertIsNotNone(chart_data)
        self.assertIn('short_term', chart_data)
        self.assertIn('long_term', chart_data)
        
        # 验证短期数据
        short_term = chart_data['short_term']
        self.assertIn('times', short_term)
        self.assertIn('temperatures', short_term)
        self.assertIn('humidity', short_term)
        self.assertIn('windSpeed', short_term)
        self.assertIn('precipitation', short_term)
        
        # 验证长期数据
        long_term = chart_data['long_term']
        self.assertIn('dates', long_term)
        self.assertIn('max_temps', long_term)
        self.assertIn('min_temps', long_term)
        self.assertIn('humidity', long_term)
        self.assertIn('windSpeed', long_term)
        self.assertIn('precipitation', long_term)

    def test_null_data_handling(self):
        # 测试空数据处理
        self.assertIsNone(analyze_weather_trends(None))
        self.assertIsNone(prepare_chart_data(None))

class WeatherAnalyzer:
    @staticmethod
    def analyze_weather_trends(forecast_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
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
        timestamps = []
        
        # 收集数据
        for item in forecast_data['list'][:8]:
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
            feels_like = temp - 0.4 * (temp - 10) * (1 - humid/100)
            wind_chill = 13.12 + 0.6215 * temp - 11.37 * (wind ** 0.16) + 0.3965 * temp * (wind ** 0.16)
            
            comfort_level = WeatherAnalyzer._get_comfort_level(feels_like)
            
            analysis['comfort_analysis'][time_str] = {
                'temp': round(temp, 1),
                'feels_like': round(feels_like, 1),
                'wind_chill': round(wind_chill, 1),
                'comfort_level': comfort_level
            }
        
        # 天气预警
        WeatherAnalyzer._add_weather_alerts(analysis, temps, wind_speeds, humidity)
        
        # 户外活动建议
        weather_score = WeatherAnalyzer._calculate_outdoor_score(
            temps, wind_speeds, weather_conditions)
        analysis['outdoor_activity_score'] = weather_score
        
        # 生成趋势描述
        analysis['trend_description'] = WeatherAnalyzer._generate_trend_description(
            analysis['temperature_trend']['trend'], 
            weather_conditions, 
            wind_speeds
        )
        
        return analysis

    @staticmethod
    def _get_comfort_level(feels_like: float) -> str:
        if feels_like < 10:
            return 'cold'
        elif feels_like > 28:
            return 'hot'
        return 'comfortable'

    @staticmethod
    def _add_weather_alerts(analysis: Dict[str, Any], 
                          temps: list, 
                          wind_speeds: list, 
                          humidity: list) -> None:
        if max(temps) > 35:
            analysis['weather_alerts'].append({
                'type': 'high_temperature',
                'message': '高温预警：注意防暑降温，避免长时间户外活动'
            })
        if max(wind_speeds) > 10.8:
            analysis['weather_alerts'].append({
                'type': 'strong_wind',
                'message': '大风预警：注意防风，户外活动需谨慎'
            })
        if any(h > 85 for h in humidity):
            analysis['weather_alerts'].append({
                'type': 'high_humidity',
                'message': '湿度较大：注意防潮，户外运动可能不适'
            })

    @staticmethod
    def _calculate_outdoor_score(temps: list, 
                               wind_speeds: list, 
                               weather_conditions: list) -> int:
        weather_score = 100
        
        if 'Rain' in weather_conditions or 'Snow' in weather_conditions:
            weather_score -= 30
        if max(wind_speeds) > 5:
            weather_score -= 20
        if max(temps) > 30 or min(temps) < 10:
            weather_score -= 20
            
        return max(0, weather_score)

    @staticmethod
    def _generate_trend_description(temp_trend: str, 
                                  weather_conditions: list, 
                                  wind_speeds: list) -> str:
        trend_desc = []
        
        if temp_trend == 'rising':
            trend_desc.append('温度呈上升趋势')
        elif temp_trend == 'falling':
            trend_desc.append('温度呈下降趋势')
        else:
            trend_desc.append('温度相对稳定')
        
        if 'Rain' in weather_conditions:
            trend_desc.append('有降雨')
        if max(wind_speeds) > 5:
            trend_desc.append('风力较大')
        
        return '，'.join(trend_desc) + '。'

if __name__ == '__main__':
    unittest.main() 