import sys
import json 
from sokoban import Sokoban, SokobanState
from search_methods import *
import numpy as np 

def h1(node:Node):
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


def pathfinding_recursive(matrix, x, y, counter):

    if x < 0 or x > len(matrix) or y < 0 or y > len(matrix[x]):
        return 99999999999999

    if matrix[x][y] == '.':
        return counter
    
    sum = 99999999999
    matrix[x][y] = 'x'

    if (matrix[x-1][y-1] != 'x' or matrix[x-1][y-1] != '#'):
        sum = min(sum, pathfinding_recursive(matrix, x-1, y-1, counter + 1))
    if (matrix[x-1][y] != 'x' or matrix[x-1][y] != '#'):
        sum = min(sum, pathfinding_recursive(matrix, x-1, y, counter + 1))
    if (matrix[x-1][y+1] != 'x' or matrix[x-1][y+1] != '#'):
        sum = min(sum, pathfinding_recursive(matrix, x-1, y+1, counter + 1))
    if (matrix[x][y-1] != 'x' or matrix[x][y-1] != '#'):
        sum = min(sum, pathfinding_recursive(matrix, x, y-1, counter + 1))
    if (matrix[x][y+1] != 'x' or matrix[x][y+1] != '#'):
        sum = min(sum, pathfinding_recursive(matrix, x, y+1, counter + 1))
    if (matrix[x+1][y-1] != 'x' or matrix[x+1][y-1] != '#'):
        sum = min(sum, pathfinding_recursive(matrix, x+1, y-1, counter + 1))
    if (matrix[x+1][y] != 'x' or matrix[x+1][y] != '#'):
        sum = min(sum, pathfinding_recursive(matrix, x+1, y, counter + 1))
    if (matrix[x+1][y+1] != 'x' or matrix[x+1][y+1] != '#'):
        sum = min(sum, pathfinding_recursive(matrix, x+1, y+1, counter + 1))
    
    return sum

def h3(node:Node):
    sum=0
    for boxes_positions in node.state.boxes_positions:
        x, y = boxes_positions
        sum += pathfinding_recursive(node.state.matrix, x, y, 0)
    return sum


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

    sokoban = Sokoban(matrix)


    if params["algorithm"]=="a*" or params["algorithm"]=="greedy":
        result:Result = algorithm_map[params["algorithm"]](sokoban,h1)
    elif params["algorithm"]=="dfs":
        result:Result=algorithm_map[params["algorithm"]](sokoban,params["limit"])
    else:
        result:Result = algorithm_map[params["algorithm"]](sokoban)

    print("Success:", result.success)
    print("Cost:", result.result_cost)
    print(f"Result {result.processing_time}")
    print(f"expanded: {result.nodes_expanded}")
    print(f"limit reades {result.limit_reached}")
    print(f"asfasfasf")

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

    sokoban = Sokoban(matrix)


    if params["algorithm"]=="a*" or params["algorithm"]=="greedy":
        result:Result = algorithm_map[params["algorithm"]](sokoban, h1)
    elif params["algorithm"]=="dfs":
        result:Result=algorithm_map[params["algorithm"]](sokoban,params["limit"])
    else:
        result:Result = algorithm_map[params["algorithm"]](sokoban)

    print("Success:", result.success)
    print("Cost:", result.result_cost)
    print(f"Result {result.processing_time}")
    print(f"expanded: {result.nodes_expanded}")
    print(f"limit reached {result.limit_reached}")
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