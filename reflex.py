import database
import sqlite3

reflex_database = sqlite3.connect("in/reflex.db")

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

        print("IMPORTING ROUTE:", route_name, "(" + route_number + ")")

        database.insert_route(company, route_id, route_name, route_number, direction1, direction2, days_active)
        load_stops(route_id, direction1, days_active)
        load_stops(route_id, direction2, days_active)

    reflex_database.close()

# Load the stops alphabetically into the database
def load_stops(route_id, direction, days_active):
    c = reflex_database.cursor()
    order = 1
    for stop in c.execute('''select * from stops where route_id=? and direction=? order by stop_number''', [route_id, direction]):
        company = stop[0]
        route_id = stop[1]
        direction = stop[2]
        stop_id = stop[3]
        stop_number = stop[4]
        stop_name = stop[5]
        latitude = stop[6]
        longitude = stop[7]
        stop_order = stop[8]

        database.insert_stop_location(company, route_id, direction, stop_id, stop_name, latitude, longitude)
        database.insert_stop_order(company, route_id, direction, stop_id, stop_name, order, days_active)
        # TODO: The day above might need to be derived from the route.
        order = order + 1
