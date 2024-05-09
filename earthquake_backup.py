import sqlite3
from datetime import datetime

def backup_and_clear_data():
    # Connect to SQLite database
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    # Step 1: Backup Old Data
    # Create past_earthquakes table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS past_earthquakes (
        id INTEGER PRIMARY KEY,
        magnitude REAL,
        place TEXT,
        time TEXT,
        latitude REAL,
        longitude REAL,
        archived_time TEXT
    )
    """)

    # Insert data from earthquakes to past_earthquakes (without duplicates)
    cursor.execute("""
    INSERT INTO past_earthquakes (magnitude, place, time, latitude, longitude, archived_time)
    SELECT e.magnitude, e.place, e.time, e.latitude, e.longitude, ?
    FROM earthquakes e
    LEFT JOIN past_earthquakes p ON e.magnitude = p.magnitude AND e.place = p.place AND e.time = p.time
    WHERE p.id IS NULL
    """, (datetime.utcnow().isoformat(),))

    # Step 2: Clear Current Data
    # Delete data from earthquakes table
    cursor.execute("DELETE FROM earthquakes")

    # Commit the changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    backup_and_clear_data()
