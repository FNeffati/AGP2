from collections import deque
import pandas as pd
import numpy as np
from data_wrangling import df_full
from AdjacencyMatrix import create_matrix, distance_calc
from networkFlowAlgorithm import ford_fulkerson

def subset_flights(df_full, source, sink):
    if len(source)>3:
        df_possible_flights = df_full[df_full["Src City"].str.contains(source) |
                                                df_full["Dest City"].str.contains(sink)]

    else: 
        df_possible_flights = df_full[df_full["Source Airport"].str.contains(source) |
                                                df_full["Destination Airport"].str.contains(sink)]

    sub_df = df_possible_flights.dropna(subset=['Airline_Name'])

    if not sub_df.empty:
        # Find indices of airports in the overall list of airports
        airports = sorted(set(sub_df["Source Airport"]).union(set(sub_df["Destination Airport"])))

        if len(source)>3:
        # the is identifying what the start node is (source) and end node(sink) by making sure the airport exists
        # in the true source or sink city
            source_aiports = sub_df[sub_df['Src City'] == source]['Source Airport'].unique().tolist()
            sink_airports = sub_df[sub_df['Dest City'] == sink]['Destination Airport'].unique().tolist()

            # the is identifying what the start node is (source) and end node(sink)
            sources = [airports.index(src) for src in source_aiports if src in airports]
            sinks = [airports.index(sink) for sink in sink_airports if sink in airports]
        else:
            source_aiports = sub_df[sub_df['Source Airport'] == source]['Source Airport'].unique().tolist()
            sink_airports = sub_df[sub_df['Destination Airport'] == sink]['Destination Airport'].unique().tolist()

            # the is identifying what the start node is (source) and end node(sink)
            sources = [airports.index(src) for src in source_aiports if src in airports]
            sinks = [airports.index(sink) for sink in sink_airports if sink in airports]

    source = []
    sink = []
    for item in source_aiports:
        source.append(airports.index(item))
    for item in sink_airports:
        sink.append(airports. index(item))
        
    return df_possible_flights, sources, sinks 


# Testing 
##########################################################################################
start = input("Enter start airport/City:")
end = input("Enter destination airport/City:")

sub_df, sources, sinks = subset_flights(df_full, start, end)
airports = sorted(set(sub_df["Source Airport"]).union(set(sub_df["Destination Airport"])))
adjacency_matrix = create_matrix(sub_df, airports)
adjacency_df = pd.DataFrame(adjacency_matrix, columns=airports, index=airports)

ford_fulkerson(adjacency_matrix, sources, sinks, airports)

# csv_file_path = "/Users/yuhanburgess/Documents/GitHub/AGP2/csv_files/Flow_matrix.csv"
# adjacency_df.to_csv(csv_file_path, index=True, header=True) 