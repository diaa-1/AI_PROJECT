import time
import networkx as nx
from pathlib import Path


BASE_DIR = Path(__file__).parent          
DATA_DIR = BASE_DIR.parent / "Data"             

DATASET_BASENAME = "g_random_10"            
DATASET_EXT = ".col"                

DATASET_FILE = DATA_DIR / (DATASET_BASENAME + DATASET_EXT)

print(f"[CONFIG] Using dataset: {DATASET_FILE}")


def valid_color(G, node, color, assigned):
    for nbr in G.neighbors(node):
        if nbr in assigned and assigned[nbr] == color:
            return False
    return True

def order_by_degree(G, nodes):
    return sorted(nodes, key=lambda n: G.degree(n), reverse=True)

def mrv_order(G, domains, assigned):
    best = None
    best_size = None
    for n in G.nodes():
        if n in assigned:
            continue
        size = len(domains[n])
        if best is None or size < best_size:
            best = n
            best_size = size
    return best

def forward_checking_update(domains, node, color, G, assigned):
    removed = []
    for nbr in G.neighbors(node):
        if nbr in assigned:
            continue
        if color in domains[nbr]:
            domains[nbr].remove(color)
            removed.append((nbr, color))
    return removed

def restore_domains(domains, removed):
    for n, c in removed:
        domains[n].add(c)

def backtrack_search(G, max_colors, use_mrv=True, time_limit=None):
    nodes = list(G.nodes())
    domains = {n: set(range(max_colors)) for n in nodes}
    assigned = {}
    start = time.time()

    degree_ordered = order_by_degree(G, nodes)

    def backtrack():
        if time_limit is not None and (time.time() - start) > time_limit:
            return False

        if len(assigned) == len(nodes):
            return True

        if use_mrv:
            var = mrv_order(G, domains, assigned)
            if var is None:
                return False
        else:
            var = next((n for n in degree_ordered if n not in assigned), None)
            if var is None:
                return False

        for color in sorted(list(domains[var])):
            if valid_color(G, var, color, assigned):
                assigned[var] = color

                removed = []
                if use_mrv:
                    removed = forward_checking_update(domains, var, color, G, assigned)

                wipeout = any(len(domains[n]) == 0 for n in G.nodes() if n not in assigned)
                if not wipeout:
                    if backtrack():
                        return True

                if use_mrv:
                    restore_domains(domains, removed)
                del assigned[var]
        return False

    ok = backtrack()
    elapsed = time.time() - start
    return ok, dict(assigned), elapsed

def try_min_colors(G, max_try=6, **kwargs):
    for k in range(1, max_try+1):
        ok, colors, t = backtrack_search(G, k, **kwargs)
        if ok:
            return k, colors, t
    return None, {}, None



if __name__ == "_main_":

    try:
        from graph_utils import load_edgelist
        G = load_edgelist(DATASET_FILE)
    except Exception as e:
        print("Error loading dataset from config:", e)
        print("Using fallback: cycle_graph(5)")
        G = nx.cycle_graph(5)

    print("Running coloring algorithm…")
    k, colors, t = try_min_colors(G, max_try=8, use_mrv=True, time_limit=10)

    print("=================================================")
    print("   RESULT")
    print("   Min Colors:", k)
    print("   Assignments:", colors)
    print("   Time:", t)
    print("=================================================")