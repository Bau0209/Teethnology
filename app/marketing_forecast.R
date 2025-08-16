library(dplyr)
library(lubridate)
library(ggplot2)
library(scales)

tryCatch({

  # Load CSV
  df <- read.csv("C:\\Users\\admin\\Downloads\\csv\\procedure.csv",
                 stringsAsFactors = FALSE)

  if (nrow(df) == 0) stop("The file is empty")

  # Standardize column names
  names(df) <- tolower(gsub("[^a-zA-Z0-9]", "_", names(df)))

  # Ensure procedure_date exists
  if (!"procedure_date" %in% names(df)) {
    stop("CSV must contain a 'procedure_date' column")
  }

  # Parse procedure_date
  df$procedure_date <- suppressWarnings(parse_date_time(
    df$procedure_date,
    orders = c("ymd", "mdy", "dmy", "Y/m/d", "m/d/Y", "d/m/Y",
               "ymd HMS", "mdy HMS", "dmy HMS"),
    tz = "UTC"
  ))

  if (all(is.na(df$procedure_date))) stop("Could not parse procedure_date values")
  df$procedure_date <- as.Date(df$procedure_date)

  # Monthly service counts
  service_trend <- df %>%
    filter(!is.na(procedure_date)) %>%
    mutate(month = floor_date(procedure_date, "month")) %>%
    group_by(month, treatment_procedure) %>%
    summarise(total_procedures = n(), .groups = "drop")

  if (nrow(service_trend) < 1) {
    stop("Not enough data to plot service trends.")
  }

  # 🔹 Fill missing combinations manually (no tidyr)
  all_months <- seq(
    from = min(service_trend$month),
    to   = max(service_trend$month),
    by   = "month"
  )
  all_services <- unique(service_trend$treatment_procedure)

  all_combinations <- expand.grid(
    month = all_months,
    treatment_procedure = all_services,
    stringsAsFactors = FALSE
  )

  service_trend <- all_combinations %>%
    left_join(service_trend, by = c("month", "treatment_procedure")) %>%
    mutate(total_procedures = ifelse(is.na(total_procedures), 0, total_procedures))

  # 🔹 Get most popular service per month
  popular_service <- service_trend %>%
    group_by(month) %>%
    slice_max(order_by = total_procedures, n = 1, with_ties = FALSE) %>%
    ungroup()

  print("Most popular service each month:")
  print(popular_service)

  # 🔹 Grouped Bar Chart
  p <- ggplot(service_trend, aes(x = month, y = total_procedures, fill = treatment_procedure)) +
    geom_bar(stat = "identity", position = "dodge", color = "black") +
    labs(
      title = "Service Usage Trend",
      subtitle = "Grouped by Service",
      x = "Month",
      y = "Number of Procedures",
      fill = "Service"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(size = 9, color = "#00898E", face = "bold"),
      plot.subtitle = element_text(size = 9),
      legend.position = "bottom",
      axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)
    ) +
    scale_y_continuous(labels = comma) +
    scale_x_date(
      breaks = seq(
        as.Date(paste0(format(Sys.Date(), "%Y"), "-01-01")),
        as.Date(paste0(format(Sys.Date(), "%Y"), "-12-01")),
        by = "1 month"
      ),
      date_labels = "%b",
      limits = c(
        as.Date(paste0(format(Sys.Date(), "%Y"), "-01-01")),
        as.Date(paste0(format(Sys.Date(), "%Y"), "-12-31"))
      )
    )

  print(p)

  # Save to static folder
  save_dir <- "C:\\Users\\admin\\Teethnology\\Teethnology\\app\\static"
  dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)
  ggsave(file.path(save_dir, "service_usage_trend.png"),
         plot = p, width = 7, height = 3.5, dpi = 150)

}, error = function(e) {
  message("Error: ", e$message)
})
