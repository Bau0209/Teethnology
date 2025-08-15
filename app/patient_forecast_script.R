library(dplyr)
library(lubridate)
library(ggplot2)
library(forecast)
library(scales)

tryCatch({

  # Load CSV
  df <- read.csv("C:\\Users\\admin\\Downloads\\appointment\\appointments.csv",
                 stringsAsFactors = FALSE)

  if (nrow(df) == 0) stop("The file is empty")

  # Standardize column names
  names(df) <- tolower(gsub("[^a-zA-Z0-9]", "_", names(df)))

  # Ensure appointment_date exists
  if (!"appointment_date" %in% names(df)) {
    stop("CSV must contain an 'appointment_date' column")
  }

  # Parse appointment_date
  df$appointment_date <- suppressWarnings(parse_date_time(
    df$appointment_date,
    orders = c("ymd", "mdy", "dmy", "Y/m/d", "m/d/Y", "d/m/Y",
               "ymd HMS", "mdy HMS", "dmy HMS"),
    tz = "UTC"
  ))

  if (all(is.na(df$appointment_date))) stop("Could not parse appointment_date values")
  df$appointment_date <- as.Date(df$appointment_date)

  # Monthly totals
  monthly_appointments <- df %>%
    filter(!is.na(appointment_date)) %>%
    mutate(month = floor_date(appointment_date, "month")) %>%
    group_by(month) %>%
    summarise(total_appointments = n(), .groups = "drop") %>%
    mutate(type = factor("Actual", levels = c("Actual", "Forecast")))

  if (nrow(monthly_appointments) < 2) {
    stop("Not enough data to forecast — at least 2 months required.")
  }

  # Time series
  appointments_ts <- ts(
    monthly_appointments$total_appointments,
    start = c(year(min(monthly_appointments$month)),
              month(min(monthly_appointments$month))),
    frequency = 12
  )

  # Forecast using ARIMA
  fit <- auto.arima(appointments_ts)
  fc <- forecast(fit, h = 1)

  # Next month forecast
  forecast_df <- data.frame(
    month = max(monthly_appointments$month) %m+% months(1),
    total_appointments = as.numeric(fc$mean),
    type = factor("Forecast", levels = c("Actual", "Forecast"))
  )

  # Combine data
  combined_df <- bind_rows(monthly_appointments, forecast_df)

  # Filter last 12 months + forecast month
  last_month <- max(combined_df$month)
  first_month <- last_month %m-% months(11)
  combined_df <- combined_df %>%
    filter(month >= first_month)

  # Bar chart
  p <- ggplot(combined_df, aes(x = month, y = total_appointments, fill = type)) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  scale_fill_manual(values = c("Actual" = "#1f77b4", "Forecast" = "#ff7f0e")) +
  labs(
    title = "Total Appointments",
    subtitle = paste0(
      "Forecast for ", format(forecast_df$month, "%B %Y"),
      ": ", round(forecast_df$total_appointments), " appointments"
    ),
    x = "Month",
    y = "Number of Appointments",
    fill = "Type"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(
      size = 9,          # 0.75rem ≈ 9pt
      color = "#00898E", # title color
      face = "bold"
    ),
    plot.subtitle = element_text(size = 9),
    legend.position = "bottom",
    axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)
  ) +
  scale_y_continuous(labels = comma) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b")


  print(p)

  # Save to static folder
  save_dir <- "C:\\Users\\admin\\Teethnology\\Teethnology\\app\\static"
  dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)
  ggsave(file.path(save_dir, "appointments_forecast.png"),
         plot = p, width = 7, height = 3.5, dpi = 150)

}, error = function(e) {
  message("Error: ", e$message)
})
