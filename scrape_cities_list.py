import pandas as pd

def canadian_cities_scrape(url):

    # create dataframe from table in above html
    can_cities_table = pd.read_html(url)

    # It will give us all the tables in a list, we only want the first table.
    can_cities_table = can_cities_table[0]
    
    # Dropping columns that I do not want
    can_cities_table = can_cities_table.drop(columns=["Rank(2016)", 
                                                    "Municipal status",
                                                    "Province",
                                                    "Population(2011)",
                                                    "Population(2006)",
                                                    "Population(2001)",
                                                    "Population(1996)"])

    # Just renaming first column
    can_cities_table.rename(columns={"Municipality": "City"}, inplace=True)
    
    # City, population column into a list.
    can_cities = can_cities_table["City"].tolist()
    can_pop2016 = can_cities_table["Population(2016)"].tolist()


    return can_cities, can_pop2016


