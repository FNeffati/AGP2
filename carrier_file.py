import pandas as pd

plane_data = pd.read_csv('/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/planes.dat.txt', sep=',', header=None)
plane_data = plane_data.rename(columns={0: 'Carrier', 1: 'Carrier_IATA', 2: 'Carrier_ICAO'})
plane_data['Carrier_IATA'] = plane_data.Carrier_IATA.astype(str)



