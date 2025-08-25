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

    const branch = document.getElementById("selected_branch").value;

    //forecast chart
    fetch("/dashboard/patient_forecast")
    .then(res => res.json())
    .then(data => {
        console.log("Patient forecast API response:", data);

        const appointments = data.appointments;

        if (!appointments || !appointments.history_dates || !appointments.history) {
            throw new Error("Missing history data in patient_forecast response");
        }

        // Get last history point
        const lastHistoryDate = appointments.history_dates.slice(-1);
        const lastHistoryValue = appointments.history.slice(-1);

        // Combine history + forecast
        const labels = [...lastHistoryDate, ...appointments.dates];
        const values = [...lastHistoryValue, ...appointments.forecast];

        // Format labels: "This Month" for first, then month names
        const allLabels = labels.map((dateStr, i) => {
            const date = new Date(dateStr);
            const monthName = date.toLocaleString("default", { month: "long" });
            return i === 0 ? "This Month" : monthName;
        });

        // Base color & lighten function
        const baseColor = "#FF6384"; // pinkish for appointments
        function lightenColor(hex, factor) {
            const num = parseInt(hex.slice(1), 16);
            let r = (num >> 16) + factor;
            let g = ((num >> 8) & 0x00FF) + factor;
            let b = (num & 0x0000FF) + factor;
            return `rgb(${Math.min(255, r)},${Math.min(255, g)},${Math.min(255, b)})`;
        }

        const bgColors = values.map((_, i) =>
            i === 0 ? baseColor : lightenColor(baseColor, 70)
        );

        // Dataset
        const datasets = [{
            label: "Appointments Forecast",
            data: values,
            backgroundColor: bgColors,
            borderRadius: 6
        }];

        // Destroy previous chart if exists
        const ctx = document.getElementById("forecastChart").getContext("2d");
        if (window.patientChart) window.patientChart.destroy();

        // Create new chart
        window.patientChart = new Chart(ctx, {
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
                        text: "Patient Appointments Forecast (This Month + Next 6 Months)"
                    },
                    legend: { display: false }
                },
                scales: {
                    x: { stacked: true, title: { display: true, text: "Month" } },
                    y: { stacked: true, beginAtZero: true, title: { display: true, text: "Appointments" } }
                }
            }
        });
    })
    .catch(err => console.error("Patient forecast fetch failed:", err));


});