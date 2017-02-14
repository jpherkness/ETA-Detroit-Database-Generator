import database
import sqlite3
import fb
from models import *

class DDOT(object):
    ddot_database = None
    data = None
    company = "DDOT"

    def __init__(self, data):
        self.data = data
        self.ddot_database = sqlite3.connect("in/ddot.db")

    def load_data(self):
        self.load_ddot_data()

    def load_ddot_data(self):
        print("*************************************************************")
        print("**********     IMPORTING DDOT ROUTES AND STOPS     **********")
        print("*************************************************************")

        c = self.ddot_database.cursor()
        for route in c.execute('''select * from routes'''):

            route_id = route[1]
            route_name = route[3]
            route_number = route[2].lstrip("0")
            direction1, direction2 = self.get_directions(route_id)

            # If reflex already has this route, ignore it
            skip = False
            if "reflex" in self.data.all_routes:
                for reflex_route in self.data.all_routes["reflex"]:
                    if reflex_route["route_id"] == route_id:
                        skip = True
                        break
            if skip:
                continue

            new_route = Route(self.company, route_id, route_name, route_number, direction1, direction2, "Everyday")
            database.insert_route(new_route)
            self.data.saveRoute(new_route)

            self.load_stops(route_id, direction1)
            self.load_stops(route_id, direction2)

            print("IMPORTED ROUTE:", route_name, "(" + route_number + ")")


        # Close our connection
        self.ddot_database.close()

    def get_directions(self, route_id):
        c2 = self.ddot_database.cursor()
        c2.execute('''select * from routedirections where rt=?''', [route_id])
        direction1 = c2.fetchone()[2].replace("\r", "")
        direction2 = c2.fetchone()[2].replace("\r", "")
        return (direction1, direction2)

    def load_stops(self, route_id, direction):
        c = self.ddot_database.cursor()
        c.execute('''select * from stops where rt=? and dir=?''', [route_id, direction])
        stops = c.fetchall()
        stops.sort(key=lambda stop: stop[5])

        stop_order = 1
        for stop in stops:
            # set derived stop properties
            stop_id = stop[1]
            stop_name = stop[2]
            latitude = stop[3]
            longitude = stop[4]

            # Add the stop location
            new_stop_location = StopLocation(self.company, route_id, direction, stop_id, stop_name, latitude, longitude)
            database.insert_stop_location(new_stop_location)
            self.data.saveStopLocation(new_stop_location)

            # Add the stop order
            new_stop_order = StopOrder(self.company, route_id, direction, stop_id, stop_name, stop_order, "Everyday")
            database.insert_stop_order(new_stop_order)
            self.data.saveStopOrder(new_stop_order)

            # Update the stop order counter
            stop_order = stop_order + 1
