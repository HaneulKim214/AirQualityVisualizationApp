from flask import Flask, jsonify, render_template
import os
import pandas as pd


# My dependencies
import scrape_cities_list


app = Flask(__name__)


# for list of 100 largest canadian cities by pop
can_cities_url = "https://en.wikipedia.org/wiki/List_of_the_100_largest_municipalities_in_Canada_by_population"

# Using function from scrape_cities_list.py to scrape table from html and get list of 100 cities
canadian_cities = scrape_cities_list.canadian_cities_scrape(can_cities_url)

print(canadian_cities)

# Pass list of canadian cities to app.js where it can call api for each cities.
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html", canada_cities=canadian_cities)

    
if __name__ == "__main__":
    app.run(debug=True)