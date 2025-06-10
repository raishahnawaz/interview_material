"""
Time Series Forecasting Example: Prophet, AirPassengers
This script demonstrates time series forecasting with Prophet.
"""

import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# --- 1. Data Loading ---
# AirPassengers dataset (monthly airline passengers 1949-1960)
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url)
df.columns = ["ds", "y"]  # Prophet expects 'ds' (date) and 'y' (value)

# --- 2. Model Training ---
model = Prophet()
model.fit(df)

# --- 3. Forecasting ---
future = model.make_future_dataframe(periods=24, freq='M')
forecast = model.predict(future)

# --- 4. Visualization ---
fig1 = model.plot(forecast)
plt.title("AirPassengers Forecast")
plt.savefig("airpassengers_forecast.png")
print("Forecast plot saved as airpassengers_forecast.png")

fig2 = model.plot_components(forecast)
plt.savefig("airpassengers_components.png")
print("Component plot saved as airpassengers_components.png") 