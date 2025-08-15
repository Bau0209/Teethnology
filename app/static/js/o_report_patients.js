document.addEventListener('DOMContentLoaded', function () {
    const el = document.getElementById('newReturningByAgeChart');
    const src = window.chartData && window.chartData.new_vs_returning_by_age;

    if (el && src) {
        new Chart(el.getContext('2d'), {
        type: 'bar',
        data: {
            labels: src.labels,           // e.g., ["0-12","13-19","20-35","36-50","51+"]
            datasets: src.datasets        // [{label:"New Patients",...},{label:"Returning Patients",...}]
        },
        options: {
            responsive: true,
            plugins: {
            tooltip: { mode: 'index', intersect: false },
            legend: { position: 'top' }
            },
            scales: {
            x: { stacked: true },
            y: {
                stacked: true,
                beginAtZero: true,
                ticks: { callback: v => v.toLocaleString() }
            }
            }
        }
        });
    }

    const newReturningPatientsBarStackedChart = document.getElementById('newReturningPatientsBarStackedChart');
    if (newReturningPatientsBarStackedChart) {
        new Chart(newReturningPatientsBarStackedChart.getContext('2d'), {
            type: 'bar',
            data: {
                labels: window.chartData.months_labels,
                datasets: window.chartData.new_returning_stacked_datasets
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    legend: {
                        position: 'top'
                    }
                },
                scales: {
                    x: {
                        stacked: true
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) {
                                return value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    //forecast chart
    function renderForecastChart() {
    const forecastChartEl = document.getElementById('forecastChart');
        if (!forecastChartEl || !window.chartData || !window.chartData.forecast_chart_data) return;

        new Chart(forecastChartEl.getContext('2d'), {
            type: 'line',
            data: window.chartData.forecast_chart_data,
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.raw.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }
    renderForecastChart();

    //function for the forecast chart to display in the dashboard
    // Get the canvas element's parent
    const canvas = document.getElementById("forecastChart");

    // Create an <img> element
    const img = document.createElement("img");
    img.src = "/static/appointments_forecast.png"; // Path to your PNG
    img.style.width = "100%";
    img.style.height = "480px";   
    img.style.display = "block";

    // Replace the canvas with the image
    canvas.parentNode.replaceChild(img, canvas);

});
