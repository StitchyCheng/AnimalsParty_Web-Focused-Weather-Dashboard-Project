import time
import statistics
from main import get_weather, get_forecast, get_air_quality
from concurrent.futures import ThreadPoolExecutor

def measure_response_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time, result

def test_api_performance(city="wenzhou", iterations=5):
    print(f"\nTesting API performance with {iterations} iterations:")
    
    # 存储响应时间
    weather_times = []
    forecast_times = []
    air_quality_times = []
    
    for i in range(iterations):
        print(f"\nIteration {i + 1}/{iterations}")
        
        # 测试天气数据获取
        weather_time, weather_data = measure_response_time(get_weather, city)
        weather_times.append(weather_time)
        print(f"Weather API response time: {weather_time:.2f}s")
        
        # 测试天气预报获取
        forecast_time, forecast_data = measure_response_time(get_forecast, city)
        forecast_times.append(forecast_time)
        print(f"Forecast API response time: {forecast_time:.2f}s")
        
        # 如果有天气数据，测试空气质量获取
        if weather_data:
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            air_time, _ = measure_response_time(get_air_quality, lat, lon)
            air_quality_times.append(air_time)
            print(f"Air Quality API response time: {air_time:.2f}s")
        
        time.sleep(1)  # 避免过快请求
    
    # 计算统计数据
    print("\nPerformance Statistics:")
    print("\nWeather API:")
    print(f"Average response time: {statistics.mean(weather_times):.2f}s")
    print(f"Min response time: {min(weather_times):.2f}s")
    print(f"Max response time: {max(weather_times):.2f}s")
    
    print("\nForecast API:")
    print(f"Average response time: {statistics.mean(forecast_times):.2f}s")
    print(f"Min response time: {min(forecast_times):.2f}s")
    print(f"Max response time: {max(forecast_times):.2f}s")
    
    if air_quality_times:
        print("\nAir Quality API:")
        print(f"Average response time: {statistics.mean(air_quality_times):.2f}s")
        print(f"Min response time: {min(air_quality_times):.2f}s")
        print(f"Max response time: {max(air_quality_times):.2f}s")

def test_concurrent_requests(cities=None, max_workers=3):
    if cities is None:
        cities = ["wenzhou", "beijing", "shanghai", "guangzhou", "shenzhen"]
    
    print(f"\nTesting concurrent requests for {len(cities)} cities:")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 并发获取天气数据
        weather_futures = {executor.submit(get_weather, city): city for city in cities}
        for future in weather_futures:
            city = weather_futures[future]
            try:
                result = future.result()
                if result:
                    print(f"Successfully retrieved weather data for {city}")
                else:
                    print(f"Failed to retrieve weather data for {city}")
            except Exception as e:
                print(f"Error retrieving weather data for {city}: {str(e)}")
    
    end_time = time.time()
    print(f"\nTotal time for concurrent requests: {end_time - start_time:.2f}s")

if __name__ == "__main__":
    # 运行性能测试
    test_api_performance(iterations=3)
    
    # 运行并发测试
    test_concurrent_requests() 