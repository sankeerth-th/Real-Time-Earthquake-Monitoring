import requests
import sqlite3
from datetime import datetime, timedelta

def create_database():
    # Create a new SQLite database and set up the earthquakes table
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    # Create the earthquakes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS earthquakes (
        id INTEGER PRIMARY KEY,
        magnitude REAL,
        place TEXT,
        time TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    conn.commit()
    conn.close()

def fetch_earthquake_data(min_magnitude=5.0, days=7):
    # Calculate the time range for the past 'days'
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    # Construct the API endpoint URL
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time.isoformat()}&endtime={end_time.isoformat()}&minmagnitude={min_magnitude}"

    # Fetch the data
    response = requests.get(url)
    data = response.json()

    # Extract earthquake data
    earthquakes = data['features']

    # Store data in SQLite
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    for eq in earthquakes:
        magnitude = eq['properties']['mag']
        place = eq['properties']['place']
        time = datetime.utcfromtimestamp(eq['properties']['time'] / 1000).isoformat()
        longitude = eq['geometry']['coordinates'][0]
        latitude = eq['geometry']['coordinates'][1]

        cursor.execute("INSERT INTO earthquakes (magnitude, place, time, latitude, longitude) VALUES (?, ?, ?, ?, ?)", 
                       (magnitude, place, time, latitude, longitude))

    conn.commit()
    conn.close()

    print(f"{len(earthquakes)} earthquake records inserted into the database.")

import sqlite3

def load_into_warehouse():
    # Connect to the source database
    source_conn = sqlite3.connect('earthquakes.db')
    source_cursor = source_conn.cursor()

    # Extract data from source

    source_cursor.execute("SELECT magnitude, place, time, latitude, longitude FROM earthquakes")
    data = source_cursor.fetchall()

    # Connect to the warehouse database
    warehouse_conn = sqlite3.connect('earthquake_dw.db')
    warehouse_cursor = warehouse_conn.cursor()

    # Create table in warehouse database (if needed)
    warehouse_cursor.execute("""
    CREATE TABLE IF NOT EXISTS earthquakes_dw (
        id INTEGER PRIMARY KEY,
        magnitude REAL,
        place TEXT,
        time TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    # Load data into warehouse
    warehouse_cursor.executemany("INSERT INTO earthquakes_dw (magnitude, place, time, latitude, longitude) VALUES (?, ?, ?, ?, ?)", data)
    warehouse_conn.commit()

if __name__ == "__main__":
    create_database()  # Ensure database and table are set up
    fetch_earthquake_data(days=30)
    load_into_warehouse()
