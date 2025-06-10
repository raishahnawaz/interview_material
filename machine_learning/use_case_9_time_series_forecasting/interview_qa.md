# Time Series Forecasting Interview Q&A

## General Questions

**Q: What are common approaches to time series forecasting?**
A: Classical (ARIMA, Exponential Smoothing), machine learning (RandomForest, XGBoost), and deep learning (LSTM, GRU, TCN), as well as specialized models like Prophet.

**Q: What are key challenges in time series forecasting?**
A: Seasonality, trend, missing data, outliers, and non-stationarity.

**Q: Why use Prophet for time series?**
A: Prophet is robust, handles seasonality/holidays, and is easy to use for business users.

## Code-Specific Questions

**Q: How is the AirPassengers dataset loaded and prepared?**
A: Loaded from CSV, converted to Prophet's expected format (`ds`, `y`).

**Q: How is forecasting performed in this example?**
A: The model is fit to historical data, then used to predict future values with `predict`.

**Q: How are forecasts visualized?**
A: The code plots historical and forecasted values using matplotlib. 