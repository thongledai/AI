from collections import deque
from Support_Functions.CheckSolve import check_solve
from Support_Functions.SupportFunctions import *
from Support_Functions.CalculateCost import difference_cost, manhattan_cost

class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g  
        self.h = h  
        self.f = g + h  

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.f < other.f
    

# IDA*
# f(n)=g(n)+h(n)
# g(n): manhattan, h(n): difference

def IDAStar(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
    
    h_start=difference_cost(start)
    for depth in range(h_start, 500): 
        result = DLS(start, goal, depth)
        if result != "cutoff" and result != "failure":
            return result
        
    return "failure", "N/A"


def DLS(start, goal, limit):
    node = Node(state=start, g=0, h=difference_cost(start))

    if check_goal(node.state, goal):
        return get_path(node), node.f
    
    frontier = deque([node])
    frontier_set = set() # Lưu note.state tìm kiếm cho nhanh
    frontier_set.add(tuple(map(tuple, node.state))) 
    explored = set() # Lưu note.state đã xét
    
    result = "failure"
    while frontier:
        node = frontier.pop()
        if check_goal(node.state, goal):
            return get_path(node), node.f

        state_parent = tuple(map(tuple, node.state))
        frontier_set.discard(state_parent)
        explored.add(state_parent)

        if node.f >= limit:
            result = "cutoff"
        else:
            actions = get_actions(node.state)
            for action in actions:
                new_state = child_state(node.state, action)
                g_new = node.g + manhattan_cost(new_state)
                h_new = difference_cost(new_state)

                child = Node(state=new_state, 
                             parent=node, 
                             action=action, 
                             g=g_new,
                             h=h_new)
                
                state_child = tuple(map(tuple, child.state))
                if state_child not in explored and state_child not in frontier_set:
                    frontier.append(child)
                    frontier_set.add(state_child)

    return result