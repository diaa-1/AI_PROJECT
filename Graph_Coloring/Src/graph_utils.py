# src/graph_utils.py
import networkx as nx
import matplotlib.pyplot as plt
import json

def load_edgelist(path):
    """
    Reads an edge list file (each line: u v) and returns a networkx.Graph
    """
    G = nx.Graph()
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            u, v = int(parts[0]), int(parts[1])
            G.add_edge(u, v)
    return G

def save_edgelist(G, path):
    nx.write_edgelist(G, path, data=False)

def load_json_graph(path):
    with open(path, 'r') as f:
        obj = json.load(f)
    G = nx.Graph()
    nodes = obj.get("nodes", [])
    edges = obj.get("edges", [])
    G.add_nodes_from(nodes)
    for e in edges:
        if len(e) >= 2:
            G.add_edge(int(e[0]), int(e[1]))
    return G

def draw_colored_graph(G, colors_dict=None, title=None, figsize=(6,6)):
    """
    colors_dict: dict node -> color_index (int). If None: draw without coloring.
    """
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=figsize)
    if colors_dict:
        nodes = list(G.nodes())
        node_colors = [colors_dict.get(n, 0) for n in nodes]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.tab20, node_size=600, edgecolors='k')
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, edgecolors='k')
    if title:
        plt.title(title)
    plt.show()

if _name_ == "_main_":
    # small demo
    G = load_edgelist("../data/g_cycle_5.edgelist")
    draw_colored_graph(G)