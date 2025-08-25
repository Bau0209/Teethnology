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

    // Helper function to make color lighter
    function lightenColor(hex, percent) {
        const num = parseInt(hex.slice(1), 16),
            amt = Math.round(2.55 * percent),
            R = (num >> 16) + amt,
            G = (num >> 8 & 0x00FF) + amt,
            B = (num & 0x0000FF) + amt;

        return "#" + (
            0x1000000 +
            (R < 255 ? (R < 0 ? 0 : R) : 255) * 0x10000 +
            (G < 255 ? (G < 0 ? 0 : G) : 255) * 0x100 +
            (B < 255 ? (B < 0 ? 0 : B) : 255)
        ).toString(16).slice(1);
    }

    const forecastChart = document.getElementById('forecastChart');
    const branch = document.getElementById("selected_branch").value;
    const colors = [
        '#FF6384', // 0-12
        '#36A2EB', // 13-19
        '#FFCE56', // 20-35
        '#4BC0C0', // 36-50
        '#5157a3', // 51+
    ];

    fetch("/dashboard/service_trend_forecast")
        .then(res => res.json())
        .then(data => {
            const datasets = [];
            let allLabels = [];

            Object.keys(data).forEach((category, index) => {
                const service = data[category];

                // Get this month's point
                const lastHistoryDate = service.history_dates.slice(-1);
                const lastHistoryValue = service.history.slice(-1);

                // Forecast (next 6 months)
                const labels = [...lastHistoryDate, ...service.dates];
                const values = [...lastHistoryValue, ...service.forecast];

                // Format labels
                const formattedLabels = labels.map((dateStr, i) => {
                    if (i === 0) return "This month";
                    const date = new Date(dateStr);
                    return new Intl.DateTimeFormat("en-US", { month: "long" }).format(date);
                });

                if (index === 0) {
                    allLabels = formattedLabels;
                }

                // Assign colors → 1 solid, rest lighter
                const baseColor = colors[index % colors.length];
                const bgColors = values.map((_, i) =>
                    i === 0 ? baseColor : lightenColor(baseColor, 20) // 20% lighter
                );

                datasets.push({
                    label: category,
                    data: values,
                    backgroundColor: bgColors,
                    borderRadius: 6
                });
            });

            new Chart(document.getElementById('forecastChart').getContext('2d'), {
                type: "bar",
                data: {
                    labels: allLabels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: "Service Trend Forecast (Current + Next 6 Months)"
                        },
                        tooltip: {
                            mode: "index",
                            intersect: false
                        }
                    },
                    scales: {
                        x: { stacked: true, title: { display: true, text: "Month" } },
                        y: { stacked: true, beginAtZero: true, title: { display: true, text: "Appointments" } }
                    }
                }
            });
        })
        .catch(err => console.error("Forecast fetch failed:", err));

    // //function for the forecast chart to display in the dashboard
    // // Get the canvas element's parent
    // const canvas = document.getElementById("forecastChart");

    // // Create an <img> element
    // const img = document.createElement("img");
    // img.src = "/static/service_usage_trend.png"; // Path to your PNG
    // img.style.width = "100%";
    // img.style.height = "480px";   
    // img.style.display = "block";

    // // Replace the canvas with the image
    // canvas.parentNode.replaceChild(img, canvas);
});
