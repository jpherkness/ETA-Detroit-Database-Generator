# To use this file, cd into this files directory and run the following commands:
#
# > pip3 install requests
# > python3 smartDataImporter.py
#
# The data will be saved in the current directory in both json and csv formats

import json
import csv
import requests
import os
import database
import difflib
import sqlite3
import fb
from models import *

current_path = os.path.dirname(os.path.abspath(__file__))

routes = []
stop_orders = []
stop_locations = []

company = "SmartBus"

def load_data(all_routes, all_stop_orders, all_stop_locations):
    load_smart_data()
    all_routes += routes
    all_stop_orders += stop_orders
    all_stop_locations += stop_locations

def load_smart_data():

    print("*************************************************************")
    print("**********   IMPORTING SMARTBUS ROUTES AND STOPS   **********")
    print("*************************************************************")
    routes_request = requests.get("http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getroutesforselect").json()
    for route in routes_request:
        route_id = route["Value"]
        route_number = route_id
        route_name = route["Text"].replace(route["Value"] + " - ", "")

        # Get both possible directions for the route
        direction_request = requests.get("http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getdirectionbyroute&routeid=" + route_id).json()
        direction1 = direction_request[0]
        direction2 = direction_request[1]

        # Add the days that the route is active
        days = requests.get("http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getservicedaysforschedules&routeid=" + route_id).json()
        days_array = []
        for day in days:
            days_array.append(day["Text"])
            load_stop_orders(day["Text"], day["Value"], direction1, route_id)
            load_stop_orders(day["Text"], day["Value"], direction2, route_id)
        days_active = ",".join(days_array)

        # Add the route to the sqlite database and firebase
        new_route = Route(company, route_id, route_name, route_number, direction1, direction2, days_active)
        database.insert_route(new_route)
        routes.append(new_route.__dict__)

        # Load all stop locations for both direction1 and direction2
        load_all_stops(route_id, direction1)
        load_all_stops(route_id, direction2)

        print("IMPORTED ROUTE:", route_name, "(" + route_number + ")")


def load_stop_orders(stop_day, day_code, direction, route_id):
    stops_request = requests.get("http://www.smartbus.org/DesktopModules/SMART.Schedules/ScheduleService.ashx?route="+ route_id +"&scheduleday="+ day_code +"&direction="+ direction).json()
    # sorts stops by name
    # stops_request = sorted(stops_request, key=lambda stop: stop["Name"])
    stop_order = 1
    for stop in stops_request:
        # set derived stop properties
        stop_name = stop["Name"]

        # Add the stop order
        new_stop_order = StopOrder(company, route_id, direction, None, stop_name, stop_order, stop_day)
        database.insert_stop_order(new_stop_order)
        stop_orders.append(new_stop_order.__dict__)

        # Update the stop order counter
        stop_order = stop_order + 1

def load_all_stops(route_id, direction):
    stops_request = requests.get("http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getstopsbyrouteanddirection&routeid=" + route_id + "&d=" + direction).json()
    for stop in stops_request:
        # Set derived stop properties
        stop_id = stop["StopId"]
        stop_name = stop["Name"]
        latitude = stop["Latitude"]
        longitude = stop["Longitude"]

        # Add the stop location
        new_stop_location = StopLocation(company, route_id, direction, stop_id, stop_name, latitude, longitude)
        database.insert_stop_location(new_stop_location)
        stop_locations.append(new_stop_location.__dict__)

# Creates a csv file with the contents of the array at the specified file path
def export_array_to_csv(array, file_name):
    with open(file_name, "w") as f:
        w = csv.writer(f)

        # If there are no items, then nothing to write...
        if len(array) <= 0:
            return

        # Write the keys as the first row
        keys = list(array[0].keys())
        keys.sort()
        w.writerow(keys)

        # Write each row to correspond with the keys
        for obj in array:
            row = []
            for key in keys:
                row.append(obj[key])
            w.writerow(row)

        print("EXPORTED:", current_path + "/" + file_name)

def update_smart_stop_ids():
    connection = database.connect()
    c = connection.cursor()
    for stop in c.execute('select * from stop_orders'):
        get_matching_stop_id_within_bounds(stop[1], stop[2], stop[4])

def get_matching_stop_id_within_bounds(route_id, direction, stop_name):
    connection = database.connect()
    c = connection.cursor()
    #search_name = "".join(sorted(stop_name.replace("&", "+"))).lstrip()
    search_name = "".join(sorted(stop_name.replace("+", "&").split(" "))).replace(" ", "")
    current_best_delta = 0
    current_best_name = ""
    current_best_stop_id = None

    for location in c.execute('select * from stop_locations'):
        original_name = location[4]
        match_name = "".join(sorted(original_name.split(" "))).replace(" ", "")
        delta = difflib.SequenceMatcher(None, search_name, match_name).ratio()
        #print("       ", search_name, match_name, delta)
        if delta > current_best_delta:
            current_best_delta = delta
            current_best_name = original_name
            current_best_stop_id = location[3]

    print(stop_name.ljust(30), "->" , current_best_name.ljust(30),current_best_stop_id.ljust(30), current_best_delta)

# All routes can be found here:
# http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getroutesforselect
#
# Both directions for a specific route can be found here:
# http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getdirectionbyroute&routeid=140
# The directions are not always NORTHBOUND and SOUTHBOUND, they might be EASTBOUND and WESTBOUND
#
# Ordered route stops (stop name and schedules) can be found here:
# http://www.smartbus.org/DesktopModules/SMART.Schedules/ScheduleService.ashx?route=140&scheduleday=2&direction=NORTHBOUND
#
# All route stops (longitude, latitude, stop name, and stop id) can be found here:
# http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getstopsbyrouteanddirection&routeid=140&d=Northbound
# The stop names that this endpoint returns prevents us from ever matching the ordered stops to a specific location
# (DEARBORN TRANSIT CTR vs DEARBORN TRANSIT CENTER) as well as many other naming issues.
# Currently, I don't see a way to match the ordered stops to their location without using a percentage based string comparison algorithm.
#
# A detailed description of a route can be found here:
# http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getroutebyid&routeid=140
#
#
# Questions
# 1. Do you want the output as a mongodb or csv?
# 2. Should I create a new table for just the stop orders
#       Routes
#       Stops
#       Schedules
#       Order
