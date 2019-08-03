from flask import Flask, jsonify, request, redirect, render_template
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
import json
import os
import pandas as pd
import pymysql
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import time

#my dependencies
from AirQualityVisualzationApp.air_quality_api import get_aqi
from summarize_text import *



app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# ---------------------------------- Database setup -------------------------------- #
# setting up which database I will use
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', '') or 'mysql://root:Gksmf12#@localhost:3306/aqi_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # Creating database instance
db = SQLAlchemy(app)

# SQLAlchemy represents db structure as a class(Model)
# Creating table. class name = table name
class Aqi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Country = db.Column(db.String(30))
    City = db.Column(db.String(50))
    Aqi = db.Column(db.String(10))

    o3 = db.Column(db.Float)
    so2 = db.Column(db.Float)
    no2 = db.Column(db.Float)
    pm25 = db.Column(db.Float)
    co = db.Column(db.Float)

    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    time = db.Column(db.DateTime)

    def __init__(self, Country, City, Aqi,o3, so2, no2, pm25, co, lat, lng, time):
        self.Country = Country
        self.City = City
        self.Aqi = Aqi
        self.o3 = o3
        self.so2 = so2
        self.no2 = no2
        self.pm25 = pm25
        self.co = co
        self.lat = lat
        self.lng = lng
        self.time = time

    # ????????????? declare how query is outputted.
    def __repr__(self):
        return f"Aqi('{self.Countries}', '{self.Cities}', '{self.aqi}')"

# ------------------------------------ Database setup end --------------------------------- #
# Pass list of canadian cities to app.js where it can call api for each cities.
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/nlp/<country>")
def text_summarization(country):
    """
    For inputted country, grab its paragraphs from wikipedia and summarize it.
    """
    summarized_text = text_summarizer(country)
    return jsonify(summarized_text)

@app.route("/cities/<country>")
def cities(country):
    """ for given country
    1. get list of cities from json file.
    2. loop through each city and call api to get AQI data.
    3. store into db
    4. return {city:[], aqi:[], lat_lng:[a,b]} so heat map can be made.
    """
    with open('static/db/final_cities_countries.json') as f:
        data = json.load(f)

    # if data exists grab data, if not query again and store into db, then grab data
    query = db.select([Aqi]).where(Aqi.Country == country)
    result = db.engine.execute(query).fetchall()
    if len(result) < 1:
        list_of_cities = data[country]
        for city in list_of_cities:
            # store into db if aqi_call is ONLY successful with status:ok
            if get_aqi(city) != None:
                aqi_response = get_aqi(city)
                time = aqi_response['data']['time']['s']
                try:
                    lat = aqi_response['data']['city']['geo'][0]
                    lng = aqi_response['data']['city']['geo'][1]
                except:
                    continue # skipping city that have no defined coordinates.

                # Top 5 pollutants
                try:
                    o3 = aqi_response['data']['iaqi']['o3']['v']
                except:
                    o3 = -1
                try:
                    so2 = aqi_response['data']['iaqi']['so2']['v']
                except:
                    so2 = -1
                try:
                    no2 = aqi_response['data']['iaqi']['no2']['v']
                except:
                    no2 = -1
                try:
                    pm25 = aqi_response['data']['iaqi']['pm25']['v'] #pm2.5
                except:
                    pm25 = -1
                try:
                    co = aqi_response['data']['iaqi']['co']['v']
                except:
                    co = -1

                # creating instance of Aqi class(row in MySQL table) and inserting into aqi table
                insert_to_db = Aqi(country, city, aqi_response['data']['aqi'], o3, so2, no2, pm25, co, lat, lng, time)
                db.session.add(insert_to_db)
                db.session.commit()

        # this time it will have more  
        query = db.select([Aqi]).where(Aqi.Country == country)
        # result = [(id, country, city,...), (id, country, city,...), ...etc.]
        result = db.engine.execute(query).fetchall()
    
    # sending back list of dictionaries. [{id:x, country:y, city:z, etc...}, {},{},...]
    return jsonify([dict(row) for row in result])


@app.route("/hardships")
def hardships():
    return render_template('hardships.html')


# Auto update MySQL DB every 24hours. --> runs parallely.
@scheduler.task('interval', id="update_aqi", hours=23)
def update_aqi():
    """
    Every 24 hours, update aqi, time column for each city with api_received response
    """ 
    query = db.select([Aqi.id, Aqi.City])
    result = db.engine.execute(query).fetchall()
    for each_city in result:
        current_city = each_city[1]
        current_id = each_city[0]
        aqi_response = get_aqi(current_city)
        returned_aqi_data = aqi_response['data']['aqi']
        returned_time = aqi_response['data']['time']['s']

        update_this = Aqi.query.filter_by(id=current_id).first()
        update_this.Aqi = returned_aqi_data
        update_this.time = returned_time
        db.session.commit()

    return f"updated at {time.strftime('%Y/%m/%d, %H:%M%S')}"


if __name__ == "__main__":
    app.run(debug=True)