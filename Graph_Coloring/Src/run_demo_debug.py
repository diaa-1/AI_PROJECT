import os
import sys
import traceback
from pathlib import Path

sys.path.append(os.path.dirname(__file__))

print("=== RUN DEMO DEBUG START ===")
print("Current folder:", os.path.dirname(__file__))
print("Files in folder:", os.listdir(os.path.dirname(__file__)))

try:
    import graph_utils
    from graph_utils import load_edgelist, draw_colored_graph
    print("Imported graph_utils")
except Exception as e:
    print("Failed to import graph_utils:", e)
    traceback.print_exc()
    sys.exit(1)

try:
    import backtracking
    from backtracking import try_min_colors
    print("Imported backtracking")
except Exception as e:
    print("Failed to import backtracking:", e)
    traceback.print_exc()
    sys.exit(1)



if len(sys.argv) > 1:
    override = sys.argv[1]
    print(f"[CLI] Dataset overridden to: {override}")
    data_file = Path(override)
else:
    if hasattr(backtracking, "DATASET_FILE"):
        data_file = Path(backtracking.DATASET_FILE)
    else:
        data_file = Path(__file__).parent / "data" / "g_cycle_5.edgelist"

data_file = Path(os.path.normpath(str(data_file)))

print("Looking for data file at:", data_file)


if not data_file.exists():
    print("ERROR: data file not found. Please check the path and filename.")
    sys.exit(1)

try:
    G = load_edgelist(data_file)
    print(f"Loaded graph: nodes={G.number_of_nodes()} edges={G.number_of_edges()}")
except Exception as e:
    print("Error while loading edgelist:", e)
    traceback.print_exc()
    sys.exit(1)

try:
    print("Running try_min_colors(...)")
    k, colors, t = try_min_colors(G, max_try=8, use_mrv=True, time_limit=10)
    print("RESULTS:")
    print("  min colors =", k)
    print("  assignments =", colors)
    print("  time(s) =", t)
except Exception as e:
    print("Error while running coloring:", e)
    traceback.print_exc()
    sys.exit(1)

try:
    draw_colored_graph(G, colors_dict=colors, title=f"Coloring (k={k})")
    print("Graph drawn (matplotlib window should be visible).")
except Exception as e:
    print("Error while drawing graph:", e)
    traceback.print_exc()

print("=== RUN DEMO DEBUG END ===")