import sqlite3
import folium

def plot_earthquakes_on_map():
    # Connect to the SQLite database
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    # Fetch earthquake data from the database (including latitude and longitude)
    cursor.execute("SELECT latitude, longitude, magnitude FROM earthquakes")
    earthquakes = cursor.fetchall()

    # Create a base map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Loop through the earthquake data and add markers to the map
    for earthquake in earthquakes:
        lat, lon, magnitude = earthquake
        
        # Check if lat and lon are not None and can be converted to float
        try:
            lat_float = float(lat)
            lon_float = float(lon)
            folium.CircleMarker(
                location=[lat_float, lon_float],
                radius=magnitude*2,  # Radius of the circle is proportional to the magnitude
                color="red",
                fill=True,
                fill_opacity=0.6
            ).add_to(m)
        except (TypeError, ValueError):
            continue

    # Save the map to an HTML file
    m.save("earthquake_map.html")
    print("Map saved as earthquake_map.html")

if __name__ == "__main__":
    plot_earthquakes_on_map()
