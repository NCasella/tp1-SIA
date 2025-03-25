import sys
import json 
from sokoban import Sokoban, SokobanState
from search_methods import *

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

    sokoban = Sokoban(matrix)

    result = algorithm_map[params["algorithm"]](sokoban)

    print("Success:", result.success)
    print("Cost:", result.result_cost)

    #TODO animar el resultado

    # print("Parsed Matrix:")
    # for row in matrix:
    #     print(row)

if __name__ == "__main__":
    main()