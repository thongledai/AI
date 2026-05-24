import heapq
from Support_Functions.CheckSolve import check_solve
from Support_Functions.Node import Node
from Support_Functions.SupportFunctions import *
from Support_Functions.CalculateCostUSC import cal_cost

# Uniform Cost Search 
def UCS(start):
    if not check_solve(start):
        return "failure"
    
    node = Node(state=start)
    
    if check_goal(node.state):
        return solution(node)
    
    # frontier dùng hàng đợi ưu tiên
    frontier = []
    heapq.heappush(frontier, (node.path_cost, node))
    
    # các node.state đã xét
    explored = set()
    
    while frontier:
        node = heapq.heappop(frontier)[1]
        if check_goal(node.state):
            return solution(node)
    
        state_parent = tuple(map(tuple, node.state))
        explored.add(state_parent)

        # các action
        actions = get_actions(node.state)
        
        for action in actions:
            new_state= child_state(node.state, action)
            child = Node(state=new_state, 
                         parent=node, 
                         action=action, 
                         path_cost=node.path_cost + cal_cost(new_state))
            
            child_state_tuple = tuple(map(tuple, child.state))
            in_explored= child_state_tuple in explored
            in_frontier= any(child == item[1] for item in frontier)
            if not in_explored and not in_frontier:               
                heapq.heappush(frontier, (child.path_cost, child))

    return "failure"


