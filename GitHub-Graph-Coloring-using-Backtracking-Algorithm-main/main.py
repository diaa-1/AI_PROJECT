import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from Backtracking_Algorithm import graph_colouring
import numpy as np

fp = r"C:\Users\W.I\OneDrive\Desktop\AI_PROJECT\GitHub-Graph-Coloring-using-Backtracking-Algorithm-main\datasets\shapefile\ne_10m_admin_0_countries.shp"

data = gpd.read_file(fp)


def african():
    african_countries_list = data[data["CONTINENT"] == "Africa"]["ADMIN"].unique()

    # Create an empty DataFrame
    adjacency_matrix = pd.DataFrame(
        index=african_countries_list, columns=african_countries_list
    )
    adjacency_matrix = adjacency_matrix.fillna(0)

    # Iterate over each country and its neighbors
    for _, country in data[data["CONTINENT"] == "Africa"].iterrows():
        country_name = country["ADMIN"]
        neighboring = data[data.geometry.touches(country["geometry"])]["ADMIN"].tolist()
        for neighbor in neighboring:
            if neighbor in african_countries_list:
                adjacency_matrix.loc[country_name, neighbor] = 1

    return adjacency_matrix

# Get the adjacency matrix
adjacency_matrix = african()
adjacency_array = adjacency_matrix.values.tolist()  # Display the adjacency matrix
min_colors, all_colorings = graph_colouring(np.array(adjacency_array))

print("Minimum number of colors needed:", min_colors)
chosen_solution = (
    all_colorings[0] if all_colorings else None
)  # Choose the first found solution

if chosen_solution:
    # Assuming chosen_solution is a list of color numbers for each country
    african_countries = data[data["CONTINENT"] == "Africa"]
    # african_countries.loc[:, 'Color'] = chosen_solution
    african_countries.loc[:, 'Color'] = chosen_solution  # Adding color numbers as a column

    # Plotting the map based on color numbers
    african_countries.plot(column="Color", cmap="Set1", legend=True)
    plt.title("Map of African Countries - Colored based on Graph Coloring")
    plt.show()
else:
    print("No solution found.")
