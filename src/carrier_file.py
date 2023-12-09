import pandas as pd

plane_data = pd.read_csv('../csv_files/planes.dat.txt', sep=',', header=None)
plane_data = plane_data.rename(columns={0: 'Airline_Name', 1: 'Airline_IATA', 2: 'Airline_ICAO'})
plane_data['Airline_IATA'] = plane_data.Airline_IATA.astype(str)



