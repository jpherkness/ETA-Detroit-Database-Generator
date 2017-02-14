from firebase import firebase
import requests

firebase_url = "https://eta-detroit-3f7a4.firebaseio.com/"
firebase = firebase.FirebaseApplication(firebase_url, None)

# Inserts the data from the DataSet object into the firebase database
def insert_data_set(data):
    empty_firebase_database()

    firebase.put("", "routes_exp", data.all_routes)
    print("Routes uploaded to firebase:", firebase_url)

    firebase.put("", "stop_locations_exp", data.all_stop_locations)
    print("Stop Locations uploaded to firebase:", firebase_url)

    firebase.put("", "stop_orders_exp", data.all_stop_orders)
    print("Stop Orders uploaded to firebase:", firebase_url)

# Removes the data from the firebase database
def empty_firebase_database():
    firebase.delete("/routes_exp", None)
    firebase.delete("/stop_locations_exp", None)
    firebase.delete("/stop_orders_exp", None)
