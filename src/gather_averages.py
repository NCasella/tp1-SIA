from main import run_with_params
import time
import threading
from search_methods import *

levels = ["levels/box1.txt",
         "levels/box2.txt",
         "levels/box3.txt",
         "levels/box4.txt",
         "levels/box5.txt",
         "levels/box6.txt",
         "levels/box7.txt",
         "levels/box8.txt",
         "levels/box9.txt",
        ]

algorithms = ["a*",
              "greedy",
              "dfs",
              "bfs",
              ]

limit = 200


for algorithm in algorithms:
    cost = 0
    nodes_expanded = 0
    nodes_frontier = 0
    processing_time = 0.0
    print("For Algorithm: ", algorithm)
    for level in levels:
        result = run_with_params(algorithm, limit, level)
        print("level: ", level, " | cost=", result.result_cost, " | expanded=", result.nodes_expanded, " | frontier=", result.nodes_frontier, " | s=", result.processing_time)
        cost += result.result_cost
        nodes_expanded += result.nodes_expanded
        nodes_frontier += result.nodes_frontier
        processing_time += result.processing_time
    print("Averages: ")
    amount = len(levels)
    print("cost=", cost/amount, " | expanded=", nodes_expanded/amount, " | frontier=", nodes_frontier/amount, " | s=", processing_time/amount)
    print("---------------------------------------------------------------------")
    