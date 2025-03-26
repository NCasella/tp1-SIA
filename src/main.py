import sys
import json 
from sokoban import Sokoban, SokobanState
from search_methods import *
import numpy as np 

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

    algorithm_map = {
        "bfs": breath_first_search,
        "dfs": depth_first_search,
        "greedy": greedy_search,
        "a*": a_star_search,
    }

    sokoban = Sokoban(matrix)

    result:Result = algorithm_map[params["algorithm"]](sokoban)

    print("Success:", result.success)
    print("Cost:", result.result_cost)

    states = []

    for node in result.solution:
        states.append(node)
        print(node.action)

    # for node in result.solution:
    #     n:Node = node
    #     print(n.state)

    #TODO animar el resultado

    # print("Parsed Matrix:")
    # for row in matrix:
    #     print(row)

    return states

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

            
            

        
    algorithm_map = {
        "bfs": breath_first_search,
        "dfs": depth_first_search,
        "greedy": greedy_search,
        "a*": a_star_search,
    }
    def h1(node:Node):
        sum=0
        for boxes_positions in node.state.boxes_positions:
            distances=[]
            for objectives in sokoban.objective_positions:
                distances.append(abs(objectives[0]-boxes_positions[0])+abs(objectives[1]-boxes_positions[1]))
            sum+=np.min(distances)
        return sum


    sokoban = Sokoban(matrix)


    if params["algorithm"]=="a*" or params["algorithm"]=="greedy":
        result:Result = algorithm_map[params["algorithm"]](sokoban,h1)
    else:
        result:Result=algorithm_map[params["algorithm"]](sokoban)

    print("Success:", result.success)
    print("Cost:", result.result_cost)
    print(f"Result {result.processing_time}")
    states = []
    for node in result.solution:
        states.append(node.action)
        print(node.action)

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