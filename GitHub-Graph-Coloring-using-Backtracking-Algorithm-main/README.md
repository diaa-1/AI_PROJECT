# Graph-Coloring-using-Backtracking-Algorithm

## Graph Coloring using Backtracking Algorithm

This project, authored by **AZIOUANE KHEDIDJA**, implements a backtracking algorithm to perform graph coloring. Graph coloring is a classic problem in graph theory where the goal is to assign colors to the vertices of a graph such that no two adjacent vertices share the same color.

### Problem Statement

Given a graph representing relationships between entities (e.g., countries and their borders), the task is to color the vertices of the graph using the minimum number of colors such that no two adjacent vertices have the same color.

### Implementation

The project provides a Python implementation of the backtracking algorithm to solve the graph coloring problem. The `backtracking()` function recursively explores possible color assignments for each vertex, ensuring that adjacent vertices have different colors. Once a solution is found, the algorithm returns the minimum number of colors needed to color the graph.

### Usage

To use the project, simply execute the provided Python script. It loads a shapefile containing geographic data of African countries and constructs a graph based on the adjacency matrix. The backtracking algorithm is then applied to color the countries on the map. The colored map is displayed using Matplotlib.

### Example Execution

Map of African Countries - Colored based on Graph Coloring
![image](https://github.com/AZIOUANEkhedidja/Graph-Coloring-using-Backtracking-Algorithm/assets/141507872/beb99f17-fe0f-4020-b0c9-bdca0ea28726)

### Dependencies

- Python 3.x
- Geopandas
- Matplotlib
- Pandas

### How to Run

1. To install the required dependencies, you can use pip:

```bash
pip install geopandas matplotlib pandas
```

2. To execute the Python script, run the following command:

```bash
python your_script.py
```
