library(dplyr)
library(lubridate)
library(ggplot2)
library(forecast)

# Read the CSV file (assuming you've exported the SQL data to CSV)
df <- read.csv("C:\\Users\\admin\\Downloads\\teethnology_appointments.csv")

# Data cleaning and preparation
df_clean <- df %>%
  mutate(
    appointment_date = ymd(appointment_date),
    month = floor_date(appointment_date, "month")
  ) %>%
  filter(!is.na(appointment_date)) # Remove any rows with NA dates

# Create monthly summary of actual appointments
monthly_appointments <- df_clean %>%
  group_by(month) %>%
  summarise(total_appointments = n(), .groups = "drop") %>%
  mutate(type = factor("Actual", levels = c("Actual", "Forecast")))

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
ggsave("appointments_forecast.png", plot = p, width = 12, height = 6, dpi = 300)