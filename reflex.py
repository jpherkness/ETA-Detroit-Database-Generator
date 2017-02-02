import database
import sqlite3
import fb
from models import *

reflex_database = sqlite3.connect("in/reflex.db")

routes = []
stop_orders = []
stop_locations = []
company = "RefleX"

def load_data(all_routes, all_stop_orders, all_stop_locations):
    load_reflex_data()
    all_routes += routes
    all_stop_orders += stop_orders
    all_stop_locations += stop_locations

def load_reflex_data():
    print("*************************************************************")
    print("**********    IMPORTING REFLEX ROUTES AND STOPS    **********")
    print("*************************************************************")

    c = reflex_database.cursor()
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
        routes.append(new_route.__dict__)

        load_stops(route_id, direction1, days_active)
        load_stops(route_id, direction2, days_active)

        print("IMPORTED ROUTE:", route_name, "(" + route_number + ")")

    reflex_database.close()

# Load the stops alphabetically into the database
def load_stops(route_id, direction, days_active):
    c = reflex_database.cursor()
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
        stop_locations.append(new_stop_location.__dict__)

        # Add the stop order
        new_stop_order = StopOrder(company, route_id, direction, stop_id, stop_name, order, days_active)
        database.insert_stop_order(new_stop_order)
        stop_orders.append(new_stop_order.__dict__)

        # Update the stop order counter
        order = order + 1
