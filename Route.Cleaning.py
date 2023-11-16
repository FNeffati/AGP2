import pandas as pd
from pathlib import Path

# change file path to your local device
file_path_route = '/Users/yuhanburgess/Documents/GitHub/AGP2/routes.csv'
file_path_airport = '/Users/yuhanburgess/Documents/GitHub/AGP2/airports.csv'
file_path_airlines = '/Users/yuhanburgess/Documents/GitHub/AGP2/airlines.csv'

# setting up a pandas df for both csv file
df_route = pd.read_csv(file_path_route)
df_airport = pd.read_csv(file_path_airport)
df_airlines = pd.read_csv(file_path_airlines)

# Filling missing values in 'IATA' with corresponding values from 'ICAO'
df_airlines['IATA'] = df_airlines['IATA'].fillna(df_airlines['ICAO'])
df_airport['IATA'] = df_airport['IATA'].fillna(df_airport['ICAO'])
df_airlines = df_airlines.rename(columns= {'IATA': 'Airline IATA'})

pd.set_option('display.max_columns', None)
print(df_airlines)
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
                                                   'Country': 'Dest Country',
                                                    'IATA': 'Dest IATA'})
# pd.set_option('display.max_columns', None)
# print(df_merged_destination)

# filepath = Path('/Users/yuhanburgess/Documents/GitHub/AGP2/df_merged_source.csv')
# filepath.parent.mkdir(parents=True, exist_ok=True)
# df_merged_destination.to_csv(filepath)

# # Merging with airlines based on 'IATA'
df_merged_airline = pd.merge(df_merged_destination, df_airlines,
                                 how='left', left_on='Airline',
                                 right_on='Airline IATA')
# df_merged_airline = df_merged_airline.rename(columns={'Airline': 'Airline Code'})
df_merged_airline = df_merged_airline.rename(columns={'Name': 'Airline Name'})
# pd.set_option('display.max_columns', None)
# print(df_merged_airline)

# filepath = Path('/Users/yuhanburgess/Documents/GitHub/AGP2/df_merged_source.csv')
# filepath.parent.mkdir(parents=True, exist_ok=True)
# df_merged_airline.to_csv(filepath)

# # Add Source and Destination City Columns to df_route
df_route['Src City'] = df_merged_source['Src City']
df_route['Dest City'] = df_merged_destination['Dest City']
# df_route['Airline Code'] = df_merged_airline['Airline Code']
df_route['Airline Name'] = df_merged_airline['Airline Name']

# allows you to see all columns in console
pd.set_option('display.max_columns', None)
print(df_route)

# filtering columns in which the start is New York or the end is San Fran
viable_df = df_route[df_route["Src City"].str.contains("New York") |
                     df_route["Dest City"].str.contains("San Francisco")]

# # # see all columns of pd df in console
# # pd.set_option('display.max_columns', None)
# # print(viable_df)
# #
# # creates a csv file that allows you to look at new df
# # change file path to your local device
filepath = Path('/Users/yuhanburgess/Documents/GitHub/AGP2/viable_df.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
viable_df.to_csv(filepath)
