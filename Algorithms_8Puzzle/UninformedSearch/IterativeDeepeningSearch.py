from collections import deque
from Support_Functions.CheckSolve import check_solve
from Support_Functions.Node import *
from Support_Functions.SupportFunctions import *



# Iterative Deepening Search
def IDS(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
    
    for depth in range(50): 
        result = DLS(start, goal, depth)
        if result != "cutoff" and result != "failure":
            return result
        
    return "failure", "N/A"
         

def DLS(start, goal, limit):
    node = Node(state=start)

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
            return get_path(node), node.path_cost

        state_parent = tuple(map(tuple, node.state))
        frontier_set.discard(state_parent)
        explored.add(state_parent)

        if node.path_cost >= limit:
            result = "cutoff"
        else:
            actions = get_actions(node.state)
            for action in actions:
                child = Node(state=child_state(node.state, action), 
                             parent=node, 
                             action=action, 
                             path_cost=node.path_cost + 1)
                
                state_child = tuple(map(tuple, child.state))
                if state_child not in explored and state_child not in frontier_set:
                    frontier.append(child)
                    frontier_set.add(state_child)

    return result
       