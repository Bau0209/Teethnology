# app/scripts/forecast_appointments.R
library(jsonlite)
library(dplyr)
library(lubridate)
library(forecast)

# --- 1. Read JSON from Python (stdin) ---
input <- file("stdin")
json_data <- readLines(input, warn = FALSE)
close(input)

if (length(json_data) == 0) stop("No data received")
data <- fromJSON(paste(json_data, collapse = ""))

# --- 2. Ensure columns ---
data$appointment_date <- as.Date(data$appointment_date)

# --- 3. Group by category and month ---
monthly <- data %>%
  mutate(month = floor_date(appointment_date, "month")) %>%
  group_by(appointment_category, month) %>%
  summarise(count = n(), .groups = "drop") %>%
  arrange(month)

results <- list()

# --- 4. Forecast for each category ---
for (cat in unique(monthly$appointment_category)) {
  cat_data <- monthly %>% filter(appointment_category == cat)

  # Skip if less than 2 months of data
  if (nrow(cat_data) < 2) {
    results[[cat]] <- list(
      dates = character(0),
      forecast = numeric(0),
      history_dates = as.character(cat_data$month),
      history = as.numeric(cat_data$count),
      note = "Not enough data for forecasting"
    )
    next
  }

  # Build time series
  ts_data <- ts(
    cat_data$count,
    frequency = 12,
    start = c(year(min(cat_data$month)), month(min(cat_data$month)))
  )

  # Forecast 6 months ahead
  fit <- auto.arima(ts_data)
  fcast <- forecast(fit, h = 6)

  # Build result
  results[[cat]] <- list(
    dates = as.character(seq(max(cat_data$month) %m+% months(1), by = "month", length.out = 6)),
    forecast = round(as.numeric(fcast$mean), 2), # rounded for readability
    history_dates = as.character(cat_data$month),
    history = as.numeric(cat_data$count)
  )
}

# --- 5. Output JSON back to Python ---
cat(toJSON(results, pretty = FALSE, auto_unbox = TRUE))
