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
                with open(f'CS_122_Final_Project\stockDataJsons\{symbol}_data.JSON', 'w') as json_file:
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
    filepath = f'CS_122_Final_Project/stockDataJsons/{symbol}_data.JSON'
    
   
    
    with open(filepath, 'r') as file:
        contents = json.load(file)
        keyList = contents.keys()
        data = contents

    

    return render_template('TestAPI.html', symbols=symbols, data=data, keyList=keyList, symbol=symbol)
  

@views.route('/<symbol>')
def graphPage(symbol):
    val_arr = []
    vol_arr = []
    filepath = f'CS_122_Final_Project/stockDataJsons/{symbol}_data.JSON'
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