import json
from air_quality_api import clean_json

# loading json file into data variable
with open('static/db/countries_cities3.json') as f:
    data = json.load(f)

# Clean existing json file and combine them => final_cities_countries.json
for city_list in data.values():
    for city in city_list:
        # if no data or station, delete that city.
        if not clean_json(city):
            city_list.pop(city_list.index(city))

# create json file out of cleaned json data.
with open('static/db/cleaned_cities_countries3.json', 'w', encoding='utf-8') as f:
    json.dump(data, f,  ensure_ascii=False, indent=4)