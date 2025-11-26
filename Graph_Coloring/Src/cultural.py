import random
import copy
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

MAX_GEN = 600
POP_SIZE = 100
NUM_VERTICES = 0
ADJ_LIST = {}
generation = 0
population = []
belief_space = {"best_ever": None}

def load_dimacs_col(file_path: str) -> None:
    global NUM_VERTICES, ADJ_LIST
    ADJ_LIST = {}
    edges = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            parts = line.split()
            if parts[0] == 'p':
                NUM_VERTICES = int(parts[2])
                ADJ_LIST = {i: [] for i in range(NUM_VERTICES)}
            elif parts[0] == 'e':
                u = int(parts[1]) - 1
                v = int(parts[2]) - 1
                edges.append((u, v))
    for u, v in edges:
        ADJ_LIST[u].append(v)
        ADJ_LIST[v].append(u)
    print(f"Loaded: {NUM_VERTICES} vertices, {len(edges)} edges\n")

def fitness(coloring: List[int]) -> int:
    conflicts = 0
    for u in range(NUM_VERTICES):
        for v in ADJ_LIST[u]:
            if u < v and coloring[u] == coloring[v]:
                conflicts += 1
    return -conflicts

def create_individual(k: int) -> List[int]:
    return [random.randint(0, k-1) for _ in range(NUM_VERTICES)]

def smart_mutate(individual: List[int], k: int) -> List[int]:
    coloring = individual[:]
    for _ in range(50):
        v = random.choice(range(NUM_VERTICES))
        old = coloring[v]
        for c in random.sample(range(k), k):
            if c == old:
                continue
            coloring[v] = c
            if fitness(coloring) > fitness(individual):
                return coloring
        coloring[v] = old
    return coloring

def solve_with_k(file_path: str, k: int) -> Tuple[bool, Optional[List[int]], float]:
    global generation, population, belief_space
    
    load_dimacs_col(file_path)
    population = [create_individual(k) for _ in range(POP_SIZE)]
    belief_space["best_ever"] = max(population, key=fitness).copy()
    
    start = time.time()
    print(f"Trying to color with {k} colors...\n")
    
    for generation in range(1, MAX_GEN + 1):
        new_pop = [belief_space["best_ever"].copy()]
        while len(new_pop) < POP_SIZE:
            if random.random() < 0.15:
                child = create_individual(k)
            else:
                child = smart_mutate(belief_space["best_ever"], k)
            new_pop.append(child)
        
        population = new_pop
        current_best = max(population, key=fitness)
        
        if fitness(current_best) > fitness(belief_space["best_ever"]):
            belief_space["best_ever"] = current_best.copy()
        
        conflicts = -fitness(current_best)
        colors_used = len(set(current_best))
        
        if generation % 10 == 0 or conflicts == 0:
            print(f"Gen {generation:3d} | Conflicts: {conflicts:3d} | Colors used: {colors_used}")
        
        if conflicts == 0:
            elapsed = time.time() - start
            print(f"\nCHROMATIC NIRVANA ACHIEVED with {k} colors!")
            print(f"Valid coloring found in {generation} generations")
            print(f"Colors actually used: {colors_used}")
            print(f"Time: {elapsed:.2f}s\n")
            return True, current_best, elapsed
    
    elapsed = time.time() - start
    print(f"Failed with {k} colors (best conflicts: {-fitness(belief_space['best_ever'])}) in {elapsed:.2f}s\n")
    return False, None, elapsed

def find_chromatic_number(file_path: str):
    print("Searching for the smallest number of colors...\n")
    total_start = time.time()
    
    for k in range(1, 50):
        success, coloring, t = solve_with_k(file_path, k)
        if success:
            total_time = time.time() - total_start
            used = len(set(coloring))
            print("="*60)
            print(f"SUCCESS! Graph is {k}-colorable")
            print(f"Chromatic number = {k}")
            print(f"Colors used: {used}")
            print(f"Total time: {total_time:.2f} seconds")
            print("="*60)
            
            sol_file = Path(file_path).stem + f"_sol_k{k}.txt"
            with open(sol_file, "w") as f:
                f.write(f"Colors used: {used}\n")
                f.write(" ".join(map(str, coloring)))
            print(f"Solution saved to {sol_file}")
            print("Coloring:", coloring)
            return
        
    print("No solution found with reasonable k.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cultural.py <graph.col>")
        sys.exit(1)
    
    graph = sys.argv[1]
    if not Path(graph).exists():
        print("File not found!")
        sys.exit(1)
    
    find_chromatic_number(graph)