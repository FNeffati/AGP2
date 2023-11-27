import numpy as np
from data_wrangling import df_possible_flights


def create_matrix(df, airports):
    num_airports = len(airports)

    # Create an adjacency matrix with zeros
    adjacency_matrix = np.zeros((num_airports, num_airports), dtype=int)

    # Fill the adjacency matrix based on the flights
    for index, row in df.iterrows():
        source_index = airports.index(row["Source Airport"])
        dest_index = airports.index(row["Destination Airport"])
        adjacency_matrix[source_index][dest_index] = 1

    source = [airports.index('JFK'), airports.index('LGA')]
    sink = airports.index('SFO')

    return adjacency_matrix, source, sink
