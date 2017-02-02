from firebase import firebase
import requests

firebase = firebase.FirebaseApplication("https://eta-detroit-3f7a4.firebaseio.com/", None)

def empty_firebase_database():
    firebase.delete("/routes", None)
    firebase.delete("/stop_locations", None)
    firebase.delete("/stop_orders", None)

def insert_route(company, route_id, route_name, route_number, direction1, direction2, days_active):
    new_route = {"company": company,
                 "route_number": route_number,
                 "direction1": direction1,
                 "direction2": direction2,
                 "days_active": days_active,
                 "route_id": route_id}


    firebase.post("/routes", new_route)

def insert_stop_location(company, route_id, direction, stop_id, stop_name, latitude, longitude):
    new_location = {"company": company,
                     "route_id": route_id,
                     "direction": direction,
                     "stop_id": stop_id,
                     "stop_name": stop_name,
                     "latitude": latitude,
                     "longitude": longitude}

    firebase.post("/stop_locations", new_location)

def insert_stop_order(company, route_id, direction, stop_id, stop_name, stop_order, stop_day):
    new_order = {"company": company,
                 "route_id": route_id,
                 "direction": direction,
                 "stop_id": stop_id,
                 "stop_name": stop_name,
                 "stop_order": stop_order,
                 "stop_day": stop_day}

    firebase.post("/stop_order", new_order)
