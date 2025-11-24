# run_demo_debug.py
import os
import sys
import traceback

# بضمان إن نفس فولدر Src في الـ path
sys.path.append(os.path.dirname(_file_))

print("=== RUN DEMO DEBUG START ===")

# 1) check files in this folder
print("Current folder:", os.path.dirname(_file_))
print("Files in folder:", os.listdir(os.path.dirname(_file_)))

# 2) try import graph utils
try:
    from graph_utils import load_edgelist, draw_colored_graph
    print("Imported graph_utils ✅")
except Exception as e:
    print("Failed to import graph_utils:", e)
    traceback.print_exc()
    sys.exit(1)

# 3) try import coloring code (backtracking or coloring_algorithm)
try:
    # try the usual name first
    from coloring_algorithm import try_min_colors
    print("Imported coloring_algorithm.try_min_colors ✅")
except Exception as e1:
    print("Import coloring_algorithm failed:", e1)
    print("Trying to import backtracking.try_min_colors as fallback...")
    try:
        from backtracking import try_min_colors
        print("Imported backtracking.try_min_colors ✅")
    except Exception as e2:
        print("Import fallback failed:", e2)
        traceback.print_exc()
        sys.exit(1)

# 4) build path to data file (relative to Src)
data_file = os.path.normpath(os.path.join(os.path.dirname(_file_), "..", "Data", "g_cycle_5.edgelist"))
print("Looking for data file at:", data_file)

if not os.path.exists(data_file):
    print("ERROR: data file not found. Please check the path and filename.")
    sys.exit(1)

# 5) load graph
try:
    G = load_edgelist(data_file)
    print(f"Loaded graph: nodes={G.number_of_nodes()} edges={G.number_of_edges()}")
except Exception as e:
    print("Error while loading edgelist:", e)
    traceback.print_exc()
    sys.exit(1)

# 6) run coloring
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

# 7) draw (wrap in try so even if plotting fails we still keep logs)
try:
    draw_colored_graph(G, colors_dict=colors, title=f"Coloring (k={k})")
    print("Graph drawn (matplotlib window should be visible).")
except Exception as e:
    print("Error while drawing graph:", e)
    traceback.print_exc()

print("=== RUN DEMO DEBUG END ===")