library(dplyr)
library(ggplot2)
library(scales)

tryCatch({

  # Load CSV
  df <- read.csv("C:\\Users\\admin\\Downloads\\csv\\inventory.csv",
                 stringsAsFactors = FALSE)

  if (nrow(df) == 0) stop("The file is empty")

  # Standardize column names
  names(df) <- tolower(gsub("[^a-zA-Z0-9]", "_", names(df)))

  # Ensure required columns exist
  if (!all(c("procedure_id", "quantity_used") %in% names(df))) {
    stop("CSV must contain 'procedure_id' and 'quantity_used' columns")
  }

  # Summarize by procedure_id
  demand_summary <- df %>%
    group_by(procedure_id) %>%
    summarise(total_quantity = sum(quantity_used, na.rm = TRUE), .groups = "drop") %>%
    arrange(desc(total_quantity))

  if (nrow(demand_summary) == 0) {
    stop("No demand data available.")
  }

  # Pick top 10 high-demand items
  top_items <- demand_summary %>%
    slice_head(n = 10)

  # 🔹 Convert procedure_id to factor
  top_items$procedure_id <- factor(top_items$procedure_id)

  # Bar chart
  p <- ggplot(top_items, aes(x = reorder(procedure_id, -total_quantity),
                             y = total_quantity, fill = procedure_id)) +
    geom_bar(stat = "identity", color = "black") +
    labs(
      title = "Top High-Demand Items",
      subtitle = "Based on Total Quantity Used",
      x = "Procedure ID",
      y = "Total Quantity Used",
      fill = "Procedure ID"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(size = 10, color = "#00898E", face = "bold"),
      plot.subtitle = element_text(size = 9),
      legend.position = "none",
      axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1)
    ) +
    scale_y_continuous(labels = comma)

  print(p)

  # Save to static folder
  save_dir <- "C:\\Users\\admin\\Teethnology\\Teethnology\\app\\static"
  dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)
  ggsave(file.path(save_dir, "items_forecast.png"),
         plot = p, width = 7, height = 3.5, dpi = 150)

}, error = function(e) {
  message("Error: ", e$message)
})
