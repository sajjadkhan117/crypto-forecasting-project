import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from tkinter import Tk, Button, Label, StringVar, OptionMenu, Frame
from tkinter.messagebox import showinfo, showerror
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# Global canvas and flags
canvas_widget = None
auto_refresh = True

# Fetch crypto data
def fetch_data(asset):
    try:
        data = yf.download(asset, period="7d", interval="1h", progress=False)
        if data.empty:
            raise ValueError("No data fetched")
        data.reset_index(inplace=True)
        data.rename(columns={
            'Datetime': 'timestamp',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }, inplace=True)
        return data[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    except Exception as e:
        showerror("Data Error", f"Error fetching data: {e}")
        return pd.DataFrame()

# Show chart with indicators
def show_plot():
    global canvas_widget
    data = fetch_data(asset_var.get())
    if data.empty:
        return

    data['SMA_20'] = data['close'].rolling(window=20).mean()
    data['EMA_20'] = data['close'].ewm(span=20, adjust=False).mean()
    data['RSI'] = compute_rsi(data['close'])
    data['Upper_BB'], data['Lower_BB'] = compute_bollinger_bands(data['close'])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    ax1.plot(data['timestamp'], data['close'], label='Close')
    ax1.plot(data['timestamp'], data['SMA_20'], label='SMA 20', linestyle='--')
    ax1.plot(data['timestamp'], data['EMA_20'], label='EMA 20', linestyle=':')
    ax1.plot(data['timestamp'], data['Upper_BB'], label='Upper BB', color='orange', linestyle='-.')
    ax1.plot(data['timestamp'], data['Lower_BB'], label='Lower BB', color='orange', linestyle='-.')
    ax1.set_title(f'{asset_var.get()} Price with SMA, EMA, BB')
    ax1.legend()

    ax2.plot(data['timestamp'], data['RSI'], label='RSI', color='purple')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='green', linestyle='--')
    ax2.set_title("Relative Strength Index (RSI)")
    ax2.legend()

    fig.tight_layout()
    fig.savefig("crypto_chart.png")

    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()

    canvas_widget = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack()

# RSI Calculation
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Bollinger Bands Calculation
def compute_bollinger_bands(series, window=20, num_std=2):
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper_band = sma + num_std * std
    lower_band = sma - num_std * std
    return upper_band, lower_band

# Stationarity Test
def stationarity_test():
    data = fetch_data(asset_var.get())
    if data.empty:
        return
    result = adfuller(data['close'].dropna())
    p_value = result[1]
    if p_value < 0.05:
        showinfo("Stationarity Test", "✅ Data is stationary (p < 0.05)")
    else:
        showinfo("Stationarity Test", "❌ Data is NOT stationary (p ≥ 0.05)")

# ARIMA Forecast
def run_arima():
    data = fetch_data(asset_var.get())
    if data.empty:
        return
    series = data['close'].fillna(method='ffill')
    model = ARIMA(series, order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=24)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(series.index[-100:], series.values[-100:], label='Actual')
    ax.plot(range(len(series), len(series) + 24), forecast, label='Forecast', color='red')
    ax.set_title(f'{asset_var.get()} Forecast (Next 24 Hours)')
    ax.legend()

    global canvas_widget
    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()

    canvas_widget = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack()

    forecast_df = pd.DataFrame({'forecast_price': forecast})
    filename = f"{asset_var.get().replace('-', '')}_forecast.csv"
    forecast_df.to_csv(filename, index=False)
    showinfo("Saved", f"Forecast saved to {filename}")

# Auto-refresh
def auto_refresh_loop():
    while auto_refresh:
        time.sleep(60)
        try:
            show_plot()
        except Exception as e:
            print(f"Auto-refresh error: {e}")

# GUI Setup
window = Tk()
window.title("Crypto Forecasting App")
window.geometry("800x700")

Label(window, text="Crypto Forecasting App", font=("Arial", 16)).pack(pady=10)

asset_var = StringVar(window)
asset_var.set("ETH-USD")
assets = ["ETH-USD", "BTC-USD"]
OptionMenu(window, asset_var, *assets).pack(pady=5)

Button(window, text="📈 Show Chart with SMA/EMA/RSI/BB", command=show_plot).pack(pady=5)
Button(window, text="📊 Stationarity Test (ADF)", command=stationarity_test).pack(pady=5)
Button(window, text="🔮 Forecast + Save to CSV", command=run_arima).pack(pady=5)

chart_frame = Frame(window)
chart_frame.pack(pady=10)

threading.Thread(target=auto_refresh_loop, daemon=True).start()

window.mainloop()
