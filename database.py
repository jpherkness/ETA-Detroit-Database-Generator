import sqlite3
import fb

def connect():
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

def insert_route(company, route_id, route_name, route_number, direction1, direction2, days_active):
    # Insert into SQLite
    connection = connect()
    c = connection.cursor()
    params = [company, route_id, route_name, route_number, direction1, direction2, days_active]
    c.execute("INSERT INTO routes VALUES (?,?,?,?,?,?,?)", params)
    connection.commit()
    connection.close()

def insert_stop_location(company, route_id, direction, stop_id, stop_name, latitude, longitude):
    # Insert into SQLite
    connection = connect()
    c = connection.cursor()
    params = [company, route_id, direction, stop_id, stop_name, latitude, longitude]
    c.execute("INSERT INTO stop_locations VALUES (?,?,?,?,?,?,?)", params)
    connection.commit()
    connection.close()

def insert_stop_order(company, route_id, direction, stop_id, stop_name, stop_order, stop_day):
    # Insert into SQLite
    connection = connect()
    c = connection.cursor()
    params = [company, route_id, direction, stop_id, stop_name, stop_order, stop_day]
    c.execute("INSERT INTO stop_orders VALUES (?,?,?,?,?,?,?)", params)
    connection.commit()
    connection.close()
