import requests
import json
from datetime import datetime
import unittest
from main import get_weather, get_forecast, get_air_quality, API_KEY
from typing import Optional, Dict, Any

def test_weather_api():
    """测试OpenWeather API是否可用"""
    
    # API配置
    API_KEY = "ffbd62ce8de707d8aef093dca5dce999"
    city = "shanghai"
    
    # 当前天气API端点
    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_cn"
    # 5天预报API端点
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=zh_cn"
    # 空气质量API端点
    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat=31.2222&lon=121.4581&appid={API_KEY}"
    
    try:
        print(f"正在测试OpenWeather API...")
        
        # 1. 获取当前天气
        print("\n1. 测试当前天气数据")
        print(f"请求URL: {current_url}")
        current_response = requests.get(current_url, timeout=10)
        
        if current_response.status_code == 200:
            data = current_response.json()
            print("\n当前天气数据:")
            print(f"城市: {data['name']}")
            print(f"天气: {data['weather'][0]['description']}")
            print(f"温度: {data['main']['temp']}°C")
            print(f"体感温度: {data['main']['feels_like']}°C")
            print(f"最高温度: {data['main']['temp_max']}°C")
            print(f"最低温度: {data['main']['temp_min']}°C")
            print(f"湿度: {data['main']['humidity']}%")
            print(f"气压: {data['main']['pressure']}hPa")
            print(f"风速: {data['wind']['speed']}m/s")
            print(f"风向: {data['wind']['deg']}°")
            print(f"云量: {data['clouds']['all']}%")
            if 'rain' in data:
                print(f"降雨量(1h): {data['rain'].get('1h', 0)}mm")
            if 'snow' in data:
                print(f"降雪量(1h): {data['snow'].get('1h', 0)}mm")
            print(f"日出时间: {datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')}")
            print(f"日落时间: {datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')}")
        
        # 2. 获取天气预报
        print("\n2. 测试天气预报数据")
        print(f"请求URL: {forecast_url}")
        forecast_response = requests.get(forecast_url, timeout=10)
        
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            print("\n未来5天天气预报:")
            prev_date = None
            for item in forecast_data['list']:
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                time = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
                if date != prev_date:
                    print(f"\n日期: {date}")
                    prev_date = date
                print(f"\n时间: {time}")
                print(f"天气: {item['weather'][0]['description']}")
                print(f"温度: {item['main']['temp']}°C")
                print(f"湿度: {item['main']['humidity']}%")
                print(f"风速: {item['wind']['speed']}m/s")
        
        # 3. 获取空气质量数据
        print("\n3. 测试空气质量数据")
        print(f"请求URL: {air_url}")
        air_response = requests.get(air_url, timeout=10)
        
        if air_response.status_code == 200:
            air_data = air_response.json()
            aqi_levels = {
                1: "优", 2: "良", 3: "轻度污染",
                4: "中度污染", 5: "重度污染"
            }
            print("\n空气质量数据:")
            aqi = air_data['list'][0]['main']['aqi']
            components = air_data['list'][0]['components']
            print(f"空气质量指数(AQI): {aqi} - {aqi_levels.get(aqi, '未知')}")
            print(f"CO浓度: {components['co']}μg/m³")
            print(f"NO浓度: {components['no']}μg/m³")
            print(f"NO2浓度: {components['no2']}μg/m³")
            print(f"O3浓度: {components['o3']}μg/m³")
            print(f"SO2浓度: {components['so2']}μg/m³")
            print(f"PM2.5: {components['pm2_5']}μg/m³")
            print(f"PM10: {components['pm10']}μg/m³")
            print(f"NH3浓度: {components['nh3']}μg/m³")
            
            return True
            
        else:
            print(f"\n请求失败!")
            print(f"状态码: {current_response.status_code}")
            print(f"错误信息: {current_response.text}")
            return False
            
    except Exception as e:
        print(f"\n测试过程中出现错误:")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        return False

def main():
    print("开始OpenWeather API测试...")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    result = test_weather_api()
    
    print("-" * 50)
    print(f"测试结果: {'成功' if result else '失败'}")

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.test_city = "wenzhou"
        self.invalid_city = "nonexistentcity123456789"
        self.lat = 28.0
        self.lon = 120.7
        
    def test_get_weather(self):
        # 测试有效城市
        result = get_weather(self.test_city)
        self.assertIsNotNone(result)
        self.assertIn('name', result)
        self.assertIn('main', result)
        self.assertIn('weather', result)
        
        # 测试无效城市
        result = get_weather(self.invalid_city)
        self.assertIsNone(result)
        
    def test_get_forecast(self):
        # 测试有效城市
        result = get_forecast(self.test_city)
        self.assertIsNotNone(result)
        self.assertIn('list', result)
        self.assertTrue(len(result['list']) > 0)
        
        # 测试无效城市
        result = get_forecast(self.invalid_city)
        self.assertIsNone(result)
        
    def test_get_air_quality(self):
        # 测试有效坐标
        result = get_air_quality(self.lat, self.lon)
        self.assertIsNotNone(result)
        self.assertIn('list', result)
        
        # 测试API响应格式
        if result and 'list' in result and result['list']:
            aqi_data = result['list'][0]
            self.assertIn('main', aqi_data)
            self.assertIn('aqi', aqi_data['main'])
            
    def test_api_key_validity(self):
        # 测试API密钥是否有效
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.test_city}&appid={API_KEY}"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

class WeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """获取当前天气数据"""
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'zh_cn'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    def get_forecast(self, city: str) -> Optional[Dict[str, Any]]:
        """获取5天预报数据"""
        url = f"{self.base_url}/forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'zh_cn'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    def get_air_quality(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """获取空气质量数据"""
        url = f"{self.base_url}/air_pollution"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_aqi_description(aqi: int) -> tuple[str, str]:
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

if __name__ == "__main__":
    main()
    unittest.main() 