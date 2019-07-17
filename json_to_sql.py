from itertools import chain, repeat
import json
import os
from pprint import pprint
import pymysql
import pandas as pd
import requests
import sqlalchemy

# connect to db names 'aqi_db'
engine = sqlalchemy.create_engine('mysql+pymysql://root:Gksmf12#@localhost:3306/aqi_db')

# loading json file into data variable
with open('static/db/countries_cities.json') as f:
    data = json.load(f)
aqi_list = []

beijing_api = os.environ.get('AQI_api_key')

# for each city, if aqi data exists append it to aqi_list
def get_aqi(city):
    url = f'https://api.waqi.info/feed/{city}/?token={beijing_api}'
    response = requests.get(url).json()
    if response['status'] == 'ok':
        aqi_list.append(response["data"]["aqi"])
    else: 
        aqi_list.append(None)
        pass

chainer = chain.from_iterable
countries_cities_df = pd.DataFrame.from_dict({'Countries':list(chainer(repeat(k, len(v)) for k,v in data.items())),
                            'Cities':list(chainer(data.values()))})

for index, row in countries_cities_df.iterrows():
    city = countries_cities_df["Cities"].values[index]
    get_aqi(city)
    
# adding AQI column into df.
countries_cities_df["AQI"] = aqi_list

# convert df -> SQL
countries_cities_df.to_sql(
    name="aqi_info",
    con=engine,
    index=False,
    if_exists="append"
)