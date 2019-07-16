from flask import Flask, jsonify, render_template
import os
import pandas as pd


# My dependencies
# import scrape_cities_list


app = Flask(__name__)


# Pass list of canadian cities to app.js where it can call api for each cities.
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

    
if __name__ == "__main__":
    app.run(debug=True)