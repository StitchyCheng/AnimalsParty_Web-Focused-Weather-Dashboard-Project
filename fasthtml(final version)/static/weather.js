// Create Temperature Chart
function createTemperatureChart(data) {
    const ctx = document.getElementById('temperatureChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: 'Temperature (°C)',
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
                    text: 'Temperature Trend'
                }
            }
        }
    });
}

// Create Humidity Chart
function createHumidityChart(data) {
    const ctx = document.getElementById('humidityChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: 'Humidity (%)',
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
                    text: 'Humidity Trend'
                }
            }
        }
    });
}

// Create Wind Chart
function createWindChart(data) {
    const ctx = document.getElementById('windChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: 'Wind Speed (m/s)',
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
                    text: 'Wind Speed Trend'
                }
            }
        }
    });
}

// Create Rain Chart
function createRainChart(data) {
    const ctx = document.getElementById('rainChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.times,
            datasets: [{
                label: 'Precipitation Probability (%)',
                data: data.precipitation,
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Precipitation Probability Forecast'
                }
            }
        }
    });
}

// Create Short Term Charts
function createShortTermCharts(data) {
    // Temperature Chart
    new Chart(document.getElementById('shortTermTemp').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: 'Temperature (°C)',
                data: data.temperatures,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '24-hour Temperature Change' }
            }
        }
    });

    // Humidity Chart
    new Chart(document.getElementById('shortTermHumidity').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: 'Humidity (%)',
                data: data.humidity,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '24-hour Humidity Change' }
            }
        }
    });

    // Wind Chart
    new Chart(document.getElementById('shortTermWind').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.times,
            datasets: [{
                label: 'Wind Speed (m/s)',
                data: data.windSpeed,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '24-hour Wind Speed Change' }
            }
        }
    });

    // Precipitation Probability Chart
    new Chart(document.getElementById('shortTermRain').getContext('2d'), {
        type: 'bar',
        data: {
            labels: data.times,
            datasets: [{
                label: 'Precipitation Probability (%)',
                data: data.precipitation,
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '24-hour Precipitation Probability' }
            }
        }
    });
}

// Create Long Term Charts
function createLongTermCharts(data) {
    // Temperature Range Chart
    new Chart(document.getElementById('longTermTemp').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Max Temperature (°C)',
                data: data.max_temps,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }, {
                label: 'Min Temperature (°C)',
                data: data.min_temps,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '5-day Temperature Range' }
            }
        }
    });

    // Humidity Chart
    new Chart(document.getElementById('longTermHumidity').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Humidity (%)',
                data: data.humidity,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '5-day Humidity Change' }
            }
        }
    });

    // Wind Speed Chart
    new Chart(document.getElementById('longTermWind').getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Wind Speed (m/s)',
                data: data.windSpeed,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '5-day Wind Speed Change' }
            }
        }
    });

    // Precipitation Probability Chart
    new Chart(document.getElementById('longTermRain').getContext('2d'), {
        type: 'bar',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Precipitation Probability (%)',
                data: data.precipitation,
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: '5-day Precipitation Probability' }
            }
        }
    });
}

// Add forecast switch function
function switchForecast(type) {
    // Update button status
    document.getElementById('shortTermBtn').classList.toggle('active', type === 'short');
    document.getElementById('longTermBtn').classList.toggle('active', type === 'long');
    
    // Update panel display
    document.getElementById('shortTerm').classList.toggle('active', type === 'short');
    document.getElementById('longTerm').classList.toggle('active', type === 'long');
}

// Add forecast panel switch function
function switchForecastPanel(type) {
    // Update button status
    document.getElementById('hourlyBtn').classList.toggle('active', type === 'hourly');
    document.getElementById('dailyBtn').classList.toggle('active', type === 'daily');
    
    // Update panel display
    document.getElementById('hourlyForecast').classList.toggle('active', type === 'hourly');
    document.getElementById('dailyForecast').classList.toggle('active', type === 'daily');
}

// Add settings panel toggle function
function toggleSettings() {
    const panel = document.getElementById('settingsPanel');
    const overlay = document.querySelector('.overlay');
    
    if (!overlay) {
        // Create overlay
        const newOverlay = document.createElement('div');
        newOverlay.className = 'overlay';
        document.body.appendChild(newOverlay);
        
        // Close settings panel when overlay is clicked
        newOverlay.addEventListener('click', toggleSettings);
    }
    
    panel.classList.toggle('active');
    document.querySelector('.overlay').classList.toggle('active');
}

// Temperature conversion function
function convertTemperature(value, toUnit) {
    if (toUnit === 'fahrenheit') {
        return (value * 9/5) + 32;
    }
    return value;
}

// Change theme function
function changeTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update chart colors
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

// Listen for theme change events
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

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function() {
    const theme = document.documentElement.getAttribute('data-theme') || 'light';
    changeTheme(theme);
    // Default to show 24-hour forecast
    switchForecastPanel('hourly');
    // Default to show short-term charts
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