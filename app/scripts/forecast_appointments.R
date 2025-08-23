# app/scripts/forecast_appointments.R
library(jsonlite)
library(dplyr)
library(lubridate)
library(forecast)

# Read stdin
input <- file("stdin")
json_data <- readLines(input, warn = FALSE)
close(input)
if (length(json_data) == 0) stop("No data received")
data <- fromJSON(paste(json_data, collapse = ""))

# Ensure columns
data$appointment_date <- as.Date(data$appointment_date)

# Group by category and month
monthly <- data %>%
  mutate(month = floor_date(appointment_date, "month")) %>%
  group_by(appointment_category, month) %>%
  summarise(count = n(), .groups = "drop")

results <- list()

# Forecast for each category
for (cat in unique(monthly$appointment_category)) {
  cat_data <- monthly %>% filter(appointment_category == cat)
  ts_data <- ts(
    cat_data$count,
    frequency = 12,
    start = c(year(min(cat_data$month)), month(min(cat_data$month)))
  )

  fit <- auto.arima(ts_data)
  fcast <- forecast(fit, h = 6)

  results[[cat]] <- list(
    dates = as.character(seq(max(cat_data$month) %m+% months(1), by = "month", length.out = 6)),
    forecast = as.numeric(fcast$mean),
    history_dates = as.character(cat_data$month),
    history = as.numeric(cat_data$count)
  )
}

cat(toJSON(results, pretty = FALSE, auto_unbox = TRUE))
