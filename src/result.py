from collections import deque
class Result:
    def __init__(self,success:bool=False, result_cost:int=0,nodes_expanded:int=0,nodes_frontier:int=0,solution:deque=None,processing_time:float=0):
        self.success=success
        self.result_cost=result_cost
        self.nodes_expanded=nodes_expanded
        self.nodes_frontier=nodes_frontier
        self.solution=solution
        self.processing_time=processing_time
        pass
