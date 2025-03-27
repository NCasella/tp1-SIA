import sys
import json 
from sokoban import Sokoban, SokobanState
from search_methods import *
import numpy as np 

global sokoban

def h1(node:Node):
        global sokoban
        sum=0
        for boxes_positions in node.state.boxes_positions:
            distances=[]
            for objectives in sokoban.objective_positions:
                distances.append(abs(objectives[0]-boxes_positions[0])+abs(objectives[1]-boxes_positions[1]))
            sum+=np.min(distances)
        return sum
    
def h2(node:Node):
    sum=0
    for boxes_positions in node.state.boxes_positions:
        x, y = boxes_positions
        if node.state.matrix[x][y] == "$":
            sum += 1
    return sum


from collections import deque

def find_shortest_path(matrix, objectives, x, y, sum):
    queue = [(x, y, sum)]
    visited = set()
    
    while queue:
        cx, cy, steps = queue.pop(0)
        
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        
        if (cx, cy) in objectives:
            return steps
        
        for nx, ny in [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
            if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and matrix[nx][ny] != '#' and (nx, ny) not in visited:
                queue.append((nx, ny, steps + 1))
    
    return float('inf') 


def h3(node):
    global sokoban
    total_sum = 0
    objectives = set(sokoban.objective_positions)
    for box in node.state.boxes_positions:
        x, y = box
        total_sum += find_shortest_path(node.state.matrix, objectives, x, y, 0)
    return total_sum


def h3(node):
    global sokoban
    total_sum = 0
    objectives = set(sokoban.objective_positions) 
    for box in node.state.boxes_positions:
        x, y = box
        total_sum += find_shortest_path(node.state.matrix, objectives, x, y, 0)
    return total_sum


algorithm_map = {
    "bfs": breath_first_search,
    "dfs": limited_depth_first_search,
    "greedy": greedy_search,
    "a*": a_star_search,
    "iddfs": iterative_depth_limited_first_search
}

heuristics_map = {
    "h1": h1,
    "h2": h2,
    "h3": h3
}

class TxtToMatrixParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def txt_to_matrix(self):
        matrix = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    row = list(line.replace('\n', ''))
                    matrix.append(row)
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            sys.exit(1)
        return matrix

def run(config_path):

    with open(config_path, 'r') as file:
        params = json.load(file)

    filepath = params["filepath"]
    parser = TxtToMatrixParser(filepath)
    matrix = parser.txt_to_matrix()

    global sokoban
    sokoban = Sokoban(matrix)

    algo = params["algorithm"]

    if algo not in algorithm_map:
        print("Invalid specified algorithm")
        sys.exit(1)

    if algo=="a*" or algo=="greedy":
        result:Result = algorithm_map[algo](sokoban, h1)
    elif algo=="dfs":
        result:Result=algorithm_map[algo](sokoban,params["limit"])
    else:
        result:Result = algorithm_map[algo](sokoban)

    
    
    
    
    
    

   # for node in result.solution:
   #     states.append(node.action)
   #     print(node.action)

    # for node in result.solution:
    #     n:Node = node
    #     print(n.state)

    #TODO animar el resultado

    # print("Parsed Matrix:")
    # for row in matrix:
    #     print(row)
    return result

def run_with_params(algorithm, heuristic, limit, filepath):

    parser = TxtToMatrixParser(filepath)
    matrix = parser.txt_to_matrix()
    
    global sokoban
    sokoban = Sokoban(matrix)

    if algorithm=="a*" or algorithm=="greedy":
        result:Result = algorithm_map[algorithm](sokoban,heuristics_map[heuristic])
    elif algorithm=="dfs":
        result:Result=algorithm_map[algorithm](sokoban,limit)
    else:
        result:Result = algorithm_map[algorithm](sokoban)

   # for node in result.solution:
   #     states.append(node.action)
   #     print(node.action)

    # for node in result.solution:
    #     n:Node = node
    #     print(n.state)

    #TODO animar el resultado

    # print("Parsed Matrix:")
    # for row in matrix:
    #     print(row)
    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py config.json")
        sys.exit(1)

    params = sys.argv[1]
    with open(params, 'r') as file:
        params = json.load(file)

    filepath = params["filepath"]
    parser = TxtToMatrixParser(filepath)
    matrix = parser.txt_to_matrix()

    global sokoban
    sokoban = Sokoban(matrix)


    if params["algorithm"]=="a*" or params["algorithm"]=="greedy":
        result:Result = algorithm_map[params["algorithm"]](sokoban, h1)
    elif params["algorithm"]=="dfs":
        result:Result=algorithm_map[params["algorithm"]](sokoban,params["limit"])
    else:
        result:Result = algorithm_map[params["algorithm"]](sokoban)

    
    
    
    
    
    states = []
    # for node in result.solution:
    #     states.append(node.action)
    #     print(node.action)

    # for node in result.solution:
    #     n:Node = node
    #     print(n.state)

    #TODO animar el resultado

    # print("Parsed Matrix:")
    # for row in matrix:
    #     print(row)
    return states

if __name__ == "__main__":
    main()