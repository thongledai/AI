from collections import deque
from Support_Functions.SupportFunctions import check_goal
from Support_Functions.Node import Node
from Support_Functions.CheckSolve import check_solve
from Support_Functions.SupportFunctions import *

# Depth First Search
# giới hạn độ sâu tối đa là 50
def DFS(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
    
    node = Node(state=start)
    if check_goal(node.state, goal):
        return get_path(node), node.path_cost
    
    # frontier dùng LIFO
    frontier = deque([node])
    # các node.state cần xét
    frontier_set=set()
    frontier_set.add(tuple(map(tuple, node.state)))
    # các node.state đã xét
    explored = set()
    
    while frontier:
        node = frontier.pop()

        state_parent = tuple(map(tuple, node.state))
        explored.add(state_parent)
        frontier_set.discard(state_parent)

        # các action
        actions = get_actions(node.state)
        for action in actions:
            child = Node(state=child_state(node.state, action), 
                         parent=node, 
                         action=action, 
                         path_cost=node.path_cost + 1)
            
            state_child = tuple(map(tuple, child.state))
            if state_child not in explored and state_child not in frontier_set:               
                if check_goal(child.state, goal):
                    return get_path(child), child.path_cost
                elif child.path_cost >= 50: # giới hạn độ sâu tối đa là 50
                    raise RecursionError("maximum recursion depth exceeded")
                else:
                    frontier.append(child)
                    frontier_set.add(state_child)

    return "failure", "N/A"
