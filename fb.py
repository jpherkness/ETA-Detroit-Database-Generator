from firebase import firebase
import requests

firebase = firebase.FirebaseApplication("https://eta-detroit-3f7a4.firebaseio.com/", None)

def empty_firebase_database():
    firebase.delete("/routes", None)
    firebase.delete("/stop_locations", None)
    firebase.delete("/stop_orders", None)

def insert_routes(routes):
    firebase.put("", "routes", routes)

def insert_stop_locations(stop_locations):
    firebase.put("", "stop_locations", stop_locations)

def insert_stop_orders(stop_orders):
    firebase.put("", "stop_orders", stop_orders)
