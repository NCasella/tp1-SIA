from problem_def import Problem
from enum import Enum

class BlockType(Enum):
    WALL=0
    BOX=1
    OBJECTIVE=2
    EMPTYNESS=3


class Sokoban(Problem):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state=initial_state,goal_state= goal_state)

    def get_actions(self,state):
        return super().get_actions(state=state)
    