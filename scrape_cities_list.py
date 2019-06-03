import pandas as pd


def canadian_cities_scrape(url):

    # create dataframe from table in above html
    can_cities_table = pd.read_html(url)

    # It will give us all the tables in a list, we only want the first table.
    can_cities_table = can_cities_table[0]

    # Dropping columns that I do not want
    can_cities_table = can_cities_table.drop(columns=[0,3,7,8,9,10])

    # Change column names appropriately
    can_cities_table.columns = ["Cities", "Province", "Land mass(km^2, 2011)", "Growth rate 2011~2016", "Population(2016)"]

    # clean redundent data
    can_cities_table = can_cities_table.iloc[1:]

    # change cities column into a list
    canadian_cities = can_cities_table["Cities"].tolist()

    return canadian_cities


