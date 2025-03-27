from collections import deque
import math
import time
from functools import cmp_to_key
from _collections_abc import Callable
from sortedcontainers.sortedlist import SortedList
from problem_def import Problem,Node
from result import Result


def depth_first_search(problem:Problem) -> Result:
    return limited_depth_first_search(problem=problem,limit=math.inf)
def iterative_depth_limited_first_search(problem:Problem):
    depth=0
    cutoff=True
    while cutoff:
        result:Result=limited_depth_first_search(problem=problem,limit=depth)
        depth+=1
        cutoff=result.limit_reached
    return result

def limited_depth_first_search(problem:Problem,limit:int) -> Result:#STACK
    return _general_search(problem=problem,limit=limit,collection=list())

def breath_first_search(problem:Problem) -> Result:#COLA
    return _general_search(problem=problem,limit=math.inf,collection=deque())

def _check_explored(node: Node, explored_states: dict):
    return node.state in explored_states and node.depth >= explored_states[node.state] # basically, we check if it is explored and the node is deeper than the saved one (there's a shorter path)

def _general_search(problem:Problem,limit:int,collection:list[Node]|deque[Node]) -> Result:
    start_time=time.perf_counter()
    node:Node=Node(problem.initial_state)
    fr=collection
    fr.append(node)
    explored_states={}
    nodes_expanded=0
    cutoff=False
    while len(fr)!=0:
        node=fr.popleft() if isinstance(fr,deque) else fr.pop()
        if problem.is_goal_state(node.state):
            end_time=time.perf_counter()
            return Result(success=True,result_cost=node.cost,nodes_expanded=nodes_expanded,nodes_frontier=len(fr),solution=node.get_action_sequence_to_root(),processing_time=end_time-start_time)
        if node.depth>=limit:
            cutoff=True
            continue
        if _check_explored(node, explored_states):
            continue
        explored_states[node.state] = node.depth
        for action in problem.get_actions(node.state):
            child=node.generate_child_node(problem=problem,action=action)
            nodes_expanded+=1
            if not _check_explored(child, explored_states):
                fr.append(child)
        
    end_time=time.perf_counter()
    return Result(success=False,nodes_expanded=nodes_expanded,processing_time=end_time-start_time,limit_reached=cutoff)

def best_first_search(problem:Problem,f:tuple[Callable,Callable]) -> Result:
    def node_comparator(node1,node2):
        primary_diff=f[0](node1)-f[0](node2)
        if primary_diff!=0:
            return primary_diff
        return f[1](node1)-f[1](node2) if len(f)>1 else 0

    node:Node=Node(state=problem.initial_state)
    fr=SortedList(key=cmp_to_key(node_comparator))
    start_time=time.perf_counter()
    fr.add(node)
    explored_states=set()
    nodes_expanded=0
    while len(fr)!=0:
        node=fr.pop(0)
        if problem.is_goal_state(node.state):
            end_time=time.perf_counter()
            return Result(success=True,result_cost=node.cost,nodes_expanded=nodes_expanded,nodes_frontier=len(fr),solution=node.get_action_sequence_to_root(),processing_time=end_time-start_time)
        explored_states.add(node.state)
        for action in problem.get_actions(node.state):
            child=node.generate_child_node(problem=problem,action=action)
            nodes_expanded+=1
            try:
                child_index=fr.index(child)
            except ValueError:
                child_index=None
            if child.state not in explored_states and child_index is None:
                fr.add(child)
            elif child_index is not None and f[0](child)<f[0](fr[child_index]):
                fr.pop(child_index)
                fr.add(child)
    end_time=time.perf_counter()
    return Result(success=False,nodes_expanded=nodes_expanded,processing_time=end_time-start_time)

def a_star_search(problem:Problem,h:Callable) -> Result:
    return best_first_search(problem=problem,f=(lambda node:node.cost+h(node),h) )

def greedy_search(problem:Problem,h:Callable) -> Result:
    return best_first_search(problem=problem,f=(h,) )
