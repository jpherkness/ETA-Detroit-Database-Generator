import sqlite3
import os

def connect():
    if not os.path.exists("out"):
        os.makedirs("out")
    return sqlite3.connect("out/ETADetroitDatabase.db")

def setupDatabase():
    connection = connect()
    c = connection.cursor()

    # Delete the tables
    c.execute('drop table if exists routes')
    c.execute('drop table if exists stop_locations')
    c.execute('drop table if exists stop_orders')
    c.execute('drop table if exists stop_schedules')

    # Create the tables
    c.execute('''CREATE TABLE routes
             (company text, route_id text, route_name text, route_number text,
             direction1 text, direction2 text, days_active text)''')
    c.execute('''CREATE TABLE stop_locations
             (company text, route_id text, direction text, stop_id text,
             stop_name text, latitude text, longitude text)''')
    c.execute('''CREATE TABLE stop_orders
             (company text, route_id text, direction text, stop_id text,
             stop_name text, stop_order text, stop_day text)''')
    c.execute('''CREATE TABLE stop_schedules
             (company text, route_id text, direction text, day text, stop_name text,
             time text)''')
    connection.close()

def insert_route(route):
    # Insert into SQLite
    connection = connect()
    c = connection.cursor()
    params = [route.company, route.route_id, route.route_name, route.route_number, route.direction1, route.direction2, route.days_active]
    c.execute("INSERT INTO routes VALUES (?,?,?,?,?,?,?)", params)
    connection.commit()
    connection.close()

def insert_stop_location(stop_location):
    # Insert into SQLite
    connection = connect()
    c = connection.cursor()
    params = [stop_location.company, stop_location.route_id, stop_location.direction, stop_location.stop_id, stop_location.stop_name, stop_location.latitude, stop_location.longitude]
    c.execute("INSERT INTO stop_locations VALUES (?,?,?,?,?,?,?)", params)
    connection.commit()
    connection.close()

def insert_stop_order(stop_order):
    # Insert into SQLite
    connection = connect()
    c = connection.cursor()
    params = [stop_order.company, stop_order.route_id, stop_order.direction, stop_order.stop_id, stop_order.stop_name, stop_order.stop_order, stop_order.stop_day]
    c.execute("INSERT INTO stop_orders VALUES (?,?,?,?,?,?,?)", params)
    connection.commit()
    connection.close()
