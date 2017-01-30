import database
import sqlite3

ddot_database = sqlite3.connect("ddot.db")

def load_ddot_data():
    print("*************************************************************")
    print("**********     IMPORTING DDOT ROUTES AND STOPS     **********")
    print("*************************************************************")

    c = ddot_database.cursor()
    for route in c.execute('''select * from routes'''):
        route_id = route[1]
        route_name = route[3]
        route_number = route[2]

        print("IMPORTING ROUTE:", route_name, "(", route_number, ")")

        direction1, direction2 = get_directions(route_id)
        database.insert_route("DDOT", route_id, route_name, route_number, direction1, direction2, "All")

        load_stops(route_id, direction1)
        load_stops(route_id, direction2)

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
    stops.sort(key=lambda stop: stop[2])

    stop_order = 1
    for stop in stops:
        #(12709, 'DDOT_811', 'Wyoming & Warren', '42.344104', '-83.157492', 'DDOT_6449', 'southbound')
        stop_id = stop[1]
        stop_name = stop[2]
        latitude = stop[3]
        longitude = stop[4]

        database.insert_stop_location("DDOT", route_id, direction, stop_id, stop_name, latitude, longitude)
        database.insert_stop_order("DDOT", route_id, direction, stop_id, stop_name, stop_order, "All")

        stop_order = stop_order + 1
