import database
import smart
import ddot
import reflex
import os
import fb

current_path = os.path.dirname(os.path.abspath(__file__))

def main():
    database.setupDatabase()

    all_routes = []
    all_stop_orders = []
    all_stop_locations = []

    smart.load_data(all_routes, all_stop_orders, all_stop_locations)
    ddot.load_data(all_routes, all_stop_orders, all_stop_locations)
    reflex.load_data(all_routes, all_stop_orders, all_stop_locations)

    fb.empty_firebase_database()
    fb.insert_routes(all_routes)
    fb.insert_stop_orders(all_stop_orders)
    fb.insert_stop_locations(all_stop_locations)

    print("Database saved to", current_path + "/ETADetroitDatabase.db")

main()
