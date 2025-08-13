document.addEventListener('DOMContentLoaded', function () {
  // Stacked Bar Chart for Monthly Revenue by Top Services
  const barStacked = document.getElementById('topServicesChart');
  if (barStacked) {
    new Chart(barStacked.getContext('2d'), {
      type: 'bar',
      data: {
        labels: window.chartData.labels,
        datasets: window.chartData.stacked_datasets
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Monthly Revenue by Service'
          },
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
                return '₱' + value.toLocaleString();
              }
            }
          }
        }
      }
    });
  }

  // Monthly Revenue Bar Chart
  const barCtx = document.getElementById('revenueByServiceChart');
  if (barCtx) {
    new Chart(barCtx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: window.chartData.labels,
        datasets: [{
          label: 'Monthly Revenue (₱)',
          data: window.chartData.values,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value) {
                return '₱' + value.toLocaleString();
              }
            }
          }
        }
      }
    });
  }

  // Forecast Chart
  const forecastCtx = document.getElementById('forecastChart');
  if (forecastCtx) {
    new Chart(forecastCtx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: window.chartData.labels,
        datasets: [
          {
            label: 'Actual Revenue',
            data: window.chartData.values,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          },
          {
            label: 'Forecast Revenue (Moving Avg)',
            data: window.chartData.forecast_values,
            type: 'line',
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderWidth: 2,
            fill: false,
            tension: 0.4,
            borderDash: [5, 5]
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Total Revenue: Actual vs Forecast (Moving Average)'
          },
          tooltip: {
            mode: 'index',
            intersect: false
          },
          legend: {
            position: 'top'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value) {
                return '₱' + value.toLocaleString();
              }
            }
          }
        }
      }
    });
  }
});
