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


app = Flask(__name__)

# ---------------------------------- Database setup -------------------------------- #
# setting up which database I will use
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Gksmf12#@localhost:3306/aqi_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # Creating database instance
db = SQLAlchemy(app)

# SQLAlchemy represents db structure as a class(Model)
# Creating table. class name = table name
class Aqi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Country = db.Column(db.String(30), unique=True)
    City = db.Column(db.String(30), unique=True)
    Aqi = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __init__(self, Country, City, Aqi, lat, lng):
        self.Country = Country
        self.City = City
        self.Aqi = Aqi
        self.lat = lat
        self.lng = lng

    # ????????????? declare how query is outputted.
    def __repr__(self):
        return f"Aqi('{self.Countries}', '{self.Cities}', '{self.aqi}')"

# example = Aqi("Canada", "Trontn", 23, 123.3, 12.2)
# db.session.add(example)
# db.session.commit()
# x = Aqi.query.filter_by(Cities="Willowdale").all()
# print(x[0])
# ------------------------------------ Database setup end --------------------------------- #


# Pass list of canadian cities to app.js where it can call api for each cities.
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/cities/<country>")
def cities(country):
    """ for given country
    1. get list of cities from json file.
    2. loop through each city and call api to get AQI data.
    3. store into db
    4. return {city:[], aqi:[], lat_lng:[a,b]} so heat map can be made.
    """
    # openning json file in python.
    with open('static/db/final_cities_countries.json') as f:
        data = json.load(f)

    # list of cities for inputted country.
    list_of_cities = data[country]
    for city in list_of_cities:

        # store into db if aqi_call is successful with status:ok
        if get_aqi(city) != None:
            aqi_response = get_aqi(city)
            lat = aqi_response['data']['city']['geo'][0]
            lng = aqi_response['data']['city']['geo'][1]

            #creating instance of Aqi class(row in table MySQL) and insert to db
            aqi_data = Aqi(country, city, aqi_response['data']['aqi'], lat, lng)
            db.session.add(aqi_data)
            db.session.commit()

    return country

@app.route("/hardships")
def hardships():
    return render_template('hardships.html')
if __name__ == "__main__":
    app.run(debug=True)