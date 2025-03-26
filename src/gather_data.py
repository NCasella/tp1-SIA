import json
import sys
import csv
import os
import multiprocessing
from main import run_with_params

def process_algorithm(algorithm, levels, limit, queue):
    print(f"[INFO] Process started for algorithm: {algorithm}")
    results = []
    for i, level in enumerate(levels, start=1):
        print(f"[INFO] {algorithm}: Processing level {i}/{len(levels)} - {level}")
        result = run_with_params(algorithm, "h3", limit, level)
        results.append([algorithm, level, result.result_cost, result.nodes_expanded, result.nodes_frontier, result.processing_time])
    print(f"[INFO] Process finished for algorithm: {algorithm}")
    queue.put(results)

def gather_data(algorithms, levels, limit, output_file):
    print(f"[INFO] Starting data gathering. Output file: {output_file}")
    processes = []
    queue = multiprocessing.Queue()
    
    for algorithm in algorithms:
        p = multiprocessing.Process(target=process_algorithm, args=(algorithm, levels, limit, queue))
        p.start()
        processes.append(p)
    
    all_results = []
    for p in processes:
        all_results.extend(queue.get())
    
    for p in processes:
        p.join()
    
    print(f"[INFO] Writing results to {output_file}")
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Algorithm", "Level", "Cost", "Nodes Expanded", "Nodes Frontier", "Processing Time (s)"])
        writer.writerows(all_results)
    print(f"[INFO] Data gathering completed for {output_file}")

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
    
    for group in config_data:
        group_name = group.get("group", "default")
        output_file = os.path.join(output_dir, f"{group_name}-output.csv")
        algorithms = group.get("algorithms", [])
        levels = group.get("levels", [])
        limit = group.get("limit", 600)
        gather_data(algorithms, levels, limit, output_file)
