from collections import deque
import numpy as np
from AdjacencyMatrix import create_matrix
from data_wrangling import df_possible_flights


def ford_fulkerson(graph, sources, terminals):
    def residual_capacity(u, v):
        return graph[u][v] - flow[u][v]

    def augment(path):
        # Initialize min_capacity to an infinitely large number
        # this is similar to the relaxing schema seen in the Bellman-Ford Algorithm
        min_capacity = float('inf')

        # go through path array
        for i in range(len(path) - 1):
            # find the minimum capacity between the airports
            min_capacity = min(min_capacity, residual_capacity(path[i], path[i + 1]))

        # update flow of the edges and reverse edges along the path
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            flow[u][v] += min_capacity # update augmenting path
            flow[v][u] -= min_capacity # update flow on residual edges
        return min_capacity

    def bfs():
        visited = [False] * len(graph) # similar to the color system, but using True/False instead
        queue = deque(sources) # getting the first source in the list
        for source in sources:
            visited[source] = True

        # setting the sources as parents initially
        parent = {source: None for source in sources}

        # while there is a source in the queue, find flights
        # that connect from source to terminal
        while queue:
            # getting the first element in the queue
            u = queue.popleft()
            # go through the airports that are connected to the parent
            for v in range(len(graph)):
                # if it hasn't been visited and it can  be augmented
                if not visited[v] and residual_capacity(u, v) > 0:
                    # add it to the queue
                    queue.append(v)
                    visited[v] = True
                    # set the u the parent of v
                    parent[v] = u

                    # if v is a terminal then we will create a path for the
                    # flight
                    if v in terminals:
                        path = []
                        # adding cities into the path
                        while v is not None:
                            path.insert(0, v)
                            v = parent[v]
                        return path

        return None

    # Initialize flow to zero
    flow = np.zeros_like(graph)

    # Ford-Fulkerson algorithm
    total_flow = 0
    while True:
        augmenting_path = bfs()
        if augmenting_path is None:
            break
        min_capacity = augment(augmenting_path)
        total_flow += min_capacity
        print(f"Flight Route: {[airports[node] for node in augmenting_path]}, "
              f"Maximum Passenger Capacity: {min_capacity}")

    # Print the visited airports in the final path
    final_path = bfs()
    if final_path is not None:
        print("Final Path:", " --> ".join(airports[node] for node in final_path))

    print("Max Flow:", total_flow)


# Example usage
# df = df_possible_flights
# airports = sorted(set(df["Source Airport"]).union(set(df["Destination Airport"])))
# print(airports)
# adjacency_matrix, sources, sinks = create_matrix(df_possible_flights, airports)

# ford_fulkerson(adjacency_matrix, sources, sinks)
