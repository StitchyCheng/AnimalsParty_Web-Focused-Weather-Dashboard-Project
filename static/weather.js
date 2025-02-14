// 创建温度图表
function createTemperatureChart(data) {
    const ctx = document.getElementById('temperatureChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: '温度 (°C)',
                data: data.temperatures,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: '温度变化趋势'
                }
            }
        }
    });
}

// 创建湿度图表
function createHumidityChart(data) {
    const ctx = document.getElementById('humidityChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: '湿度 (%)',
                data: data.humidity,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: '湿度变化趋势'
                }
            }
        }
    });
}

// 创建风速图表
function createWindChart(data) {
    const ctx = document.getElementById('windChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: '风速 (m/s)',
                data: data.windSpeed,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: '风速变化趋势'
                }
            }
        }
    });
}

// 创建降水图表
function createRainChart(data) {
    const ctx = document.getElementById('rainChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.times,
            datasets: [{
                label: '降水概率 (%)',
                data: data.precipitation,
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: '降水概率预报'
                }
            }
        }
    });
}

// 创建短期预报图表
function createShortTermCharts(data) {
    // 温度图表
    new Chart(document.getElementById('shortTermTemp').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: '温度 (°C)',
                data: data.temperatures,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '24小时温度变化' }
            }
        }
    });

    // 湿度图表
    new Chart(document.getElementById('shortTermHumidity').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: '湿度 (%)',
                data: data.humidity,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '24小时湿度变化' }
            }
        }
    });

    // 风速图表
    new Chart(document.getElementById('shortTermWind').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: '风速 (m/s)',
                data: data.windSpeed,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '24小时风速变化' }
            }
        }
    });

    // 降水概率图表
    new Chart(document.getElementById('shortTermRain').getContext('2d'), {
        type: 'bar',
        data: {
            labels: data.times,
            datasets: [{
                label: '降水概率 (%)',
                data: data.precipitation,
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '24小时降水概率' }
            }
        }
    });
}

// 创建长期预报图表
function createLongTermCharts(data) {
    // 温度范围图表
    new Chart(document.getElementById('longTermTemp').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: '最高温度 (°C)',
                data: data.max_temps,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }, {
                label: '最低温度 (°C)',
                data: data.min_temps,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '5天温度范围' }
            }
        }
    });

    // 湿度图表
    new Chart(document.getElementById('longTermHumidity').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: '湿度 (%)',
                data: data.humidity,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '5天湿度变化' }
            }
        }
    });

    // 添加风速图表
    new Chart(document.getElementById('longTermWind').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: '风速 (m/s)',
                data: data.windSpeed,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '5天风速变化' }
            }
        }
    });

    // 降水概率图表
    new Chart(document.getElementById('longTermRain').getContext('2d'), {
        type: 'bar',
        data: {
            labels: data.dates,
            datasets: [{
                label: '降水概率 (%)',
                data: data.precipitation,
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '5天降水概率' }
            }
        }
    });
}

// 添加预报切换函数
function switchForecast(type) {
    // 更新按钮状态
    document.getElementById('shortTermBtn').classList.toggle('active', type === 'short');
    document.getElementById('longTermBtn').classList.toggle('active', type === 'long');
    
    // 更新面板显示
    document.getElementById('shortTerm').classList.toggle('active', type === 'short');
    document.getElementById('longTerm').classList.toggle('active', type === 'long');
}

// 添加预报面板切换函数
function switchForecastPanel(type) {
    // 更新按钮状态
    document.getElementById('hourlyBtn').classList.toggle('active', type === 'hourly');
    document.getElementById('dailyBtn').classList.toggle('active', type === 'daily');
    
    // 更新面板显示
    document.getElementById('hourlyForecast').classList.toggle('active', type === 'hourly');
    document.getElementById('dailyForecast').classList.toggle('active', type === 'daily');
}

// 添加设置面板切换函数
function toggleSettings() {
    const panel = document.getElementById('settingsPanel');
    const overlay = document.querySelector('.overlay');
    
    if (!overlay) {
        // 创建遮罩层
        const newOverlay = document.createElement('div');
        newOverlay.className = 'overlay';
        document.body.appendChild(newOverlay);
        
        // 点击遮罩层关闭设置面板
        newOverlay.addEventListener('click', toggleSettings);
    }
    
    panel.classList.toggle('active');
    document.querySelector('.overlay').classList.toggle('active');
}

// 温度转换函数
function convertTemperature(value, toUnit) {
    if (toUnit === 'fahrenheit') {
        return (value * 9/5) + 32;
    }
    return value;
}

// 修改主题切换函数
function changeTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    
    // 更新图表颜色
    const textColor = theme === 'dark' ? '#f8f9fa' : '#212529';
    Chart.instances.forEach(chart => {
        if (chart.options.plugins.title) {
            chart.options.plugins.title.color = textColor;
        }
        if (chart.options.scales) {
            Object.values(chart.options.scales).forEach(scale => {
                if (scale.ticks) {
                    scale.ticks.color = textColor;
                }
            });
        }
        chart.update();
    });
}

// 监听主题变化事件
document.addEventListener('htmx:afterSettle', function(evt) {
    const headers = evt.detail.xhr?.getResponseHeader('HX-Trigger');
    if (headers) {
        try {
            const triggers = JSON.parse(headers);
            if (triggers.themeChanged) {
                changeTheme(triggers.themeChanged);
            }
        } catch (e) {
            console.error('Error parsing HX-Trigger:', e);
        }
    }
});

// 在页面加载时初始化主题
document.addEventListener('DOMContentLoaded', function() {
    const theme = document.documentElement.getAttribute('data-theme') || 'light';
    changeTheme(theme);
    // 默认显示24小时预报
    switchForecastPanel('hourly');
    // 默认显示短期图表
    switchForecast('short');
});

function getChartOptions(title, unit = 'celsius') {
    return {
        responsive: true,
        plugins: {
            title: { 
                display: true, 
                text: title,
                color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#f8f9fa' : '#212529'
            }
        },
        scales: {
            x: {
                ticks: {
                    color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#f8f9fa' : '#212529'
                }
            },
            y: {
                ticks: {
                    color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#f8f9fa' : '#212529'
                }
            }
        }
    };
} 