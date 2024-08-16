# Disclaimer: Make sure to install the required libraries before running this code.
# Install the necessary packages using pip:
# pip install statsmodels
# pip install matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Load the CSV file into a DataFrame
file_path = r'C:\Users\KRAVEN\Documents\Project\Stock Market Analysis of AAPL\Data File\AAPL.csv'
df = pd.read_csv(file_path)

# Display the first few rows of the DataFrame
print(df.head())

# Check for missing values
missing_values = df.isnull().sum()
print("Missing Values in Each Column:\n", missing_values)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' as the index (optional but common for time series data)
df.set_index('Date', inplace=True)

# Check data types of each column
print("Data Types:\n", df.dtypes)

# Convert columns to appropriate data types if necessary
df['Open'] = df['Open'].astype(float)
df['High'] = df['High'].astype(float)
df['Low'] = df['Low'].astype(float)
df['Close'] = df['Close'].astype(float)
df['Adj Close'] = df['Adj Close'].astype(float)
df['Volume'] = df['Volume'].astype(int)

# Check for duplicate rows
duplicate_rows = df.duplicated().sum()
print("Number of Duplicate Rows:", duplicate_rows)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Check the first few rows of the cleaned DataFrame
print(df.head())

# Check the summary statistics to ensure numerical integrity
print(df.describe())

# Calculate additional statistics
mean_close = df['Close'].mean()
median_close = df['Close'].median()
std_close = df['Close'].std()

print(f"Mean Closing Price: {mean_close:.2f}")
print(f"Median Closing Price: {median_close:.2f}")
print(f"Standard Deviation of Closing Price: {std_close:.2f}")

# Plotting the closing prices over time
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label='Close Price', color='blue')
plt.title('AAPL Closing Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.legend()
plt.show()

# Calculate daily returns (percentage change)
df['Daily_Return'] = df['Close'].pct_change()

# Plotting the daily returns
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Daily_Return'], label='Daily Return', color='green')
plt.title('AAPL Daily Returns Over Time')
plt.xlabel('Date')
plt.ylabel('Daily Return (%)')
plt.legend()
plt.show()

# Calculate moving averages
df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()

# Plotting the closing price with moving averages
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label='Close Price', color='blue')
plt.plot(df.index, df['SMA_20'], label='20-Day SMA', color='orange')
plt.plot(df.index, df['SMA_50'], label='50-Day SMA', color='red')
plt.title('AAPL Closing Price with 20-Day and 50-Day Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Decompose the time series
decomposition = seasonal_decompose(df['Close'], model='multiplicative', period=30)

# Plot the decomposition
decomposition.plot()
plt.show()

# Identify crossovers
df['Signal'] = 0  # Default no signal
df['Signal'] = np.where(df['SMA_20'] > df['SMA_50'], 1, 0)  # 1 for buy signal
df['Crossover'] = df['Signal'].diff()  # 1 for buy, -1 for sell

# Plotting crossovers
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label='Close Price', color='blue')
plt.plot(df.index, df['SMA_20'], label='20-Day SMA', color='orange')
plt.plot(df.index, df['SMA_50'], label='50-Day SMA', color='red')
plt.plot(df[df['Crossover'] == 1].index, 
         df['SMA_20'][df['Crossover'] == 1], 
         '^', markersize=10, color='g', lw=0, label='Buy Signal')
plt.plot(df[df['Crossover'] == -1].index, 
         df['SMA_20'][df['Crossover'] == -1], 
         'v', markersize=10, color='r', lw=0, label='Sell Signal')
plt.title('AAPL Close Price with Buy/Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Calculate the EMA
df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()

# Plot the closing prices and EMA
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label='Close Price', color='blue')
plt.plot(df.index, df['EMA_20'], label='20-Day EMA', color='green')
plt.title('AAPL Closing Price with 20-Day EMA')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Calculate rolling standard deviation (volatility)
df['Volatility'] = df['Close'].rolling(window=20).std()

# Plot the volatility
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Volatility'], label='20-Day Rolling Std Dev', color='purple')
plt.title('AAPL Volatility (Rolling 20-Day Standard Deviation)')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()
plt.show()

plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label='Close Price', color='blue')
plt.plot(df.index, df['SMA_20'], label='20-Day SMA', color='orange')
plt.plot(df.index, df['SMA_50'], label='50-Day SMA', color='red')
plt.title('AAPL Close Price with Trend Identification')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()

# Highlighting trends
for i in range(1, len(df)):
    if df['SMA_20'][i] > df['SMA_50'][i]:
        plt.axvspan(df.index[i-1], df.index[i], color='green', alpha=0.1)  # Uptrend
    elif df['SMA_20'][i] < df['SMA_50'][i]:
        plt.axvspan(df.index[i-1], df.index[i], color='red', alpha=0.1)  # Downtrend

plt.show()

# Plotting the Close Price, SMA, and EMA with Buy/Sell Signals
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label='Close Price', color='blue')
plt.plot(df.index, df['SMA_20'], label='20-Day SMA', color='orange')
plt.plot(df.index, df['SMA_50'], label='50-Day SMA', color='red')
plt.plot(df.index, df['EMA_20'], label='20-Day EMA', color='purple')
plt.plot(df[df['Crossover'] == 1].index, 
         df['Close'][df['Crossover'] == 1], 
         '^', markersize=10, color='green', label='Buy Signal')
plt.plot(df[df['Crossover'] == -1].index, 
         df['Close'][df['Crossover'] == -1], 
         'v', markersize=10, color='red', label='Sell Signal')

plt.title('AAPL Closing Price with Moving Averages and Buy/Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Calculate Rolling Standard Deviation (Volatility)
df['Rolling_Std_20'] = df['Close'].rolling(window=20).std()

# Plotting Rolling Standard Deviation
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Rolling_Std_20'], label='20-Day Rolling Std', color='orange')
plt.title('AAPL 20-Day Rolling Standard Deviation (Volatility)')
plt.xlabel('Date')
plt.ylabel('Standard Deviation')
plt.legend()
plt.show()

# Calculate Daily Returns
df['Daily_Returns'] = df['Close'].pct_change()

# Plotting the Distribution of Daily Returns
plt.figure(figsize=(14, 7))
plt.hist(df['Daily_Returns'].dropna(), bins=50, color='blue', alpha=0.7)
plt.title('AAPL Daily Returns Distribution')
plt.xlabel('Daily Returns')
plt.ylabel('Frequency')
plt.show()
