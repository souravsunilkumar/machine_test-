import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import os

data_dir = "data"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)


latitude_longitude_file = os.path.join(data_dir, "latitude_longitude_details.csv")
terrain_file = os.path.join(data_dir, "terrain_classification.csv")
corrected_output_file = os.path.join(output_dir, "latitude_longitude_corrected.csv")
database_file = "geodata.db"


coords_df = pd.read_csv(latitude_longitude_file)
terrain_df = pd.read_csv(terrain_file)


coords_df['distance_to_prev'] = np.sqrt(
    (coords_df['latitude'] - coords_df['latitude'].shift())**2 +
    (coords_df['longitude'] - coords_df['longitude'].shift())**2
)


threshold = 0.0005
out_of_line = coords_df[coords_df['distance_to_prev'] > threshold]


print("Non continuous coordinates:")
print(out_of_line[['latitude', 'longitude', 'distance_to_prev']])


coords_df['latitude_corrected'] = coords_df['latitude']
coords_df['longitude_corrected'] = coords_df['longitude']


window_size = 3


rolling_latitude = coords_df['latitude'].rolling(window=window_size, center=True).mean()
rolling_longitude = coords_df['longitude'].rolling(window=window_size, center=True).mean()


valid_latitude = rolling_latitude.dropna()
valid_longitude = rolling_longitude.dropna()


coords_df.loc[valid_latitude.index, 'latitude_corrected'] = valid_latitude
coords_df.loc[valid_longitude.index, 'longitude_corrected'] = valid_longitude


coords_df = coords_df.dropna(subset=['latitude_corrected', 'longitude_corrected'])


coords_df[['latitude_corrected', 'longitude_corrected']].to_csv(corrected_output_file, index=False)
print(f"Corrected coordinates saved to {corrected_output_file}")



conn = sqlite3.connect(database_file)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS latitude_longitude_details (
    id INTEGER PRIMARY KEY,
    latitude REAL,
    longitude REAL,
    distance_to_prev REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS terrain_classification (
    terrain TEXT,
    distance REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS latitude_longitude_corrected (
    id INTEGER PRIMARY KEY,
    latitude_corrected REAL,
    longitude_corrected REAL
)
""")


coords_df[['latitude', 'longitude', 'distance_to_prev']].to_sql('latitude_longitude_details', conn, if_exists='replace', index=False)
terrain_df.to_sql('terrain_classification', conn, if_exists='replace', index=False)


coords_df[['latitude_corrected', 'longitude_corrected']].to_sql('latitude_longitude_corrected', conn, if_exists='replace', index=False)


conn.commit()
conn.close()
print(f"Data loaded into database {database_file}")


fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True, sharey=True)

# Original Path
axes[0].plot(coords_df['longitude'], coords_df['latitude'], 'o-', color="blue", markersize=3)
axes[0].set_title("Original Path")
axes[0].set_xlabel("Longitude")
axes[0].set_ylabel("Latitude")

# Corrected Path
axes[1].plot(coords_df['longitude_corrected'], coords_df['latitude_corrected'], 'x-', color="red", markersize=3)
axes[1].set_title("Corrected Path")
axes[1].set_xlabel("Longitude")


plt.suptitle("Before and After Path Correction")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
