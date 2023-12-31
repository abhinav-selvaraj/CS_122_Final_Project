from flask import Blueprint, render_template, request, jsonify
import requests #API Import
import json, time, requests
from datetime import datetime
import numpy as np

views = Blueprint('views', __name__)







@views.route('/')
def homePage():
    symbols = ['Select a stock', 'AAPL', 'AMZN', 'AVGO','BRK-B', 'GOOG', 'HD' , 'IBM', 'JNJ', 'JPM', 'LLY', 'MA', 'META', 'MSFT', 'NVDA', 'PG', 'TSLA','TSM','UNH', 'V', 'XOM' ] 
    api_key = 'S1WA6956TYGOYFGH'
    current_time = datetime.now().time()
    print(current_time)
    if current_time.hour == 0 and current_time.minute == 0: #time for update
        print("fetching data")
        for symbol in symbols:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
            response = requests.get(url)
            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
        
            # Process the data as needed
        
            # Write the data to a new JSON file
                with open(f'/Users/CS_122_Final_Project\stockDataJsons\{symbol}_data.JSON', 'w') as json_file:
                    json.dump(data, json_file, indent=2)
                    print(f"Data for {symbol} written to {symbol}_data.json")
                
            else:
                print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")
                return "failed"  
      

    return render_template('base.html' , symbols=symbols)

@views.route('/RawData/<symbol>')
def data(symbol):
    symbols = ['Select a stock', 'AAPL', 'AMZN', 'AVGO','BRK-B', 'GOOG', 'HD' , 'IBM', 'JNJ', 'JPM', 'LLY', 'MA', 'META', 'MSFT', 'NVDA', 'PG', 'TSLA','TSM','UNH', 'V', 'XOM' ] 

    # Construct the file path based on the symbol parameter
    filepath = f'/Users/carissalee/CS_122_Final_Project/stockDataJsons/{symbol}_data.JSON'
    
   
    
    with open(filepath, 'r') as file:
        contents = json.load(file)
        keyList = contents.keys()
        data = contents

    
    # Extract numerical data
    open_prices = [float(entry["1. open"]) for entry in data["Time Series (Daily)"].values()]
    high_prices = [float(entry["2. high"]) for entry in data["Time Series (Daily)"].values()]
    low_prices = [float(entry["3. low"]) for entry in data["Time Series (Daily)"].values()]
    close_prices = [float(entry["4. close"]) for entry in data["Time Series (Daily)"].values()]
    volumes = [int(entry["5. volume"]) for entry in data["Time Series (Daily)"].values()]

    # Convert to NumPy arrays
    open_prices_array = np.array(open_prices)
    high_prices_array = np.array(high_prices)
    low_prices_array = np.array(low_prices)
    close_prices_array = np.array(close_prices)
    volumes_array = np.array(volumes)

    # Create X values (assuming sequential days)
    x_values = np.arange(len(close_prices))

    # Perform linear regression
    slope, intercept = np.polyfit(x_values, close_prices, 1)


    # Calculate minimum, maximum, and standard deviation
    min_open = np.min(open_prices_array)
    max_open = np.max(open_prices_array)
    std_open = np.std(open_prices_array)

    min_high = np.min(high_prices_array)
    max_high = np.max(high_prices_array)
    std_high = np.std(high_prices_array)

    min_low = np.min(low_prices_array)
    max_low = np.max(low_prices_array)
    std_low = np.std(low_prices_array)

    min_close = np.min(close_prices_array)
    max_close = np.max(close_prices_array)
    std_close = np.std(close_prices_array)

    min_volume = np.min(volumes_array)
    max_volume = np.max(volumes_array)
    std_volume = np.std(volumes_array)

    # Calculate daily percentage changes in closing prices
    daily_returns = np.diff(close_prices) / close_prices[:-1] * 100

    # Calculate mean, median, and standard deviation
    mean_close = np.mean(close_prices)
    median_close = np.median(close_prices)
    std_close = np.std(close_prices)

    # Calculate daily volatility
    daily_volatility = np.std(daily_returns)

    # Calculate correlation between closing prices and volumes
    correlation = np.corrcoef(close_prices, volumes)[0, 1]
    # Handle user input for timeframe
    selectedtimeframe = request.args.get('timeframe', 'weekly')

    # Calculate statistics based on the selected timeframe
    if selectedtimeframe == 'weekly':
        statistics = calculate_statistics_for_period(close_prices, period=5)  # Assuming a week has 5 days
        x_values, weekly_close_prices = aggregate_data_by_period(data["Time Series (Daily)"], period=5)
        slope, intercept = calculate_linear_regression(x_values, weekly_close_prices)
    elif selectedtimeframe == 'monthly':
        statistics = calculate_statistics_for_period(close_prices, period=20)  # Assuming a month has 20 days
        x_values, monthly_close_prices = aggregate_data_by_period(data["Time Series (Daily)"], period=20)
        slope, intercept = calculate_linear_regression(x_values, monthly_close_prices)
    else:
        return "Invalid timeframe"

    return render_template('TestAPI.html', symbols=symbols, data=data, keyList=keyList, symbol=symbol,
                           min_open=min_open, max_open=max_open, std_open=std_open,
                           min_high=min_high, max_high=max_high, std_high=std_high,
                           min_low=min_low, max_low=max_low, std_low=std_low,
                           min_close=min_close, max_close=max_close, std_close=std_close,
                           min_volume=min_volume, max_volume=max_volume, std_volume=std_volume,
                           mean_close=mean_close,
                           median_close=median_close,
                           daily_volatility=daily_volatility,
                           correlation=correlation, statistics=statistics, selectedtimeframe=selectedtimeframe,
                           slope=slope, intercept=intercept)


def calculate_statistics(data):
    mean = np.mean(data)
    median = np.median(data)
    std_dev = np.std(data)
    return {'mean': mean, 'median': median, 'std_dev': std_dev}

def calculate_statistics_for_period(data, period):
    statistics = {}
    for i in range(0, len(data), period):
        subset = data[i:i+period]
        statistics[f'{i//period + 1}'] = calculate_statistics(subset)
    return statistics

def calculate_linear_regression(x_values, y_values):
    X = np.column_stack((np.ones_like(x_values), x_values))
    coefficients = np.linalg.lstsq(X, y_values, rcond=None)[0]
    intercept, slope = coefficients
    return slope, intercept

def aggregate_data_by_period(time_series, period):
    x_values = []
    close_prices = []
    current_period = 0
    for date, data in sorted(time_series.items()):
        current_period += 1
        if current_period > period:
            current_period = 1
        x_values.append(current_period)
        close_prices.append(float(data["4. close"]))

    return np.array(x_values), np.array(close_prices)

@views.route('/<symbol>')
def graphPage(symbol):
    val_arr = []
    vol_arr = []
    filepath = f'/Users/carissalee/CS_122_Final_Project/stockDataJsons/{symbol}_data.JSON'
    with open(filepath, 'r') as file:
        contents = json.load(file)
        keyList = contents.keys()
        data = contents
        for date, values in data['Time Series (Daily)'].items():
            if '4. close' in values:  # Check if '4. close' key exists in the inner dictionary
                close_value = values['4. close']
                val_arr.append(close_value)
            if '5. volume' in values:  # Check if '4. close' key exists in the inner dictionary
                close_value = values['5. volume']
                vol_arr.append(close_value)
    
    val_arr = np.array(val_arr)
    val_arr = val_arr.astype(float)
    min_val = np.min(val_arr)
    max_val = np.max(val_arr)
    # print(val_arr)
    # print(min_val)
    # print(max_val)
    
    vol_arr  = np.array(vol_arr)
    vol_arr = vol_arr.astype(float)
    
    min_vol = np.min(vol_arr)
    max_vol = np.max(vol_arr)

    symbols = ['Select a stock', 'AAPL', 'AMZN', 'AVGO','BRK-B', 'GOOG', 'HD' , 'IBM', 'JNJ', 'JPM', 'LLY', 'MA', 'META', 'MSFT', 'NVDA', 'PG', 'TSLA','TSM','UNH', 'V', 'XOM' ] 

    return render_template('graphs.html', symbols=symbols, keyList=keyList, data=data, min_val=min_val, max_val=max_val, min_vol=min_vol, max_vol=max_vol)