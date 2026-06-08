from Support_Functions.SupportFunctions import *
from Support_Functions.CheckSolve import check_solve
from Support_Functions.CalculateCost import manhattan_cost
from math import exp
import random

# Simulated Annealing
def SA(start, goal):
    if not check_solve(start):
        return "failure", "N/A"
    
    current_state = start
    current_path = []
    current_cost = manhattan_cost(current_state)
    T = 100.0
    cooling_rate = 0.99

    while T > 0.1:
        if check_goal(current_state, goal):
            return current_path, len(current_path)

        actions = get_actions(current_state)
        action = random.choice(actions)
        next_state = child_state(current_state, action)
        next_cost = manhattan_cost(next_state)
        delta= next_cost - current_cost
        
        if delta < 0:
            current_state = next_state
            current_path.append(action)
            current_cost = next_cost
        else:
            p = exp(-delta / T)
            if random.random() < p:
                current_state = next_state
                current_path.append(action)
                current_cost = next_cost

        T *= cooling_rate

    return "failure", "N/A"