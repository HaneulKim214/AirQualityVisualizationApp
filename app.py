from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd

app = Flask(__name__)
# setting up database location
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Gksmf12#@localhost:3306/aqi_db'

# Creating database instance.
db = SQLAlchemy(app)

# SQLAlchemy represents database structure as a class and these classes are called Model
class Aqi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(30), unique=True)
    cities = db.Column(db.String(50), unique=True)
    aqi_info = db.Column(db.Integer)

    # declare how our object is printed 
    def __repr__(self):
        return f"Aqi('{self.country}', '{self.cities}', '{self.aqi_info}')"




# Pass list of canadian cities to app.js where it can call api for each cities.
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/cities/<list_of_cities>")

    
if __name__ == "__main__":
    app.run(debug=True)