import json
import sys
import csv
import os
from main import run_with_params

def gather_data(algorithms, levels, limit, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Algorithm", "Level", "Cost", "Nodes Expanded", "Nodes Frontier", "Processing Time (s)"])
        
        for algorithm in algorithms:
            for level in levels:
                result = run_with_params(algorithm, limit, level)
                writer.writerow([algorithm, level, result.result_cost, result.nodes_expanded, result.nodes_frontier, result.processing_time])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py config.json")
        sys.exit(1)

    config_file = sys.argv[1]
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(config_file, "r") as file:
            config_data = json.load(file)
    except Exception as e:
        print("Error loading JSON file:", e)
        sys.exit(1)
    
    for i, group in enumerate(config_data, start=1):
        output_file = os.path.join(output_dir, f"{i}-output.csv")
        algorithms = group.get("algorithms", [])
        levels = group.get("levels", [])
        limit = group.get("limit", 600)
        gather_data(algorithms, levels, limit, output_file)