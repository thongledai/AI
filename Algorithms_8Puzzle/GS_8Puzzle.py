from collections import deque
from Support_Functions.CheckSolve import check_solve
from Support_Functions.Node import *
from Support_Functions.SupportFunctions import *
from Support_Functions.CalculateCost import *

# Greedy Search
# h(n) = path_cost

def GS(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
    
    node = Node(state=start)
    frontier = deque([node])
    frontier_set = set() # Lưu note.state tìm kiếm cho nhanh
    frontier_set.add(tuple(map(tuple, node.state)))
    reached = set() # Lưu note.state đã xét

    while frontier:
        pass
