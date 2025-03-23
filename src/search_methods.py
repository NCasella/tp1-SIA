from problem_def import *
from collections import deque
from _collections_abc import Callable
from sortedcontainers.sortedlist import SortedList
from functools import cmp_to_key

_LIMIT_REACHED_STRING="Limit reached"
_NO_SOLUTION_FOUND_STRING="No solution present"

def depth_limited_search(problem:Problem,limit:int) -> tuple[bool,deque|str]:
    """devuelve tupla con resultado de busqueda. si primer valor es true devuelve cola, sino, devuelve razon de fallo"""
    return _recursive_depth_limited_search(node=problem.initial_state, limit=limit)

def _recursive_depth_limited_search(node:Node,problem:Problem,limit:int) -> tuple[bool,deque|str]:
    if problem.is_goal_state(node.state):
        return (True,node.get_action_sequence_to_root())
    if limit==0:
        return (False,_LIMIT_REACHED_STRING)
    reached_limit=False
    for action in problem.get_actions(state=node.state):
        child=node.generate_child_node(problem=problem,action=action)
        result=_recursive_depth_limited_search(node=child,problem=problem,limit=limit-1)
        reached_limit=result[1]==_LIMIT_REACHED_STRING
        if result[0]:
            return result
    return (False,_LIMIT_REACHED_STRING) if reached_limit else (False,_NO_SOLUTION_FOUND_STRING)

def best_first_search(problem:Problem,f:tuple[Callable,Callable]) -> deque:
    def compare_nodes(node1,node2):
        primary_diff=f[0](node1)-f[0](node2)
        if primary_diff!=0:
            return primary_diff
        return f[1](node1)-f[1](node2) if len(f)>1 else 0

    node:Node=Node(state=problem.initial_state)
    fr=SortedList(key=cmp_to_key(compare_nodes))
    fr.append(node)
    explored_states=set()
    while len(fr)!=0:
        node=fr.pop()
        if problem.is_goal_state(node.state):
            return node.get_action_sequence_to_root()
        explored_states.add(node.state)
        for action in problem.get_actions(node.state):
            child=node.generate_child_node(problem=problem,action=action)
            if child.state not in explored_states and child not in fr:
                fr.append(child)
            else:
                try:
                    child_index=fr.index(node)
                except ValueError:
                    child_index=None
                if child_index is not None and f[0](child)<f[0](fr[child_index]):
                    fr.pop(child_index)
                    fr.append(child)
    return None

def a_star_search(problem:Problem,h:Callable) -> deque:
    return best_first_search(problem=problem,f=(lambda node:node.cost+h(node),h) )

def greedy_search(problem:Problem,h:Callable) -> deque:
    return best_first_search(problem=problem,f=(h,) )
