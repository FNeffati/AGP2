import pandas as pd
from pathlib import Path # used to create csv file from pandas df

# change file path to your local device
file_path_route = '/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/routes.csv'
file_path_airport = '/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/airports.csv'
file_path_airlines = '/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/airlines.csv'

# setting up a pandas df for both csv file
df_route = pd.read_csv(file_path_route)
df_airport = pd.read_csv(file_path_airport)
df_airlines = pd.read_csv(file_path_airlines)

# Filling missing values in 'IATA' with corresponding values from 'ICAO'
df_airlines['IATA'] = df_airlines['IATA'].fillna(df_airlines['ICAO'])
df_airport['IATA'] = df_airport['IATA'].fillna(df_airport['ICAO'])
df_airlines = df_airlines.rename(columns={'IATA': 'Airline IATA'})


# removing information that is not relevant
# Codeshare = NA
# Stops = 0
df_route = df_route.drop(columns=['Codeshare', 'Stops'])
# subset airport dataframes
df_airport = df_airport[['Name', 'City', 'Country', 'IATA']]

# Creating a copy of the original 'Airline' column
df_route['Original Airline'] = df_route['Airline'].copy()

# Merge the DataFrames based on source airport IATA code
df_merged_source = pd.merge(df_route, df_airport,
                            left_on='Source Airport',
                            right_on='IATA', how='left')

# Merge the DataFrames based on source airport IATA code
# rename city to takeoff city
df_merged_source = df_merged_source.rename(columns={'City': 'Src City',
                                                    'Name': 'Src Name',
                                                    'Country': 'Src Country',
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
                                                              'IATA': 'Dest IATA'})
# pd.set_option('display.max_columns', None)
# print(df_merged_destination)

# # Merging with airlines based on 'IATA'
df_merged_airline = pd.merge(df_merged_destination, df_airlines,
                             how='left', left_on='Airline',
                             right_on='Airline IATA')
df_merged_airline = df_merged_airline.rename(columns={'Name': 'Aircraft Name'})
df_merged_flights = df_merged_airline.drop(columns=['Original Airline', 'Airline IATA', 'ICAO',
                                                    'Active', 'Country', 'Src IATA', 'Dest IATA'])

# # LOOK at merged_flight dataframe in console
# pd.set_option('display.max_columns', None)
# print(df_merged_airline)

# filtering columns in which the start is New York or the end is San Fran
viable_df = df_merged_flights[df_merged_flights["Src City"].str.contains("New York") |
                              df_merged_flights["Dest City"].str.contains("San Francisco")]

# pd.set_option('display.max_columns', None)
# print(viable_df)


# Creates a csv file to look at the df_merged_airline dataframe
filepath = Path('/Users/yuhanburgess/Documents/GitHub/AGP2/df_possible_flights.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
viable_df.to_csv(filepath)

# Splits up entry/row if it has more than one equipment value
# that can be used in further analysis

# get rows that contain more than one equipment option
multiple_equip = viable_df[viable_df['Equipment'].str.len() > 3]

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
            'Dest Name': row['Dest Name'], 'Dest City': row['Dest City'],
            'Dest Country': row['Dest Country'],
            'Aircraft Name': row['Aircraft Name'], 'Callsign': row['Callsign']
        }

        # Append the new row to the list
        new_rows.append(new_row_data)

# Drop the original rows where the length of 'Equipment' is greater than 3
viable_df = viable_df.drop(multiple_equip.index)

# Reset the index after dropping rows
viable_df = viable_df.reset_index(drop=True)

# Append the new rows to the DataFrame
viable_df = viable_df._append(new_rows, ignore_index=True)

# TEST: look at all direct flights
direct_df = viable_df[viable_df["Src City"].str.contains("New York") &
                      viable_df["Dest City"].str.contains("San Francisco")]
# Display the result
# pd.set_option('display.max_columns', None)
print(direct_df)

# # Creates a csv file to look at the direct flight dataframe (direct_df) when equipment is split up
# filepath = Path('/Users/yuhanburgess/Documents/GitHub/AGP2/split.equip.csv')
# filepath.parent.mkdir(parents=True, exist_ok=True)
# direct_df.to_csv(filepath)
