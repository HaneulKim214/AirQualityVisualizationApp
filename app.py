from flask import Flask, jsonify, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import os
import pandas as pd
import pymysql
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#my dependencies
from air_quality_api import get_aqi
from summarize_text import *


app = Flask(__name__)

# ---------------------------------- Database setup -------------------------------- #
# setting up which database I will use
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:Gksmf12#@localhost:3306/aqi_db'
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
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    time = db.Column(db.DateTime)

    def __init__(self, Country, City, Aqi, lat, lng, time):
        self.Country = Country
        self.City = City
        self.Aqi = Aqi
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
    # check if in NoSQL db. if not, call text_summarize function and store it into db then use
    # that db to retrieve info and send it to JS.
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
                lat = aqi_response['data']['city']['geo'][0]
                lng = aqi_response['data']['city']['geo'][1]
                time = aqi_response['data']['time']['s']

                # creating instance of Aqi class(row in MySQL table) and inserting into aqi table
                insert_to_db = Aqi(country, city, aqi_response['data']['aqi'], lat, lng, time)
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


if __name__ == "__main__":
    app.run(debug=True)