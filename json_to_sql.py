from air_quality_api import get_aqi
from itertools import chain, repeat
import json
import pymysql
import pandas as pd
import requests
import sqlalchemy
import time

aqi_list = []
# connect to db named 'aqi_db'
engine = sqlalchemy.create_engine('mysql+pymysql://root:Gksmf12#@localhost:3306/aqi_db')

# loading json file into data variable
with open('static/db/final_cities_countries.json') as f:
    data = json.load(f)

# # creating df with countries and cities. for each city there will be corresponding country.
# chainer = chain.from_iterable
# countries_cities_df = pd.DataFrame.from_dict({'Countries':list(chainer(repeat(k, len(v)) for k,v in data.items())),
#                             'Cities':list(chainer(data.values()))})


# # for each city call air quality api and append to aqi_list if exists appropriate aqi data.
# for index, row in countries_cities_df.iterrows():
#     city = countries_cities_df["Cities"].values[index]
#     aqi_list.append(get_aqi(city))
        
# # adding AQI column into df.
# countries_cities_df["AQI"] = aqi_list

# # convert df -> SQL
# countries_cities_df.to_sql(
#     name="aqi_info", # Creates table named aqi_info
#     con=engine,
#     index=False,d
#     if_exists="append"
# )