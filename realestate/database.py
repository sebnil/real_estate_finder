from peewee import *
import os

script_location = os.path.dirname(os.path.abspath(__file__))
print script_location
db = SqliteDatabase(script_location + '/realestate.db')

class RealEstate(Model):
    link = CharField()
    price_per_week = CharField(null=True)
    location = CharField(null=True)
    bedrooms = IntegerField(null=True)
    car_spaces = IntegerField(null=True)
    date_available = DateField(null=True)
    time_to_work = TimeField(null=True)
    time_from_work = TimeField(null=True)
    time_to_surfers = TimeField(null=True)

    class Meta:
        database = db