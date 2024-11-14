**README: Coordinate Correction and Terrain Classification Scripts**

This README provides an overview of the fix_coordinates.py and terrain.py scripts, detailing the purpose, setup, and execution instructions for each.

-----
**Overview**

1. **fix_coordinates.py**: This script processes a set of GPS coordinates, detects out-of-sequence points, corrects the path using a moving average, stores data in an SQLite database, and visualizes the corrected path.
1. **terrain.py**: This script interacts with the SQLite database to filter specific terrain classifications, and retrieves relevant corrected GPS points.
-----
**Requirements**

Both scripts require the following libraries:

- **Python Libraries**:
  - pandas
  - numpy
  - sqlite3
  - matplotlib
  - os
- **Data Files**:
  - latitude_longitude_details.csv: Contains GPS coordinates with columns for latitude and longitude.
  - terrain_classification.csv: Contains terrain types and distances.
- **SQLite Database**: An SQLite database (geodata.db) will be created to store processed and filtered data.
-----
**fix_coordinates.py**

This script identifies out-of-sequence GPS coordinates, applies a moving average to correct them, saves corrected data to an SQLite database, and visualizes the results.

**1. Script Details**

- **Input Files**:
  - latitude_longitude_details.csv
  - terrain_classification.csv
- **Database**:
  - geodata.db

**2. Script Functionality**

1. **Setup Directories**:
   1. Creates a data directory for input files and an output directory for storing output files.
1. **Load Data**:
   1. Loads latitude_longitude_details.csv and terrain_classification.csv into pandas DataFrames.
1. **Identify Out-of-Sequence Points**:
   1. Calculates the distance between consecutive points to detect outliers.
1. **Correct Path with Moving Average**:
   1. Applies a moving average on latitude and longitude to correct the path, ignoring NaN values at the edges.
   1. Saves corrected coordinates to latitude_longitude_corrected.csv.
1. **Store Data in SQLite**:
   1. Creates three tables in geodata.db:
      1. latitude_longitude_details: Stores original coordinates and distances.
      1. terrain_classification: Stores terrain data.
      1. latitude_longitude_corrected: Stores corrected coordinates.
1. **Visualize Before and After**:
   1. Plots the original and corrected paths for comparison.

**3. Execution**

Run the script with:

python scripts/fix_coordinates.py

**4. Output**

- **CSV File**: latitude_longitude_corrected.csv containing corrected GPS coordinates.
- **Database**: geodata.db with three tables.
- **Visualization**: Shows plots comparing the original and corrected paths.
-----


**terrain.py**

This script queries the database for specific terrain types and filtered GPS points based on the presence of "road" and exclusion of "civil station."

**1. Script Details**

- **Database File**:
  - geodata.db

**2. Script Functionality**

1. **Filter Terrain Types:**
   1. **Queries the terrain_classification table for rows containing "road" but excluding "civil station."**


1. **Retrieve Corrected GPS Points:**
   1. **Fetches GPS points from the latitude_longitude_corrected table related to the filtered terrain types.**

**3. Execution**

**Run the script with:**

python scripts/terrain.py

**4. Output**

- **Console Output**:
  - Latitude and longitude points that meet the filtering criteria (coordinates of roads without civil station)



PROVIDING SCREENSHOTS OF THE OUTPUTS IN THE RESULTS FOLDER.
