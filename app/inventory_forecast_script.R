library(dplyr)
library(ggplot2)
library(scales)
library(lubridate)

tryCatch({
  
  # Load CSVs
  inventory <- read.csv("C:\\Users\\admin\\Downloads\\csv\\inventory.csv", stringsAsFactors = FALSE)
  procedure <- read.csv("C:\\Users\\admin\\Downloads\\csv\\procedure.csv", stringsAsFactors = FALSE)

  # Check if files are empty
  if (nrow(inventory) == 0 | nrow(procedure) == 0) {
    stop("Error: One of the CSV files is empty.")
  }

  # Clean column names
  names(inventory) <- tolower(trimws(gsub("[^a-zA-Z0-9]", "_", names(inventory))))
  names(procedure) <- tolower(trimws(gsub("[^a-zA-Z0-9]", "_", names(procedure))))

  # Verify required columns
  required_inventory_cols <- c("procedure_id", "inventory_item_id", "quantity_used")
  required_procedure_cols <- c("procedure_id", "procedure_date", "treatment_plan")

  if (!all(required_inventory_cols %in% names(inventory))) {
    stop("Error: inventory.csv is missing required columns.")
  }
  if (!all(required_procedure_cols %in% names(procedure))) {
    stop("Error: procedure.csv is missing required columns.")
  }

  # Parse dates and extract month name
  procedure <- procedure %>%
    mutate(
      procedure_date = as.Date(procedure_date, format = "%Y-%m-%d"),
      month = floor_date(procedure_date, "month"),
      month_name = factor(format(month, "%b"),  # Month abbreviation
                        levels = c("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))
    )

  # Merge inventory and procedure data
  merged_data <- inventory %>%
    inner_join(procedure, by = "procedure_id")

  if (nrow(merged_data) == 0) {
    stop("Error: No matching procedure_id found between files.")
  }

  # Summarize quantity used by month and treatment plan
  demand_summary <- merged_data %>%
    group_by(month_name, treatment_plan) %>%
    summarise(total_quantity = sum(quantity_used, na.rm = TRUE), .groups = "drop") %>%
    arrange(month_name)  # Ensure proper ordering

  if (nrow(demand_summary) == 0) {
    stop("Error: No data available for plotting.")
  }

  # --- Generate Combined Bar Chart ---
  bar_chart <- ggplot(demand_summary, aes(x = month_name, y = total_quantity, fill = treatment_plan)) +
    geom_bar(stat = "identity", position = position_dodge(preserve = "single"), width = 0.7) +
    labs(
      title = "Items High Demand Prediction",
      x = "Month",
      y = "Total Quantity Used",
      fill = "Treatment Plan"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(size = 16, face = "bold", hjust = 0.5, margin = margin(b = 20)),
      axis.text.x = element_text(angle = 0, hjust = 0.5, size = 10),
      axis.text.y = element_text(size = 10),
      axis.title = element_text(size = 12),
      legend.position = "bottom",
      legend.title = element_text(face = "bold"),
      panel.grid.major.x = element_blank()
    ) +
    scale_y_continuous(labels = comma, expand = expansion(mult = c(0, 0.1))) +
    scale_fill_brewer(palette = "Set2") +
    guides(fill = guide_legend(nrow = 2, byrow = TRUE))

  # Print the chart
  print(bar_chart)

  # Save the chart
  save_dir <- "C:\\Users\\admin\\Teethnology\\Teethnology\\app\\static"
  dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)
  ggsave(
    file.path(save_dir, "items_forecast.png"),
    plot = bar_chart,
    width = 12,
    height = 8,
    dpi = 300
  )

  message("Success! Monthly bar chart saved to: ", save_dir)

}, error = function(e) {
  message("Error: ", e$message)
})