def conditionBacktrack(graph, sommet_index, color, c):
    return all(graph[sommet_index][i] == 0 or color[i] != c for i in range(len(graph)))

def backtracking(graph, m, color, sommet_index, all_colorings, found_solution):
    if sommet_index == len(graph):  # condition d'arret found solution
        found_solution.append(color)
        return True
    for c in range(1, m + 1):
        if conditionBacktrack(graph, sommet_index, color, c):
            color[sommet_index] = c
            if backtracking(graph, m, color, sommet_index + 1, all_colorings, found_solution):
                return True  # Exit if a solution is found
            color[sommet_index] = 0
    return False  # Return False if no solution is found

def graph_colouring(graph):
    color = [0] * len(graph)
    m = 1
    all_colorings = []
    found_solution = []
    while not found_solution:
        if backtracking(graph, m, color, 0, all_colorings, found_solution):
            break  # Exit while loop if a solution is found
        m = m+1
        color = [0]*len(graph)
    min_colors_used = min(len(set(coloring)) for coloring in found_solution)
    return min_colors_used, found_solution
