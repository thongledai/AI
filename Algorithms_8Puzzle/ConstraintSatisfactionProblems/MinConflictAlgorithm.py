# Chọn giá trị gây ít xung đột nhất
from Algorithms_8Puzzle.ConstraintSatisfactionProblems.Ultis import *
from copy import deepcopy
import random

states = []

#Min Conflict
def MC():
    states.clear()
    current_state = random_start()
    states.append(deepcopy(current_state))
    
    max_steps = 20000
    for i in range(max_steps):
        if count_conflicts(current_state) == 0:
            return current_state, states
            
        conflicts = conflicted_variables(current_state)
        if not conflicts:
            return current_state, states
            
        var = random.choice(conflicts)
        value = min_conflict_value(current_state, var)
        
        current_state[var[0]][var[1]] = value
        states.append(deepcopy(current_state))
        
    return None, states
