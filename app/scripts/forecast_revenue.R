# app/scripts/forecast_revenue.R
library(jsonlite)
library(dplyr)
library(lubridate)
library(forecast)

# --- 1. Read JSON input from Python (stdin) ---
input <- file("stdin")
json_data <- readLines(input, warn = FALSE)
close(input)

if (length(json_data) == 0) stop("No data received")
data <- fromJSON(paste(json_data, collapse = ""))

# --- 2. Data Cleaning & Preparation ---
data <- data %>%
  mutate(
    transaction_datetime = as.POSIXct(transaction_datetime, tz = "UTC"),
    total_amount_paid = as.numeric(total_amount_paid)
  )

# --- 3. Aggregate Monthly Revenue ---
monthly <- data %>%
  mutate(month = floor_date(transaction_datetime, "month")) %>%
  group_by(month) %>%
  summarise(total_revenue = sum(total_amount_paid), .groups = "drop") %>%
  arrange(month)

# Initialize results list
results <- list()

# --- 4. Forecasting with ETS ---
if (nrow(monthly) < 2) {
  # Not enough data to build a time series
  results$revenue <- list(
    dates = character(0),
    forecast = numeric(0),
    history_dates = as.character(monthly$month),
    history = as.numeric(monthly$total_revenue),
    note = "Not enough data for forecasting"
  )
} else {
  # Build time series from monthly data
  ts_data <- ts(
    monthly$total_revenue,
    frequency = 12,  # monthly frequency
    start = c(year(min(monthly$month)), month(min(monthly$month)))
  )
  
  # Fit ETS model & forecast 6 months ahead
  fit <- ets(ts_data, model = "AAA")  # Additive error, trend, and seasonality
  fcast <- forecast(fit, h = 6)
  
  # Prepare forecast result
  results$revenue <- list(
    dates = as.character(seq(max(monthly$month) %m+% months(1), by = "month", length.out = 6)),
    forecast = round(as.numeric(fcast$mean), 2),
    history_dates = as.character(monthly$month),
    history = as.numeric(monthly$total_revenue)
  )
}

# --- 5. Output JSON back to Python ---
cat(toJSON(results, pretty = FALSE, auto_unbox = TRUE))
