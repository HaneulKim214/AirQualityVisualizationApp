from itertools import chain, repeat
import json
from pprint import pprint
import pandas as pd

# loading json file into data variable
with open('static/db/sample.json') as f:
    data = json.load(f) 


chainer = chain.from_iterable
countries_cities_df = pd.DataFrame.from_dict({'Countries':list(chainer(repeat(k, len(v)) for k,v in data.items())),
                            'Cities':list(chainer(data.values()))})

# Loop through each row in DataFrame and fill up AQI column with corresponding city.
for index, row in countries_cities_df.iterrows():
    print(index)
    countries_cities_df["AQI"] = get_aqi(countries_cities_df["Cities"]) #passing in city name to get_aqi function which returns AQI data.

print(countries_cities_df.head())


# {country:[cities],
#  country2: [cities],
#  country3: [cities],....}
def get_aqi(city):
    