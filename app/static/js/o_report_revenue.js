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
  let revenueChart; // global

const branch = document.getElementById("selected_branch").value;
fetch("/dashboard/revenue_forecast")
  .then(res => res.json())
  .then(data => {
      console.log("Revenue forecast API response:", data);

      // unwrap the nested "revenue" object
      const revenue = data.revenue;

      if (!revenue || !revenue.history_dates || !revenue.history) {
          throw new Error("Missing history data in revenue_forecast response");
      }

      // Labels
      const lastHistoryDate = revenue.history_dates.slice(-1);
      const lastHistoryValue = revenue.history.slice(-1);

      const labels = [...lastHistoryDate, ...revenue.dates];
      const values = [...lastHistoryValue, ...revenue.forecast];

      const allLabels = labels.map((dateStr, i) => {
          const date = new Date(dateStr);
          const monthName = date.toLocaleString("default", { month: "long" });
          return i === 0 ? "This Month" : monthName;
      });

      // Colors
      const baseColor = "#36A2EB";
      function lightenColor(hex, factor) {
          const num = parseInt(hex.slice(1), 16);
          let r = (num >> 16) + factor;
          let g = ((num >> 8) & 0x00FF) + factor;
          let b = (num & 0x0000FF) + factor;
          return `rgb(${Math.min(255, r)},${Math.min(255, g)},${Math.min(255, b)})`;
      }

      const bgColors = values.map((_, i) =>
          i === 0 ? baseColor : lightenColor(baseColor, 70) // 20% lighter
      );

      const datasets = [{
          label: "Revenue Forecast",
          data: values,
          backgroundColor: bgColors,
          borderRadius: 6
      }];

      // Ensure we don’t stack charts on one canvas
      const ctx = document.getElementById("forecastChart").getContext("2d");
      if (revenueChart) revenueChart.destroy();

      revenueChart = new Chart(ctx, {
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
                      text: "Revenue Forecast (This Month + Next 6 Months)"
                  },
                  legend: { display: false }
              },
              scales: {
                  x: { stacked: true, title: { display: true, text: "Month" } },
                  y: { stacked: true, beginAtZero: true, title: { display: true, text: "Revenue" } }
              }
          }
      });
  })
  .catch(err => console.error("Revenue forecast fetch failed:", err));

});
