document.addEventListener('DOMContentLoaded', function () {
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
