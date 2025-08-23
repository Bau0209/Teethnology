library(plumber)
library(DBI)
library(RMySQL)
library(dplyr)
library(lubridate)
library(tidyr)
library(forecast)
library(zoo)

#* Forecast next 6 months of appointments per category
#* @get /forecast
function() {
  # Connect to DB
  con <- dbConnect(
    MySQL(),
    host = "localhost",
    port = 3306,
    user = "root",
    password = "@Eddielynjoy123",
    dbname = "teethnology_test"
  )
  
  appointments <- dbGetQuery(con, "SELECT appointment_category, appointment_date FROM appointments;")
  dbDisconnect(con)
  
  # Prepare data
  appointments <- appointments %>%
    mutate(appointment_date = as.Date(appointment_date)) %>%
    mutate(
      year = year(appointment_date),
      month = month(appointment_date, label = TRUE, abbr = TRUE),
      month_num = as.numeric(month)
    )
  
  # Count appointments per category per month/year
  appointments_summary <- appointments %>%
    group_by(year, month, month_num, appointment_category) %>%
    summarise(total_appointments = n(), .groups = "drop") %>%
    arrange(year, month_num, appointment_category)
  
  # Pivot to wide format
  appointments_wide <- appointments_summary %>%
    select(year, month_num, appointment_category, total_appointments) %>%
    unite("year_month", year, month_num, sep="-") %>%
    pivot_wider(names_from = appointment_category, values_from = total_appointments, values_fill = 0)
  
  # Forecast next 6 months
  forecast_list <- list()
  for(cat in colnames(appointments_wide)[-1]) {
    ts_data <- ts(appointments_wide[[cat]], frequency = 12)
    fit <- auto.arima(ts_data)
    fcast <- forecast(fit, h=6)
    forecast_list[[cat]] <- as.numeric(fcast$mean)
  }
  
  # Create data frame for forecast
  future_months <- seq.Date(
    from = as.Date(paste0(max(appointments$year), "-", max(appointments$month_num), "-01")) %m+% months(1),
    by = "month",
    length.out = 6
  )
  
  forecast_df <- data.frame(month = format(future_months, "%Y-%m"))
  forecast_df <- cbind(forecast_df, as.data.frame(forecast_list))
  
  # Return as JSON
  return(forecast_df)
}
