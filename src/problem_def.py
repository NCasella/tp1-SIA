from abc import ABC,abstractmethod
from collections import deque

#implementaciones basadas en los pseudocodigos de AI A Modern Approach

class Problem(ABC):
    def __init__(self,initial_state,goal_state):
        self.initial_state=initial_state
        self.goal_state=goal_state

    @abstractmethod
    def get_state_result(current_state,action):
        """estado resultante de aplicar action a current_state"""
        #TODO cada uno de los problemas
        
    @abstractmethod
    def get_actions(current_state):
        """todas las acciones disponibles en current_state"""
        #TODO cada uno de los problemas

    @abstractmethod
    def get_cost_to_state(start_state,action,end_state):
        """costo de llegar desde start_state hasta end_state, con action"""
        #TODO cada uno de los problemas

    def is_goal_state(self,state):
        return state == self.goal_state

class Node:
    def __init__(self,state,parent=None,cost=0,action=None,path=[]):
        self.state=state
        self.parent=parent
        self.cost=cost
        self.action=action


    def get_action_sequence(self):
        action_sequence=deque()
        node=self
        while(node is not None):
            action_sequence.appendleft(node.action)
            node=node.parent
        return action_sequence

    def generate_child_node(self,problem:Problem, action):
        state=problem.get_state_result(self.state,action)
        cost=self.cost+problem.get_cost_to_state(self.state,action,state)
        return Node(state,self,action,cost)


