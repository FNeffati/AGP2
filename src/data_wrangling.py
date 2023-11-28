import pandas as pd
from pathlib import Path  # used to create csv file from pandas df
from carrier_file import plane_data

# change file path to your local device
file_path_route = '/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/routes.csv'
file_path_airport = '/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/airports.csv'
file_path_airlines = '/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/airlines.csv'
file_path_pass_capacity = "/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/Passenger_Capacities.csv"
# setting up a pandas df for both csv file
df_route = pd.read_csv(file_path_route)
df_airport = pd.read_csv(file_path_airport)
df_airlines = pd.read_csv(file_path_airlines)
df_passenger_cap = pd.read_csv(file_path_pass_capacity)

# Filling missing values in 'IATA' with corresponding values from 'ICAO'
df_airlines['IATA'] = df_airlines['IATA'].fillna(df_airlines['ICAO'])
df_airport['IATA'] = df_airport['IATA'].fillna(df_airport['ICAO'])
df_airlines = df_airlines.rename(columns={'IATA': 'Airline IATA'})

# removing information that is not relevant
# Codeshare = NA, Stops = 0
df_route = df_route.drop(columns=['Codeshare', 'Stops'])

# Merge the DataFrames based on source airport IATA code
df_merged_source = pd.merge(df_route, df_airport,
                            left_on='Source Airport',
                            right_on='IATA', how='left')

# Merge the DataFrames based on source airport IATA code
# rename city to takeoff city
df_merged_source = df_merged_source.rename(columns={'City': 'Src City',
                                                    'Name': 'Src Name',
                                                    'Country': 'Src Country',
                                                    'ICAO': 'Src ICAO',
                                                    'Latitude': 'Src Latitude',
                                                    'Longitude': 'Src Longitude',
                                                    'Altitude': 'Src Altitude',
                                                    'Timezone': 'Src Timezone',
                                                    'Timezone.1': 'Src Timezone Name',
                                                    'DST': 'Src DST',
                                                    'IATA': 'Src IATA'})
# pd.set_option('display.max_columns', None)
# print(df_merged_source)

# Merge again for destination airport IATA
df_merged_destination = pd.merge(df_merged_source, df_airport,
                                 how='left', left_on='Destination Airport',
                                 right_on='IATA')

# rename city to landing city
df_merged_destination = df_merged_destination.rename(columns={'City': 'Dest City',
                                                              'Name': 'Dest Name',
                                                              'Country': 'Dest Country',
                                                              'ICAO': 'Dest ICAO',
                                                              'Latitude': 'Dest Latitude',
                                                              'Longitude': 'Dest Longitude',
                                                              'Altitude': 'Dest Altitude',
                                                              'Timezone': 'Dest Timezone',
                                                              'Timezone.1': 'Dest Timezone Name',
                                                              'DST': 'Dest DST',
                                                              'IATA': 'Dest IATA'})
# pd.set_option('display.max_columns', None)
# print(df_merged_destination)

# # Merging with airlines based on 'IATA'
df_merged_airline = pd.merge(df_merged_destination, df_airlines,
                             how='left', left_on='Airline',
                             right_on='Airline IATA')
df_merged_airline = df_merged_airline.rename(columns={'Name': 'Carrier'})

df_merged_flights = df_merged_airline.drop(columns=['Airline IATA', 'ICAO',
                                                    'Active', 'Country', 'Src IATA', 'Dest IATA'])

# # LOOK at merged_flight dataframe in console
# pd.set_option('display.max_columns', None)
# print(df_merged_airline)

# Splits up entry/row if it has more than one equipment value
# that can be used in further analysis

# get rows that contain more than one equipment option
multiple_equip = df_merged_flights[df_merged_flights['Equipment'].str.len() > 3]

# Create an empty list to store new rows
new_rows = []

# Iterate through rows
for index, row in multiple_equip.iterrows():

    # Split 'Equipment' based on space
    equipment_values = row['Equipment'].split()

    # Iterate through the split values and create a new row for each
    for equipment_value in equipment_values:
        # Create a new row with the current equipment value
        new_row_data = {
            'Airline': row['Airline'], 'Airline ID': row['Airline ID'],
            'Source Airport': row['Source Airport'],
            'Source Airport ID': row['Source Airport ID'],
            'Destination Airport': row['Destination Airport'],
            'Destination Airport ID': row['Destination Airport ID'],
            'Equipment': equipment_value, 'Src Name': row['Src Name'],
            'Src City': row['Src City'], 'Src Country': row['Src Country'],
            'Src ICAO': row['Src ICAO'], 'Src Latitude': row['Src Latitude'],
            'Src Longitude': row['Src Longitude'], 'Src Altitude': row['Src Altitude'],
            'Src Timezone': row['Src Timezone'], 'Src DST': row['Src DST'],
            'Src Timezone Name': row['Src Timezone Name'],
            'Dest Name': row['Dest Name'], 'Dest City': row['Dest City'],
            'Dest Country': row['Dest Country'], 'Dest ICAO': row['Dest ICAO'],
            'Dest Latitude': row['Dest Latitude'], 'Dest Longitude': row['Dest Longitude'],
            'Dest Altitude': row['Dest Altitude'], 'Dest Timezone': row['Dest Timezone'],
            'Dest DST': row['Dest DST'], 'Dest Timezone Name': row['Dest Timezone Name'],
            'Carrier': row['Carrier'], 'Callsign': row['Callsign']
        }

        # Append the new row to the list
        new_rows.append(new_row_data)

# Drop the original rows where the length of 'Equipment' is greater than 3
df_merged_flights = df_merged_flights.drop(multiple_equip.index)

# Reset the index after dropping rows
df_merged_flights = df_merged_flights.reset_index(drop=True)

# Append the new rows to the DataFrame
df_merged_flights = df_merged_flights._append(new_rows, ignore_index=True)

df_merged_carrier = pd.merge(df_merged_flights, plane_data,
                             how='left', left_on='Equipment',
                             right_on='Airline_IATA')

df_merged_carrier = df_merged_carrier.drop(columns=['Airline_IATA', 'Airline_ICAO'])
#
df_merged_passenger = pd.merge(df_merged_carrier, df_passenger_cap,
                               how='left', left_on='Airline_Name',
                               right_on='Aircraft')

df_possible_flights = df_merged_passenger[df_merged_passenger["Src City"].str.contains("New York") |
                                          df_merged_passenger["Dest City"].str.contains("San Francisco")]

df_possible_flights = df_possible_flights.dropna(subset=['Airline_Name'])
# # TEST: look at all direct flights
# direct_df = pd.DataFrame(df_possible_flights[df_possible_flights["Src City"].str.contains("New York") &
#                               df_possible_flights["Dest City"].str.contains("San Francisco")])
#
# # Display the result
# # pd.set_option('display.max_columns', None)
# print(direct_df)

# # Creates a csv file to look at the df_merged_airline dataframe
# filepath = Path('/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/df_possible_flights.csv')
# filepath.parent.mkdir(parents=True, exist_ok=True)
# df_possible_flights.to_csv(filepath)
