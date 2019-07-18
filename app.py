from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import pymysql
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

# ---------------------------------- Database setup -------------------------------- #
# setting up which database I will use
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Gksmf12#@localhost:3306/aqi_db'

# Creating database instance
db = SQLAlchemy(app)

# SQLAlchemy represents db structure as a class(Model)
# use existing table called "aqi_info"
class Aqi(db.Model):
    __tablename__ ='aqi_info'
    id = db.Column('id', db.Integer, primary_key=True)
    Countries = db.Column(db.String(30), unique=True)
    Cities = db.Column(db.String(30), unique=True)
    aqi = db.Column(db.Integer)
    # declare how query is outputted.
    def __repr__(self):
        return f"Aqi('{self.Countries}', '{self.Cities}', '{self.aqi}')"

x = Aqi.query.filter_by(Cities="Willowdale").all()
print(x[0])
# ------------------------------------ Database setup end --------------------------------- #


# Pass list of canadian cities to app.js where it can call api for each cities.
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# @app.route("/cities/<list_of_cities>")

    
if __name__ == "__main__":
    app.run(debug=True)