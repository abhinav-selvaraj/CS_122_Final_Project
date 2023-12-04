from flask import Blueprint, render_template, request, jsonify
import requests #API Import
import json, time, requests
from datetime import datetime

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
    filepath = f'CS_122_Final_Project/stockDataJsons/{symbol}_data.JSON'
    with open(filepath, 'r') as file:
        contents = json.load(file)
        keyList = contents.keys()
        data = contents

    symbols = ['Select a stock', 'AAPL', 'AMZN', 'AVGO','BRK-B', 'GOOG', 'HD' , 'IBM', 'JNJ', 'JPM', 'LLY', 'MA', 'META', 'MSFT', 'NVDA', 'PG', 'TSLA','TSM','UNH', 'V', 'XOM' ] 
    return render_template('graphs.html', symbols=symbols, keyList=keyList, data=data)