import sqlite3
import pandas as pd

# Database file
database_file = "geodata.db"

# Connect to the SQLite database
conn = sqlite3.connect(database_file)

# Step 1: Query the terrain_classification table for rows with 'road' and exclude 'civil station'
cursor = conn.cursor()
cursor.execute("""
SELECT terrain
FROM terrain_classification
WHERE terrain LIKE '%road%' AND terrain NOT LIKE '%civil station%'
""")
roads_terrain = cursor.fetchall()

# Display the filtered terrain types
print("Filtered terrain types (contains 'road' but not 'civil station'):")
for terrain in roads_terrain:
    print(terrain[0])

# Step 2: Query the latitude_longitude_corrected table for relevant latitude and longitude points
# We can directly query latitude_longitude_corrected as there is no direct relationship between
# latitude_longitude_corrected and terrain_classification based on terrain.
# We assume here the terrain information is already embedded in the latitude_longitude_corrected data

# Assuming the `latitude_longitude_corrected` table contains terrain info in the "terrain" column
query = """
SELECT l.latitude_corrected, l.longitude_corrected
FROM latitude_longitude_corrected l
WHERE EXISTS (
    SELECT 1
    FROM terrain_classification t
    WHERE t.terrain LIKE '%road%' AND t.terrain NOT LIKE '%civil station%'
)
"""
filtered_points = pd.read_sql_query(query, conn)

# Display the filtered points
print("\nFiltered Latitude and Longitude points with 'road' but without 'civil station':")
print(filtered_points)

# Close the database connection
conn.close()
