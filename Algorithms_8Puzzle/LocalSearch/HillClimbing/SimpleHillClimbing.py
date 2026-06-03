from Support_Functions.SupportFunctions import *
from Support_Functions.CheckSolve import check_solve
from Support_Functions.CalculateCost import manhattan_cost

# simple hill climbing
def SHC(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
    
    current_state=start
    path =[]
    cost=0

    while True:
        if current_state== goal:
            return path, cost
        actions= get_actions(current_state)
        check_improved=False
        for action in actions:
            next_state=child_state(current_state, action)
            if manhattan_cost(next_state)<manhattan_cost(current_state):
                current_state=next_state
                path+=action
                cost+=1
                check_improved=True
                break
        if not check_improved:
            return "failure", "N/A" 
    
        



