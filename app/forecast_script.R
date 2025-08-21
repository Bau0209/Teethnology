library(dplyr)
library(lubridate)
library(ggplot2)
library(forecast)
library(tibble)

# Load CSV
df_raw <- read.csv("C:\\Users\\admin\\Downloads\\csv\\transacts.csv",
                   stringsAsFactors = FALSE)

# Clean
df_clean <- df_raw %>%
  mutate(
    transaction_datetime = ymd_hms(transaction_datetime),
    month = floor_date(transaction_datetime, "month"),
    month_label = factor(month.abb[month(transaction_datetime)], 
                         levels = month.abb, ordered = TRUE) # short month names Jan-Dec
  )

# Aggregate monthly revenue (by month only, across all years)
monthly_df <- df_clean %>%
  group_by(month_label) %>%
  summarise(total_revenue = sum(total_amount_paid), .groups = "drop") %>%
  mutate(type = factor("Actual", levels = c("Actual", "Forecast")))

# Build time series with frequency 12 (monthly pattern)
revenue_ts <- ts(monthly_df$total_revenue, frequency = 12)
fit_snaive <- snaive(revenue_ts, h = 6)

# Forecast results (next 6 months)
forecast_df <- data.frame(
  month_label = factor(rep(month.abb, length.out = length(fit_snaive$mean)),
                       levels = month.abb, ordered = TRUE),
  total_revenue = as.numeric(fit_snaive$mean),
  type = factor("Forecast", levels = c("Actual", "Forecast"))
)

# Combine actual + forecast
combined_df <- bind_rows(monthly_df, forecast_df)

# Plot (x = month names only)
p <- ggplot(combined_df, aes(x = month_label, y = total_revenue, color = type, group = type)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  scale_color_manual(values = c("Actual" = "blue", "Forecast" = "red")) +
  labs(
    title = "Revenue by Month: Actual vs Forecast (Seasonal Naive)",
    x = "Month",
    y = "Revenue",
    color = "Legend"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 12, color = "#00898E", face = "bold"),
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

# Save chart as PNG
save_dir <- "C:\\Users\\admin\\Teethnology\\Teethnology\\app\\static"
dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)

ggsave(file.path(save_dir, "forecast.png"),
       plot = p, width = 8, height = 5, dpi = 150)