# Load required packages
library(dplyr)
library(lubridate)
library(ggplot2)
library(forecast)
library(scales)

# Read the CSV file with error handling
tryCatch({
  df <- read.csv("C:\\Users\\admin\\Downloads\\appointment\\appointments.csv", 
                 stringsAsFactors = FALSE)
  
  # Check if file loaded correctly
  if (nrow(df) == 0) stop("The file is empty")
  
  # Standardize column names (handle case differences, spaces, etc.)
  names(df) <- tolower(gsub("[^a-zA-Z0-9]", "_", names(df)))
  
  # Try common date column names if appointment_date doesn't exist
  date_cols <- c("appointment_date", "date", "appointmentdate", "appt_date")
  date_col_found <- FALSE
  
  for (col in date_cols) {
    if (col %in% names(df)) {
      df <- df %>% rename(appointment_date = !!col)
      date_col_found <- TRUE
      break
    }
  }
  
  if (!date_col_found) stop("No recognizable date column found in the data")
  
  # Data cleaning and preparation with error handling
  df_clean <- df %>%
    mutate(
      appointment_date = tryCatch(
        {
          # Try multiple date formats if ymd fails
          parsed_date <- ymd(appointment_date)
          if (all(is.na(parsed_date))) {
            parsed_date <- mdy(appointment_date) # Try month-day-year format
          }
          if (all(is.na(parsed_date))) {
            parsed_date <- dmy(appointment_date) # Try day-month-year format
          }
          parsed_date
        },
        error = function(e) {
          stop("Failed to parse dates. Check date format in your data.")
        }
      ),
      month = floor_date(appointment_date, "month")
    ) %>%
    filter(!is.na(appointment_date))
  
  # Check if we have enough data
  if (nrow(df_clean) == 0) stop("No valid dates remaining after cleaning")
  
  # Create monthly summary of actual appointments
  monthly_appointments <- df_clean %>%
    group_by(month) %>%
    summarise(total_appointments = n(), .groups = "drop") %>%
    mutate(type = factor("Actual", levels = c("Actual", "Forecast")))
  
  # Check if we have sufficient data for time series
  if (nrow(monthly_appointments) < 12) {
    warning("Less than 12 months of data available. Forecast may be unreliable.")
  }
  
  # Convert to time series for forecasting
  appointments_ts <- ts(monthly_appointments$total_appointments, 
                        start = c(year(min(monthly_appointments$month)), 
                                 month(min(monthly_appointments$month))), 
                        frequency = 12)
  
  # Create forecast using seasonal naive method (6 months ahead)
  fit_snaive <- snaive(appointments_ts, h = 6)
  
  # Prepare forecast data frame
  forecast_df <- data.frame(
    month = seq(from = max(monthly_appointments$month) %m+% months(1),
                by = "1 month",
                length.out = length(fit_snaive$mean)),
    total_appointments = as.numeric(fit_snaive$mean),
    type = factor("Forecast", levels = c("Actual", "Forecast"))
  )
  
  # Combine actual and forecast data
  combined_df <- bind_rows(monthly_appointments, forecast_df)
  
  # Create the visualization
  p <- ggplot(combined_df, aes(x = month, y = total_appointments, color = type)) +
    geom_line(size = 1.2) +
    geom_point(size = 2) +
    scale_color_manual(values = c("Actual" = "#1f77b4", "Forecast" = "#ff7f0e")) +
    labs(
      title = "Total Appointments: Actual vs Forecast",
      subtitle = "Using Seasonal Naive Forecasting Method",
      x = "Month",
      y = "Number of Appointments",
      color = "Type"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(size = 16, face = "bold"),
      plot.subtitle = element_text(size = 12),
      legend.position = "bottom"
    ) +
    scale_y_continuous(labels = scales::comma) +
    scale_x_date(date_breaks = "3 months", date_labels = "%b %Y")
  
  # Display the plot
  print(p)
  
  # Save the plot
  ggsave("static/patient_forecast.png",
       plot = p, width = 8, height = 5)
