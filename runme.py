import database
import smart
import ddot
import reflex
import os
import fb

current_path = os.path.dirname(os.path.abspath(__file__))

def main():

    fb.empty_firebase_database()
    database.setupDatabase()
    smart.load_smart_data()
    ddot.load_ddot_data()
    reflex.load_reflex_data()

    print("Database saved to", current_path + "/ETADetroitDatabase.db")

main()
