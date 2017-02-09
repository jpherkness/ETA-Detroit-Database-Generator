# Project Title

The purpose of these scripts is to combine SmartBus, DDOT, and Reflex databases into a shared sqlite database file, as well as a firebase database.

## Getting Started

To setup and use this project, follow the steps below:

1. `Download` or `Clone` this repository
2. Replace `/in/ddot.db` with the updated DDOT sqlite database
3. Run `sudo pip3 install requests`
4. Run `sudo pip3 install python-firebase`
5. Run `python3 runme.py`

The result will be a sqlite database called `ETADetroitDatabase.db` inside the `/out` directory. The database will also write to a firebase database at `https://eta-detroit-3f7a4.firebaseio.com/`

## Authors

* **Joseph Herkness**

## License

This project is licensed under the MIT License
