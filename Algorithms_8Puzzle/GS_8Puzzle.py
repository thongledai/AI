import heapq
from Support_Functions.CheckSolve import check_solve
from Support_Functions.Node import *
from Support_Functions.SupportFunctions import *
from Support_Functions.CalculateCost import difference_cost

# Greedy Search
# h(n) = path_cost : số ô sai

def GS(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
    
    node = Node(state=start, path_cost=difference_cost(start))
    if check_goal(node.state, goal):
        return solution(node), node.path_cost
    
    # frontier dùng hàng đợi ưu tiên
    frontier = []
    heapq.heappush(frontier, (node.path_cost, node))
    frontier_set = set()
    frontier_set.add(tuple(map(tuple, node.state)))
    # các node.state đã xét
    explored = set()
    
    while frontier:
        node = heapq.heappop(frontier)[1]
        if check_goal(node.state, goal):
            return solution(node), node.path_cost
        
        state_parent = tuple(map(tuple, node.state))
        explored.add(state_parent)
        frontier_set.discard(state_parent)

        # các action
        actions = get_actions(node.state)
        for action in actions:
            new_state = child_state(node.state, action)
            child = Node(state=new_state, 
                         parent=node, 
                         action=action, 
                         path_cost=difference_cost(new_state))
            
            state_child = tuple(map(tuple, child.state))
            if state_child not in explored and state_child not in frontier_set:              
                heapq.heappush(frontier, (child.path_cost, child))
                frontier_set.add(state_child)
    
    return "failure", "N/A"