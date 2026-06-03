from Support_Functions.SupportFunctions import *
from Support_Functions.CheckSolve import check_solve
from Support_Functions.CalculateCost import manhattan_cost

# steepest-ascent hill climbing
def SAHC(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
    
    current_state=start
    path =[]
    cost=0

    while True:
        if current_state== goal:
            return path, cost
        
        actions= get_actions(current_state)
        better_neighbors=[]
        for action in actions:
            next_state=child_state(current_state, action)
            if manhattan_cost(next_state)<manhattan_cost(current_state):
                better_neighbors.append((action, next_state))

        if better_neighbors:
            best_action, best_state = min(better_neighbors, key=lambda x: manhattan_cost(x[1]))
            current_state=best_state
            path+=best_action
            cost+=1
        else:
            return "failure", "N/A" 
    
        



