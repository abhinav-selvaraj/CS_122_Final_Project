from flask import Blueprint, render_template
import requests #API Import
import json


views = Blueprint('views', __name__)

@views.route('/')
def homePage():
   

    return render_template('base.html')

@views.route('/TestAPI')
def data():
    #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=S1WA6956TYGOYFGH' #test
    #r = requests.get(url)
    #data = r.json()
    
    filepath = './IBM_TIME_SERIES_DATA.json'
    with open(filepath, 'r') as file:
        contents = json.load(file)
        keyList = contents.keys()
        data = contents
       
    return render_template('TestAPI.html', data=data, keyList=keyList)
    
  

