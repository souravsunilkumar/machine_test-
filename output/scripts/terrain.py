import sqlite3
import pandas as pd

database_file = "geodata.db"

conn = sqlite3.connect(database_file)

cursor = conn.cursor()
cursor.execute("""
SELECT terrain
FROM terrain_classification
WHERE terrain LIKE '%road%' AND terrain NOT LIKE '%civil station%'
""")
roads_terrain = cursor.fetchall()

print("Filtered terrain types (contains 'road' but not 'civil station'):")
for terrain in roads_terrain:
    print(terrain[0])


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

print("\nFiltered Latitude and Longitude points with 'road' but without 'civil station':")
print(filtered_points)

conn.close()
