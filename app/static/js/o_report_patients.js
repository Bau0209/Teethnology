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
});
