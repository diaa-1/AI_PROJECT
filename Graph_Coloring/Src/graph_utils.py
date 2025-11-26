import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import json

DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "g_cycle_5.edgelist"

def load_edgelist(path=None):
    """
    Read an edgelist / .col / .json graph.
    If path is None, uses DEFAULT_DATA_PATH.
    Returns a networkx.Graph().
    """
    p = Path(path) if path is not None else DEFAULT_DATA_PATH
    if not p.exists():
        raise FileNotFoundError(f"Dataset not found: {p}")

    ext = p.suffix.lower()
    if ext == ".json":
        return load_json_graph(p)

    G = nx.Graph()
    edges = []
    with open(p, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('c') or line.startswith('#'):
                continue
            parts = line.split()
            if parts[0] == 'e' and len(parts) >= 3:
                try:
                    u = int(parts[1]); v = int(parts[2])
                except ValueError:
                    continue
                edges.append((u, v))
                continue
            if len(parts) >= 2:
                try:
                    u = int(parts[0]); v = int(parts[1])
                except ValueError:
                    continue
                edges.append((u, v))
    if edges:
        G.add_edges_from(edges)
    return G

def save_edgelist(G, path):
    nx.write_edgelist(G, path, data=False)

def load_json_graph(path):
    p = Path(path)
    with open(p, 'r', encoding='utf-8') as f:
        obj = json.load(f)
    G = nx.Graph()
    nodes = obj.get("nodes", [])
    edges = obj.get("edges", [])
    G.add_nodes_from(int(n) for n in nodes)
    for e in edges:
        if len(e) >= 2:
            G.add_edge(int(e[0]), int(e[1]))
    return G

def draw_colored_graph(G, colors_dict=None, title=None, figsize=(6,6)):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=figsize)
    if colors_dict is not None:
        nodes = list(G.nodes())
        node_colors = [colors_dict.get(n, 0) for n in nodes]
        nx.draw(
            G, pos, with_labels=True,
            node_color=node_colors,
            cmap=plt.cm.tab20,
            node_size=600,
            edgecolors='k'
        )
    else:
        nx.draw(
            G, pos, with_labels=True,
            node_color='lightblue',
            node_size=600,
            edgecolors='k'
        )
    if title:
        plt.title(title)
    plt.show()

if __name__ == "_main_":
    try:
        G = load_edgelist(None)
        print("Loaded demo graph:", G.number_of_nodes(), "nodes,", G.number_of_edges(), "edges")
        draw_colored_graph(G, title="Uncolored Graph (demo)")
    except Exception as e:
        print("graph_utils demo error:", e)