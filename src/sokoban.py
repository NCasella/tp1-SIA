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

        #import sys  
        #for i in range(len(matrix)):
        #    sys.stdout.write("[")
        #    for j in range(len(matrix[i])):
        #        sys.stdout.write(matrix[i][j])
        #    print("]")
        #print("----------------")

    def __hash__(self):
        return hash((tuple(map(tuple,self.matrix))))

    def __eq__(self, value):
        return isinstance(value,SokobanState) and self.matrix==value.matrix


class Sokoban(Problem):
    def __init__(self, initial_state):
        self.objective_positions=set()
        boxes_positions=set()
        all_positions=set()
        for i in range(len(initial_state)):
            walls_amount=0
            for j in range(len(initial_state[i])):
                if initial_state[i][j]!=_WALL:
                    if initial_state[i][j]==_EMPTYNESS and walls_amount==0:
                        initial_state[i][j]=_WALL
                    else: all_positions.add((i,j))
                    if initial_state[i][j]==_OBJECTIVE or initial_state[i][j]==_BOX_ON_OBJECTIVE or initial_state[i][j]==_PLAYER_ON_OBJECTIVE:
                        self.objective_positions.add((i,j))
                    if initial_state[i][j]==_PLAYER or initial_state[i][j]==_PLAYER_ON_OBJECTIVE:
                        player_position=(i,j)
                    if initial_state[i][j]==_BOX or initial_state[i][j]==_BOX_ON_OBJECTIVE:
                        boxes_positions.add((i,j))
                else: walls_amount+=1
        # rechable_positions=set()
        # for op in self.objective_positions:
        #     self._reachable_positions(initial_state,op,rechable_positions)
        # self.dead_squares:set[tuple] = all_positions-rechable_positions

        self.initial_state=SokobanState(matrix=initial_state,player_position=player_position,boxes_positions=boxes_positions)

    def _reachable_positions(self,matrix,objective_position,reachable_positions):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j]!=_WALL:
                    if ((i<objective_position[0] and matrix[i-1][j]!=_WALL) or (i>objective_position[0] and matrix[i+1][j]!=_WALL) or i==objective_position[0]) and ((j<objective_position[1] and matrix[i][j-1]!=_WALL) or (j>objective_position[1] and matrix[i][j+1]!=_WALL) or j==objective_position[1]):
                        reachable_positions.add((i,j))

    def _is_valid_position(self,matrix,position,movement):
        if matrix[position[0]][position[1]]==_EMPTYNESS or matrix[position[0]][position[1]]==_OBJECTIVE:
            return True
        if matrix[position[0]][position[1]]==_BOX or matrix[position[0]][position[1]]==_BOX_ON_OBJECTIVE:
            new_box_position=(position[0]+movement.value[0],position[1]+movement.value[1])
            #and (new_box_position not in self.dead_squares)
            if (matrix[new_box_position[0]][new_box_position[1]]==_EMPTYNESS or matrix[new_box_position[0]][new_box_position[1]]==_OBJECTIVE):
                matrix_copy=[row.copy() for row in matrix]
                matrix_copy[position[0]][position[1]]=_PLAYER
                all_on_objective=True
                deadlock=self._is_deadlock_position(matrix_copy,new_box_position,movement)
                if (not deadlock) or all_on_objective:
                    return True
        return False

    def _is_deadlock_position(self, matrix, box_position, movement):
        x, y = box_position
        dx, dy = movement.value
        new_pos = (x + dx, y + dy)
        if not (0 <= new_pos[0] < len(matrix) and 0 <= new_pos[1] < len(matrix[0])):
            return True
        if matrix[new_pos[0]][new_pos[1]] == _WALL:
            return True
        box_positions = {(i, j) for i in range(len(matrix)) for j in range(len(matrix[i])) if matrix[i][j] == _BOX or matrix[i][j] == _BOX_ON_OBJECTIVE}
        box_positions.add(new_pos)
        return (
            self._is_static_deadlock(matrix, new_pos, box_positions, set()) or
            self._box_is_frozen(matrix, new_pos, True)
        )

    def _is_static_deadlock(self, matrix, pos, box_positions, visited):
        if pos in visited:
            return True
        visited.add(pos)

        directions = [Movement.UP, Movement.RIGHT, Movement.DOWN, Movement.LEFT]

        length = len(directions)

        for i in range(length):

            all_directions = [
                directions[i].value,
                directions[(i + 1) % length].value,
                directions[(i + 2) % length].value
            ]

            all_positions = [(pos[0] + d[0], pos[1] + d[1]) for d in all_directions]

            if all(
                matrix[x[0]][x[1]] == _WALL or 
                (x in box_positions and self._is_static_deadlock(matrix, x, box_positions, visited.copy())) for x in all_positions
            ):
                return True
        return False
    
    def _box_is_frozen(self,matrix,box_position,all_on_objectives):
        all_on_objectives=all_on_objectives and box_position in self.objective_positions
        return self._is_frozen_vertically(matrix,box_position,all_on_objectives) and self._is_frozen_horizontally(matrix,box_position,all_on_objectives)

    def _is_frozen_vertically(self,matrix,box_position,all_on_objectives):
        above_box=matrix[box_position[0]-1][box_position[1]]
        below_box=matrix[box_position[0]+1][box_position[1]]
        if (above_box==_WALL or below_box==_WALL):
            return True
        if above_box==_BOX or above_box==_BOX_ON_OBJECTIVE:
            matrix[box_position[0]][box_position[1]]=_WALL
            return self._box_is_frozen(matrix,(box_position[0]-1,box_position[1]),all_on_objectives) 
        if below_box==_BOX or below_box==_BOX_ON_OBJECTIVE:
            matrix[box_position[0]][box_position[1]]=_WALL
            return self._box_is_frozen(matrix,(box_position[0]+1,box_position[1]),all_on_objectives)
        return False


    def _is_frozen_horizontally(self,matrix,box_position,all_on_objectives):
        left_box=matrix[box_position[0]][box_position[1]-1]
        right_box=matrix[box_position[0]][box_position[1]+1]
        if (left_box==_WALL or right_box==_WALL):
            return True
        if left_box==_BOX or left_box==_BOX_ON_OBJECTIVE:
            matrix[box_position[0]][box_position[1]]=_WALL
            return self._box_is_frozen(matrix,(box_position[0],box_position[1]-1),all_on_objectives)
        if right_box==_BOX or right_box==_BOX_ON_OBJECTIVE:
            matrix[box_position[0]][box_position[1]]=_WALL
            return self._box_is_frozen(matrix,(box_position[0],box_position[1]+1),all_on_objectives)
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
