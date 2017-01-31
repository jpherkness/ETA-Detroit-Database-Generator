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

current_path = os.path.dirname(os.path.abspath(__file__))

def load_smart_data():
    print("*************************************************************")
    print("**********   IMPORTING SMARTBUS ROUTES AND STOPS   **********")
    print("*************************************************************")
    routes_request = requests.get("http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getroutesforselect").json()
    for route in routes_request:

        route_id = route["Value"]
        route_number = route_id
        route_name = route["Text"].replace(route["Value"] + " - ", "")

        print("IMPORTING ROUTE:", route_name, "(" + route_number + ")")

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
        days_string = ",".join(days_array)

        database.insert_route("SmartBus", route_id, route_name, route_number, direction1, direction2, days_string)

        # Load all stop locations for both directions
        load_all_stops(route_id, direction1)
        load_all_stops(route_id, direction2)

def load_stop_orders(stop_day, day_code, direction, route_id):
    stops_request = requests.get("http://www.smartbus.org/DesktopModules/SMART.Schedules/ScheduleService.ashx?route="+ route_id +"&scheduleday="+ day_code +"&direction="+ direction).json()
    # sorts stops by name
    # stops_request = sorted(stops_request, key=lambda stop: stop["Name"])
    stop_order = 1
    for stop in stops_request:
        database.insert_stop_order("SmartBus", route_id, direction, None, stop["Name"], stop_order, stop_day)

        # TODO: Add this information to the stop_schedules table
        for time in stop["Times"]:
            if time["Time"] != "":
                stop_name = stop["Name"]
                direction = direction
                route_id = route_id
                day = stop_day
                time = time["Time"]
                company = "SmartBus"

        stop_order = stop_order + 1

def load_all_stops(route_id, direction):
    stops_request = requests.get("http://www.smartbus.org/desktopmodules/SMART.Endpoint/Proxy.ashx?method=getstopsbyrouteanddirection&routeid=" + route_id + "&d=" + direction).json()
    for stop in stops_request:
        database.insert_stop_location("SmartBus", route_id, direction, stop["StopId"], stop["Name"], stop["Latitude"], stop["Longitude"])

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
#
# Questions
# 1. Do you want the output as a mongodb or csv?
# 2. Should I create a new table for just the stop orders
#       Routes
#       Stops
#       Schedules
#       Order
