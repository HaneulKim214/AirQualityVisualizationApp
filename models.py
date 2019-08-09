from app import db

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