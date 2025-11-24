# src/backtracking.py
import time
import networkx as nx
from collections import defaultdict, deque

def valid_color(G, node, color, colors):
    for nbr in G.neighbors(node):
        if nbr in colors and colors[nbr] == color:
            return False
    return True

def order_by_degree(G, nodes):
    # ترتيب عقد حسب degree تنازلي (heuristic بسيط - higher degree first)
    return sorted(nodes, key=lambda n: G.degree(n), reverse=True)

def mrv_order(G, domains, assigned):
    # MRV: اختار العقدة اللي عندها أقل عدد من الألوان المتاحة حاليًا (domain size)
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

def forward_checking_update(domains, node, color, G):
    # رجّع قائمة (node, removed_color) علشان نقدر نرجعها عند الباكترك
    removed = []
    for nbr in G.neighbors(node):
        if color in domains[nbr]:
            domains[nbr].remove(color)
            removed.append((nbr, color))
    return removed

def restore_domains(domains, removed):
    for n, c in removed:
        domains[n].add(c)

def backtrack_search(G, max_colors, use_mrv=True, time_limit=None):
    """
    G: networkx graph
    max_colors: عدد الألوان المسموح
    use_mrv: whether to use MRV ordering + forward checking
    time_limit: seconds (optional) to stop early
    Returns: (success_bool, colors_dict, elapsed_time)
    """
    nodes = list(G.nodes())
    # initial domains: each node can take colors 0..max_colors-1
    domains = {n: set(range(max_colors)) for n in nodes}
    assigned = {}
    start = time.time()

    # optionally sort nodes to fixed order (degree heuristic) - used by non-MRV fallback
    degree_ordered = order_by_degree(G, nodes)

    def backtrack():
        # time limit check
        if time_limit and (time.time() - start) > time_limit:
            return False

        if len(assigned) == len(nodes):
            return True

        # select variable (node)
        if use_mrv:
            var = mrv_order(G, domains, assigned)
            if var is None:
                return False
        else:
            # choose next unassigned in degree order
            var = next((n for n in degree_ordered if n not in assigned), None)
            if var is None:
                return False

        # value ordering: try colors in increasing order (can use heuristics)
        for color in sorted(domains[var]):
            if valid_color(G, var, color, assigned):
                # assign
                assigned[var] = color
                # forward checking: remove color from neighbors' domains
                removed = []
                if use_mrv:
                    removed = forward_checking_update(domains, var, color, G)
                # check no domain wiped out
                wipeout = any(len(domains[n]) == 0 for n in G.nodes() if n not in assigned)
                if not wipeout:
                    if backtrack():
                        return True
                # undo
                if use_mrv:
                    restore_domains(domains, removed)
                del assigned[var]
        return False

    ok = backtrack()
    elapsed = time.time() - start
    return ok, dict(assigned), elapsed

def try_min_colors(G, max_try=6, **kwargs):
    """
    Try to find minimal colors from 1..max_try using backtracking with pruning.
    Returns first successful (k, colors, time)
    """
    for k in range(1, max_try+1):
        ok, colors, t = backtrack_search(G, k, **kwargs)
        if ok:
            return k, colors, t
    return None, {}, None

if _name_ == "_main_":
    # demo
    G = nx.cycle_graph(5)  # C5 requires 3 colors
    k, colors, t = try_min_colors(G, max_try=5, use_mrv=True, time_limit=5)
    print("result:", k, colors, "time:", t)