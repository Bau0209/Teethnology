document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('popularServicesPatientsBarStackedChart');
    const ageData = window.chartData.popular_service_by_age; // Updated key name

    if (ctx && ageData) {
        new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ageData.labels, // e.g., ['Cleaning', 'Braces', ...]
                datasets: ageData.datasets.map((dataset, index) => {
                    const colors = [
                        '#FF6384', // 0-12
                        '#36A2EB', // 13-19
                        '#FFCE56', // 20-35
                        '#4BC0C0', // 36-50
                        '#5157a3ff', // 51+
                    ];

                    return {
                        ...dataset,
                        backgroundColor: colors[index % colors.length]
                    };
                })
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
    const genderChartCanvas = document.getElementById('popularServicesByGenderBarStackedChart');
    const genderData = window.chartData.popular_service_by_gender; // matches key in your <script> data

    if (genderChartCanvas && genderData) {
        new Chart(genderChartCanvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels: genderData.labels, // ['Cleaning', 'Braces', ...]
                datasets: genderData.datasets.map((dataset, index) => {
                    const colors = [
                        '#36A2EB', // Male
                        '#FF6384', // Female
                        '#FFCE56', // Unknown / Other
                    ];

                    return {
                        ...dataset,
                        backgroundColor: colors[index % colors.length]
                    };
                })
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

    //function for the forecast chart to display in the dashboard
    // Get the canvas element's parent
    const canvas = document.getElementById("forecastChart");

    // Create an <img> element
    const img = document.createElement("img");
    img.src = "/static/service_usage_trend.png"; // Path to your PNG
    img.style.width = "100%";
    img.style.height = "480px";   
    img.style.display = "block";

    // Replace the canvas with the image
    canvas.parentNode.replaceChild(img, canvas);
});
