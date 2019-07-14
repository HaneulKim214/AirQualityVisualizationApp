from flask import Flask, jsonify, render_template
import os
import pandas as pd


# My dependencies
import scrape_cities_list


app = Flask(__name__)


# for list of 100 largest canadian cities by pop
can_cities_url = "https://en.wikipedia.org/wiki/List_of_the_100_largest_municipalities_in_Canada_by_population"

# returned list of cities and population
can_cities, can_pop2016 = scrape_cities_list.canadian_cities_scrape(can_cities_url)



# Pass list of canadian cities to app.js where it can call api for each cities.
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html", 
                            canada_cities=can_cities,
                            pop=can_pop2016)

@app.route("/search/<cities>")
def location(cities):
    print(cities)
    return(jsonify(cities))

    
if __name__ == "__main__":
    app.run(debug=True)