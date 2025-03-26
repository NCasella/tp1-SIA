import json
import sys
from main import run_with_params

def gather_data(algorithms, levels, limit):
    for algorithm in algorithms:
        cost = 0
        nodes_expanded = 0
        nodes_frontier = 0
        processing_time = 0.0
        print("For Algorithm:", algorithm)
        for level in levels:
            result = run_with_params(algorithm, limit, level)
            print("level:", level, "| cost=", result.result_cost, "| expanded=", result.nodes_expanded,
                  "| frontier=", result.nodes_frontier, "| s=", result.processing_time)
            cost += result.result_cost
            nodes_expanded += result.nodes_expanded
            nodes_frontier += result.nodes_frontier
            processing_time += result.processing_time
        print("Averages:")
        amount = len(levels)
        print("cost=", cost/amount, "| expanded=", nodes_expanded/amount, "| frontier=", nodes_frontier/amount,
              "| s=", processing_time/amount)
        print("---------------------------------------------------------------------")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py config.json")
        sys.exit(1)

    config_file = sys.argv[1]
    
    try:
        with open(config_file, "r") as file:
            config_data = json.load(file)
    except Exception as e:
        print("Error loading JSON file:", e)
        sys.exit(1)

    print(config_data)
    
    for group in config_data:
        algorithms = group.get("algorithms", [])
        levels = group.get("levels", [])
        limit = group.get("limit", 600)
        gather_data(algorithms, levels, limit)
