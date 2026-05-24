import random
from collections import deque
from ModelBased_Puzzle import *
from Support_Functions.SupportFunctions import check_goal
from Support_Functions.Node import Node
from Support_Functions.CheckSolve import check_solve
from Support_Functions.SupportFunctions import *

# Depth First Search
def DFS(start):
    if not check_solve(start):
        return "failure"
    node = Node(state=start)

    if check_goal(node.state):
        return solution(node)
    
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

        # Random các action
        actions = random.sample(get_actions(node.state), len(get_actions(node.state)))
        #actions = get_actions(node.state)
        for action in actions:
            child = Node(state=child_state(node.state, action), 
                         parent=node, 
                         action=action, 
                         path_cost=node.path_cost + 1)
            state_child = tuple(map(tuple, child.state))
            if state_child not in explored and state_child not in frontier_set:               
                if check_goal(child.state):
                    return solution(child)
                else:
                    frontier.append(child)
                    frontier_set.add(state_child)

    return "failure"
