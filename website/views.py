from flask import Blueprint
import requests #API Import







views = Blueprint('views', __name__)

@views.route('/')
def home():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=S1WA6956TYGOYFGH' #test
    r = requests.get(url)
    data = r.json()

    #print(data)
    return data