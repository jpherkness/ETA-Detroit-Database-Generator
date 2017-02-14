import database
from smart import Smart
from ddot import DDOT
from reflex import Reflex
from dataset import DataSet
import ddot
import reflex
import os
import fb

current_path = os.path.dirname(os.path.abspath(__file__))

def main():
    database.setupDatabase()

    data = DataSet()


    reflex = Reflex(data)
    smart = Smart(data)
    ddot = DDOT(data)
    
    reflex.load_data() # load reflex first because the others ignore identical routes
    smart.load_data()
    ddot.load_data()

    fb.insert_data_set(data)

    print("Database saved to", current_path + "/ETADetroitDatabase.db")

main()
