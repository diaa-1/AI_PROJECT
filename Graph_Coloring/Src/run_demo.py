from graph_utils import load_edgelist, draw_colored_graph
from backtracking import try_min_colors

def main():
    G = load_edgelist("C:\\Users\\W.I\\OneDrive\\Desktop\\AI_PROJECT\\Graph_Coloring\\Data\\g_cycle_5.edgelist")

    k, colors, t = try_min_colors(G, max_try=6, use_mrv=True, time_limit=10)

    print("k:", k, "time:", t)

    if k:
        draw_colored_graph(G, colors, title=f"Backtracking coloring k={k}")

if __name__ == "_main_":
    main()