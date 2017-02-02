import database
import sqlite3
import fb
from models import *

ddot_database = sqlite3.connect("in/ddot.db")

routes = []
stop_orders = []
stop_locations = []
company = "DDOT"

def load_data(all_routes, all_stop_orders, all_stop_locations):
    load_ddot_data()
    all_routes += routes
    all_stop_orders += stop_orders
    all_stop_locations += stop_locations

def load_ddot_data():
    print("*************************************************************")
    print("**********     IMPORTING DDOT ROUTES AND STOPS     **********")
    print("*************************************************************")

    c = ddot_database.cursor()
    for route in c.execute('''select * from routes'''):

        route_id = route[1]
        route_name = route[3]
        route_number = route[2].lstrip("0")
        direction1, direction2 = get_directions(route_id)

        new_route = Route(company, route_id, route_name, route_number, direction1, direction2, "Everyday")
        database.insert_route(new_route)
        routes.append(new_route.__dict__)

        load_stops(route_id, direction1)
        load_stops(route_id, direction2)

        print("IMPORTED ROUTE:", route_name, "(" + route_number + ")")


    # Close our connection
    ddot_database.close()

def get_directions(route_id):
    c2 = ddot_database.cursor()
    c2.execute('''select * from routedirections where rt=?''', [route_id])
    direction1 = c2.fetchone()[2].replace("\r", "")
    direction2 = c2.fetchone()[2].replace("\r", "")
    return (direction1, direction2)

def load_stops(route_id, direction):
    c = ddot_database.cursor()
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
        new_stop_location = StopLocation(company, route_id, direction, stop_id, stop_name, latitude, longitude)
        database.insert_stop_location(new_stop_location)
        stop_locations.append(new_stop_location.__dict__)

        # Add the stop order
        new_stop_order = StopOrder(company, route_id, direction, stop_id, stop_name, stop_order, "Everyday")
        database.insert_stop_order(new_stop_order)
        stop_orders.append(new_stop_order.__dict__)

        # Update the stop order counter
        stop_order = stop_order + 1
