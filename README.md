You can choose to read the README in either of the two language versions.

你可以选择阅读两个语言版本的 README。

# Weather Forecast System

A feature-rich weather forecast system that provides real-time weather information, forecast analysis, and intelligent suggestions.

## Features

### 1. Weather Information Display
- Real-time weather conditions
- 24-hour forecast
- 5-day weather forecast
- Air Quality Index (AQI)

### 2. Data Visualization
- Temperature trend chart
- Humidity trend chart
- Wind speed trend chart
- Precipitation probability chart

### 3. Intelligent Analysis
- Temperature trend analysis
- Comfort level evaluation
- Weather warning alerts
- Outdoor activity suggestions

### 4. Personalized Settings
- Default city setting
- Dark/light theme toggle
- User preferences saving

### 5. User System
- User registration
- Account login
- Settings management

## Tech Stack

- Backend: Python FastHTML
- Data Storage: JSON
- Frontend Charts: Chart.js
- API: OpenWeatherMap API

## Installation Guide

1. Clone the repository
```bash
git clone [repository_url]
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure the API key
Set your OpenWeatherMap API key in `main.py`:
```python
API_KEY = "your_api_key_here"
```

4. Run the project
```bash
python main.py
```

## Usage Instructions

1. Register or log in to your account.
2. Set your default city.
3. View weather information and analysis reports.
4. Toggle between dark and light themes as needed.

## API Documentation

### OpenWeatherMap API
- Current weather data: `/data/2.5/weather`
- Weather forecast data: `/data/2.5/forecast`
- Air quality data: `/data/2.5/air_pollution`

## Project Structure

```
├── main.py              # Main program file
├── static/             # Static files directory
│   └── weather.js      # Weather-related JavaScript code
├── users.json          # User data storage
└── test_weather_api.py # API test file
```

## Feature Display

### Weather Analysis
- 24-hour temperature change trend
- Comfort level analysis chart
- Intelligent weather warning
- Outdoor activity suggestions

### Data Visualization
- Short-term (24-hour) forecast charts
- Long-term (5-day) forecast charts
- Multi-dimensional data display

---
# 天气预报系统

一个功能丰富的天气预报系统，提供实时天气信息、预报分析和智能建议。

## 功能特点

### 1. 天气信息展示
- 实时天气状况
- 24小时预报
- 5天天气预报
- 空气质量指数(AQI)

### 2. 数据可视化
- 温度变化趋势图
- 湿度变化图表
- 风速变化图表
- 降水概率图表

### 3. 智能分析
- 温度趋势分析
- 舒适度评估
- 天气预警提醒
- 户外活动建议

### 4. 个性化设置
- 默认城市设置
- 深色/浅色主题切换
- 用户偏好保存

### 5. 用户系统
- 用户注册
- 账号登录
- 设置管理

## 技术栈

- 后端：Python FastHTML
- 数据存储：JSON
- 前端图表：Chart.js
- API：OpenWeatherMap API

## 安装指南

1. 克隆项目
```bash
git clone [项目地址]
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置API密钥
在 `main.py` 中设置你的 OpenWeatherMap API 密钥：
```python
API_KEY = "your_api_key_here"
```

4. 运行项目
```bash
python main.py
```

## 使用说明

1. 注册/登录账号
2. 设置你的默认城市
3. 查看天气信息和分析报告
4. 根据需要切换深色/浅色主题

## API文档

### OpenWeatherMap API
- 当前天气数据：`/data/2.5/weather`
- 天气预报数据：`/data/2.5/forecast`
- 空气质量数据：`/data/2.5/air_pollution`

## 项目结构

```
├── main.py              # 主程序文件
├── static/             # 静态文件目录
│   └── weather.js      # 天气相关JavaScript代码
├── users.json          # 用户数据存储
└── test_weather_api.py # API测试文件
```

## 功能展示

### 天气分析
- 24小时温度变化趋势
- 舒适度分析表
- 智能天气预警
- 户外活动建议

### 数据可视化
- 短期（24小时）预报图表
- 长期（5天）预报图表
- 多维度数据展示
