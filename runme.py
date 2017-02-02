import database
import smart
import ddot
import reflex
import os
import fb

current_path = os.path.dirname(os.path.abspath(__file__))

def main():
    routes, stop_orders, stop_locations = [], [], []

    database.setupDatabase()
    reflex_routes, reflex_stop_orders, reflex_stop_locations = reflex.load_data()
    #ddot.load_ddot_data()
    #reflex.load_reflex_data()

    fb.empty_firebase_database()
    
    fb.insert_routes(reflex_routes)
    fb.insert_stop_orders(reflex_stop_orders)
    fb.insert_stop_locations(reflex_stop_locations)

    print("Database saved to", current_path + "/ETADetroitDatabase.db")

main()
