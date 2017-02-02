from firebase import firebase
import requests

firebase_url = "https://eta-detroit-3f7a4.firebaseio.com/"
firebase = firebase.FirebaseApplication(firebase_url, None)

def empty_firebase_database():
    firebase.delete("/routes", None)
    firebase.delete("/stop_locations", None)
    firebase.delete("/stop_orders", None)

def insert_routes(routes):
    firebase.put("", "routes", routes)
    print("Routes uploaded to firebase:", firebase_url)

def insert_stop_locations(stop_locations):
    firebase.put("", "stop_locations", stop_locations)
    print("Stop Locations uploaded to firebase:", firebase_url)

def insert_stop_orders(stop_orders):
    firebase.put("", "stop_orders", stop_orders)
    print("Stop Orders uploaded to firebase:", firebase_url)
