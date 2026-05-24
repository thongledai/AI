from collections import deque
from Support_Functions.CheckSolve import check_solve
from Support_Functions.Node import *
from Support_Functions.SupportFunctions import *



# Iterative Deepening Search
def IDS(start):
    if not check_solve(start):
        return "failure"
    
    for depth in range(40): 
        result = DLS(start, depth)
        if result != "cutoff":
            return result
    return "failure"
         

def DLS(start, limit):
    node = Node(state=start)

    frontier = deque([node])
    frontier_set = set() # Lưu note.state tìm kiếm cho nhanh
    frontier_set.add(tuple(map(tuple, node.state))) 
    explored = set() # Lưu note.state đã xét

    result = "failure"
    while frontier:
        node = frontier.pop()
        state_parent = tuple(map(tuple, node.state))
        frontier_set.discard(state_parent)

        if check_goal(node.state):
            return solution(node)

        explored.add(state_parent)

        if node.depth >= limit:
            result = "cutoff"
        else:
            for child in childs(node):
                state_child = tuple(map(tuple, child.state))
                if state_child not in explored and state_child not in frontier_set:
                    frontier.append(child)
                    frontier_set.add(state_child)

    return result
       