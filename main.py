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
from auth import load_users, save_users, hash_password
from components import weather_panel, forecast_panel

# API配置
API_KEY = "ffbd62ce8de707d8aef093dca5dce999"
# Styles
STYLES = Style("""
    /* 亮色主题 */
    :root[data-theme="light"] {
        --bg-color: #f8f9fa;
        --text-color: #2c3e50;
        --card-bg: white;
        --border-color: #e9ecef;
        --hover-color: #f1f3f5;
        --button-bg: #e9ecef;
        --button-text: #495057;
        --button-active: #4a90e2;
        --button-active-text: white;
        --secondary-text: #6c757d;
        --link-color: #3498db;
        --chart-grid: #e9ecef;
        --chart-gridlines: rgba(0, 0, 0, 0.1);
        --chart-text: rgba(0, 0, 0, 0.7);
    }
    
    /* 暗色主题 - 优化配色 */
    :root[data-theme="dark"] {
        --bg-color: #1e2024; 
        --text-color: #e0e0e0; 
        --card-bg: #282c34;  
        --border-color: #3a3f47; 
        --hover-color: #383d45;  
        --button-bg: #4a5568;  
        --button-text: #ffffff;  
        --button-active: #60a5fa;  
        --button-active-text: white; 
        --secondary-text: #88919c;  
        --link-color: #68a0ff;  
        --chart-grid: #3a3f47;  /
        --chart-gridlines: rgba(255, 255, 255, 0.1);
        --chart-text: rgba(255, 255, 255, 0.7);
    }
    
    body {
        background-color: var(--bg-color);
        color: var(--text-color);
        transition: all 0.3s ease;
        line-height: 1.6;
    }
    
    .weather-card,
    .forecast-card,
    .settings-panel,
    .dashboard-header,
    .search-container {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        color: var(--text-color);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    input, select, button {
        background-color: var(--button-bg);
        color: var(--text-color);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        padding: 8px 12px;
    }
    
    input:focus, select:focus {
        border-color: var(--button-active);
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
        outline: none;
    }
    
    .forecast-btn {
        background-color: var(--button-bg);
        color: var(--button-text);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .forecast-btn:hover {
        background-color: var(--hover-color);
        transform: translateY(-1px);
    }
    
    .forecast-btn.active {
        background-color: var(--button-active);
        color: var(--button-active-text);
        border-color: var(--button-active);
    }
    
    /* 标题样式 */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color);
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* 段落和文本样式 */
    p {
        color: var(--text-color);
        margin: 0.5rem 0;
    }
    
    /* 次要文本 */
    .secondary-text {
        color: var(--secondary-text);
    }
    
    /* 链接样式 */
    a {
        color: var(--link-color);
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: var(--button-active);
        text-decoration: underline;
    }
    
    /* 设置按钮样式 */
    .settings-btn {
        background-color: var(--button-bg);
        color: var(--button-text);
        padding: 8px 16px;
        border-radius: 6px;
        border: 1px solid var(--border-color);
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .settings-btn:hover {
        background-color: var(--hover-color);
        transform: translateY(-1px);
    }
    
    /* 天气卡片内容样式 */
    .weather-info p,
    .forecast-card p {
        margin: 8px 0;
        line-height: 1.5;
    }
    
    /* 图表容器样式 */
    .chart-container {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
    .form-group { max-width: 400px; margin: 0 auto; }
    .form-group label { display: block; margin: 10px 0; }
    .form-group input { width: 100%; padding: 8px; }
    .weather-card { padding: 20px; border-radius: 10px; margin: 20px 0; background-color: var(--card-bg); }
    .forecast-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }
    .forecast-card {
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        background-color: var(--card-bg);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .search-container {
        max-width: 800px;
        margin: 30px auto;
        padding: 20px;
        background-color: var(--card-bg);
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .search-bar {
        width: 100%;
        display: flex;
        gap: 15px;
        align-items: center;
    }
    .search-bar input {
        flex: 1;
        padding: 15px 20px;
        font-size: 1.2em;
        border: 2px solid #eee;
        border-radius: 8px;
        transition: all 0.3s ease;
        min-width: 300px;
    }
    .search-bar input:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 3px rgba(0,123,255,0.25);
        outline: none;
    }
    .search-bar input::placeholder {
        color: #aaa;
        font-size: 0.9em;
    }
    .search-bar button {
        padding: 15px 30px;
        font-size: 1.1em;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
        white-space: nowrap;
    }
    .search-bar button:hover {
        background: #0056b3;
    }
    .search-results {
        margin-top: 20px;
        padding: 10px;
        border-radius: 8px;
    }
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding: 20px;
        background-color: var(--card-bg);
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .user-controls {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .nav-buttons {
        display: flex;
        gap: 10px;
    }
    .logout-btn {
        background-color: #dc3545;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        transition: background-color 0.3s;
    }
    .logout-btn:hover {
        background-color: #c82333;
    }
    .settings-panel {
        display: none;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: var(--card-bg);
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 1000;
        max-width: 500px;
        width: 90%;
    }
    .settings-panel.active {
        display: block;
    }
    .settings-form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .settings-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .settings-group label {
        font-weight: bold;
        color: #495057;
    }
    .settings-group input,
    .settings-group select {
        padding: 8px;
        border: 2px solid #dee2e6;
        border-radius: 6px;
        font-size: 1em;
    }
    .settings-form button {
        padding: 12px;
        background: #28a745;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 1.1em;
        transition: background-color 0.3s;
    }
    .settings-form button:hover {
        background: #218838;
    }
    .overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 999;
    }
    .overlay.active {
        display: block;
    }
    .weather-info { margin: 15px 0; }
    #message { margin: 20px 0; text-align: center; }
    .auth-container {
        max-width: 400px;
        margin: 40px auto;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
        background-color: var(--card-bg);
    }
    .auth-links {
        margin-top: 20px;
        text-align: center;
    }
    .welcome-container {
        text-align: center;
        padding: 40px 20px;
    }
    .error-message {
        color: #ff6b6b;
        background-color: rgba(220, 53, 69, 0.1);
        border: 1px solid rgba(220, 53, 69, 0.3);
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        text-align: center;
    }
    .success-message {
        color: #51cf66;
        background-color: rgba(40, 167, 69, 0.1);
        border: 1px solid rgba(40, 167, 69, 0.3);
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        text-align: center;
    }
    .charts-section {
        margin: 40px 0;
        padding: 20px;
        background-color: var(--card-bg);
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .charts-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-top: 20px;
    }
    
    .forecast-switch {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px 0;
    }
    
    .forecast-panel {
        display: none;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .forecast-panel.active {
        display: block;
        opacity: 1;
    }
    
    .forecast-section {
        margin-top: 20px;
    }
    
    .forecast-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    
    .weather-grid {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 20px;
        align-items: start;
    }
    
    .aqi-info {
        padding: 15px;
        background-color: var(--card-bg);
        border-radius: 8px;
        text-align: center;
        min-width: 150px;
        border: 1px solid var(--border-color);
    }
    
    .aqi-info h4 {
        margin: 0 0 10px 0;
        color: #495057;
    }
    
    .aqi-info p {
        margin: 5px 0;
        font-size: 1.1em;
    }
    
    @media (max-width: 768px) {
        .weather-grid {
            grid-template-columns: 1fr;
        }
        
        .aqi-info {
            margin-top: 15px;
        }
    }

    /* 添加 Chart.js 图表样式覆盖 */
    :root[data-theme="dark"] .chart-container canvas {
        background-color: var(--card-bg);
    }

    /* 修改图表网格线颜色 */
    :root[data-theme="dark"] {
        --chart-gridlines: rgba(255, 255, 255, 0.1);
        --chart-text: rgba(255, 255, 255, 0.7);
    }

    :root[data-theme="light"] {
        --chart-gridlines: rgba(0, 0, 0, 0.1);
        --chart-text: rgba(0, 0, 0, 0.7);
    }

    .weather-analysis {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .analysis-title {
        color: var(--text-color);
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border-color);
    }
    
    .trend-description {
        font-size: 1.1em;
        color: var(--text-color);
        margin-bottom: 20px;
    }
    
    .analysis-section {
        margin: 20px 0;
        padding: 15px;
        background-color: var(--bg-color);
        border-radius: 6px;
    }
    
    .comfort-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
    }
    
    .comfort-table th,
    .comfort-table td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
    }
    
    .comfort-table th {
        background-color: var(--button-bg);
        color: var(--text-color);
    }
    
    .alert {
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .alert-high_temperature {
        background-color: #ff6b6b;
        color: white;
    }
    
    .alert-strong_wind {
        background-color: #4a90e2;
        color: white;
    }
    
    .alert-high_humidity {
        background-color: #5f27cd;
        color: white;
    }
""")

# Initialize FastHTML app
app, rt = fast_app(
    debug=True,
    pico=True,
    hdrs=(
        STYLES,
        Script(src="https://cdn.jsdelivr.net/npm/chart.js"),
        Script(src="/static/weather.js"),
    ),
    secret_key="weather"
)

def login_required(f):
    @wraps(f)
    async def decorated_function(request, *args, **kwargs):
        session = request.session
        if "auth" not in session:
            return RedirectResponse("/login", status_code=303)
        return await f(request, *args, **kwargs)
    return decorated_function

# Login routes
@rt("/login")
def get():
    return Titled("Login",
        Div(
            H1("Welcome Back", style="text-align: center;"),
            Form(
                Div(
                    Label("Username", Input(type="text", name="username", required=True)),
                    cls="form-group"
                ),
                Div(
                    Label("Password", Input(type="password", name="password", required=True)),
                    cls="form-group"
                ),
                Button("Login", type="submit"),
                method="post",
                cls="auth-form"
            ),
            Div(
                A("Need an account? Register here", href="/register"),
                cls="auth-links"
            ),
            Div(id="message"),
            cls="auth-container"
        )
    )

@rt("/login")
async def post(request, username: str, password: str):
    users = load_users()
    if username in users and compare_digest(hash_password(password), users[username]["password"]):
        request.session["auth"] = username
        
        # 确保新用户有默认设置
        if "settings" not in users[username]:
            users[username]["settings"] = {
                "default_city": "wenzhou",
                "theme": "light"
            }
            save_users(users)
        
        return RedirectResponse("/dashboard", status_code=303)
    return Div("Invalid username or password", cls="error-message", id="message")

# Register routes
@rt("/register")
def get():
    return Titled("Register",
        Div(
            H1("Create Account", style="text-align: center;"),
            Form(
                Div(
                    Label("Username", Input(type="text", name="username", required=True)),
                    cls="form-group"
                ),
                Div(
                    Label("Password", Input(type="password", name="password", required=True)),
                    cls="form-group"
                ),
                Div(
                    Label("Confirm Password", 
                         Input(type="password", name="confirm_password", required=True)),
                    cls="form-group"
                ),
                Button("Register", type="submit"),
                method="post",
                cls="auth-form"
            ),
            Div(
                A("Already have an account? Login here", href="/login"),
                cls="auth-links"
            ),
            Div(id="message"),
            cls="auth-container"
        )
    )

@rt("/register")
def post(username: str, password: str, confirm_password: str):
    users = load_users()
    
    if username in users:
        return Div("Username already exists", cls="error-message", id="message")
    
    if password != confirm_password:
        return Div("Passwords do not match", cls="error-message", id="message")
    
    if len(password) < 6:
        return Div("Password must be at least 6 characters", 
                  cls="error-message", id="message")
    
    users[username] = {
        "password": hash_password(password),
        "created_at": str(datetime.datetime.now()),
        "settings": {
            "default_city": "wenzhou",
            "theme": "light"
        }
    }
    save_users(users)
    
    return RedirectResponse("/login", status_code=303)

# Dashboard route
@rt("/dashboard")
@login_required
async def get(request):
    session = request.session
    username = session["auth"]
    users = load_users()
    settings = users[username]["settings"]
    
    city = settings.get("default_city", "wenzhou")
    
    weather_data = get_weather(city)
    forecast_data = get_forecast(city)
    
    error = request.query_params.get("error")
    
    # 准备图表数据
    chart_data = prepare_chart_data(forecast_data)
    
    # 添加天气分析
    weather_analysis = analyze_weather_trends(forecast_data)
    
    return Titled(f"",
        Script(f"""
            document.documentElement.setAttribute('data-theme', '{settings.get("theme", "light")}');
        """),
        Container(
            Div(
                H1("Weather Dashboard"),
                Div(
                    P(f"Welcome back, {username}!"),
                    Div(
                        Button("⚙️ Settings", 
                               onclick="toggleSettings()", 
                               cls="settings-btn"),
                        A("Logout", href="/logout", cls="logout-btn"),
                        cls="nav-buttons"
                    ),
                    cls="user-controls"
                ),
                cls="dashboard-header"
            ),
            Div(error, cls="error-message") if error else None,
            
            # 搜索区域
            Div(
                Form(
                    Div(
                        Input(type="text", name="city", 
                              placeholder="输入城市名称", 
                              value=city,
                              autocomplete="off"),
                        Button("搜索天气", type="submit"),
                        cls="search-bar"
                    ),
                    action="/search",
                    method="get"
                ),
                cls="search-container"
            ),
            
            Div(
                weather_panel(weather_data),
                # 添加预报切换按钮
                Div(
                    Button("24小时预报", 
                           onclick="switchForecastPanel('hourly')", 
                           id="hourlyBtn",
                           cls="forecast-btn active"),
                    Button("5天预报", 
                           onclick="switchForecastPanel('daily')", 
                           id="dailyBtn",
                           cls="forecast-btn"),
                    cls="forecast-switch"
                ),
                # 24小时预报面板
                Div(
                    forecast_panel(forecast_data, 'hourly'),
                    id="hourlyForecast",
                    cls="forecast-panel active"
                ),
                # 5天预报面板
                Div(
                    forecast_panel(forecast_data, 'daily'),
                    id="dailyForecast",
                    cls="forecast-panel"
                ),
                id="weather-content"
            ),
            
            # 添加图表区域
            Div(
                H2("天气预报", style="text-align: center; margin: 30px 0;"),
                # 添加切换按钮
                Div(
                    Button("24小时预报", 
                           onclick="switchForecast('short')", 
                           id="shortTermBtn",
                           cls="forecast-btn active"),
                    Button("5天预报", 
                           onclick="switchForecast('long')", 
                           id="longTermBtn",
                           cls="forecast-btn"),
                    cls="forecast-switch"
                ),
                
                # 短期预报面板
                Div(
                    Grid(
                        Div(Canvas(id="shortTermTemp"), cls="chart-container"),
                        Div(Canvas(id="shortTermHumidity"), cls="chart-container"),
                        Div(Canvas(id="shortTermWind"), cls="chart-container"),
                        Div(Canvas(id="shortTermRain"), cls="chart-container"),
                        cls="charts-grid"
                    ),
                    id="shortTerm",
                    cls="forecast-panel active"
                ),
                
                # 长期预报面板
                Div(
                    Grid(
                        Div(Canvas(id="longTermTemp"), cls="chart-container"),
                        Div(Canvas(id="longTermHumidity"), cls="chart-container"),
                        Div(Canvas(id="longTermWind"), cls="chart-container"),
                        Div(Canvas(id="longTermRain"), cls="chart-container"),
                        cls="charts-grid"
                    ),
                    id="longTerm",
                    cls="forecast-panel"
                ),
                
                # 初始化图表的脚本
                Script(f"""
                    document.addEventListener('DOMContentLoaded', function() {{
                        const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
                        const chartOptions = {{
                            scales: {{
                                x: {{
                                    grid: {{
                                        color: getComputedStyle(document.documentElement).getPropertyValue('--chart-gridlines')
                                    }},
                                    ticks: {{
                                        color: getComputedStyle(document.documentElement).getPropertyValue('--chart-text')
                                    }}
                                }},
                                y: {{
                                    grid: {{
                                        color: getComputedStyle(document.documentElement).getPropertyValue('--chart-gridlines')
                                    }},
                                    ticks: {{
                                        color: getComputedStyle(document.documentElement).getPropertyValue('--chart-text')
                                    }}
                                }}
                            }},
                            plugins: {{
                                legend: {{
                                    labels: {{
                                        color: getComputedStyle(document.documentElement).getPropertyValue('--chart-text')
                                    }}
                                }}
                            }}
                        }};
                        
                        const data = {json.dumps(chart_data)};
                        createShortTermCharts(data.short_term, chartOptions);
                        createLongTermCharts(data.long_term, chartOptions);
                    }});
                """),
                cls="charts-section"
            ),
            
            # 添加天气分析面板
            Div(
                H3("天气趋势分析", cls="analysis-title"),
                P(weather_analysis['trend_description'], cls="trend-description"),
                
                # 温度趋势
                Div(
                    H4("温度趋势"),
                    P(f"最低温度: {weather_analysis['temperature_trend']['min']:.1f}°C "
                      f"(出现时间: {weather_analysis['temperature_trend']['min_time']})"),
                    P(f"最高温度: {weather_analysis['temperature_trend']['max']:.1f}°C "
                      f"(出现时间: {weather_analysis['temperature_trend']['max_time']})"),
                    cls="analysis-section"
                ),
                
                # 舒适度分析
                Div(
                    H4("舒适度分析"),
                    Table(
                        Tr(
                            Th("时间"), 
                            Th("温度"), 
                            Th("体感温度"), 
                            Th("风寒指数"), 
                            Th("舒适度")
                        ),
                        *[Tr(
                            Td(time),
                            Td(f"{data['temp']}°C"),
                            Td(f"{data['feels_like']}°C"),
                            Td(f"{data['wind_chill']}°C"),
                            Td(data['comfort_level'])
                        ) for time, data in weather_analysis['comfort_analysis'].items()],
                        cls="comfort-table"
                    ),
                    cls="analysis-section"
                ),
                
                # 天气预警
                Div(
                    H4("天气预警"),
                    *[Div(alert['message'], 
                         cls=f"alert alert-{alert['type']}") 
                      for alert in weather_analysis['weather_alerts']],
                    cls="analysis-section"
                ) if weather_analysis['weather_alerts'] else None,
                
                # 户外活动建议
                Div(
                    H4("户外活动建议"),
                    P(f"活动指数: {weather_analysis['outdoor_activity_score']}/100"),
                    Ul(*[Li(suggestion) for suggestion in weather_analysis['outdoor_suggestions']]),
                    cls="analysis-section"
                ),
                
                cls="weather-analysis"
            ),
            
            # 添加设置面板
            Div(
                H2("Settings"),
                Form(
                    # 默认城市设置
                    Div(
                        Label("Default City",
                              Input(type="text", name="default_city", 
                                    value=settings.get("default_city", ""),
                                    placeholder="Enter your default city")),
                        cls="settings-group"
                    ),
                    # 主题设置
                    Div(
                        Label("Theme"),
                        Select(
                            Option("Light Theme", value="light",
                                   selected=settings.get("theme") == "light"),
                            Option("Dark Theme", value="dark",
                                   selected=settings.get("theme") == "dark"),
                            name="theme",
                            onchange="changeTheme(this.value)"
                        ),
                        cls="settings-group"
                    ),
                    Button("Save Settings", type="submit"),
                    action="/update-settings",
                    method="post",
                    cls="settings-form"
                ),
                id="settingsPanel",
                cls="settings-panel"
            )
        )
    )

# 添加搜索处理路由
@rt("/search")
@login_required
async def get(request, city: str):
    session = request.session
    username = session["auth"]
    users = load_users()
    
    # 验证城市是否存在
    weather_data = get_weather(city)
    if not weather_data:
        # 如果城市不存在，返回到 dashboard 并显示错误
        return RedirectResponse(
            f"/dashboard?error=City '{city}' not found",
            status_code=303
        )
    
    # 更新用户默认城市
    users[username]["settings"]["default_city"] = city
    save_users(users)
    
    # 重定向回 dashboard
    return RedirectResponse("/dashboard", status_code=303)

# Logout route
@rt("/logout")
async def get(request):
    session = request.session
    if "auth" in session:
        del session["auth"]
    return RedirectResponse("/login", status_code=303)

# Root route
@rt("/")
async def get(request):
    session = request.session
    if "auth" in session:
        return RedirectResponse("/dashboard", status_code=303)
    return RedirectResponse("/login", status_code=303)

# 添加一个选择城市的路由
@rt("/select-city")
@login_required
async def get(request):
    session = request.session
    username = session["auth"]
    return Titled("Select Your City",
        Container(
            H1("Welcome to Weather Dashboard"),
            P(f"Hello {username}, please select or search your city"),
            
            # 热门城市快速选择
            Div(
                H2("Popular Cities"),
                Grid(
                    *[city_card(city) for city in [
                        "Beijing", "Shanghai", "Guangzhou", "Shenzhen",
                        "Hangzhou", "Wenzhou", "Chengdu", "Wuhan"
                    ]],
                    cls="popular-cities"
                ),
                cls="city-section"
            ),
            
            # 城市搜索
            Form(
                Div(
                    Input(type="text", name="city", 
                          placeholder="Or search your city...",
                          required=True),
                    Button("Search", type="submit"),
                    cls="city-search"
                ),
                hx_post="/search-city",
                hx_target="#search-results"
            ),
            
            # 搜索结果区域
            Div(id="search-results", cls="search-results"),
            
            # 返回登录
            Div(A("Logout", href="/logout", cls="button"), cls="nav-links")
        )
    )

def city_card(city_name):
    """创建城市卡片组件"""
    return Card(
        H3(city_name),
        Form(
            Hidden(name="city", value=city_name),
            Button("Select", type="submit"),
            hx_post="/set-city",
            hx_target="#message"
        ),
        cls="city-card"
    )

# 添加搜索城市的路由
@rt("/search-city")
def post(city: str):
    # 这里可以添加城市验证逻辑
    weather = get_weather(city)
    if not weather:
        return Div("City not found", cls="error-message")
    
    return city_card(city)

# 添加设置城市的路由
@rt("/set-city")
@login_required
async def post(request, city: str):
    session = request.session
    username = session["auth"]
    users = load_users()
    
    if username in users:
        users[username]["settings"]["default_city"] = city
        save_users(users)
        return RedirectResponse("/dashboard", status_code=303)
    
    return Div("Error updating settings", cls="error-message")

@rt("/update-settings")
@login_required
async def post(request, default_city: str, theme: str):
    session = request.session
    username = session["auth"]
    users = load_users()
    
    if username in users:
        # 验证城市是否有效
        if not get_weather(default_city):
            return RedirectResponse(
                f"/dashboard?error=Invalid city: {default_city}",
                status_code=303
            )
        
        # 更新设置
        users[username]["settings"].update({
            "default_city": default_city,
            "theme": theme
        })
        save_users(users)
        
        # 返回一个特殊的响应，包含新的主题信息
        return RedirectResponse(
            "/dashboard", 
            status_code=303,
            headers={"HX-Trigger": json.dumps({"themeChanged": theme})}
        )
    
    return RedirectResponse(
        "/dashboard?error=Failed to update settings",
        status_code=303
    )

if __name__ == "__main__":
    print("Starting server on http://localhost:5001")
    print("Available routes:")
    print("  - /login")
    print("  - /register")
    print("  - /dashboard")
    print("  - /logout")
    serve(port=5001) 