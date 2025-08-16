document.addEventListener("DOMContentLoaded", function () {
    // Check if chartData is available from Flask
    if (!window.inventoryReportData) {
        console.error("No inventory report data found in window.inventoryReportData");
        return;
    }

    const { inventory_vs_consumption, supply_use_per_service } = window.inventoryReportData;

    // -------- Inventory vs Consumption Chart --------
    const inventoryCtx = document.getElementById("inventoryVsConsumptionChart");
    if (inventoryCtx) {
        new Chart(inventoryCtx.getContext("2d"), {
            type: "bar",
            data: {
                labels: inventory_vs_consumption.labels,
                datasets: [
                    {
                        label: "Inventory",
                        data: inventory_vs_consumption.inventory,
                        backgroundColor: "rgba(54, 162, 235, 0.6)",
                        borderColor: "rgba(54, 162, 235, 1)",
                        borderWidth: 1
                    },
                    {
                        label: "Consumption",
                        data: inventory_vs_consumption.consumption,
                        backgroundColor: "rgba(255, 99, 132, 0.6)",
                        borderColor: "rgba(255, 99, 132, 1)",
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "top" },
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    // -------- Supply Use per Service Chart --------
    const supplyCtx = document.getElementById("supplyUsePerServicetChart");
    if (supplyCtx) {
        new Chart(supplyCtx.getContext("2d"), {
            type: "bar",
            data: {
                labels: supply_use_per_service.labels,
                datasets: [
                    {
                        label: "Usage",
                        data: supply_use_per_service.data,
                        backgroundColor: "rgba(75, 192, 192, 0.6)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
    //function for the forecast chart to display in the dashboard
    // Get the canvas element's parent
    const canvas = document.getElementById("forecastChart");

    // Create an <img> element
    const img = document.createElement("img");
    img.src = "/static/items_forecast.png"; // Path to your PNG
    img.style.width = "100%";
    img.style.height = "480px";   
    img.style.display = "block";

    // Replace the canvas with the image
    canvas.parentNode.replaceChild(img, canvas);
});
