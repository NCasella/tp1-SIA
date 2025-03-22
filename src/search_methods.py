from problem_def import *
from collections import deque

_LIMIT_REACHED_STRING="Limit reached"
_NO_SOLUTION_FOUND_STRING="No solution present"

def depth_limited_search(problem:Problem,limit:int)-> tuple[bool,deque|str]:
    """devuelve tupla con resultado de busqueda. si primer valor es true devuelve cola, sino, devuelve razon de fallo"""
    return _recursive_depth_limited_search(node=problem.initial_state, limit=limit)

def _recursive_depth_limited_search(node:Node,problem:Problem,limit:int) -> tuple[bool,deque]:
    if problem.is_goal_state(node.state):
        return (True,node.get_action_sequence())
    if limit==0:
        return (False,_LIMIT_REACHED_STRING)
    reached_limit=False
    for action in problem.get_actions(node.state):
        child=node.generate_child_node(problem=problem,action=action)
        result=_recursive_depth_limited_search(node=child,problem=problem,limit=limit-1)
        reached_limit=result[1]==_LIMIT_REACHED_STRING
        if result[0]:
            return result
    return (False,_LIMIT_REACHED_STRING) if reached_limit else (False,_NO_SOLUTION_FOUND_STRING)
    