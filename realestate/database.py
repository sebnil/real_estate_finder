from peewee import *
import os

script_location = os.path.dirname(os.path.abspath(__file__))
database_path = script_location + '/realestate.db'
db = SqliteDatabase(database_path)

class RealEstate(Model):
    link = CharField()
    price_per_week = CharField(null=True)
    location = CharField(null=True)
    bedrooms = IntegerField(null=True)
    date_available = DateField(null=True)
    time_to_work = TimeField(null=True)
    time_from_work = TimeField(null=True)
    time_to_surfers_with_transit = TimeField(null=True)
    time_to_surfers_by_car = TimeField(null=True)

    class Meta:
        database = db