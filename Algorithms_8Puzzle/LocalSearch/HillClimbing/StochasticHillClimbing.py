from Support_Functions.SupportFunctions import *
from Support_Functions.CheckSolve import check_solve
from Support_Functions.CalculateCost import manhattan_cost
from random import choice

# stochastic hill climbing
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
        better_neighbors=[]
        for action in actions:
            next_state=child_state(current_state, action)
            if manhattan_cost(next_state)<manhattan_cost(current_state):
                better_neighbors.append((action, next_state))

        if better_neighbors:
            best_action, best_state = choice(better_neighbors) #chọn random
            current_state=best_state
            path+=best_action
            cost+=1
        else:
            return "failure", "N/A" 
    
        



