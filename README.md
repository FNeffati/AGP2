# Flight Routing and Capacity Analysis

## Project Overview

This Python script aims to analyze and optimize flight routing and capacity for trips with at most one layover. The Ford-Fulkerson algorithm is employed to find the maximal flow in the network, allowing for detailed insights into the movement of passengers between source and target cities or airports.

### Features and Components

1. **Data Loading and Wrangling:**
   - Utilizes the Pandas library to load and process flight data from a given source or module (`data_wrangling`).
   - Subsets flights based on specified source and destination cities or airports.

2. **Graph Construction:**
   - Constructs an adjacency matrix representing the flight network.
   - Incorporates relevant information such as distances, route capacities, aircraft capacities, and flight details.

3. **Haversine Distance Calculation:**
   - Implements the Haversine formula to accurately calculate distances between airports based on their geographical coordinates.

4. **Ford-Fulkerson Algorithm:**
   - Applies the Ford-Fulkerson algorithm to find the maximal flow in the flight network.
   - Considers constraints on each flight segment, including direct flights and those with one layover.

5. **Output and Analysis:**
   - Prints detailed information about each flight segment, including routes, capacities, and distances.
   - Reports the maximal number of people that can be moved from the source to the target.
   - Identifies the carrier with the maximal flow, providing valuable insights for capacity planning.

6. **CSV Output (Optional):**
   - Generates CSV files containing adjacency matrices for further analysis or visualization.
   - Uncomment relevant lines in the script to save these CSV files.

## Decisions and Assumptions

1. **Counting People:**
   - Individuals are counted based on the total number of passengers each flight can carry.

2. **Counting Flights:**
   - Each flight segment (direct or with one layover) is considered a separate flight.

3. **Maximal Flow Definition:**
   - The maximal flow represents the maximum number of individuals that can be transported from the source to the target while adhering to the given constraints.

## Getting Started

1. **Environment Setup:**
   - Ensure you have Python 3.x installed.
   - Install required libraries using `pip install -r requirements.txt`.

2. **Running the Script:**
   - Execute the Python script (`flight_analysis.py`) in a compatible environment.
   - Follow the prompts to input source and destination airports or cities.

3. **Reviewing Output:**
   - Examine the detailed output, including routes, capacities, and the identified carrier with the maximal flow.

4. **Optional CSV Output:**
   - Uncomment relevant lines in the script to save CSV files for further analysis.

## Project Structure

- `flight_analysis.py`: Main script containing the analysis logic.
- `data_wrangling.py`: Module or source for loading flight data.
- `requirements.txt`: File specifying the required Python libraries.

## Contributors

- [YuHan Burgess]
- [Fehmi Neffati]
- [Emma Horton]
