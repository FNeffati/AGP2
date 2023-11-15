import pandas as pd
from pathlib import Path

# by Jin YuHan Burgess

# change file path to your local device
file_path_route = '/Users/yuhanburgess/Documents/GitHub/AGP2/routes.csv'
file_path_airport = '/Users/yuhanburgess/Documents/GitHub/AGP2/airports.csv'
file_path_airlines = '/Users/yuhanburgess/Documents/GitHub/AGP2/airlines.csv'


# setting up a pandas df for both csv file
df_route = pd.read_csv(file_path_route)
df_airport = pd.read_csv(file_path_airport)

# removing information that is not relevant
# Codeshare = NA
# Stops = 0
df_route = df_route.drop(columns=['Codeshare', 'Stops'])
# subset airport dataframes
df_airport = df_airport[['Name', 'City', 'Country', 'IATA']]

# Merge the DataFrames based on source airport IATA code
df_merged_source = pd.merge(df_route, df_airport, how='left',
                            left_on='Source Airport',
                            right_on='IATA' or 'ICAO')
# rename city to takeoff city
df_merged_source = df_merged_source.rename(columns={'City': 'Source City'})

# Merge again for destination airport IATA
df_merged_destination = pd.merge(df_merged_source, df_airport,
                                 how='left', left_on='Destination Airport',
                                 right_on='IATA' or 'ICAO')
# rename city to landing city
df_merged_destination = df_merged_destination.rename(columns={'City': 'Destination City'})

# Add Source and Destination City Columns to df_route
df_route['Source City'] = df_merged_destination['Source City']
df_route['Destination City'] = df_merged_destination['Destination City']

# allows you to see all columns in console
# pd.set_option('display.max_columns', None)
# print(df_route)

# filtering columns in which the start is New York or the end is San Fran
viable_df = df_route[df_route["Source City"].str.contains("New York") |
                     df_route["Destination City"].str.contains("San Francisco")]

# see all columns of pd df in console
pd.set_option('display.max_columns', None)
print(viable_df)

# # creates a csv file that allows you to look at new df
# # change file path to your local device
# filepath = Path('/Users/yuhanburgess/Documents/GitHub/AGP2/viable_df.csv')
# filepath.parent.mkdir(parents=True, exist_ok=True)
# viable_df.to_csv(filepath)
