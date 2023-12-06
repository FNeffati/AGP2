import numpy as np
import pandas as pd
from data_wrangling import df_possible_flights
from pathlib import Path

def create_matrix(df, airports):
    num_airports = len(airports)

    # Create an adjacency matrix with zeros
    adjacency_matrix = np.zeros((num_airports, num_airports), dtype=int)

    # Fill the adjacency matrix based on the flights
    for index, row in df.iterrows():
        source_index = airports.index(row["Source Airport"])
        dest_index = airports.index(row["Destination Airport"])
        if adjacency_matrix[source_index][dest_index] < row["Passengers"]:
            adjacency_matrix[source_index][dest_index] = row["Passengers"]

    source = [airports.index('JFK'), airports.index('LGA')]
    sink = [airports.index('SFO')]
    # filepath = Path('/Users/yuhanburgess/Documents/GitHub/AGP2/dataset/adjacency_matrix.csv')
    # filepath.parent.mkdir(parents=True, exist_ok=True)
    # adjacency_df = pd.DataFrame(adjacency_matrix, columns=airport_ids, index=airport_ids)

    # adjacency_df.to_csv(filepath)
    return adjacency_matrix, source, sink
