import database
import sqlite3
import fb
from models import *

class Reflex(object):
    reflex_database = None
    data = None
    company = "RefleX"

    def __init__(self, data):
        self.data = data
        self.reflex_database = sqlite3.connect("in/reflex.db")

    def load_data(self):
        self.load_reflex_data()

    def load_reflex_data(self):
        print("*************************************************************")
        print("**********    IMPORTING REFLEX ROUTES AND STOPS    **********")
        print("*************************************************************")

        c = self.reflex_database.cursor()
        for route in c.execute('''select * from routes'''):
            company = route[0]
            route_id = route[1]
            route_number = route[2]
            route_name = route[3]
            direction1 = route[4]
            direction2 = route[5]
            days_active = route[6]

            new_route = Route(company, route_id, route_name, route_number, direction1, direction2, days_active)
            database.insert_route(new_route)
            self.data.saveRoute(new_route)

            self.load_stops(route_id, direction1, days_active)
            self.load_stops(route_id, direction2, days_active)

            print("IMPORTED ROUTE:", route_name, "(" + route_number + ")")

        self.reflex_database.close()

    # Load the stops alphabetically into the database
    def load_stops(self, route_id, direction, days_active):
        c = self.reflex_database.cursor()
        order = 1
        for stop in c.execute('''select * from stops where route_id=? and direction=? order by stop_number''', [route_id, direction]):
            # set derived stop properties
            company = stop[0]
            route_id = stop[1]
            direction = stop[2]
            stop_id = stop[3]
            stop_number = stop[4]
            stop_name = stop[5]
            latitude = stop[6]
            longitude = stop[7]
            stop_order = stop[8]

            # Add the stop location
            new_stop_location = StopLocation(company, route_id, direction, stop_id, stop_name, latitude, longitude)
            database.insert_stop_location(new_stop_location)
            self.data.saveStopLocation(new_stop_location)

            # Add the stop order
            new_stop_order = StopOrder(company, route_id, direction, stop_id, stop_name, order, days_active)
            database.insert_stop_order(new_stop_order)
            self.data.saveStopOrder(new_stop_order)

            # Update the stop order counter
            order = order + 1
