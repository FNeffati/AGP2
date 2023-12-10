# import pandas as pd

# plane_data = pd.read_csv('../csv_files/planes.dat.txt', sep=',', header=None)

import os
import pandas as pd

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, '..', 'csv_files', 'planes.dat.txt')

# Read the CSV file
plane_data = pd.read_csv(file_path, sep=',', header=None)
                         
# Construct the absolute path to the CSV file
plane_data = plane_data.rename(columns={0: 'Airline_Name', 1: 'Airline_IATA', 2: 'Airline_ICAO'})
plane_data['Airline_IATA'] = plane_data.Airline_IATA.astype(str)



