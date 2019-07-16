from itertools import chain, repeat
import json
import os
from pprint import pprint
import pandas as pd
import requests

beijing_api = os.environ.get('AQI_api_key')
def get_aqi(city):
    url = f'https://api.waqi.info/feed/{city}/?token={beijing_api}'
    response = requests.get(url).json()
    # if station DNE return none otherwise return AQI information
    if response['status'] == 'error':
        return None
    else:
        #return AQI info for each city.
        return response["data"]["aqi"]

# loading json file into data variable
with open('static/db/sample.json') as f:
    data = json.load(f) 

chainer = chain.from_iterable
countries_cities_df = pd.DataFrame.from_dict({'Countries':list(chainer(repeat(k, len(v)) for k,v in data.items())),
                            'Cities':list(chainer(data.values()))})

# for each city, get AQI data and add it to new column called "AQI".
for index, row in countries_cities_df.iterrows():
    city = countries_cities_df["Cities"].values[index]
    countries_cities_df["AQI"] = get_aqi(city) # passing in city name to get_aqi function which returns AQI data.

countries_cities_df.head()