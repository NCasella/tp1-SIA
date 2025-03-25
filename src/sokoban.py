from problem_def import Problem
from enum import Enum


_WALL='#'
_BOX='$'
_OBJECTIVE='.'
_BOX_ON_OBJECTIVE='*'
_EMPTYNESS=' '
_PLAYER='@'
_PLAYER_ON_OBJECTIVE='+'

class Movement(Enum):
    UP=(-1,0)
    DOWN=(1,0)
    LEFT=(0,-1)
    RIGHT=(0,1)

class SokobanState:
    def __init__(self, matrix, player_position,boxes_positions:set[tuple]):
        self.matrix=matrix
        self.player_position=player_position
        self.boxes_positions=boxes_positions

    def __hash__(self):
        return hash(str(self.matrix))

    def __eq__(self, value):
        return isinstance(value,SokobanState) and self.matrix==value.matrix


class Sokoban(Problem):
    def __init__(self, initial_state):
        self.objective_positions=set()
        boxes_positions=set()
        for i in range(len(initial_state)):
            for j in range(len(initial_state[i])):
                if initial_state[i][j]==_OBJECTIVE or initial_state[i][j]==_BOX_ON_OBJECTIVE or initial_state[i][j]==_PLAYER_ON_OBJECTIVE:
                    self.objective_positions.add((i,j))
                if initial_state[i][j]==_PLAYER or initial_state[i][j]==_PLAYER_ON_OBJECTIVE:
                    player_position=(i,j)
                if initial_state[i][j]==_BOX or initial_state[i][j]==_BOX_ON_OBJECTIVE:
                    boxes_positions.add((i,j))
        self.initial_state=SokobanState(matrix=initial_state,player_position=player_position,boxes_positions=boxes_positions)

    def _is_valid_position(self,matrix,position,movement):
        if matrix[position[0]][position[1]]==_EMPTYNESS or matrix[position[0]][position[1]]==_OBJECTIVE:
            return True
        if matrix[position[0]][position[1]]==_BOX or matrix[position[0]][position[1]]==_BOX_ON_OBJECTIVE:
            new_box_position=(position[0]+movement.value[0],position[1]+movement.value[1])
            if matrix[new_box_position[0]][new_box_position[1]]==_EMPTYNESS or matrix[new_box_position[0]][new_box_position[1]]==_OBJECTIVE:
                return True
        return False


    def get_actions(self,state:SokobanState):
        actions=[]
        for movement in Movement:
            new_position=(state.player_position[0]+movement.value[0],state.player_position[1]+movement.value[1])
            if self._is_valid_position(matrix=state.matrix,position=new_position,movement=movement):
                actions.append(movement)
        return actions

    def get_state_result(self,current_state,action):
        new_boxes_positions=set(current_state.boxes_positions)
        matrix=[row.copy() for row in current_state.matrix]
        new_player_position=(current_state.player_position[0]+action.value[0],current_state.player_position[1]+action.value[1])
        if matrix[new_player_position[0]][new_player_position[1]]==_BOX or matrix[new_player_position[0]][new_player_position[1]]==_BOX_ON_OBJECTIVE:
            new_box_position=(new_player_position[0]+action.value[0],new_player_position[1]+action.value[1])
            new_boxes_positions.remove(new_player_position)
            new_boxes_positions.add(new_box_position)
            if matrix[new_box_position[0]][new_box_position[1]]==_OBJECTIVE:
                matrix[new_box_position[0]][new_box_position[1]]=_BOX_ON_OBJECTIVE
            else:
                matrix[new_box_position[0]][new_box_position[1]]=_BOX
            if matrix[new_player_position[0]][new_player_position[1]]==_BOX:
                matrix[new_player_position[0]][new_player_position[1]] = _PLAYER
            else:
                matrix[new_player_position[0]][new_player_position[1]] = _PLAYER_ON_OBJECTIVE
        else:
            if current_state.matrix[new_player_position[0]][new_player_position[1]]==_OBJECTIVE:
                matrix[new_player_position[0]][new_player_position[1]]=_PLAYER_ON_OBJECTIVE
            else: matrix[new_player_position[0]][new_player_position[1]]=_PLAYER

        if current_state.player_position in self.objective_positions:
            matrix[current_state.player_position[0]][current_state.player_position[1]]=_OBJECTIVE
        else:
            matrix[current_state.player_position[0]][current_state.player_position[1]]=_EMPTYNESS
        return SokobanState(matrix=matrix,player_position=new_player_position,boxes_positions=new_boxes_positions)

    def get_cost_to_state(self,start_state,action,end_state):
        return 1

    def is_goal_state(self,state):
        return all([state.matrix[objective[0]][objective[1]]==_BOX_ON_OBJECTIVE for objective in self.objective_positions])
