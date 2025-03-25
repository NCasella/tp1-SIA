from problem_def import Problem
from enum import Enum


_WALL='#'
_BOX='$'
_OBJECTIVE='.'
_EMPTYNESS=' '
_PLAYER='@'

class Movement(Enum):
    UP=(1,0)
    DOWN=(-1,0)
    LEFT=(0,-1)
    RIGHT=(0,1)


class Sokoban(Problem):
    def __init__(self, initial_state):
        super().__init__(initial_state=initial_state)
        self.objective_positions=set()
        for i in range(initial_state):
            for j in range(initial_state[i]):
                if initial_state[i][j]==_OBJECTIVE:
                    self.objective_positions.add((i,j))

    def get_actions(self,state):
        pass

    def get_state_result(self,state,action):
        pass

    def get_cost_to_state(self,start_state,action,end_state):
        return 1
