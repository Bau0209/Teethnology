// Include this if not already in your HTML
// <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

document.addEventListener('DOMContentLoaded', () => {
  // Initialize dropdown selector
  new DateSelector('.date-selector-container');

  // === Revenue by Service (Line Chart) ===
  const revenueCtx = document.getElementById('revenueByServiceChart');
  if (revenueCtx) {
    new Chart(revenueCtx, {
      type: 'line',
      data: {
        labels: Array.from({ length: 25 }, (_, i) => i + 1), // Days 1–25
        datasets: [{
          label: 'Revenue',
          data: [2, 3, 1, 4, 2, 6, 4, 7, 2, 4, 5, 4, 6, 12, 20, 12, 6, 3, 2, 3, 4, 2, 1, 2, 1],
          borderColor: '#007bff',
          fill: true,
          backgroundColor: 'rgba(0,123,255,0.1)',
          tension: 0.4,
          pointRadius: 3
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }

  // === Top Earning Services (Doughnut Chart) ===
  const topServicesCtx = document.getElementById('topServicesChart');
  if (topServicesCtx) {
    new Chart(topServicesCtx, {
      type: 'doughnut',
      data: {
        labels: ['Root Canal', 'Braces', 'Cleanings', 'Others'],
        datasets: [{
          data: [3000, 2500, 1200, 7500],
          backgroundColor: ['#17a2b8', '#ffc107', '#28a745', '#6c757d'],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        cutout: '60%',
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    });
  }

  // === Forecast Chart (Line Comparison) ===
  const forecastCtx = document.getElementById('forecastChart');
  if (forecastCtx) {
    new Chart(forecastCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        datasets: [
          {
            label: 'Actual',
            data: [10000, 15000, 14000, 17000, 16000, 18000, 23000, 22000, 21000],
            borderColor: '#007bff',
            backgroundColor: 'rgba(0,123,255,0.1)',
            fill: false,
            tension: 0.4,
            pointRadius: 4
          },
          {
            label: 'Forecast',
            data: [12000, 16000, 15000, 16500, 17000, 17500, 20000, 23000, 22000],
            borderColor: '#fd7e14',
            backgroundColor: 'rgba(253,126,20,0.1)',
            fill: false,
            tension: 0.4,
            pointRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top'
          }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }
});
