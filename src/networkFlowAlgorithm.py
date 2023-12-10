from collections import deque
import pandas as pd
import numpy as np


def ford_fulkerson(graph, sources, terminals, airports):
    def residual_capacity(u, v):
        route_capacity = graph[u][v]['route_max_capacity'] - flow[u][v]
        aircraft_capacity = graph[u][v]['aircraft_max_capacity'] - flow[u][v]
        return route_capacity, aircraft_capacity

    def augment(path):
        # this will allow us to print the flights_info
        flights_and_capacity = []

        # total distance is initized as 0 for all flights 
        total_distance = 0

        #zip(path, path[1:]) helps when it looks something like [A, B, C] because it breakes it apart into
        # [A,B] and [B,C] in which we can do the calculations associateed with each leg of the flight separately
        #https://realpython.com/python-zip-function/
        route_min_capacity, aircraft_min_capacity = zip(*[residual_capacity(u, v) for u, v in zip(path, path[1:])])
            
        # go through and adjust the flow based on the leg of the flight
        # route_min_capcaity: contains the minimum route capacities for each segment of the path
        # flight_min_capacity: contains the minimum flight capacities for each segment of the path
        for u, v, route_min_cap, aircraft_min_cap in zip(path, path[1:], route_min_capacity, aircraft_min_capacity):
            edge_info = graph[u][v] # getting information about the edge between the two nodes
            total_distance += edge_info['distance'] # adding to distnace 

            # we want to change the flow for the max passenger capcity for the route and the aircraft repectively
            flow[u][v] += route_min_cap # heading towards sink (update the augmenting path)
            flow[v][u] -= route_min_cap # heading back towards source (update flow on residual edges)
            flow[u][v] += aircraft_min_cap # heading towards sink (update the augmenting path)
            flow[v][u] -= aircraft_min_cap # heading back towards source (update flow on residual edges)

        # we add the information form the flights info into the array
        for u, v in zip(path, path[1:]):
            flights_and_capacity.extend(graph[u][v]['flights'].items())

        return min(route_min_capacity), min(aircraft_min_capacity), total_distance, flights_and_capacity

    # the BFS utilizes queues to decrease the runtime 
    def bfs():
        # intializing an array that flags if a node has been visited
        # similar to the color system, but using True/False instead
        visited = [False] * len(graph) # getting the first source in the list
        queue = deque(sources)

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
                route, aircraft = residual_capacity(u, v)
                # if it hasn't been visited and it can be augmented
                if not visited[v] and (route > 0 and aircraft > 0):
                    # add it to the queue
                    queue.append(v)
                    visited[v] = True
                    # set the u the parent of v
                    parent[v] = u

                    # if v is a terminal then we will create a path for the flight
                    if v in terminals:
                        path = []
                        # adding cities into the path
                        while v is not None:
                            path.insert(0, v)
                            v = parent[v]
                        return path

        return None
    # Initialize flow to zero
    flow = np.zeros_like(graph, dtype=int)

    route_total_flow = 0
    flight_total_flow = 0

    # Ford-Fulkerson algorithm part of the code 
    while True:

        augmenting_path = bfs()
        if augmenting_path is None:
            break
        route_min_capacity, aircraft_min_capcity, total_distance, flights_and_capacity = augment(augmenting_path)
        route_total_flow += route_min_capacity# updating the total route flow
        flight_total_flow += aircraft_min_capcity # updating the total flight flow
        route = [airports[node] for node in augmenting_path]
        direct = True if len(route) == 2 else False
        # printing out reach route
        print()
        print("----------------------------------------------------------------------")
        print(f"Flight Route: {[airports[node] for node in augmenting_path]} \n "
              f"Direct: {direct} \n "
              f"Max Passenger Capacity: {route_min_capacity} \n "
              f"Max Flight Capacity: {aircraft_min_capcity} \n "
              f"Total Distance: {round(total_distance, 2)}km \n "
              f"Flights: {flights_and_capacity} \n ")

    print("----------------------------------------------------------------------")

    # Print the visited airports in the final path
    final_path = bfs()
    if final_path is not None:
        print("Final Path:", " --> ".join(airports[node] for node in final_path))

    print("Max Route Flow:", route_total_flow, "  Max Flight Flow:", flight_total_flow)