import numpy as np
import pandas as pd
from pathlib import Path

# utilize the Haversine equation to find the distance between two coordinates
def distance_calc(lat1, lon1, lat2, lon2):
    # Earth radius in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Compute differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula for distance calculation
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Calculate the distance
    distance = earth_radius * c
    
    return np.round(distance, 2)

# create the adjacency matrix that contains pertainate information to answer the two questions
# 1. what is the max flow from any two given cities?
# 2. which carrier has the max load?

def create_matrix(df, airports):
    num_airports = len(airports)

    # Create an adjacency matrix with dictionaries
    adjacency_matrix = [[{
        'distance': 0, # distance between the two cities and will be used to determine total distance travelled
        'route_max_capacity': 0,  # Added max_capacity field
        'aircraft_max_capacity': 0, # looking at an the max capacity of the largest aircraft(s)
        'flights': {}, # contains information about the airline and aircraft that carriers the max_capcity of passengers

        # helpful for later studies if we we want to see if passengers will be gaining or losing time 
        'SrcTimezone': "", 
        'DestTimezone': ""
    } for _ in range(num_airports)] for _ in range(num_airports)]

    # Fill the adjacency matrix based on the flights
    for _, row in df.iterrows():
        # identifying the row and column 
        source_index = airports.index(row["Source Airport"])
        dest_index = airports.index(row["Destination Airport"])

        # calculating the distance between the two airports
        lat1, lon1 = row["Src Latitude"], row["Src Longitude"]
        lat2, lon2 = row["Dest Latitude"], row["Dest Longitude"]
        distance = distance_calc(lat1, lon1, lat2, lon2)

        # flight info is a diction that contians infomration about the carrier's aircraft and its flight 
        # capcity
        flight_info = {
            'Aircraft': row["Airline_Name"],
            'Flight Capacity': row["Passengers"]
        }

        # setting distance to what is outputted from the distance_calc function
        adjacency_matrix[source_index][dest_index]['distance'] = distance

        # setting route_max_capacity to the sum of all aircraft's passenger capacity
        adjacency_matrix[source_index][dest_index]['route_max_capacity'] += row["Passengers"]

        # Update maximum capacity aircraft for the route
        current_capacity = adjacency_matrix[source_index][dest_index]['aircraft_max_capacity']

        # checking to see if there is an aircraft with a higher passenger capacity
        if row["Passengers"] > current_capacity:
            # If the current flight has higher capacity, update max_capacity and clear existing flights
            adjacency_matrix[source_index][dest_index]['flights'] = {row["Carrier"]: flight_info}
            adjacency_matrix[source_index][dest_index]['aircraft_max_capacity'] = row['Passengers']

        # adds a new entry to the list if there are mutiple planes with the same max capacity
        elif row["Passengers"] == current_capacity:
            adjacency_matrix[source_index][dest_index]['flights'][row["Carrier"]] = flight_info
        
        # Set timezone info only if it hasn't been set yet since timezone
        if not adjacency_matrix[source_index][dest_index]['SrcTimezone']:
            adjacency_matrix[source_index][dest_index]['SrcTimezone'] = row["Src Timezone Name"]

        if not adjacency_matrix[source_index][dest_index]['DestTimezone']:
            adjacency_matrix[source_index][dest_index]['DestTimezone'] = row["Dest Timezone Name"]

    return adjacency_matrix
