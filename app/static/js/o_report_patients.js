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
});
